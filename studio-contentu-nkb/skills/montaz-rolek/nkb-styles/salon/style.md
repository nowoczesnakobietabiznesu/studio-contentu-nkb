# Salon (styl całościowy NKB)

Z katalogu stylów NKB: Domowy styl NKB.

- Type: napisy Gabinet (rozstrzelone kapitaliki Poppins, słowa kluczowe kursywą Playfair w akcencie).
- Colour: ciepła korekta (sepia .16, saturate 1.06, contrast 1.02).
- Captions: przy dolnej krawędzi strefy bezpiecznej.
- Pace: spokojne, pauzy skrócone do 0,3 s.
- Sound: miękkie kliknięcia, dzwonek na wezwaniu do działania.
- Akcent = kolor marki klientki (domyślnie złoto NKB #CD9F38); w css i warstwach var(--acc).

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Przypięty tytuł u góry przez całą rolkę (warstwa bez from/to), z hooka TEJ rolki: krótki nadtytuł
(temat, 2–3 słowa) i tytuł (obietnica, do 28 znaków), oba z jej słów:
```json
{"id": "tytul", "anchor": "full", "in": "fade",
 "html": "<div class='sl-t'><span class='e'>AI w biznesie</span><span class='h'>Jak odzyskać wieczory</span></div>",
 "css": ".sl-t{position:absolute;left:86px;right:86px;top:236px;text-align:center;display:grid;gap:12px}.sl-t .e{font:500 39px/1 Poppins;letter-spacing:.28em;text-transform:uppercase;color:var(--acc)}.sl-t .h{font:italic 500 76px/1.1 'Playfair Display';color:#fff;text-shadow:0 9px 47px rgba(0,0,0,.35)}"}
```
Tytuł nie może zejść na czubek głowy: dół tytułu co najmniej 40 px nad `head.top` z `layout.json`.

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
