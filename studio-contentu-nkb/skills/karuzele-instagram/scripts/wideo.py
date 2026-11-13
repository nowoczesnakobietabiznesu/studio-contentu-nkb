#!/usr/bin/env python3
"""Studio Contentu NKB: slajdy z ruchomym okienkiem (wideo albo przewijana strona www) w karuzeli.

Slajd z okienkiem to zwykły slajd z polem "image" w carousel.json, do którego dochodzi jedno z dwóch pól:
  "video": "assets/klip.mp4", "start": 3.2, "end": 9.0, "sound": false     fragment nagrania w okienku
  "page": "assets/strona.png", "seconds": 12                               długi zrzut strony, przewijany w okienku
"src" to obraz, który okienko pokazuje na PNG (klatka z nagrania albo sam zrzut strony).

Użycie:
  PY wideo.py strona "<url>" "<plik.png>" [--szerokosc 460] [--zdanie "zdanie do podświetlenia"]...
        zrzut całej strony www (bez banerów cookies), wybrane zdania w złotym markerze
  PY wideo.py zloz "<folder karuzeli>" [--only 2,5]
        po `carousel.py render`: składa MP4 1080 px szerokości, 30 kl./s, dla każdego slajdu z okienkiem
        (slides/<nazwa>-NN.mp4) i kładzie gotowy zestaw do wrzucenia w folder do-publikacji/
        (PNG albo MP4 w kolejności slajdów)

Linie wyniku:
  STATUS strona OK <plik> | STATUS strona FAILED <dlaczego>
  STATUS wideo OK <slajd> <plik> <sekundy>s dzwiek=tak|nie
  STATUS wideo FAILED <slajd> <dlaczego>
  STATUS publikacja <folder> <ile plików>
"""
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'engine'))
import render as R  # noqa: E402
skillenv = R.skillenv

FPS = 30
MIN_S, MAX_S = 3.0, 60.0


def say(line):
    print(line, flush=True)


def opt(args, name, default=None):
    return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default


def opts(args, name):
    return [args[i + 1] for i, a in enumerate(args) if a == name and i + 1 < len(args)]


def path_in(project, p):
    p = os.path.expanduser(str(p))
    return p if os.path.isabs(p) else os.path.join(project, p)


def duration(ff_probe, f):
    out = subprocess.run([ff_probe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f],
                         capture_output=True, text=True).stdout.strip()
    try:
        return float(out)
    except ValueError:
        return 0.0


def has_audio(ff_probe, f):
    out = subprocess.run([ff_probe, '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', f],
                         capture_output=True, text=True).stdout.strip()
    return bool(out)


def mask_png(w, h, radius, out):
    from PIL import Image, ImageDraw
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=max(0, int(radius)), fill=255)
    m.save(out)
    return out


# ------------------------------------------------------------------ zrzut strony
def podglad(page_png, ratio=1.15):
    """Górna część zrzutu w proporcjach okienka: to idzie w "src", żeby okienko na slajdzie było szerokie,
    a nie wąskie jak cały długi zrzut. Pełny zrzut idzie w "page"."""
    from PIL import Image
    im = Image.open(page_png).convert('RGB')
    h = min(im.height, round(im.width * ratio))
    out = os.path.splitext(page_png)[0] + '-podglad.jpg'
    im.crop((0, 0, im.width, h)).save(out, quality=92)
    return out


def strona(args):
    url, out = (args + [None, None])[:2]
    if not url or not out:
        sys.exit('Użycie: wideo.py strona "<url>" "<plik.png>" [--szerokosc 460] [--zdanie "..."]')
    browser = R.browser_path()
    rec = skillenv.load() if hasattr(skillenv, 'load') else {}
    node = rec.get('node') if rec.get('node') and os.path.isfile(rec.get('node')) else skillenv.find_node()[0]
    if not browser or not node:
        say('STATUS strona FAILED brak przeglądarki albo Node: uruchom najpierw sprawdzenie Studia (montaz-rolek, krok 0)')
        return
    out = os.path.abspath(os.path.expanduser(out))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cmd = [node, os.path.join(HERE, 'strona.mjs'), browser, url, out, str(opt(args, '--szerokosc', '460'))] + opts(args, '--zdanie')
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
    if r.returncode == 0 and os.path.isfile(out):
        say(f'STATUS strona OK {out}')
        say(f'STATUS strona PODGLAD {podglad(out)}')
        for line in r.stdout.splitlines():
            if line.startswith('NIE ZNALEZIONO'):
                say('STATUS strona ' + line)
    else:
        say('STATUS strona FAILED ' + ((r.stderr or r.stdout).strip().splitlines() or ['nieznany błąd'])[-1])


