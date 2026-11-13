# Elegancki (styl całościowy NKB)

Z katalogu stylów NKB: Studio wywiadu.

- Type: drobne rozstrzelone kapitaliki Montserrat 500 i pod nimi duże małe litery DM Serif Display.
- Colour: naturalny, lekki kontrast (jak Viral).
- Motion: słowa wysuwają się z rozmycia; powolny najazd kamery przez całą rolkę.
- Pace: wolne, powolny najazd zamiast cięć z uderzeniem.
- Sound: sam głos.
- Akcent = kolor marki klientki (domyślnie złoto NKB #CD9F38); w css i warstwach var(--acc).

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Jeden przelot światła na otwarcie (0–1,1 s):
```json
{"id": "swiatlo", "anchor": "full", "from": 0.0, "to": 1.1, "html": "<div class='el-sw'></div>",
 "css": ".el-sw{position:absolute;top:-200px;bottom:-200px;left:0;width:430px;background:linear-gradient(90deg,transparent,rgba(255,240,215,.35),transparent);mix-blend-mode:screen}",
 "motion": [{"target": ".el-sw", "tween": "fromTo", "from": {"x": -520, "skewX": -18}, "vars": {"x": 1300, "skewX": -18, "duration": 1.1, "ease": "power2.out"}}]}
```

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
