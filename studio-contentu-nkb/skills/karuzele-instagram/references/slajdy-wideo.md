# Slajdy z ruchomym okienkiem

Slajd karuzeli na Instagramie może być filmem. Okienko z ruchomym wideo albo przewijaną stroną www przyciąga
wzrok mocniej niż obraz. Używaj go wtedy, gdy temat tego potrzebuje, nie na siłę:

- **przed i po**: surowe nagranie i gotowy efekt, przykład z narzędzia, zmiana na ekranie;
- **demo**: coś się dzieje na ekranie (narzędzie działa, lista się wypełnia, wynik się pojawia);
- **dowód ze strony www**: przewijana strona z podświetlonym zdaniem (premiera, zasady, opis funkcji);
- **głos klientki albo autorki**: fragment nagrania, w którym ważne jest to, co słychać (opinia, głosówka).

## Dźwięk: tak albo nie

- **Bez dźwięku**, gdy liczy się obraz (przed i po, demo, ekran). Muzykę użytkowniczka dodaje w Instagramie.
- **Z dźwiękiem**, gdy liczy się to, co ktoś mówi (głosówka, opinia, fragment wypowiedzi). Wtedy przypomnij, żeby
  nie dodawała muzyki w Instagramie, bo przykryje głos, a na slajdzie daj krótką informację „Włącz dźwięk”.
  Jeśli mowa jest kluczowa, dodaj jej treść jako tekst na slajdzie (najmocniejsze zdanie), bo część osób ogląda
  bez dźwięku.

## Jak to zapisać w carousel.json

Slajd z okienkiem to zwykły slajd z polem `image` (patrz `slides.md`), do którego dochodzi jedno pole:

```json
{"label": "Przed i po", "headline": "Tak wyglądało [[surowe nagranie]]",
 "image": {"src": "assets/frames/klatka-03.jpg", "video": "assets/klip.mp4", "start": 3.2, "end": 9.0, "sound": false,
           "label": "przed"}}
```

```json
{"label": "Źródło", "headline": "Tak pisze o tym [[producent]]",
 "image": {"src": "assets/strona-podglad.jpg", "page": "assets/strona.png", "seconds": 12, "focus": "50% 0%"}}
```

- `src` to obraz w okienku na PNG i podglądzie: klatka z nagrania (`carousel.py frames "<wideo>" --at 3.2 --out
  "<folder karuzeli>"`) albo podgląd strony, który robi `wideo.py strona`. Wyznacza kształt okienka.
- `video` to plik nagrania (ścieżka w folderze karuzeli albo pełna ścieżka), `start` i `end` w sekundach.
  `sound`: `true` tylko wtedy, gdy liczy się to, co słychać.
- `page` to długi zrzut strony z `wideo.py strona`, `seconds` to długość przewijania (domyślnie 12).
- Plakietki („przed”, „po”, „Źródło: …”) dawaj w `label` i `caption` okienka albo nad nim, nigdy na samym
  okienku, bo wideo je przykryje.
- Okienko działa z każdym układem zdjęcia: w ramce (domyślnie), na pół slajdu (`"fit": "half"`) i na cały slajd
  (`"fit": "bleed"`).

## Strona www jako dowód

```
PY "CS/scripts/wideo.py" strona "<adres strony>" "<folder karuzeli>/assets/strona.png" --zdanie "zdanie do podświetlenia"
```

Robi zrzut całej strony bez banerów cookies, z podanymi zdaniami w złotym markerze (można podać kilka
`--zdanie`), i podgląd `strona-podglad.jpg` do pola `src`. Linia `NIE ZNALEZIONO zdania` znaczy, że zdanie na
stronie brzmi inaczej: przepisz je dokładnie ze strony. Dobieraj stronę, która mówi dokładnie to, co slajd.
Podpis pod okienkiem: „Źródło: domena · tytuł strony”.

## Składanie

Po akceptacji copy i po `carousel.py render`:

```
PY "CS/scripts/wideo.py" zloz "<folder karuzeli>"            wszystkie slajdy z okienkiem
PY "CS/scripts/wideo.py" zloz "<folder karuzeli>" --only 3   tylko slajd 3
```

- Każdy slajd z okienkiem dostaje plik `slides/<nazwa>-NN.mp4`: 1080 px szerokości, 30 klatek na sekundę,
  od 3 do 60 sekund (krótszy fragment zapętla się do 3 sekund). Okienko ma zaokrąglone rogi z wyglądu.
- Folder `do-publikacji/` ma gotowy zestaw w kolejności slajdów: PNG albo MP4 dla każdego slajdu. To ten folder
  użytkowniczka wrzuca na Instagram.
- Po złożeniu obejrzyj klatki z kilku momentów każdego MP4 (`ffmpeg -ss <sekunda> -i <plik> -frames:v 1 <jpg>`),
  zanim powiesz, że gotowe: czy okienko trafia w ramkę, czy na nagraniu nie widać czegoś, co nie powinno wyjść
  (imię, prywatne dane, ktoś trzeci).
- Podgląd do przewijania w przeglądarce pokazuje PNG. Powiedz użytkowniczce, że slajdy z ruchem są jako MP4
  w `do-publikacji/`.
- Po każdej zmianie slajdu z okienkiem: `render --only N`, potem `zloz --only N`.