# ------------------------------------------------------------------ składanie
def compose_video(m, project, png, box, out, work, ff, fp):
    src = path_in(project, m['video'])
    if not os.path.isfile(src):
        return f'nie ma pliku nagrania {src}'
    start = float(m.get('start') or 0)
    full = duration(fp, src)
    end = float(m.get('end') or full or start + MIN_S)
    clip = max(0.1, min(end, full or end) - start)
    secs = min(MAX_S, max(MIN_S, clip))
    loop = clip < MIN_S
    x, y, w, h, rad = box
    mask = mask_png(w, h, rad, os.path.join(work, f'maska-{os.path.basename(out)}.png'))
    sound = bool(m.get('sound')) and has_audio(fp, src)
    cmd = [ff, '-loglevel', 'error', '-y', '-loop', '1', '-framerate', str(FPS), '-i', png]
    if loop:
        cmd += ['-stream_loop', '-1']
    cmd += ['-ss', f'{start:.3f}', '-t', f'{clip:.3f}' if not loop else f'{secs:.3f}', '-i', src, '-loop', '1', '-i', mask,
            '-filter_complex',
            f'[1:v]fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,format=rgba[v];'
            f'[2:v]format=gray,scale={w}:{h}[m];[v][m]alphamerge[vm];'
            f'[0:v][vm]overlay={x}:{y}:shortest=1,format=yuv420p[out]',
            '-map', '[out]']
    if sound:
        cmd += ['-map', '1:a:0', '-c:a', 'aac', '-b:a', '160k', '-ac', '2']
    else:
        cmd += ['-an']
    cmd += ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-r', str(FPS), '-t', f'{secs:.3f}',
            '-movflags', '+faststart', out]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0 or not os.path.isfile(out):
        return (r.stderr.strip().splitlines() or ['ffmpeg nie złożył wideo'])[-1]
    return (secs, sound)


