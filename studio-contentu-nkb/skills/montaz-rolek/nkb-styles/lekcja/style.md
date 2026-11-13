# Lekcja (styl całościowy NKB)

Z katalogu stylów NKB: Krok po kroku.

- Type: napisy Marker (kremowa karteczka, zakreślacz w akcencie na słowach kluczowych).
- Colour: jasny, czysty obraz (brightness 1.07, saturate 1.08).
- Captions: przy dolnej krawędzi strefy bezpiecznej.
- Pace: średnie, każdy krok to osobna część.
- Sound: odhaczenie przy każdym kroku.
- Akcent = kolor marki klientki (domyślnie złoto NKB #CD9F38); w css i warstwach var(--acc).

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Etykieta kroku i pasek postępu w lewym górnym rogu, z kroków, które klientka SAMA wymienia
(„po pierwsze”, „krok drugi”), od słowa, które otwiera krok, do początku następnego. Bez kroków w nagraniu: bez etykiety.
```json
{"id": "krok1", "anchor": "full", "from": 0.4, "to": 6.0, "in": "pop",
 "html": "<div class='lk'><span class='c'>Krok 1 z 3</span><span class='p'><i class='on'></i><i></i><i></i></span></div>",
 "css": ".lk{position:absolute;left:65px;top:240px;display:flex;align-items:center;gap:27px}.lk .c{font:600 43px/1 Poppins;background:var(--acc);color:#141414;border-radius:999px;padding:17px 35px}.lk .p{display:flex;gap:13px}.lk .p i{width:76px;height:13px;border-radius:11px;background:rgba(255,255,255,.45)}.lk .p i.on{background:#fff}"}
```

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
