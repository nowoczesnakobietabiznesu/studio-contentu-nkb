#!/usr/bin/env python3
"""Studio Contentu NKB: the caption engine. Every caption style is a spec (the 20 NKB styles in nkb-styles/, or the
buyer's own), rendered by custom() and driven by the same word timings.

This file is a library. scripts/build_reel.py is what you run: it reads the buyer's style, calls load(project) and
then page('custom') (or page('none')) and writes <project>/index.html.

Every style reads <project>/words.json: [{text, start, end, e?}] where e marks the words a style may treat differently:
  num  = a number worth showing big        key = a name / brand
  emph = the word the line leans on        cta = the comment keyword
Nothing below is specific to any clip. Where the speaker is comes from <project>/layout.json (scripts/layout.py:
head position measured on the footage, the three caption bands worked out from it). Pinned titles and any other
per-reel text come from <project>/plan.json, written by the editing Claude from the reel's hook.
"""
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'scripts'))
import skillenv  # noqa: E402

# ----------------------------------------------------------------------------------------------------------------------
# Per-clip values. Filled by load(project); the numbers here are only the fallback for footage with nobody in it.
# All coordinates are in the 1080x1920 frame.
# ----------------------------------------------------------------------------------------------------------------------
DEFAULT_BANDS = dict(HEAD_TOP=452, Y_ABOVE_HEAD=344, Y_CHEST=1170, Y_LOWER=1376,
                     WALL_LEFT=(70, 596, 300), WALL_RIGHT=(740, 640, 280))
HEAD_TOP = 452            # y of the top of the head, for words that sit BEHIND the head
Y_ABOVE_HEAD = 344        # top of a one-line caption that floats over the head (None: no room up there)
Y_CHEST = 1170            # top of a one-line caption over the chest / lap
Y_LOWER = 1376            # top of a lower-third subtitle line (must end above y 1470)
WALL_LEFT = (70, 596, 300)     # x, y, width of the open area left of the speaker (None: no room)
WALL_RIGHT = (740, 640, 280)   # same on the right
TITLE = ('', '')          # the reel's hook as two short lines, for a pinned title
SWASH = ('', '')          # the same hook, shorter, Title Case, for a swash title
VIDEO = 'assets/aroll.mp4'
VOICE = VIDEO             # NKB: assets/voice_clean.wav once clean_voice.py made one for this cut
CUTOUT = None             # assets/subject.webm when a person cutout exists
W, DUR = [], 0.0
PROJECT = None
LAYOUT, PLAN, SEGS = {}, {}, []
FACELESS = False          # nobody on camera (voice over b-roll)
LANG = 'en'               # the language spoken (skillenv.language): captions are written in it
RTL = False               # Arabic, Persian, Urdu, Hebrew: lines read right to left, letters join, no letter spacing
STOPS = ',.?!،؟؛'          # punctuation a caption line may break after (Arabic comma, question mark, semicolon too)
ENDS = '.?!؟'              # the end of a sentence
CUES = {'comment', 'اكتب', 'أكتب', 'اكتبلي', 'اكتبي', 'علق', 'علّق', 'علقي'}   # the word that asks for a comment (marks.py)
LIFT, FILL = 0, '#0d0d10'  # close-up fallback: the picture is lifted LIFT px so captions get the collar band
HEAD = dict(top=452, chin=760, cx=540, width=250)


def _json(path, fallback):
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return fallback


def guess_title(words):
    """First guess at a pinned title: the opening line as two short lines. The editing Claude should write a better
    one into plan.json ("title"); this only keeps a build from having an empty pill."""
    line = []
    for w in words:
        line.append(w['text'])
        if w['text'][-1:] in STOPS and len(line) >= 3 or len(line) >= 9:
            break
    line = [t.strip(STOPS + ';:') for t in line]
    best = min(range(1, len(line)), key=lambda k: abs(len(' '.join(line[:k])) - len(' '.join(line[k:])))) if len(line) > 1 else 1
    return ' '.join(line[:best]), ' '.join(line[best:])