def compose_page(m, project, png, box, out, ff):
    from PIL import Image, ImageDraw
    import numpy as np
    src = path_in(project, m['page'])
    if not os.path.isfile(src):
        return f'nie ma zrzutu strony {src}'
    secs = float(m.get('seconds') or 12)
    secs = min(MAX_S, max(MIN_S, secs))
    x, y, w, h, rad = box
    bg = Image.open(png).convert('RGB')
    page = Image.open(src).convert('RGB')
    page = page.resize((w, max(h, round(page.height * w / page.width))), Image.LANCZOS)
    pa = np.asarray(page).astype(int)
    gold = (abs(pa[..., 0] - 233) < 14) & (abs(pa[..., 1] - 205) < 16) & (abs(pa[..., 2] - 148) < 22)   # złoty marker
    rows = np.where(gold.sum(1) > 40)[0]
    marks = [int(g.mean()) for g in np.split(rows, np.where(np.diff(rows) > 60)[0] + 1) if len(g)] if len(rows) else []
    maxy = page.height - h
    target = min(maxy, max(0, marks[-1] - int(h * .42))) if marks else maxy // 2
    keys = [(0, 0), (secs * .13, 0), (secs * .30, target), (secs * .53, target), (secs * .77, maxy), (secs, maxy)]
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=max(0, int(rad)), fill=255)

    def ypos(t):
        for (ta, ya), (tb, yb) in zip(keys, keys[1:]):
            if ta <= t <= tb:
                u = 0 if tb == ta else (t - ta) / (tb - ta)
                u = u * u * (3 - 2 * u)
                return ya + (yb - ya) * u
        return keys[-1][1]

    W, H = bg.size
    p = subprocess.Popen([ff, '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                          '-pix_fmt', 'yuv420p', '-an', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for k in range(int(FPS * secs)):
        top = round(ypos(k / FPS))
        fr = bg.copy()
        fr.paste(page.crop((0, top, w, top + h)), (x, y), mask)
        p.stdin.write(fr.tobytes())
    p.stdin.close()
    p.wait()
    if p.returncode != 0 or not os.path.isfile(out):
        return 'ffmpeg nie złożył przewijanej strony'
    return (secs, False)


def zloz(args):
    project = os.path.abspath(skillenv.path_arg(args[0])) if args else None
    if not project or not os.path.isfile(os.path.join(project, 'carousel.json')):
        sys.exit('Użycie: wideo.py zloz "<folder karuzeli>" [--only 2,5]')
    data = R.read_json(os.path.join(project, 'carousel.json'))
    boxes = R.read_json(os.path.join(project, 'work', 'video-boxes.json'), {})
    only = {int(n) for n in str(opt(args, '--only', '')).split(',') if n.strip().isdigit()}
    name = R.slug(data.get('slug') or os.path.basename(project))
    slides_dir = os.path.join(project, 'slides')
    work = os.path.join(project, 'work', 'wideo')
    os.makedirs(work, exist_ok=True)
    ff, fp = skillenv.tool('ffmpeg'), skillenv.tool('ffprobe')
    from PIL import Image
    for i, s in enumerate(data.get('slides', []), 1):
        m = s.get("image") if isinstance(s.get("image"), dict) else None
        out = os.path.join(slides_dir, f'{name}-{i:02d}.mp4')
        if not m or not (m.get('video') or m.get('page')):
            if os.path.isfile(out) and (not only or i in only):
                os.remove(out)   # nasz stary plik: ten slajd nie ma już okienka
            continue
        if only and i not in only:
            continue
        rec = boxes.get(str(i))
        if not rec or not rec.get('boxes') or not os.path.isfile(rec.get('png', '')):
            say(f'STATUS wideo FAILED {i} brak pomiaru okienka: najpierw carousel.py render')
            continue
        png = rec['png']
        b = rec['boxes'][0]
        pw = Image.open(png).size[0]
        k = pw / data_width(data)
        box = (round(b['x'] * k), round(b['y'] * k), round(b['w'] * k) // 2 * 2, round(b['h'] * k) // 2 * 2, b.get('r', 0) * k)
        res = compose_video(m, project, png, box, out, work, ff, fp) if m.get('video') else compose_page(m, project, png, box, out, ff)
        if isinstance(res, tuple):
            say(f'STATUS wideo OK {i} {out} {res[0]:.1f}s dzwiek={"tak" if res[1] else "nie"}')
        else:
            say(f'STATUS wideo FAILED {i} {res}')
    publish(project, name, len(data.get('slides', [])))


def data_width(data):
    prof = R.profile()
    look = R.load_look(data.get('look') or prof.get('defaultLook') or 'horizon')
    return R.SIZES.get(data.get('size') or prof.get('size') or look['size'], R.SIZES['3:4'])[0]


def publish(project, name, n):
    pub = os.path.join(project, 'do-publikacji')
    if os.path.isdir(pub):
        shutil.rmtree(pub)   # nasz własny folder, składany od nowa
    os.makedirs(pub)
    count = 0
    for i in range(1, n + 1):
        for ext in ('mp4', 'png'):
            f = os.path.join(project, 'slides', f'{name}-{i:02d}.{ext}')
            if os.path.isfile(f):
                shutil.copy2(f, os.path.join(pub, f'{name}-{i:02d}.{ext}'))   # the carousel's name, so two sets never mix on her phone
                count += 1
                break
    say(f'STATUS publikacja {pub} {count}')


def main():
    skillenv.utf8_stdio()
    a = sys.argv[1:]
    if not a or a[0] not in ('strona', 'zloz'):
        sys.exit(__doc__)
    {'strona': strona, 'zloz': zloz}[a[0]](a[1:])


if __name__ == '__main__':
    main()
