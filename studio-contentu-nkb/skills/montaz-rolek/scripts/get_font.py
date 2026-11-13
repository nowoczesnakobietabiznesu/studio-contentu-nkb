#!/usr/bin/env python3
"""Fetch one openly licensed typeface for the buyer's own style, when the example uses a face the skill does not ship.

Usage:  PY get_font.py "<Family Name>" [--weight 700] [--italic] [--list]

  It asks Google Fonts for the family (every family there is under an open licence: OFL, Apache or UFL) and saves one
  .woff file with ALL its letters (Latin plus Polish and German ones: ą ę ł ś ż, ä ö ü ß) into <state folder>/fonts/
  as <Family>-<weight>-<normal|italic>.woff. build_reel.py copies that folder into every project, and a custom
  caption spec uses the file with  "font": "<Family Name>", "file": "<that name>".
  --list   only show the fonts the skill already has (shipped + fetched), then stop

Then it checks the letters. "MISSING LETTERS pl: ..." means the face has no Polish (or German) letters at all: the
browser would draw those in another font, in the middle of a word. Do not use that face for captions in that
language: pick the nearest face that has them (PY get_font.py --list, or another Google family) and tell the buyer
which face stands in for the one in their example.

Never a paid font: if the family is not on Google Fonts this stops and says so. Pick the nearest face that is
(or one the skill ships: engine/fonts), and tell the buyer which face stands in for the one in their example.
Needs the internet once per face. Standard library only.
"""
import os
import re
import struct
import sys
import urllib.error
import urllib.parse
import urllib.request
import zlib

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skillenv  # noqa: E402

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
# a browser without unicode-range support gets ONE file with every subset the family has (a modern one gets a file per
# script, and the plain "latin" one has no Polish letters)
UA_ONE_FILE = 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'
LETTERS = {'pl': 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'de': 'äöüßÄÖÜ'}


def woff_chars(data):
    """the characters a .woff (or .ttf/.otf) file has a glyph for, read from its cmap table (formats 4 and 12)"""
    def table(tag):
        if data[:4] == b'wOFF':
            n = struct.unpack('>H', data[12:14])[0]
            for i in range(n):
                t, off, comp, orig, _ = struct.unpack('>4sIIII', data[44 + 20 * i:64 + 20 * i])
                if t == tag:
                    raw = data[off:off + comp]
                    return zlib.decompress(raw) if comp < orig else raw
        else:
            n = struct.unpack('>H', data[4:6])[0]
            for i in range(n):
                t, _, off, ln = struct.unpack('>4sIII', data[12 + 16 * i:28 + 16 * i])
                if t == tag:
                    return data[off:off + ln]
        return None
    cmap, out = table(b'cmap'), set()
    if not cmap:
        return out
    for i in range(struct.unpack('>H', cmap[2:4])[0]):
        pid, eid, off = struct.unpack('>HHI', cmap[4 + 8 * i:12 + 8 * i])
        fmt = struct.unpack('>H', cmap[off:off + 2])[0]
        if fmt == 4:
            seg = struct.unpack('>H', cmap[off + 6:off + 8])[0] // 2
            p = off + 14
            ends = struct.unpack(f'>{seg}H', cmap[p:p + 2 * seg]); p += 2 * seg + 2
            starts = struct.unpack(f'>{seg}H', cmap[p:p + 2 * seg]); p += 2 * seg
            deltas = struct.unpack(f'>{seg}h', cmap[p:p + 2 * seg]); p += 2 * seg
            ro_at = p
            ranges = struct.unpack(f'>{seg}H', cmap[p:p + 2 * seg])
            for k in range(seg):
                for c in range(starts[k], ends[k] + 1):
                    if c == 0xFFFF:
                        continue
                    if ranges[k] == 0:
                        g = (c + deltas[k]) & 0xFFFF
                    else:
                        a = ro_at + 2 * k + ranges[k] + 2 * (c - starts[k])
                        g = struct.unpack('>H', cmap[a:a + 2])[0] if a + 2 <= len(cmap) else 0
                        g = (g + deltas[k]) & 0xFFFF if g else 0
                    if g:
                        out.add(chr(c))
        elif fmt == 12:
            ng = struct.unpack('>I', cmap[off + 12:off + 16])[0]
            for k in range(ng):
                s, e, _ = struct.unpack('>III', cmap[off + 16 + 12 * k:off + 28 + 12 * k])
                if e - s < 0x30000:
                    out.update(chr(c) for c in range(s, e + 1))
    return out


def opt(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1] if i + 1 < len(sys.argv) else default
    return default