def voice_track(video, dur):
    """NKB: the cleaned voice (clean_voice.py) when it belongs to THIS cut: newer than aroll.mp4 and the same length.
    A re-assembled cut (a notes round, a trial with another hook) falls back to the a-roll's own sound until
    clean_voice.py runs again, so the voice never plays against the wrong picture."""
    wav = os.path.join(PROJECT, 'assets', 'voice_clean.wav')
    if not os.path.isfile(wav) or os.path.getmtime(wav) < os.path.getmtime(video):
        return VIDEO
    got = subprocess.run([skillenv.tool('ffprobe'), '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                          wav], **skillenv.TEXT).stdout.strip()
    try:
        ok = abs(float(got) - dur) < 0.1
    except ValueError:
        ok = False
    if not ok:
        print('NOTE voice_clean.wav does not match this cut: using the a-roll sound. Run clean_voice.py again.')
    return 'assets/voice_clean.wav' if ok else VIDEO


def load(project):
    """Point the engine at one reel project. Sets the module values every style reads."""
    global HEAD_TOP, Y_ABOVE_HEAD, Y_CHEST, Y_LOWER, WALL_LEFT, WALL_RIGHT, TITLE, SWASH, VIDEO, CUTOUT, W, DUR
    global PROJECT, LAYOUT, PLAN, SEGS, FACELESS, LIFT, FILL, HEAD, LANG, RTL, VOICE
    PROJECT = os.path.abspath(project)
    LANG = skillenv.language(PROJECT)
    RTL = skillenv.is_rtl(LANG)
    W = _json(os.path.join(PROJECT, 'words.json'), None)
    if not W:
        sys.exit('words.json is missing or empty: run transcribe_cut.py first.')
    video = os.path.join(PROJECT, 'assets', 'aroll.mp4')
    DUR = float(subprocess.run([skillenv.tool('ffprobe'), '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                'stream=duration', '-of', 'csv=p=0', video], **skillenv.TEXT).stdout.strip().split(',')[0])
    CUTOUT = 'assets/subject.webm' if os.path.isfile(os.path.join(PROJECT, 'assets', 'subject.webm')) else None
    VOICE = voice_track(video, DUR)
    LAYOUT = _json(os.path.join(PROJECT, 'layout.json'), {})
    PLAN = _json(os.path.join(PROJECT, 'plan.json'), {})
    bands = {**DEFAULT_BANDS, **(LAYOUT.get('bands') or {})}
    HEAD_TOP, Y_ABOVE_HEAD, Y_CHEST, Y_LOWER = bands['HEAD_TOP'], bands['Y_ABOVE_HEAD'], bands['Y_CHEST'], bands['Y_LOWER']
    WALL_LEFT = tuple(bands['WALL_LEFT']) if bands.get('WALL_LEFT') else None
    WALL_RIGHT = tuple(bands['WALL_RIGHT']) if bands.get('WALL_RIGHT') else None
    FACELESS = bool(LAYOUT.get('faceless'))
    LIFT, FILL = int(LAYOUT.get('lift') or 0), LAYOUT.get('fill') or '#0d0d10'
    HEAD = {**HEAD, **(LAYOUT.get('head') or {})}
    SEGS = [(s['frame'] / 30, (s['frame'] + s['frames']) / 30) for s in _json(os.path.join(PROJECT, 'segments.json'), [])]
    SEGS = SEGS or [(0.0, DUR)]
    title = [t for t in (PLAN.get('title') or []) if t] or list(guess_title(W))
    TITLE = tuple((title + [''])[:2]) if len(title) < 2 else tuple(title[:2])
    swash = [t for t in (PLAN.get('swash') or []) if t] or [' '.join(x[:1].upper() + x[1:] for x in t.split()) for t in TITLE]
    SWASH = tuple((swash + [''])[:2])
    return LAYOUT


def head_top_at(t):
    """Head top during the segment that is on screen at time t (punch-ins move the head)."""
    for s in LAYOUT.get('segments') or []:
        if s['t0'] - .02 <= t < s['t1'] and s.get('head_top') is not None:
            return s['head_top'] - LIFT
    return HEAD_TOP


WEAK ={'the', 'a', 'an', 'to', 'of', 'and', 'that', 'for', 'can', 'in', 'on', 'with', 'is', 'my', 'your', 'then',
       # Polish: one-letter words and short prepositions/conjunctions never end a line ("sierotki": "zebrałam w" /
       # "darmowym"), and "nie" belongs to the word after it
       'i', 'o', 'u', 'w', 'z', 'we', 'ze', 'na', 'do', 'od', 'po', 'za', 'że', 'bo', 'czy', 'lub', 'oraz', 'ale',
       'nie', 'dla', 'bez', 'przy', 'pod', 'nad', 'jak',
       # German articles and prepositions
       'der', 'die', 'das', 'den', 'dem', 'ein', 'eine', 'und', 'zu', 'mit', 'im', 'auf', 'für', 'von', 'aus'}
PRONOUNS = {'i', 'you', 'we', 'he', 'she', 'they', 'it'}


def counted(i):
    """end index of what a number counts: up to two more words ("21 video effects"), never past punctuation, a marked
    word, a weak word or a pronoun ("3 things" stops before "I")"""
    j = i + 1
    while (j < len(W) and j - i < 3 and W[j - 1]['text'][-1] not in STOPS and not W[j].get('e')
           and W[j]['text'].rstrip(',.;:').lower() not in WEAK | PRONOUNS):
        j += 1
    return j


def T(t):
    """snap to the frame grid, 2ms early so a tl.set lands ON that frame"""
    return max(0.0, round(t * 30) / 30 - .002)


def esc(s):
    return html.escape(s, quote=False).replace("'", '&rsquo;')


def bare(s):
    return s.rstrip(',.;:،؛')


def letters(txt):
    """the pieces a letter-by-letter animation steps through: the letters, or whole words in a joined script (an
    Arabic letter changes shape with its neighbours, so a letter on its own reads wrong)"""
    return re.findall(r'\S+|\s', txt) if RTL else list(txt)


def low(w):
    """lowercase a word for the lowercase styles, but leave names and I / I'll alone"""
    t = bare(w['text'])
    return t if w.get('e') == 'key' or t.split("'")[0] == 'I' else t.lower()


def chunk(words, max_words, max_chars, solo=()):
    """greedy phrases: break on length, on punctuation, on a pause; never leave a weak word dangling at the end"""
    groups, cur = [], []

    def flush(carry=True):
        nonlocal cur
        if not cur:
            return
        tail = []
        if carry and len(cur) > 1 and bare(cur[-1]['text']).lower() in WEAK and cur[-1]['text'][-1] not in STOPS:
            tail = [cur.pop()]
        groups.append(cur)
        cur = tail

    for w in words:
        if w.get('e') in solo:
            flush(carry=False)
            groups.append([w])
            continue
        if cur:
            text = ' '.join(x['text'] for x in cur + [w])
            # a sentence end always closes the phrase, also after a one-word sentence ("First." / "Pierwsza."):
            # otherwise it runs into the next sentence ("First Think step by step"). A comma needs two words first.
            last = cur[-1]['text'][-1]
            punct = last in ENDS or (last in STOPS and len(cur) >= 2)
            pause = w['start'] - cur[-1]['end'] > .3
            if len(cur) >= max_words or len(text) > max_chars or punct or pause:
                full = not (punct or pause)
                flush(carry=full)
                # the phrase is full and the next word ends the sentence: take one more word along, so the sentence
                # does not end on a word alone ("... nic nie" / "daje.")
                if full and len(groups[-1]) >= 3 and not cur and w['text'][-1] in ENDS \
                        and groups[-1][-1]['text'][-1] not in STOPS:
                    cur = [groups[-1].pop()]
        cur.append(w)
    flush(carry=False)
    return groups


def windows(groups, hold=.35, gap=.6):
    """(group, t_in, t_out): a phrase stays up until the next one, or drops after a pause"""
    out = []
    for i, g in enumerate(groups):
        t0, end = g[0]['start'], g[-1]['end']
        if i + 1 < len(groups):
            nxt = groups[i + 1][0]['start']
            t1 = nxt if nxt - end <= gap else end + hold
        else:
            t1 = end + hold
        out.append((g, t0, t1))
    return out


class Build:
    def __init__(self):
        self.css, self.html, self.js, self.n = [], [], [], 0
        self.back, self.cutout = [], False      # back = layer BEHIND the speaker (needs assets/subject.webm)

    def nid(self, p='c'):
        self.n += 1
        return f'{p}{self.n}'

    def cut(self, sel, t_in, t_out=None):
        """hard cut in at t_in, hard cut out at t_out"""
        if t_in > .02:
            self.js.append(f"gsap.set('{sel}',{{autoAlpha:0}});")
            self.js.append(f"tl.set('{sel}',{{autoAlpha:1}},{T(t_in):.3f});")
        if t_out is not None and t_out < DUR - .02:
            self.js.append(f"tl.set('{sel}',{{autoAlpha:0}},{T(t_out):.3f});")

    def tween_in(self, sel, t_in, frm, to, dur, ease='power2.out'):
        self.js.append(f"gsap.set('{sel}',{{autoAlpha:0}});")
        self.js.append(f"tl.fromTo('{sel}',{json.dumps({'autoAlpha': 0, **frm})},"
                       f"{json.dumps({'autoAlpha': 1, **to, 'duration': dur, 'ease': ease, 'immediateRender': False})},{T(t_in):.3f});")

    def out(self, sel, t_out, fade=0):
        if t_out >= DUR - .02:
            return
        if fade:
            self.js.append(f"tl.to('{sel}',{{autoAlpha:0,duration:{fade}}},{max(0, T(t_out) - fade):.3f});")
        self.js.append(f"tl.set('{sel}',{{autoAlpha:0}},{T(t_out):.3f});")


BASE_CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:#000;overflow:hidden}
#root{position:relative;width:1080px;height:1920px;overflow:hidden}
.full{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.cap{position:absolute;left:0;width:1080px;text-align:center;white-space:nowrap}
'''


# ----------------------------------------------------------------------------------------------------------------------
# CUSTOM: every caption style of the Studio is a spec: the 20 NKB styles (nkb-styles/) and the buyer's own
# (references/replicate.md). The same words.json, marks, phrase windows, hide windows and caption_y. build_reel.py fills CUSTOM and EXTRA from
# <project>/plan.json and the buyer's my-style.json.
# ----------------------------------------------------------------------------------------------------------------------
CUSTOM = {}               # the caption spec (see custom() for every field and its default)
EXTRA = {}                # reel-wide extras: {'css': str, 'grade': css filter, 'layers': [...], 'sounds': [...], 'fonts': [...],
                          #                 'reframe': a trial reel's own framing and colour (reframe_values)}
BEHIND = False            # the last page() put words or layers behind the speaker (a mirrored trial must not)
NOTES = []                # things the build could not do as asked; build_reel.py prints them as NOTE lines
ENTRANCES = ('none', 'pop', 'fade', 'slide-up', 'type-on', 'word-by-word')
LIT = ('none', 'color', 'stay', 'plate', 'pop')
POSITIONS = {'top': 236, 'center': 860}


def _num(v, default):
    try:
        return float(v)
    except (TypeError, ValueError):
        return float(default)


# ----------------------------------------------------------------------------------------------------------------------
# MOTION: animation the editing Claude writes itself, as GSAP tweens on the reel's one timeline (references/motion.md).
# The renderer seeks that timeline frame by frame, so a tween here always renders exactly; css @keyframes and
# transitions never do. Each entry is plain JSON:
#   {"target": ".w", "tween": "from" | "to" | "fromTo" | "set", "vars": {...gsap vars...}, "from": {...},  (fromTo only)
#    "at": 0.0  (seconds after the element comes in) | "at_end": 0.3  (seconds before it goes),
#    "on": "marks" | "words" | "cuts" | "start", "kinds": ["key", "num"], "every": 1, "offset": 0.0}  (reel motion only)
# ----------------------------------------------------------------------------------------------------------------------
TWEENS = ('from', 'to', 'fromTo', 'set')
TARGETS = {'self': '', 'footage': '#plate,#cutw', 'speaker': '#cutw', 'captions': '#caps', 'layers': '#layers'}
MOTION_MAX = 400          # tweens from one "on" entry: more than this is a mistake (a word tween on every word of a long reel is fine)


def _unsafe(v):
    """Anything that would make two renders of the same frame differ (random values: the renderer may load the page
    more than once), or that is not plain data."""
    s = json.dumps(v)
    return any(x in s for x in ('random(', '"random"', '=>', 'function', 'Math.', '<script'))


def _jsjson(v):
    return json.dumps(v).replace('</', '<\\/')


def motion(entries, scope='', base=0.0, end=None, where='Motion'):
    """GSAP lines for a list of motion entries. scope = the element they belong to (a layer, a caption line, a word):
    "target" is a selector INSIDE it, "self" (or nothing) is the element itself. Without a scope "target" is a
    selector on the page, or one of TARGETS ("footage" moves the picture and the cutout together)."""
    if isinstance(entries, dict):
        entries = [entries]
    out = []
    for k, m in enumerate(entries if isinstance(entries, list) else []):
        if not isinstance(m, dict):
            continue
        tw = m.get('tween', 'from')
        name = f'{where} {m.get("id", k + 1)}'
        if tw not in TWEENS:
            NOTES.append(f'{name}: tween "{tw}" is not one of {", ".join(TWEENS)}; left out.')
            continue
        vars_ = m.get('vars') if isinstance(m.get('vars'), dict) else {}
        if _unsafe(m):
            NOTES.append(f'{name}: random values or code are not allowed (two renders of one frame must match); left out. '
                         'Write the numbers out.')
            continue
        tgt = str(m.get('target', 'self') or 'self').strip()
        tgt = TARGETS.get(tgt, tgt)
        if scope:
            sel = scope if not tgt else ','.join(f'{scope} {t.strip()}' for t in tgt.split(',') if t.strip())
        elif tgt:
            sel = tgt
        else:
            NOTES.append(f'{name}: no target; left out.')
            continue
        t = (end - _num(m.get('at_end'), 0)) if m.get('at_end') is not None and end is not None else base + _num(m.get('at'), 0)
        t = T(max(0.0, min(t, DUR)))
        v = dict(vars_)
        if tw == 'set':
            v.pop('duration', None)
            args = _jsjson(v)
        elif tw == 'fromTo':
            v.setdefault('immediateRender', False)
            frm = m.get('from') if isinstance(m.get('from'), dict) else {}
            hide = {k: frm[k] for k in ('opacity', 'autoAlpha') if k in frm}
            if hide and t > T(base) + 0.001:
                # a fromTo that starts later than its element ("at"): without immediateRender the element shows at
                # full opacity from the element's start until its own moment (typed letters all visible at once)
                out.append(f'tl.set({_jsjson(sel)},{_jsjson(hide)},{T(base):.3f});')
            args = _jsjson(frm) + ',' + _jsjson(v)
        else:
            v.setdefault('duration', .3)
            if tw == 'from' and any(k in v for k in ('opacity', 'autoAlpha')):
                # The engine hides an element until its moment (autoAlpha 0), so a from() would animate opacity from
                # 0 to that hidden 0 and the element would never show. Opacity goes as its own fromTo, ending at 1.
                timing = {k: v[k] for k in ('duration', 'ease', 'stagger', 'delay', 'repeat', 'yoyo', 'repeatDelay') if k in v}
                fade = {k: v.pop(k) for k in ('opacity', 'autoAlpha') if k in v}
                out.append(f'tl.fromTo({_jsjson(sel)},{_jsjson(fade)},'
                           f'{_jsjson({**{k: 1 for k in fade}, **timing, "immediateRender": False})},{t:.3f});')
                if not set(v) - set(timing):
                    continue
            args = _jsjson(v)
        out.append(f'tl.{tw}({_jsjson(sel)},{args},{t:.3f});')
    return out


def reel_motion(entries):
    """Reel-wide motion (plan.json / a saved style "motion"): at fixed reel seconds ("at"), or on a pattern ("on"):
    every marked word ("marks", optionally only some "kinds"), every word, every cut, or the start. A saved style
    only keeps the "on" kind: its times come from each new reel's own words."""
    if isinstance(entries, dict):
        entries = [entries]
    out = []
    for k, m in enumerate(entries if isinstance(entries, list) else []):
        if not isinstance(m, dict):
            continue
        on = m.get('on')
        if not on:
            out += motion([m], '', 0.0, None, 'Reel motion')
            continue
        if on == 'marks':
            kinds = m.get('kinds')
            times = [w['start'] for w in W if w.get('e') and (not kinds or w.get('e') in kinds)]
        elif on == 'words':
            times = [w['start'] for w in W]
        elif on == 'cuts':
            times = [s0 for s0, _ in SEGS[1:]]
        elif on == 'start':
            times = [0.0]
        else:
            NOTES.append(f'Reel motion {m.get("id", k + 1)}: "on": "{on}" is not marks, words, cuts or start; left out.')
            continue
        every = max(1, int(_num(m.get('every'), 1)))
        times = [t + _num(m.get('offset'), 0) for t in times[::every]][:MOTION_MAX]
        one = {x: y for x, y in m.items() if x not in ('on', 'every', 'offset', 'kinds')}
        for t in times:
            out += motion([{**one, 'at': t}], '', 0.0, None, 'Reel motion')
    return out


def css_motion_note(css, where):
    """css animation never plays in the renderer: say so once, so the look is rebuilt with motion entries"""
    if css and ('@keyframes' in str(css) or 'animation:' in str(css) or 'transition:' in str(css)):
        note = (f'{where}: css @keyframes / animation / transition do not play in the renderer (it seeks frame by frame). '
                'Rewrite that movement as "motion" entries (references/motion.md).')
        if note not in NOTES:
            NOTES.append(note)


def custom_top(s=None):
    """screen y of the top of the custom caption block, from its "position" (a band name or a y), kept inside the
    safe zone and off the face"""
    s = CUSTOM if s is None else s
    size, lines = _num(s.get('size'), 64), max(1, int(_num(s.get('lines'), 1)))
    plate = s.get('plate') if isinstance(s.get('plate'), dict) else {}
    pad_y = _num((plate.get('pad') or [0, 0])[0], 0) if plate else 0
    height = lines * size * _num(s.get('line_height'), 1.12) + 2 * pad_y
    pos = s.get('position', 'chest')
    if isinstance(pos, (int, float)):
        top = float(pos)
    elif pos == 'lower':
        top = Y_LOWER
    elif pos == 'above-head':
        top = Y_ABOVE_HEAD if Y_ABOVE_HEAD is not None else Y_CHEST
        if Y_ABOVE_HEAD is None and 'no room above the head' not in ' '.join(NOTES):
            NOTES.append('Custom captions: there is no room above the head in this clip, so they sit over the chest.')
    elif pos in POSITIONS:
        top = POSITIONS[pos]
    else:
        top = Y_CHEST
    top += _num(s.get('dy'), 0)
    top = max(236.0, min(top, 1470 - 14 - height))            # inside the Reels safe zone, top and bottom
    head = LAYOUT.get('head') or {}
    # "avoid_face": false = a style that moves the speaker itself (NKB Pokaz: the speaker in a panel at the bottom),
    # so the measured head box no longer says where the face is on screen; the style places its words by design
    if head and not FACELESS and s.get('avoid_face', True) is not False:
        f0, f1 = head.get('top_min', head.get('top', 0)) - LIFT, (head.get('chin_max') or head.get('chin') or 0) - LIFT + 24
        if top < f1 and top + height > f0 + .25 * (f1 - f0):      # the block would sit on the face (brow to chin)
            moved = Y_CHEST if f1 + 100 <= Y_CHEST + 76 else max(f1, 236)
            note = (f'Custom captions: y {top:.0f} would put them on the face (it is at y {f0:.0f} to {f1 - 24:.0f}), '
                    f'so they were moved to y {moved:.0f}.')
            if note not in NOTES:
                NOTES.append(note)
            top = moved
            if top + height > 1470 - 14:
                # NKB: the Reels safe zone wins. Moved below the chin the block would run under the app's own buttons,
                # so it goes back up to the bottom of the safe zone (the head box is a cautious guess: often fine)
                top = 1470 - 14 - height
                NOTES.append(f'Custom captions: below the chin there is no room for a {height:.0f}px block inside the safe '
                             f'zone, so it sits at y {top:.0f}, over the lower edge of the head box. LOOK at the snapshots: '
                             'if it covers the chin, use a smaller size or one line.')
    return int(top)


def custom(b):
    """One caption style from a spec. Every field is optional:
      font, weight, italic, stretch   css family (one from assets/fonts/fonts.css, or a "file" in assets/fonts), 100-900,
                                      true / false, font-stretch % (125 for a wide face)
      file                            a font file in <project>/assets/fonts for a family the skill does not ship
      case                            'as-typed' | 'upper' | 'lower' | 'title'
      size, tracking, line_height     px, em, multiple of size
      color, accent                   text colour; colour of marked and lit words
      shadow                          css text-shadow, or false
      stroke                          {"color": "#000", "width": 8}: an outline around the letters
      plate                           {"color": "rgba(...)", "radius": 24, "pad": [18, 32], "blur": 0, "per": "line" | "word"}
      lit, lit_text                   how the word being said shows: 'none' | 'color' (accent while said) | 'stay' (turns
                                      accent and stays) | 'plate' (an accent plate behind it, lit_text on top) | 'pop'
      mark, mark_scale                marked words (num / key / emph / cta in words.json): 'accent' (accent colour) |
                                      'highlight' (an accent box behind the word, lit_text on top) | 'none'; size factor
      words, chars, lines             most words and characters per line; 1 or 2 lines
      position, dy, align, margin     'chest' | 'lower' | 'above-head' | 'top' | 'center' or a y in px; nudge; 'center' |
                                      'left' | 'right'; side margin px
      entrance, exit                  'none' | 'pop' | 'fade' | 'slide-up' | 'type-on' | 'word-by-word'; 'none' | 'fade'
      css                             extra css for this style (classes: .cu block, .cu .ln line, .cu .w word, .cu .w.m
                                      marked word, .cu .pl plate)
      motion, word_motion, mark_motion   the buyer's own animation (see MOTION above): for each line, for each word as
                                      it is said, for each marked word. Any of them can replace or add to "entrance"."""
    s = CUSTOM
    css_motion_note(s.get('css'), 'Custom captions')
    fam, weight = str(s.get('font') or 'Inter Tight'), int(_num(s.get('weight'), 800))
    size, lh = _num(s.get('size'), 64), _num(s.get('line_height'), 1.12)
    case = s.get('case', 'as-typed')
    color, accent = s.get('color', '#FFFFFF'), s.get('accent', '#FAE67A')
    lit = s.get('lit', 'none') if s.get('lit', 'none') in LIT else 'none'
    lit_text = s.get('lit_text', '#151517')
    entrance = s.get('entrance', 'none') if s.get('entrance', 'none') in ENTRANCES else 'none'
    if s.get('entrance') and s.get('entrance') not in ENTRANCES:
        NOTES.append(f'Custom captions: entrance "{s.get("entrance")}" is not one of {", ".join(ENTRANCES)}; used none.')
    if s.get('lit') and s.get('lit') not in LIT:
        NOTES.append(f'Custom captions: lit "{s.get("lit")}" is not one of {", ".join(LIT)}; used none.')
    lines_n = 2 if int(_num(s.get('lines'), 1)) >= 2 else 1
    margin = _num(s.get('margin'), 70)
    align = s.get('align', 'center') if s.get('align', 'center') in ('center', 'left', 'right') else 'center'
    plate = s.get('plate') if isinstance(s.get('plate'), dict) else None
    pad = (plate.get('pad') or [18, 32]) if plate else [0, 0]
    per_word = bool(plate) and plate.get('per') == 'word'
    # how many characters fit across the safe width at this size (wide capitals take more room)
    em = (.68 if case == 'upper' else .55) * (_num(s.get('stretch'), 100) / 100) + _num(s.get('tracking'), 0)
    fit = max(6, int((1080 - 2 * margin - 2 * pad[1]) / max(size * em, 1)))
    per_line_chars = min(int(_num(s.get('chars'), 18)), fit)
    per_line_words = max(1, int(_num(s.get('words'), 3)))
    if _num(s.get('chars'), 18) > fit:
        NOTES.append(f'Custom captions: at {size:.0f}px only about {fit} characters fit a line inside the safe zone, '
                     f'so lines break there instead of at {int(_num(s.get("chars"), 18))}.')
    top = custom_top(s)
    stroke = s.get('stroke') if isinstance(s.get('stroke'), dict) else None
    shadow = s.get('shadow', '0 3px 14px rgba(0,0,0,.5)')
    tt = {'upper': 'uppercase', 'lower': 'lowercase', 'title': 'capitalize'}.get(case, 'none')
    if s.get('file'):
        b.css.append(f"\n@font-face{{font-family:'{fam}';font-weight:{weight};font-style:{'italic' if s.get('italic') else 'normal'};"
                     f"font-display:block;src:url('assets/fonts/{s['file']}')}}")
    plate_css = ''
    if plate:
        blur = _num(plate.get('blur'), 0)
        plate_css = (f"background:{plate.get('color', 'rgba(21,21,23,.7)')};border-radius:{_num(plate.get('radius'), 20):.0f}px;"
                     f"padding:{pad[0]}px {pad[1]}px;"
                     + (f"backdrop-filter:blur({blur:.0f}px);-webkit-backdrop-filter:blur({blur:.0f}px);" if blur else ''))
    side = {'center': f'left:{margin:.0f}px;width:{1080 - 2 * margin:.0f}px;text-align:center',
            'left': f'left:{margin:.0f}px;width:{1080 - 2 * margin:.0f}px;text-align:left',
            'right': f'left:{margin:.0f}px;width:{1080 - 2 * margin:.0f}px;text-align:right'}[align]
    # NKB: the accent as a css variable, so a style's own css and its layers can use var(--acc) and follow the
    # buyer's brand colour when it changes
    b.css.append(f'\n:root{{--acc:{accent}}}')
    stack = s.get('stack') if isinstance(s.get('stack'), dict) else None
    if stack:
        b.css.append(f"\n.cu{{transform-origin:{'0' if align == 'left' else '100%' if align == 'right' else '50%'} 100%}}")
    b.css.append(f'''
.cu{{position:absolute;{side};top:{top}px;white-space:nowrap;font-family:'{fam}',sans-serif;font-weight:{weight};
  font-style:{'italic' if s.get('italic') else 'normal'};font-stretch:{_num(s.get('stretch'), 100):.0f}%;font-size:{size:.0f}px;
  line-height:{size * lh:.0f}px;letter-spacing:{_num(s.get('tracking'), 0)}em;text-transform:{tt};color:{color};
  {f'text-shadow:{shadow};' if shadow else ''}{f"-webkit-text-stroke:{_num(stroke.get('width'), 6):.0f}px {stroke.get('color', '#000')};paint-order:stroke fill;" if stroke else ''}}}
.cu .ln{{display:block}}
.cu .pl{{display:inline-block;{'' if per_word else plate_css}}}
.cu .w{{display:inline-block;transform-origin:50% 60%;{'margin:0 .1em;' + plate_css if per_word else ''}}}
.cu .w.m{{{f'color:{accent};' if s.get('mark', 'accent') == 'accent' else ''}{f'background:{accent};color:{lit_text};border-radius:.2em;padding:0 .16em;margin:0 -.04em;text-shadow:none;' if s.get('mark') == 'highlight' else ''}{f"font-size:{_num(s.get('mark_scale'), 1):.2f}em;" if _num(s.get('mark_scale'), 1) != 1 else ''}}}
.cu .ch{{display:inline-block;white-space:pre}}
{s.get('css') or ''}''')

    def shown(w):
        t = bare(w['text'])
        return low(w) if case == 'lower' else t

    groups = chunk(W, per_line_words * lines_n, per_line_chars * lines_n)

    def two_rows(g):
        return lines_n == 2 and len(g) > 1 and (len(g) > per_line_words or len(' '.join(x['text'] for x in g)) > per_line_chars)

    wins = windows(groups)
    if stack:
        # NKB "stack": a phrase does not leave when the next one comes, it moves up above it (dimmer, smaller) and
        # stays for "keep" phrases in all. Every block sits at the same top, so each push = the new block's height + gap.
        keep = max(2, int(_num(stack.get('keep'), 3)))
        gap_px = _num(stack.get('gap'), 14)
        dims = list(stack.get('dim') or [.45, .18])
        scales = list(stack.get('scale') or [.86, .74])
        heights = [(2 if two_rows(g) else 1) * size * lh + 2 * pad[0] for g in groups]
        last_out = wins[-1][2] if wins else DUR
        stacked = []
        for i, (g, t0, _t1) in enumerate(wins):
            t1 = groups[i + keep][0]['start'] if i + keep < len(groups) else last_out
            stacked.append((g, t0, t1))
        wins = stacked
    for gi, (g, t0, t1) in enumerate(wins):
        gid = b.nid()
        rows = [g]
        if two_rows(g):
            cut = min(range(1, len(g)), key=lambda k: abs(len(' '.join(x['text'] for x in g[:k])) - len(' '.join(x['text'] for x in g[k:]))))
            rows = [g[:cut], g[cut:]]
        n_chars = sum(len(letters(shown(w))) for w in g)
        said, ci, parts = max(.12, g[-1]['end'] - g[0]['start']), 0, []
        for row in rows:
            ws = []
            for w in row:
                wid = b.nid('w')
                txt = shown(w)
                cls = f"w m m-{w['e']}" if w.get('e') else 'w'     # m-num / m-key / m-emph / m-cta: style one kind
                if entrance == 'type-on':
                    inner = ''
                    for ch in letters(txt):
                        cid = b.nid('h')
                        inner += f'<span id="{cid}" class="ch">{esc(ch)}</span>'
                        at = T(g[0]['start'] + .85 * said * ci / max(n_chars, 1))
                        if plate:   # a plate grows with the typed text and its cursor (::after) follows the letters
                            b.js.append(f"gsap.set('#{cid}',{{display:'none'}});")
                            b.js.append(f"tl.set('#{cid}',{{display:'inline'}},{at:.3f});")
                        else:       # bare text: letters fade in at their place, so centred text does not shift
                            b.js.append(f"gsap.set('#{cid}',{{opacity:0}});")
                            b.js.append(f"tl.set('#{cid}',{{opacity:1}},{at:.3f});")
                        ci += 1
                else:
                    inner = esc(txt)
                ws.append(f'<span id="{wid}" class="{cls}">{inner}</span>')
                ts = T(w['start'])
                # the buyer's own motion for each word as it is said, and for each marked word (references/motion.md)
                if s.get('word_motion'):
                    b.js += motion(s['word_motion'], f'#{wid}', w['start'], None, 'Caption word motion')
                if w.get('e') and s.get('mark_motion'):
                    b.js += motion(s['mark_motion'], f'#{wid}', w['start'], None, 'Caption mark motion')
                if entrance == 'word-by-word' and w is not g[0]:
                    b.js.append(f"gsap.set('#{wid}',{{opacity:0}});")
                    b.js.append(f"tl.fromTo('#{wid}',{{opacity:0,scale:1.18}},{{opacity:1,scale:1,duration:.16,ease:'back.out(2)',immediateRender:false}},{ts:.3f});")
                nxt = g[g.index(w) + 1]['start'] if w is not g[-1] else None
                if lit in ('color', 'stay'):
                    b.js.append(f"tl.set('#{wid}',{{color:'{accent}'}},{ts:.3f});")
                    if lit == 'color' and nxt is not None and not w.get('e'):
                        b.js.append(f"tl.set('#{wid}',{{color:'{color}'}},{T(nxt):.3f});")
                elif lit == 'plate':
                    b.js.append(f"tl.set('#{wid}',{{backgroundColor:'{accent}',color:'{lit_text}',borderRadius:'{.18 * size:.0f}px',"
                                f"boxShadow:'0 0 0 {.12 * size:.0f}px {accent}'}},{ts:.3f});")
                    if nxt is not None:
                        b.js.append(f"tl.set('#{wid}',{{backgroundColor:'transparent',color:'{accent if w.get('e') and s.get('mark', 'accent') != 'none' else color}',"
                                    f"boxShadow:'none'}},{T(nxt):.3f});")
                if lit == 'pop' or (lit in ('color', 'plate') and entrance != 'word-by-word'):
                    if w is not g[0] or lit == 'pop':
                        b.js.append(f"tl.fromTo('#{wid}',{{scale:1.16}},{{scale:1,duration:.2,ease:'back.out(2.2)',immediateRender:false}},{ts:.3f});")
            line = ' '.join(ws)
            parts.append(f'<span class="ln">{line if per_word or not plate else f"<span class=&quot;pl&quot;>{line}</span>".replace("&quot;", chr(34))}</span>')
        b.html.append(f'<div id="{gid}" class="cap cu">{"".join(parts)}</div>')
        sel = f'#{gid}'
        if entrance == 'pop':
            b.tween_in(sel, t0, {'scale': .82}, {'scale': 1}, .18, 'back.out(2)')
        elif entrance == 'fade':
            b.tween_in(sel, t0, {}, {}, .18, 'power1.out')
        elif entrance == 'slide-up':
            b.tween_in(sel, t0, {'y': 34}, {'y': 0}, .22, 'power3.out')
        else:
            b.cut(sel, t0)
        b.out(sel, t1, fade=.12 if s.get('exit') == 'fade' else 0)
        if stack:
            cum = 0.0
            for k in range(1, keep):
                if gi + k >= len(groups):
                    break
                cum += heights[gi + k] + gap_px
                lvl = min(k - 1, len(dims) - 1)
                b.js.append(f"tl.to('{sel}',{{y:{-cum:.0f},opacity:{_num(dims[lvl], .4)},"
                            f"scale:{_num(scales[min(k - 1, len(scales) - 1)], 1)},duration:.3,ease:'power2.out'}},"
                            f"{T(groups[gi + k][0]['start']):.3f});")
        if s.get('motion'):              # the buyer's own motion for each caption line: "at" after it comes in, "at_end" before it goes
            b.js += motion(s['motion'], sel, t0, t1 if t1 < DUR - .02 else None, 'Caption motion')


STYLES = {}               # NKB: no built-in caption styles. Every style is a spec (custom) from nkb-styles or the buyer

SAFE_GUIDE = ('<div style="position:absolute;inset:0;z-index:99;pointer-events:none">'
              '<div style="position:absolute;left:0;right:0;top:0;height:220px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;right:0;top:1470px;bottom:0;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;left:0;width:35px;top:220px;height:1250px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:35px;top:220px;height:935px;background:rgba(255,0,0,.28)"></div>'
              '<div style="position:absolute;right:0;width:100px;top:1155px;height:315px;background:rgba(255,0,0,.28)"></div></div>')


def lifted(inner):
    """Close-up fallback (layout.json "lift"): when the face fills the frame there is no band under the chin, so the
    picture is lifted and the gap at the bottom is filled with the colour of the frame's bottom edge. That gap sits
    under Instagram's own caption area anyway. Returns inner unchanged for every normal shot."""
    if not LIFT:
        return inner
    return (f'<div class="full" style="background:{FILL}"></div><div class="full" style="top:{-LIFT}px">{inner}</div>'
            f'<div class="full" style="top:{1920 - LIFT - 190}px;height:{LIFT + 190}px;'
            f'background:linear-gradient(180deg,transparent 0%,{FILL} {190 / (LIFT + 190) * 100:.0f}%)"></div>')


def cap_top(key):
    """screen y of the top of the caption line (what a slot's caption_y moves): the custom spec's line"""
    return custom_top()


def caption_changes(b):
    """The moments one caption gives way to the next: every time a caption element is taken off screen (plus the
    start of the reel). A slot that moves the caption layer moves it on one of these, never in mid caption."""
    import re
    ts = {0.0}
    for line in b.js:
        if "'#caps'" in line or "'#fx" in line or "'#ly" in line:
            continue
        m = re.search(r"\{autoAlpha:0[^}]*\},(\d+(?:\.\d+)?)\);\s*$", line)
        if m:
            ts.add(float(m.group(1)))
    return sorted(ts)


def slots(b):
    """Effect slots from plan.json: a finished effect render laid over the reel for exactly its frames.
    scripts/fx_add.py writes the entries; by hand the short form still works:
      {"slots": [{"src": "assets/fx/odometer.mp4", "from": 3.2, "to": 5.9, "captions": "keep"}]}
    Fields: src, from, to (reel seconds, on the frame grid); media (seconds to skip at the head of the render);
      captions   "hide" / false = the reel's own captions are off while the slot plays (the effect carries the words
                 or sits where they go), "keep" / true = they stay on
      hide_captions  [[t0, t1], ...] reel seconds: hide the captions only for these windows (wins over "captions")
      caption_y  screen y the TOP of the reel's caption line moves to while the slot plays (the reel's captions stay
                 on, in the buyer's style, at the place the effect leaves for them; the same number is right for
                 every caption style). fx_add.py --caption-y writes it
      gain       brightness lift for the slot picture (a slot render passes through the renderer twice and comes
                 back a touch darker than the footage around it)
      overlay    true = the render is transparent graphics (.webm) laid over the reel's own footage, which keeps
                 its grade, cuts and push-ins underneath (the overlay effects: slot.json "layer": "overlay")
      sfx        [{"src", "at", "media", "dur", "vol"}] the effect's own sounds, replayed over the reel's voice track
      off        true = leave this slot out of the build
    Returns (picture layers, audio elements). The voice always comes from the reel's own a-roll, so there is no
    audio seam at the slot edges."""
    out, audio, track = [], [], 20
    changes = caption_changes(b)        # read before this function adds its own caption-layer lines
    moved = [o for o in PLAN.get('slots') or [] if not o.get('off') and o.get('caption_y') is not None]
    for n, s in enumerate(PLAN.get('slots') or []):
        if s.get('off'):
            continue
        t0, t1 = float(s['from']), min(float(s['to']), DUR)
        if t1 - t0 < .03:
            continue
        g = float(s.get('gain') or 1)
        lift = f' style="filter:brightness({g:.4f})"' if abs(g - 1) > .003 and not s.get('overlay') else ''
        # class gr: the reel grade (EXTRA "grade") lands on .gr too, so the slot gets the same grade as its neighbours.
        # An overlay slot (transparent graphics over the reel's own footage) is not footage: no grade, no lift
        grade = '' if s.get('overlay') else ' gr'
        out.append(f'<div id="fx{n}w"{lift}><video id="fx{n}" class="full{grade}" src="{s["src"]}" muted playsinline '
                   f'data-start="{T(t0):.3f}" data-media-start="{float(s.get("media", 0)):.3f}" '
                   f'data-duration="{t1 - T(t0):.3f}" data-track-index="{5 + n % 2}"></video></div>')
        b.cut(f'#fx{n}w', t0, t1)
        keep = s.get('captions') in (True, 'keep')
        windows = s.get('hide_captions')
        if windows is None:
            windows = [] if keep else [[t0, t1]]
        for h0, h1 in windows:
            h0, h1 = max(0.0, float(h0)), min(float(h1), DUR)
            if h1 - h0 < .03:
                continue
            b.js.append(f"tl.set('#caps',{{autoAlpha:0}},{T(h0):.3f});")
            if h1 < DUR - .02:
                b.js.append(f"tl.set('#caps',{{autoAlpha:1}},{T(h1):.3f});")
        if s.get('caption_y') is not None:
            # The buyer's captions stay on over an effect that needs the chest band for itself: the whole caption
            # layer moves so the TOP of the caption line sits at caption_y, whatever the style (each style starts a
            # different distance from its band: b.cap_top), then goes back.
            # It never moves in the middle of a caption: it moves in on the last caption change at or before the
            # slot, and back on the first one at or after it (within 1.5 s, and never over the face or into the
            # neighbouring slot's own move).
            dy = float(s['caption_y']) - getattr(b, 'cap_top', Y_CHEST)
            a, z = T(t0), T(t1)
            lo = max([float(o['to']) for o in moved if float(o['to']) <= t0 + .02] or [0.0])
            hi = min([float(o['from']) for o in moved if float(o['from']) >= t1 - .02] or [DUR])
            head = LAYOUT.get('head') or {}
            chin = (head.get('chin_max') or head.get('chin') or 0) - LIFT
            on_face = bool(head) and float(s['caption_y']) < chin + 24 and float(s['caption_y']) + 200 > head_top_at(t0)
            if not on_face:
                before = [c for c in changes if lo - .02 <= c <= a + .02 and a - c <= 1.5]
                after = [c for c in changes if z - .02 <= c <= hi + .02 and c - z <= 1.5]
                a = max(before) if before else a
                z = min(after) if after else z
            b.js.append(f"tl.set('#caps',{{y:{dy:.0f}}},{a:.3f});")
            if z < DUR - .02:
                b.js.append(f"tl.set('#caps',{{y:0}},{z:.3f});")
        for k, c in enumerate(s.get('sfx') or []):
            at = max(0.0, float(c['at']))
            dur = min(float(c.get('dur') or .5), DUR - at - .01)
            if dur < .03:
                continue
            audio.append(f'<audio id="fx{n}a{k}" src="{c["src"]}" data-start="{at:.3f}" '
                         f'data-media-start="{float(c.get("media") or 0):.3f}" data-duration="{dur:.3f}" '
                         f'data-track-index="{track}" data-volume="{float(c.get("vol") or .3):.3f}"></audio>')
            track += 1
    return out, audio


ANCHORS = ('full', 'behind', 'top', 'above-head', 'center', 'chest', 'lower-third')


def layers(b, behind=False):
    """The buyer's own on-screen elements from plan.json / my-style.json ("layers"): html + css with a time range and
    a named anchor. This is how a look is rebuilt that no built-in effect covers (a title card, a progress bar, a
    border, a lower third, a sticker). Each layer:
      {"id": "title", "anchor": "top", "from": 0.0, "to": 2.4, "html": "<div class='tt'>...</div>", "css": ".tt{...}",
       "in": "fade", "out": "fade", "dx": 0, "dy": 0}
      anchor   'full' (the whole frame, your html places itself), 'behind' (the whole frame, BEHIND the speaker: needs a
               person cutout), or a band the engine places for this clip: 'top' (y 236), 'above-head', 'center',
               'chest', 'lower-third'. A band layer is a 1080 px wide centred box whose top sits on the band.
      from/to  reel seconds. Leave both out for a layer that stays the whole reel (a border, a corner tag).
      in/out   'none' | 'fade' | 'pop' | 'slide-up'
    Returns the html of the layers of one kind (behind the speaker, or in front). Layers never count as caption
    changes and never move with a slot's caption_y."""
    out = []
    for n, l in enumerate(EXTRA.get('layers') or []):
        anchor = l.get('anchor', 'full')
        if anchor not in ANCHORS:
            if not behind:
                NOTES.append(f'Layer {l.get("id", n)}: anchor "{anchor}" is not one of {", ".join(ANCHORS)}; left out.')
            continue
        back = anchor == 'behind'
        if back and not CUTOUT:
            # never drawn in front instead: a layer made to sit behind the speaker would cover the face
            if behind:
                NOTES.append(f'Layer {l.get("id", n)} is meant to sit behind the speaker, which needs a person cutout '
                             '(rvm_cut.py). There is none yet, so it was left out of this build.')
            continue
        if back != behind:
            continue
        if back:
            b.cutout = True
        t0, t1 = _num(l.get('from'), 0), min(_num(l.get('to'), DUR), DUR)
        if t1 - t0 < .03:
            continue
        y = {'top': 236, 'above-head': Y_ABOVE_HEAD if Y_ABOVE_HEAD is not None else 236, 'center': 860, 'chest': Y_CHEST,
             'lower-third': Y_LOWER}.get(anchor)
        if anchor == 'above-head' and Y_ABOVE_HEAD is None and not behind:
            NOTES.append(f'Layer {l.get("id", n)}: no room above the head in this clip, so it sits at the top of the safe zone.')
        box = ('left:0;top:0;width:1080px;height:1920px' if y is None
               else f'left:{_num(l.get("dx"), 0):.0f}px;top:{y + _num(l.get("dy"), 0):.0f}px;width:1080px;text-align:center')
        lid = f'ly{n}'
        if l.get('css'):
            b.css.append('\n' + str(l['css']))
        # "media": a moving picture in the layer (a GIF the buyer asked for, made into a clip by gif_add.py). It is a
        # video element with its own track, so the renderer keeps it in step with the reel. {"src", "w", "x", "y", "radius"}
        media, m = '', l.get('media')
        if isinstance(m, dict) and m.get('src'):
            if PROJECT and not os.path.isfile(os.path.join(PROJECT, *str(m['src']).split('/'))):
                NOTES.append(f'Layer {l.get("id", n)}: {m["src"]} is not in the project, so it was left out.')
                continue
            at = (f'position:absolute;left:{_num(m.get("x"), 0):.0f}px;top:{_num(m.get("y"), 0):.0f}px;'
                  if m.get('x') is not None and m.get('y') is not None else '')
            media = (f'<video id="{lid}v" src="{m["src"]}" muted playsinline data-start="{T(t0):.3f}" data-media-start="0" '
                     f'data-duration="{t1 - T(t0):.3f}" data-track-index="{100 + n}" style="{at}width:{_num(m.get("w"), 420):.0f}px;'
                     f'height:auto;border-radius:{_num(m.get("radius"), 0):.0f}px"></video>')
        out.append(f'<div id="{lid}" class="layer" data-name="{esc(str(l.get("id", n)))}" style="position:absolute;{box}">{media}{l.get("html", "")}</div>')
        sel, how_in, how_out = f'#{lid}', l.get('in', 'none'), l.get('out', 'none')
        if t0 > .02 or how_in != 'none':
            b.js.append(f"gsap.set('{sel}',{{autoAlpha:0}});")
            frm = {'pop': "scale:.85,", 'slide-up': "y:40,"}.get(how_in, '')
            to = {'pop': "scale:1,ease:'back.out(2)',", 'slide-up': "y:0,ease:'power3.out',"}.get(how_in, '')
            dur = 0 if how_in == 'none' else .22
            b.js.append(f"tl.fromTo('{sel}',{{{frm}autoAlpha:0}},{{{to}autoAlpha:1,duration:{dur},immediateRender:false}},{T(t0):.3f});")
        if t1 < DUR - .02:
            if how_out == 'fade':
                b.js.append(f"tl.to('{sel}',{{autoAlpha:0,duration:.18}},{max(0, T(t1) - .18):.3f});")
            b.js.append(f"tl.set('{sel}',{{autoAlpha:0}},{T(t1):.3f});")
        css_motion_note(l.get('css'), f'Layer {l.get("id", n)}')
        if l.get('motion'):              # the layer's own animation: "at" after it comes in, "at_end" before it goes
            b.js += motion(l['motion'], sel, t0, t1 if t1 < DUR - .02 else None, f'Layer {l.get("id", n)} motion')
    return out


def sounds():
    """The reel's own sound cues from plan.json / my-style.json ("sounds"): [{"src": "assets/sfx/pop.mp3", "at": 1.2,
    "vol": 0.25, "dur": 0.5}]. Stock names live in <project>/assets/sfx. Returns audio elements."""
    out = []
    for k, c in enumerate(EXTRA.get('sounds') or []):
        at = max(0.0, _num(c.get('at'), 0))
        dur = min(_num(c.get('dur'), .6), DUR - at - .01)
        src = str(c.get('src', ''))
        if dur < .03 or not src:
            continue
        if PROJECT and not os.path.isfile(os.path.join(PROJECT, *src.split('/'))):
            NOTES.append(f'Sound {src} is not in the project, so that cue was left out.')
            continue
        out.append(f'<audio id="snd{k}" src="{src}" data-start="{at:.3f}" data-media-start="{_num(c.get("media"), 0):.3f}" '
                   f'data-duration="{dur:.3f}" data-track-index="{60 + k}" data-volume="{_num(c.get("vol"), .25):.3f}"></audio>')
    return out


def page(key, safe=False):
    """A caption style (or 'none', or 'custom': the buyer's own spec) over the footage."""
    b = Build()
    if key == 'custom':
        custom(b)
        b.cap_top = cap_top(key)
    elif key != 'none':
        raise ValueError(f'Unknown caption style "{key}": the Studio has no built-in caption styles, only specs (custom) or none')
    behind = layers(b, behind=True)       # the buyer's own layers that sit behind the speaker (they need the cutout)
    global BEHIND
    BEHIND = bool(b.back or behind)       # words or layers behind the head: a mirrored trial would show them backwards
    if EXTRA.get('grade'):                # one colour grade for the footage, the cutout and every effect slot (.gr)
        b.css.append(f"\n#plate,#cutw,.gr{{filter:{EXTRA['grade']}}}")
    nl = '\n'
    up = f' class="full" style="top:{-LIFT}px"' if LIFT else ''
    footage = [lifted(f'<div id="plate"><video id="bgv" class="full" src="{VIDEO}" muted playsinline data-start="0" '
                      f'data-media-start="0" data-duration="{DUR:.3f}" data-track-index="0"></video></div>'),
               '<div id="back">' + ''.join(b.back) + ''.join(behind) + '</div>']
    if b.cutout:
        footage.append(f'<div id="cutw"{up}><video id="cut" class="full" src="{CUTOUT}" muted playsinline data-start="0" '
                       f'data-media-start="0" data-duration="{DUR:.3f}" data-track-index="1"></video></div>')
    return document(b, footage, safe=safe, audio_track=2)


def reframe_values(r):
    """A trial reel's own framing and colour (scripts/variations.py, references/variations.md), as it is applied:
    -> {'zoom', 'mirror', 'ox', 'oy', 'x', 'grade'} or None. The footage, the cutout and the effect slots scale around
    one point (the face, so captions placed under it still fit), shift sideways a little, may mirror, and get a light
    grade on top. A mirrored trial turns around the middle of the frame, or the picture would not fill it; the shift
    is kept small enough that no edge of the picture ever shows."""
    if not isinstance(r, dict) or not r:
        return None
    z = max(1.0, _num(r.get('zoom'), 1.0))
    mirror = bool(r.get('mirror'))
    ox = 540.0 if mirror else min(max(_num(r.get('ox'), 540.0), 0.0), 1080.0)
    oy = min(max(_num(r.get('oy'), 960.0), 0.0), 1920.0)
    lo, hi = -(1080 - ox) * (z - 1), ox * (z - 1)          # the sideways room before an edge of the picture shows
    if r.get('x') is None and r.get('shift') is not None:   # "shift": -1..1, the share of that room (variations.py)
        sh = min(max(_num(r.get('shift'), 0.0), -1.0), 1.0)
        r = {**r, 'x': sh * hi if sh >= 0 else -sh * lo}
    tx = min(max(_num(r.get('x'), 0.0), lo), hi)
    return {'zoom': round(z, 4), 'mirror': mirror, 'ox': round(ox, 1), 'oy': round(oy, 1), 'x': round(tx, 1),
            'grade': str(r.get('grade') or '').strip()}


def reframe_css(r):
    """-> the css rule for #reframe (captions and layers are outside it: text stays sharp and where it was placed),
    or '' when the reel has no reframe"""
    v = reframe_values(r)
    if not v:
        return ''
    z = v['zoom']
    return (f"\n#reframe{{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:{v['ox']:.1f}px {v['oy']:.1f}px;"
            f"transform:translate({v['x']:.1f}px,0) scale({-z if v['mirror'] else z:.4f},{z:.4f})"
            + (f";filter:{v['grade']}" if v['grade'] else '') + '}')


ARABIC_SERIF = {'newsreader', 'playfair display', 'instrument serif', 'dm serif display'}
ARABIC_HAND = {'caveat', 'marck script', 'covered by your grace', 'permanent marker', 'elsie swash caps', 'yeseva one', 'caveat brush', 'patrick hand'}
RTL_CSS = '''
#root{direction:rtl}
#caps *,#layers *{letter-spacing:0!important;font-style:normal!important;font-synthesis:none}'''


def arabic_face(families):
    """the shipped Arabic face that suits a font-family list: serif, handwritten, or sans (anything else)"""
    first = families.split(',')[0].strip().strip('\'"').lower()
    if first in ARABIC_HAND or 'script' in first or 'hand' in first:
        return 'Studio Arabic Hand'
    if first in ARABIC_SERIF or ('serif' in first and 'sans' not in first):
        return 'Studio Arabic Serif'
    return 'Studio Arabic Sans'


def localise(doc):
    """The page in the reel's language. Right-to-left scripts (Arabic, Persian, Urdu, Hebrew) get direction:rtl on
    the 1080px frame (#root) so the words of a line run right to left. Never dir="rtl" on <html> (HyperFrames then
    renders a black video), and not on #caps alone (it is narrower than the frame: captions with no left set slide
    off centre). No letter spacing or slant (they pull joined letters apart), and an Arabic face after
    every font-family, so each caption style keeps its feel in Arabic letters (engine/fonts/fonts.css)."""
    doc = doc.replace('<html lang="en"', f'<html lang="{LANG}"', 1)
    if not RTL:
        return doc

    def add(m):
        fams = m.group(2).rstrip()
        rule = m.string[m.string.rfind('}', 0, m.start()) + 1:m.start()]
        if ('@font-face' in rule or 'Studio Arabic' in fams or 'var(' in fams
                or fams.split(',')[0].strip() in ('inherit', 'initial', 'unset')):
            return m.group(0)
        return f"{m.group(1)}{fams},'{arabic_face(fams)}'"
    doc = re.sub(r'(font-family:\s*)([^;}"<>]+)', add, doc)
    return doc.replace('</style>', RTL_CSS + '\n</style>', 1)


def document(b, footage, safe=False, audio_track=9):
    """The whole composition: footage layers, effect slots, captions, timeline. Used by page()."""
    nl = '\n'
    fx, fx_audio = slots(b)
    front = layers(b)                     # the buyer's own layers, over the slots and under the captions
    fx_audio = fx_audio + sounds()
    rf = reframe_css(EXTRA.get('reframe'))
    if rf:                                # a trial reel's own framing and colour, around the footage and the slots only
        b.css.append(rf)
    if EXTRA.get('css'):                  # the escape hatch: plain css from plan.json / my-style.json, last so it wins
        b.css.append('\n' + str(EXTRA['css']))
        css_motion_note(EXTRA['css'], 'The style css')
    b.js += reel_motion(EXTRA.get('motion'))   # reel-wide motion: punch-ins on key words, a flash on every cut, ...
    return localise(f'''<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fonts/fonts.css" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{BASE_CSS}{''.join(b.css)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR:.3f}" data-width="1080" data-height="1920">
  <audio id="bga" src="{VOICE}" data-start="0" data-media-start="0" data-duration="{DUR:.3f}" data-track-index="{audio_track}" data-volume="1"></audio>
{nl.join('  ' + h for h in fx_audio)}
{'  <div id="reframe">' if rf else ''}
  <div id="footage">
{nl.join('    ' + h for h in footage)}
  </div>
  <div id="slots">
{nl.join('    ' + h for h in fx)}
  </div>
{'  </div><!--/reframe-->' if rf else ''}
  <div id="layers">
{nl.join('    ' + h for h in front)}
  </div>
  <div id="caps">
{nl.join('    ' + h for h in b.html)}
  </div>
{SAFE_GUIDE if safe else ''}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{nl.join(b.js)}
tl.set({{}}, {{}}, {DUR:.3f});
window.__timelines["main"] = tl;
</script>
</body>
</html>
''')


if __name__ == '__main__':
    print('\n'.join(f'{v[0]}  {k:16} {v[1]}' for k, v in STYLES.items()))
    print('\nThis is the engine. Build a reel with scripts/build_reel.py <project>.')
