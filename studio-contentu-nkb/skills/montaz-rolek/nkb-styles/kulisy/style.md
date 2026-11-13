# Kulisy (styl całościowy NKB)

Z katalogu stylów NKB: Bez pokazywania twarzy.

- Obraz: przebitki od klientki (biurko, kawa, ekran, ręce) zamiast twarzy; jej głos z nagrania leci dalej.
- Type: napisy Maszynopis (JetBrains Mono na zielonym pasku, pisanie litera po literze).
- Colour: ciepła korekta na przebitkach.
- Pace: średnie, przebitka co 2–3 s.
- Sound: ciche stukanie klawiatury, szum tła.
- Akcent = kolor marki klientki (domyślnie złoto NKB #CD9F38); w css i warstwach var(--acc).

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Przebitki: klientka podsyła krótkie nagrania (pionowe 9:16). Przytnij je ffmpegiem do 2–3 s, zapisz w
`<project>/assets/broll/` (1080x1920) i połóż jako pełnoekranowe warstwy jedna po drugiej, tak żeby pokryły całą rolkę:
```json
{"id": "przebitka1", "anchor": "full", "from": 0.0, "to": 2.0,
 "media": {"src": "assets/broll/biurko.mp4", "x": 0, "y": 0, "w": 1080}, "css": "#ly0 video{filter:sepia(.16) saturate(1.06) contrast(1.02)}"}
```
Kolejność: od szerokiego ujęcia do zbliżeń, bez dwóch podobnych obok siebie. Bez przebitek nie da się zrobić tego
stylu: poproś o 3–6 krótkich nagrań.

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
