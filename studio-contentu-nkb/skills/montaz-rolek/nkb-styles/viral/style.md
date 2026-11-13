# Viral (styl całościowy NKB)

Z katalogu stylów NKB. Wielkie słowo-puenta stoi za głową w chwili, gdy je mówisz; w napisach się wtedy nie powtarza.

- Type: napisy Inter Tight 800, 93 px, małe litery, ciasno (-0.05em), białe z miękkim cieniem.
  Słowo za głową: Playfair Display 900 kursywa, w kolorze akcentu.
- Colour: naturalny obraz, lekki kontrast (contrast 1.06, saturate 1.04). Akcent = kolor marki klientki
  (domyślnie złoto NKB #CD9F38).
- Captions: 2–3 słowa, jedna linia, przy dolnej krawędzi strefy bezpiecznej. Słowa wskakują z rozmycia na swoją klatkę.
  Słowa oznaczone (emph, cta, num, key) nie pojawiają się w napisach: one idą za głowę.
- Pace: jak w nagraniu, pauzy przycięte. Bez najazdów.
- Sound: sam głos.

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Słowo-puenta za głową: na każde oznaczone słowo, które jest puentą zdania (emph albo cta, najwyżej jedno na zdanie),
dodaj warstwę `"anchor": "behind"` od początku tego słowa do początku pierwszego słowa następnej frazy (zwykle 0,8–1 s):

```json
{"id": "puenta1", "anchor": "behind", "from": 2.9, "to": 3.76,
 "html": "<div class='vp1'>poradniku.</div>",
 "css": ".vp1{position:absolute;left:0;right:0;top:442px;text-align:center;font:italic 900 173px/1 'Playfair Display';color:#CD9F38;letter-spacing:-.01em;text-shadow:0 9px 47px rgba(0,0,0,.3)}",
 "motion": [{"target": "self", "tween": "fromTo", "from": {"scale": 1.22, "filter": "blur(22px)", "opacity": 0},
             "vars": {"scale": 1, "filter": "blur(0px)", "opacity": 1, "duration": 0.2, "ease": "power3.out"}}]}
```
- Wielkość: 173 px dla słowa do 10 znaków, dłuższe mniejsze (około 1600 / liczba znaków px), żeby zmieściło się
  w szerokości 90–910 px.
- Wysokość: dół liter 20–60 px poniżej czubka głowy (`layout.json` head top), tak żeby głowa zasłaniała najwyżej
  dolne 30–40% liter. Sprawdź na klatce z renderu.
- Kolor = akcent stylu. Słowo tak, jak zostało powiedziane, z interpunkcją.
- Potrzebne wycięcie postaci z tła (rvm_cut.py) przed budową.