def have():
    shipped = os.path.join(skillenv.SKILL_DIR, 'engine', 'fonts')
    mine = skillenv.my_fonts_dir()
    out = []
    for label, d in (('shipped', shipped), ('fetched', mine)):
        if os.path.isdir(d):
            out += [(label, f) for f in sorted(os.listdir(d)) if f.lower().endswith(('.woff2', '.woff', '.ttf', '.otf'))]
    return out


def main():
    skillenv.utf8_stdio()
    args = [a for a in sys.argv[1:] if not a.startswith('--') and a != opt('--weight')]
    if '--list' in sys.argv:
        for label, f in have():
            print(f'{label:8} {f}')
        return
    if not args:
        sys.exit(__doc__)
    family = ' '.join(args[0].split())
    weight = int(opt('--weight', '400'))
    italic = '--italic' in sys.argv
    def ask(url, ua):
        return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': ua}), timeout=30).read().decode('utf-8', 'replace')

    # one .woff with every subset (Latin, Polish, German...): the older css API answers a browser without
    # unicode-range with a single file. If that fails, the newer API and its plain "latin" file (no Polish letters).
    one = f'https://fonts.googleapis.com/css?family={urllib.parse.quote_plus(family)}:{weight}{"italic" if italic else ""}' \
          '&subset=latin,latin-ext'
    spec = f'{urllib.parse.quote_plus(family)}:ital,wght@{1 if italic else 0},{weight}'
    pick, ext = None, 'woff'
    try:
        m = re.search(r'src:\s*url\(([^)]+)\)', ask(one, UA_ONE_FILE))
        pick = m.group(1) if m else None
    except urllib.error.HTTPError:
        pass
    except (urllib.error.URLError, OSError) as e:
        sys.exit(f'could not reach Google Fonts ({e}). Check the connection, or use a face the skill ships (--list).')
    if not pick:
        try:
            css = ask(f'https://fonts.googleapis.com/css2?family={spec}&display=block', UA)
        except urllib.error.HTTPError as e:
            sys.exit(f'"{family}" at weight {weight}{" italic" if italic else ""} is not on Google Fonts (HTTP {e.code}). The skill only '
                     'fetches openly licensed faces and never a paid one: pick the nearest open face, or one it ships '
                     '(PY get_font.py --list), and tell the buyer which face stands in.')
        except (urllib.error.URLError, OSError) as e:
            sys.exit(f'could not reach Google Fonts ({e}). Check the connection, or use a face the skill ships (--list).')
        blocks = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{[^}]*?src:\s*url\(([^)]+)\)', css)
        pick = next((u for name, u in blocks if name == 'latin'), None) or (blocks[-1][1] if blocks else None)
        ext = 'woff2'
    if not pick:
        sys.exit(f'Google Fonts answered, but with no font file for "{family}" {weight}. Try another weight.')
    dest_dir = skillenv.my_fonts_dir()
    os.makedirs(dest_dir, exist_ok=True)
    name = f'{re.sub(r"[^A-Za-z0-9]", "", family)}-{weight}-{"italic" if italic else "normal"}.{ext}'
    dest = os.path.join(dest_dir, name)
    data = urllib.request.urlopen(urllib.request.Request(pick.strip('\'"'), headers={'User-Agent': UA}), timeout=60).read()
    if len(data) < 2000:
        sys.exit('the font file came back empty. Try again, or use a face the skill ships (--list).')
    with open(dest, 'wb') as fh:
        fh.write(data)
    print(f'fetched {family} {weight}{" italic" if italic else ""} ({len(data) // 1024} KB, open licence, from Google Fonts)')
    print(f'file    {skillenv.shell_path(dest)}')
    try:
        chars = woff_chars(data) if ext == 'woff' else set()
    except (struct.error, zlib.error, IndexError):
        chars = set()
    if chars:
        for lang, need in LETTERS.items():
            miss = ''.join(c for c in need if c not in chars)
            if miss:
                print(f'MISSING LETTERS {lang}: {miss}   this face has no glyph for them, so the browser draws them in '
                      f'another font, mid-word. For captions in this language pick the nearest face that has them and '
                      f'tell the buyer which face stands in.')
        if not any(c not in chars for c in LETTERS['pl'] + LETTERS['de']):
            print('letters  Polish and German: all there')
    else:
        print('letters  not checked (only the plain Latin file came back): Polish letters may fall back to another font')
    print(f'use it  "font": "{family}", "weight": {weight}, "file": "{name}"' + (', "italic": true' if italic else '')
          + '   in the caption spec, or in a layer\'s css with @font-face and url(\'assets/fonts/' + name + '\')')


if __name__ == '__main__':
    main()
