#!/usr/bin/env python3
"""Narzędzia do przerabiania długiego nagrania na krótkie b-rolle.

Podkomendy:
  check     sprawdza wymagania (ffmpeg, ffprobe, czcionka, miejsce na dysku)
  info      odczytuje parametry nagrania
  arkusze   robi arkusze klatek ze znacznikami czasu
  podglady  robi lekkie podglądy kandydatów z zapasem
  strona    buduje lokalną stronę przeglądową i ją otwiera
  tnij      wycina zatwierdzone fragmenty w 1080p i je weryfikuje

Wymaga tylko Pythona 3.8+ (biblioteka standardowa) oraz ffmpeg i ffprobe w PATH.
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SKRYPT = Path(__file__).resolve()
SZABLON = SKRYPT.parent.parent / "assets" / "przeglad_szablon.html"

CZCIONKI = [
    "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeuib.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]


def znajdz_czcionke():
    for c in CZCIONKI:
        if os.path.exists(c):
            return c
    return None


def czcionka_do_filtra(p):
    # ffmpeg wymaga ukośników i escapowanego dwukropka w ścieżce czcionki
    return p.replace("\\", "/").replace(":", "\\:")


def uruchom(cmd, przechwyc=True):
    r = subprocess.run(cmd, capture_output=przechwyc, text=True, encoding="utf-8", errors="replace")
    return r


def ffprobe_json(plik, *args):
    r = uruchom(["ffprobe", "-v", "error", *args, "-of", "json", str(plik)])
    if r.returncode != 0:
        raise SystemExit(f"ffprobe nie odczytał pliku: {plik}\n{r.stderr.strip()}")
    return json.loads(r.stdout or "{}")


def fmt(t):
    t = round(float(t), 1)
    m, s = divmod(t, 60)
    s_txt = f"{s:04.1f}".replace(".", ",") if s != int(s) else f"{int(s):02d}"
    return f"{int(m):02d}:{s_txt}"


# ---------------------------------------------------------------- check
INSTRUKCJE = {
    "Windows": {
        "ffmpeg": "winget install -e --id Gyan.FFmpeg   (potem zamknij i otwórz aplikację, żeby PATH się odświeżył)",
        "python": "winget install -e --id Python.Python.3.12",
    },
    "Darwin": {
        "ffmpeg": "brew install ffmpeg   (jeśli nie ma Homebrew: https://brew.sh)",
        "python": "brew install python   albo instalator z https://www.python.org",
    },
    "Linux": {
        "ffmpeg": "sudo apt install ffmpeg   (lub odpowiednik dla dystrybucji)",
        "python": "sudo apt install python3",
    },
}


def cmd_check(a):
    system = platform.system()
    instr = INSTRUKCJE.get(system, INSTRUKCJE["Linux"])
    brak = []
    print(f"System: {system} {platform.release()}")
    print(f"[OK] Python {platform.python_version()}")
    for narz in ("ffmpeg", "ffprobe"):
        sciezka = shutil.which(narz)
        if sciezka:
            wersja = uruchom([narz, "-version"]).stdout.splitlines()[:1]
            print(f"[OK] {narz}: {wersja[0] if wersja else sciezka}")
        else:
            print(f"[BRAK] {narz}")
            brak.append(narz)
    if brak:
        print(f"  Instalacja: {instr['ffmpeg']}")
    if shutil.which("ffmpeg"):
        filtry = uruchom(["ffmpeg", "-hide_banner", "-filters"]).stdout
        for f in ("drawtext", "tile", "scale"):
            print(("[OK] " if f" {f} " in filtry else "[BRAK] ") + f"filtr ffmpeg: {f}")
            if f" {f} " not in filtry:
                brak.append(f"filtr {f}")
        if " drawtext " not in filtry:
            print("  Ta kompilacja ffmpeg nie ma drawtext. Zainstaluj pełną wersję (np. Gyan.FFmpeg na Windows).")
    cz = znajdz_czcionke()
    print(f"[OK] czcionka do znaczników czasu: {cz}" if cz else
          "[UWAGA] brak czcionki do znaczników czasu: arkusze będą bez godzin, czas liczy się z pozycji kafelka")
    folder = Path(a.folder) if a.folder else Path.home()
    kotwica = folder
    while not kotwica.exists() and kotwica != kotwica.parent:
        kotwica = kotwica.parent
    wolne = shutil.disk_usage(kotwica).free / 1024**3
    print(("[OK] " if wolne >= 2 else "[UWAGA] ") + f"wolne miejsce przy {kotwica}: {wolne:.1f} GB (potrzeba ok. 2 GB)")
    if system == "Windows" and "\\appdata\\" in str(folder).lower():
        print("[UWAGA] folder leży w AppData. Przeglądarka może nie mieć do niego dostępu. Wybierz zwykły folder na dysku.")
    if brak:
        print("\nWYNIK: brakuje: " + ", ".join(brak))
        sys.exit(1)
    print("\nWYNIK: wszystko gotowe")


# ---------------------------------------------------------------- info
def tylko_w_chmurze(plik):
    try:
        attrs = os.stat(plik).st_file_attributes  # tylko Windows
    except (AttributeError, OSError):
        return False
    return bool(attrs & (0x400000 | 0x40000 | 0x1000))


def odczytaj_info(plik):
    d = ffprobe_json(plik, "-show_format", "-show_streams")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), None)
    if not v:
        raise SystemExit("W pliku nie ma ścieżki wideo.")
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(float(sd["rotation"]))
    rot = int(v.get("tags", {}).get("rotate", rot))
    w, h = int(v["width"]), int(v["height"])
    if abs(rot) % 180 == 90:
        w, h = h, w
    num, den = (v.get("avg_frame_rate") or v.get("r_frame_rate") or "30/1").split("/")
    fps = float(num) / float(den) if float(den) else 30.0
    # odstęp klatek kluczowych z pierwszych ok. 20 s
    r = uruchom(["ffprobe", "-v", "error", "-read_intervals", "%+20", "-skip_frame", "nokey",
                 "-select_streams", "v:0", "-show_entries", "frame=pts_time", "-of", "csv=p=0", str(plik)])
    kl = [float(x.strip(",")) for x in r.stdout.split() if x.strip(",")]
    gop = (kl[-1] - kl[0]) / (len(kl) - 1) if len(kl) > 1 else None
    return {
        "plik": str(plik),
        "dlugosc_s": round(float(d["format"].get("duration", 0)), 2),
        "rozmiar_GB": round(int(d["format"].get("size", 0)) / 1024**3, 2),
        "szerokosc": w, "wysokosc": h,
        "orientacja": "pionowa" if h > w else "pozioma" if w > h else "kwadrat",
        "kodek": v.get("codec_name"), "fps": round(fps, 3), "rotacja": rot,
        "odstep_klatek_kluczowych_s": round(gop, 2) if gop else None,
        "dzwiek": any(s.get("codec_type") == "audio" for s in d.get("streams", [])),
        "tylko_w_chmurze": tylko_w_chmurze(plik),
    }


def cmd_info(a):
    i = odczytaj_info(a.wideo)
    print(json.dumps(i, ensure_ascii=False, indent=2))
    if i["tylko_w_chmurze"]:
        print("\nUWAGA: plik jest tylko w chmurze (OneDrive lub podobne). Odczyt wymusi pobranie całości. "
              "Najpierw zapytaj użytkowniczkę, czy pobrać go na dysk.")


# ---------------------------------------------------------------- arkusze
def cmd_arkusze(a):
    i = odczytaj_info(a.wideo)
    out = Path(a.folder)
    out.mkdir(parents=True, exist_ok=True)
    kol, wier = (6, 4) if i["orientacja"] == "pionowa" else (4, 6)
    miniatura = "scale=216:-2" if i["orientacja"] == "pionowa" else "scale=384:-2"
    filtr = [f"fps={1 / a.co:.6f}", miniatura]
    cz = znajdz_czcionke()
    if cz:
        filtr.append(f"drawtext=fontfile='{czcionka_do_filtra(cz)}':text='%{{pts\\:hms}}':x=6:y=6:fontsize=22:"
                     "fontcolor=white:box=1:boxcolor=black@0.65:boxborderw=4")
    filtr.append(f"tile={kol}x{wier}:padding=4:margin=4")
    tylko_kluczowe = i["odstep_klatek_kluczowych_s"] and i["odstep_klatek_kluczowych_s"] <= a.co + 0.05
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    if tylko_kluczowe:
        cmd += ["-skip_frame", "nokey"]
    cmd += ["-i", a.wideo, "-vf", ",".join(filtr), "-q:v", "3", str(out / "arkusz_%02d.jpg")]
    print(f"Dekodowanie: {'tylko klatki kluczowe (szybko)' if tylko_kluczowe else 'pełne (wolniej, rzadkie klatki kluczowe)'}")
    r = uruchom(cmd)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    pliki = sorted(out.glob("arkusz_*.jpg"))
    na_arkusz = kol * wier
    print(f"Gotowe: {len(pliki)} arkuszy, {na_arkusz} klatek na arkusz, klatka co {a.co} s.")
    print(f"Arkusz N (od 1) zaczyna się w czasie (N-1)*{na_arkusz * a.co} s." + ("" if cz else " Brak godzin na kafelkach."))
    for p in pliki:
        print(p)


# ---------------------------------------------------------------- podglady
def wczytaj_fragmenty(p):
    d = json.loads(Path(p).read_text(encoding="utf-8-sig"))
    return d, d["fragmenty"]


def cmd_podglady(a):
    _, frag = wczytaj_fragmenty(a.fragmenty)
    out = Path(a.folder) / "podglady"
    out.mkdir(parents=True, exist_ok=True)
    skala = "scale=w='if(gt(iw,ih),-2,540)':h='if(gt(iw,ih),540,-2)'"
    for f in frag:
        ss = max(0.0, float(f["start"]) - a.zapas)
        dur = float(f["koniec"]) - ss + a.zapas
        plik = out / f"klip_{int(f['id']):02d}.mp4"
        # dekodowanie programowe: dekoder sprzętowy potrafi przerwać plik w połowie
        r = uruchom(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{ss:.3f}", "-i", a.wideo,
                     "-t", f"{dur:.3f}", "-vf", skala, "-c:v", "libx264", "-preset", "veryfast", "-crf", "27",
                     "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(plik)])
        ok = r.returncode == 0 and plik.exists()
        print(f"{int(f['id']):02d} {'OK' if ok else 'BŁĄD'}" + ("" if ok else f": {r.stderr.strip()[:300]}"), flush=True)
    print(f"Podglądy w: {out}")


# ---------------------------------------------------------------- strona
def otworz(sciezka):
    s = str(sciezka)
    system = platform.system()
    if system == "Windows":
        os.startfile(s)  # noqa
    elif system == "Darwin":
        subprocess.run(["open", s])
    else:
        subprocess.run(["xdg-open", s])


def cmd_strona(a):
    d, _ = wczytaj_fragmenty(a.fragmenty)
    d.setdefault("zapas", a.zapas)
    html = SZABLON.read_text(encoding="utf-8-sig")
    dane = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__DANE__", dane)
    out = Path(a.folder)
    out.mkdir(parents=True, exist_ok=True)
    plik = out / "Przeglad_brolli.html"
    plik.write_text(html, encoding="utf-8")
    brakujace = [f["id"] for f in d["fragmenty"] if not (out / "podglady" / f"klip_{int(f['id']):02d}.mp4").exists()]
    if brakujace:
        print(f"UWAGA: brak podglądów dla: {brakujace}")
    print(f"Strona: {plik}")
    if a.otworz:
        otworz(plik)
        print("Otwarto w domyślnej przeglądarce.")


# ---------------------------------------------------------------- tnij
def policz_klatki(plik):
    r = uruchom(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                 "-show_entries", "stream=nb_read_packets:format=duration", "-of", "json", str(plik)])
    d = json.loads(r.stdout or "{}")
    kl = int((d.get("streams") or [{}])[0].get("nb_read_packets", 0))
    return float(d.get("format", {}).get("duration", 0)), kl


def cmd_tnij(a):
    i = odczytaj_info(a.wideo)
    ciecia = json.loads(Path(a.ciecia).read_text(encoding="utf-8-sig"))
    out = Path(a.folder)
    out.mkdir(parents=True, exist_ok=True)
    rob = Path(a.robocze)
    rob.mkdir(parents=True, exist_ok=True)
    skala = (f"scale=w='if(gt(iw,ih),-2,min({a.krotszy_bok},iw))':"
             f"h='if(gt(iw,ih),min({a.krotszy_bok},ih),-2)':flags=lanczos")
    wyniki = []
    for c in ciecia:
        start, koniec = float(c["start"]), float(c["koniec"])
        dur = koniec - start
        nazwa = f"{a.prefiks}_{int(c['id']):02d}_{c['nazwa']}_{a.krotszy_bok}p.mp4"
        plik = out / nazwa
        for proba in (1, 2):
            r = uruchom(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{start:.3f}", "-i", a.wideo,
                         "-t", f"{dur:.3f}", "-vf", skala, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(plik)])
            dl, kl = policz_klatki(plik) if plik.exists() else (0, 0)
            ok = abs(dl - dur) < 0.25 and kl >= round(dur * i["fps"]) - 3
            if ok:
                break
        wyniki.append({"plik": nazwa, "oczekiwane_s": round(dur, 2), "dlugosc_s": round(dl, 2), "klatki": kl,
                       "ok": ok})
        print(f"{nazwa}: {dl:.2f} s / {dur:.2f} s, {kl} klatek -> {'OK' if ok else 'PROBLEM'}", flush=True)
    # arkusz pierwszych klatek do obejrzenia
    tmp = rob / "pierwsze"
    tmp.mkdir(exist_ok=True)
    for j, w in enumerate(wyniki, 1):
        uruchom(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(out / w["plik"]), "-frames:v", "1",
                 "-vf", "scale=w='if(gt(iw,ih),-2,180)':h='if(gt(iw,ih),180,-2)'", str(tmp / f"{j:02d}.jpg")])
    kol = min(7, max(1, len(wyniki)))
    wier = (len(wyniki) + kol - 1) // kol
    arkusz = rob / "pierwsze_klatki.jpg"
    uruchom(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(tmp / "%02d.jpg"),
             "-vf", f"tile={kol}x{wier}:padding=4", "-frames:v", "1", str(arkusz)])
    zle = [w["plik"] for w in wyniki if not w["ok"]]
    print(f"\nPierwsze klatki (kolejność jak wyżej): {arkusz}")
    print("WYNIK: wszystkie pliki kompletne" if not zle else "WYNIK: problem z: " + ", ".join(zle))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("check"); p.add_argument("--folder"); p.set_defaults(f=cmd_check)
    p = sp.add_parser("info"); p.add_argument("wideo"); p.set_defaults(f=cmd_info)
    p = sp.add_parser("arkusze"); p.add_argument("wideo"); p.add_argument("folder")
    p.add_argument("--co", type=float, default=2.0, help="odstęp między klatkami w sekundach"); p.set_defaults(f=cmd_arkusze)
    p = sp.add_parser("podglady"); p.add_argument("wideo"); p.add_argument("fragmenty"); p.add_argument("folder")
    p.add_argument("--zapas", type=float, default=1.5); p.set_defaults(f=cmd_podglady)
    p = sp.add_parser("strona"); p.add_argument("fragmenty"); p.add_argument("folder")
    p.add_argument("--zapas", type=float, default=1.5); p.add_argument("--otworz", action="store_true")
    p.set_defaults(f=cmd_strona)
    p = sp.add_parser("tnij"); p.add_argument("wideo"); p.add_argument("ciecia"); p.add_argument("folder")
    p.add_argument("--robocze", required=True, help="folder roboczy na arkusz kontrolny")
    p.add_argument("--prefiks", default="brolle"); p.add_argument("--krotszy-bok", type=int, default=1080)
    p.set_defaults(f=cmd_tnij)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
