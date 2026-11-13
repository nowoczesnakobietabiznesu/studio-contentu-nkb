#!/usr/bin/env python3
"""The buyer's effects: ticked on the effects part of the NKB catalog (picker.py --tab effects) or asked for in the chat.

Usage:
  PY effects.py show                         what she has picked now (and where it is kept)
  PY effects.py set <key> [<key> ...]        these effects, nothing else       ("chcę Neon i Listę kroków")
  PY effects.py add <key> [<key> ...]        add to what she has               ("dodaj jeszcze Licznik")
  PY effects.py remove <key> [<key> ...]     take out                          ("bez Klonów")
  PY effects.py clear                        no effects at all                 ("bez efektów")
  PY effects.py auto                         none picked: you choose per reel  ("dobierz sama", "wybierz za mnie")
  ... [--style "<name>"]                     the style to change (default: her default style)

Show her the list first: references/efekty.md (Polish names, one line each, what each one needs), or open the
catalog on the effects (picker.py --tab effects) where every effect plays as a finished demo reel. The keys are the
ones in effects/index.json ("checklist", "neon-sign", ...); the Polish name from the list works too.
An empty list means AUTO (footage_check.py checks every effect and you pick what fits each reel); "clear" stores
"noEffects": true, so no effect is used until she picks some or says "dobierz sama".

Where the picks go: a saved style that carries its own "picks" (made with my_styles.py --with-picks) gets them in
its style.json; otherwise they go to studio-picks.json in the state folder, which every style without its own picks
uses. Either way the next edit sees them (skillenv.effective_picks). Standard library only.
"""
import json
import os
import sys
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skillenv  # noqa: E402


def load_index():
    with open(os.path.join(skillenv.SKILL_DIR, 'effects', 'index.json'), encoding='utf-8') as fh:
        return json.load(fh)['effects']


def polish_names():
    """{lowercased Polish name: key} from references/efekty.md rows like "| Lista kroków | `checklist` |" """
    out = {}
    try:
        with open(os.path.join(skillenv.SKILL_DIR, 'references', 'efekty.md'), encoding='utf-8') as fh:
            for line in fh:
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if len(cells) >= 2 and cells[1].startswith('`') and cells[1].endswith('`'):
                    name = cells[0].split('(')[0].strip().strip('*').lower()
                    if name:
                        out[name] = cells[1].strip('`')
    except OSError:
        pass
    return out


def resolve(words, index):
    keys = {e['key'] for e in index}
    by_name = {e['name'].lower(): e['key'] for e in index}
    by_name.update(polish_names())
    out, bad = [], []
    for w in words:
        k = w.strip().lower()
        k = k if k in keys else by_name.get(k) or k.replace(' ', '-')
        (out if k in keys else bad).append(k if k in keys else w)
    if bad:
        sys.exit('Unknown effect(s): ' + ', '.join(bad) + '. The keys are in effects/index.json and references/efekty.md.')
    return out


def target(args):
    """-> (label, path to the json file, dict holding the picks, the whole file data)"""
    name = None
    if '--style' in args:
        i = args.index('--style')
        name = args[i + 1] if i + 1 < len(args) else None
        del args[i:i + 2]
    style = None
    if name:
        style, many = skillenv.find_style(name)
        if not style:
            sys.exit(f'No saved style called "{name}"' + (' (it could be: ' + ', '.join(m['name'] for m in many) + ')'
                                                          if many else '') + '. PY my_styles.py list shows them.')
    else:
        style = skillenv.default_style()
    if style:
        spec = skillenv._read_json(style['path'], {}) or {}
        if isinstance(spec.get('picks'), dict):
            return f'the style "{style["name"]}"', style['path'], spec['picks'], spec
    path = skillenv.picks_file()
    data = skillenv._read_json(path, None)
    if not isinstance(data, dict):
        data = {'mode': 'custom', 'style': None, 'captionStyle': 'none', 'effects': [], 'effectSections': None}
    return 'the Studio picks (every style without picks of its own uses them)', path, data, data


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    os.replace(tmp, path)


def main():
    skillenv.utf8_stdio()
    args = sys.argv[1:]
    if not args or args[0] not in ('show', 'set', 'add', 'remove', 'clear', 'auto'):
        sys.exit(__doc__)
    cmd, rest = args[0], args[1:]
    index = load_index()
    label, path, picks, data = target(rest)
    now = [k for k in (picks.get('effects') or []) if isinstance(k, str)]
    if cmd == 'show':
        names = {e['key']: e['name'] for e in index}
        empty = 'none (she asked for no effects)' if picks.get('noEffects') else 'auto (you pick what fits each reel)'
        print(f'effects ({label}): ' + (', '.join(f'{names.get(k, k)} ({k})' for k in now) if now else empty))
        print(f'file    {skillenv.shell_path(path)}')
        return
    keys = resolve(rest, index) if cmd not in ('clear', 'auto') else []
    if cmd in ('set', 'add') and not keys:
        sys.exit(f'{cmd} needs at least one effect.')
    if cmd == 'set':
        new = keys
    elif cmd == 'add':
        new = now + [k for k in keys if k not in now]
    elif cmd == 'remove':
        new = [k for k in now if k not in keys]
    else:
        new = []
    order = [e['key'] for e in index]
    new = sorted(dict.fromkeys(new), key=order.index)
    picks['effects'] = new
    picks['noEffects'] = cmd == 'clear' or (cmd == 'remove' and not new and bool(picks.get('noEffects')))
    sections = picks.get('effectSections')
    if isinstance(sections, dict):          # parts limits only for effects that are still picked
        picks['effectSections'] = {p: [k for k in v if k in new] for p, v in sections.items() if isinstance(v, list)}
    picks['updated'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    save(path, data)
    names = {e['key']: e['name'] for e in index}
    print(f'STATUS effects SAVED {len(new)} -> {label}: ' + (', '.join(names[k] for k in new) if new else
                                                              'none' if picks['noEffects'] else 'auto'))
    needs = [names[k] for k in new if next(e for e in index if e['key'] == k).get('cutout') == 'clean']
    if needs:
        print('note: ' + ', '.join(needs) + ' cut her out of their own seconds (the clean cutout): a few minutes per '
              'effect on a computer without Apple Silicon. Say so when you use one.')


if __name__ == '__main__':
    main()
