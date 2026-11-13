# Notatnik (styl całościowy NKB)

Z katalogu stylów NKB: Jasno, z kursywą i dopiskami.

- Type: drobne małe litery Inter 500 (kremowe) i pod nimi linia kursywą Instrument Serif w akcencie.
- Colour: jasny, czysty i neutralny (brightness 1.07, saturate 1.08), bez sepii i winiety.
- Captions: dwie linie przy dolnej krawędzi strefy bezpiecznej.
- Pace: spokojne, naturalne pauzy zostają.
- Sound: sam głos.
- Akcent = kolor marki klientki (domyślnie złoto NKB #CD9F38); w css i warstwach var(--acc).

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Iskierki ✦ w akcencie obok kursywy na słowach kluczowych i odręczny dopisek Caveat ze strzałką, który
klientka MÓWI albo który komentuje jej słowa („za darmo!” przy „darmowym”), najwyżej jeden na 8–10 s:
```json
{"id": "iskry1", "anchor": "full", "from": 2.9, "to": 3.76,
 "html": "<span class='spk a'>✦</span><span class='spk b'>✦</span>",
 "css": ".spk{position:absolute;color:var(--acc);font:400 65px/1 Poppins;text-shadow:0 0 22px rgba(255,255,255,.5)}.spk.a{left:130px;top:1150px}.spk.b{right:130px;top:1270px}",
 "motion": [{"target": ".spk", "tween": "fromTo", "from": {"scale": 0.7, "opacity": 0.25}, "vars": {"scale": 1.1, "opacity": 1, "duration": 0.55, "yoyo": true, "repeat": 3, "stagger": 0.2}}]}
```

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
