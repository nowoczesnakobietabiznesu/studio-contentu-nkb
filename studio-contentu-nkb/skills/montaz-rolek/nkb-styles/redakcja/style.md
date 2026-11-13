# Redakcja (styl całościowy NKB)

Z katalogu stylów NKB: Rolka jak okładka magazynu.

- Type: napisy Cytat (Cormorant Garamond kursywa w polskim cudzysłowie, złota linia).
- Colour: ciepła korekta, kremowa ramka 32 px dookoła kadru (warstwa stała).
- Captions: przy dolnej krawędzi strefy bezpiecznej.
- Pace: spokojne.
- Sound: szelest papieru przy zmianie sekcji.
- Akcent = kolor marki klientki (domyślnie złoto NKB #CD9F38); w css i warstwach var(--acc).

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Winieta jak na okładce: nazwa marki klientki (zapytaj raz i zapisz w „Standing notes”) i podpis z TĄ
rolką (miesiąc i rok albo temat), przez całą rolkę:
```json
{"id": "winieta", "anchor": "full", "in": "fade",
 "html": "<div class='rd-m'><span class='m'>Twoja marka</span><span class='i'>listopad 2026</span></div>",
 "css": ".rd-m{position:absolute;left:0;right:0;top:236px;text-align:center;display:grid;gap:13px}.rd-m .m{font:900 91px/1 'Bodoni Moda';letter-spacing:.04em;text-transform:uppercase;color:#fff;text-shadow:0 9px 56px rgba(0,0,0,.3)}.rd-m .i{font:500 35px/1 Poppins;letter-spacing:.24em;text-transform:uppercase;color:#fff;opacity:.85}"}
```
Nigdy wymyślony numer wydania. Długa nazwa marki: mniejszy krój, tak żeby zmieściła się w 980 px.

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
