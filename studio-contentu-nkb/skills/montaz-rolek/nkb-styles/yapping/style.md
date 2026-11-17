# Yapping (styl całościowy NKB)

Z katalogu stylów NKB: Krem, mięta i mieszane kroje.

- Napisy: zawsze JEDNO bieżące słowo, Instrument Serif 56 px, kremowe #F4F1EA, z lewej (x 80, y 845), bez podświetleń. Nigdy całe zdania na środku kadru i nigdy pochylone słowa w innym kolorze.
- Kolory stałe: krem #FCF5BC, mięta #D8FBE7, biel #F4F1EA. Kolor marki klientki NIE pojawia się nigdzie (ani w napisach, ani w kompozycjach, ani na storyboardzie).
- Kompozycje: tylko pięć z katalogu, jedna naraz, 1 do 4 słów z jej zdania: tytuł szeryfem za głową (yp-t), grube kapitaliki Rubik Mono One pisane litera po literze (yp-c), biała karta (yp-card), pędzel Caveat Brush (yp-brush), odręczny dopisek Patrick Hand (yp-note). Ich wygląd jest już w stylu (css): piszesz tylko html.
- Needs: wycięcie postaci (rvm_cut.py) tylko wtedy, gdy tytuł idzie za głowę.
- Pace: cięcia zdanie po zdaniu (1–2,3 s), przy każdym cięciu inna wielkość kadru: 1.0 / 1.3 / 1.7 przy planie średnim, 1.0 / 1.12 / 1.25 przy bliskim ujęciu (głowa nigdy nie wychodzi poza kadr, sprawdź check.jpg).
- Sound: sam głos, 3–4 ciche dzwonki na nagrodę, ciche stukanie pod pisanym tekstem.

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Wygląd pięciu kompozycji jest gotowy w stylu (klasy yp-t, yp-c, yp-card, yp-brush, yp-note). W plan.json
każdej rolki piszesz tylko warstwy z html i czasem, z jej słów. NIE dopisuj własnego css do tych klas, NIE zmieniaj
krojów, kolorów ani miejsc, NIE wymyślaj innych kompozycji. Jedna kompozycja naraz, a między nimi samo bieżące słowo.
Rytm jak w katalogu: tytuł na hook, potem kapitaliki, karta, pędzel z dopiskiem na końcu. W dłuższej rolce
kapitaliki i karty wracają na kolejne ważne zdania (co 2 do 4 zdań), a reszta rolki to samo bieżące słowo.

1. Tytuł z hooka (2 do 4 słów) za głową od 0 s, tylko gdy nad głową jest miejsce (plan średni: w layout.json głowa
   zaczyna się niżej niż y 400). Przy bliskim ujęciu daj go na pierś: klasa "yp-t piers", "anchor": "full", bez
   wycięcia postaci.
```json
{"id": "tytul", "anchor": "behind", "from": 0, "to": 2.45, "html": "<div class='yp-t'>Resztę zasad</div>"}
```
2. Kapitaliki na piersi: 1 do 2 linijek po 1 do 2 słowa, krem i mięta na zmianę, litery pisane jedna po drugiej
   od chwili, gdy pada słowo (bez przecinków: krój o stałej szerokości robi z przecinka przerwę "TO ,").
```json
{"id": "kaps1", "anchor": "full", "from": 2.4, "to": 3.76,
 "html": "<div class='yp-c'><span>W <b class='t1'><i class='ch'>D</i><i class='ch'>A</i><i class='ch'>R</i></b></span><span class='mint'><b class='t2'><i class='ch'>P</i><i class='ch'>O</i></b></span></div>",
 "motion": [{"target": ".t1 .ch", "tween": "fromTo", "at": 0.1, "from": {"opacity": 0}, "vars": {"opacity": 1, "duration": 0.01, "stagger": 0.033}},
            {"target": ".t2 .ch", "tween": "fromTo", "at": 0.54, "from": {"opacity": 0}, "vars": {"opacity": 1, "duration": 0.01, "stagger": 0.033}}]}
```
3. Biała karta (szary podpis + pogrubione słowo pisane litera po literze), na wezwanie do działania albo nazwę:
```json
{"id": "karta", "anchor": "full", "from": 3.78, "to": 5.14,
 "html": "<div class='yp-card'><small>Skomentuj:</small><b class='t1'><i class='ch'>p</i><i class='ch'>r</i></b></div>",
 "motion": [{"target": ".t1 .ch", "tween": "fromTo", "at": 0.6, "from": {"opacity": 0}, "vars": {"opacity": 1, "duration": 0.01, "stagger": 0.033}}]}
```
4. Pędzel na puentę (2 do 3 słów), mięta, do końca rolki, a pod nim 5. odręczny dopisek pół sekundy później:
```json
{"id": "pedzel", "anchor": "full", "from": 5.18, "to": 99, "html": "<div class='yp-brush'>wyślę Ci go.</div>"}
{"id": "dopisek", "anchor": "full", "from": 5.7, "to": 99, "html": "<div class='yp-note'>👉 sprawdź wiadomości</div>"}
```
Linijka kapitalików ma najwyżej 10 znaków (inaczej wchodzi pod przyciski Instagrama); dłuższe słowo daj na kartę.

Storyboard i podgląd: klatki z silnika (build_reel.py --safe, potem hf.py snapshot), nigdy rysowane ręcznie. Zanim
je pokażesz, porównaj z kartą Yapping w katalogu (picker/nkb.html): jedno słowo z lewej, krem i mięta, mieszane
kroje. Coś wygląda inaczej? Popraw plan.json, zanim pokażesz.

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
