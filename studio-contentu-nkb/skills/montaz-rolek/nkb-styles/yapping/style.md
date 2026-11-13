# Yapping (styl całościowy NKB)

Z katalogu stylów NKB: Krem, mięta i mieszane kroje.

- Type: bieżące słowo Instrument Serif 56 px z lewej (x 80, y 845), zawsze na wierzchu.
- Colour: naturalny, krem #FCF5BC i mięta #D8FBE7 na zmianę w kompozycjach.
- Kompozycje (warstwy na rolkę): tytuł szeryfem za głową, grube kapitaliki Rubik Mono One pisane litera po literze, białe karty, pędzel Caveat Brush, odręczne dopiski Patrick Hand.
- Kolory stałe (krem i mięta): kolor marki ich nie zmienia.
- Needs: wycięcie postaci (rvm_cut.py) tylko wtedy, gdy któraś kompozycja idzie za głowę.
- Pace: cięcia zdanie po zdaniu (1–2,3 s), przy każdym cięciu inna wielkość kadru: 1.0 / 1.3 / 1.7 przy planie średnim, 1.0 / 1.12 / 1.25 przy bliskim ujęciu (głowa nigdy nie wychodzi poza kadr, sprawdź check.jpg).
- Sound: sam głos, 3–4 ciche dzwonki na nagrodę, ciche stukanie pod pisanym tekstem.

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Jedna kompozycja naraz, z jej słów. Tytuł z hooka za głową od 0 s, tylko gdy nad głową jest miejsce
(plan średni: w layout.json głowa zaczyna się niżej niż y 400). Przy bliskim ujęciu głowa zasłoni tytuł: daj go
wtedy na pierś ("anchor": "full", top około 1190px, 128px) i nie licz wycięcia postaci:
```json
{"id": "tytul", "anchor": "behind", "from": 0, "to": 2.45, "html": "<div class='yp-t'>Resztę zasad</div>",
 "css": ".yp-t{position:absolute;left:0;right:0;top:326px;text-align:center;font:400 162px/1 'Instrument Serif';color:#FCF5BC;text-shadow:0 4px 22px rgba(0,0,0,.25)}"}
```
Grube kapitaliki na piersi (krem / mięta na zmianę), litery pisane jedna po drugiej (1 znak na klatkę) od słowa:
```json
{"id": "kaps1", "anchor": "full", "from": 2.4, "to": 3.76,
 "html": "<div class='yp-c'><span>W <b class='t1'><i class='ch'>D</i><i class='ch'>A</i>...</b></span><span class='mint'>...</span></div>",
 "css": ".yp-c{position:absolute;left:54px;right:54px;top:1170px;text-align:center;display:grid;gap:11px}.yp-c span{font:400 82px/1.05 'Rubik Mono One';color:#FCF5BC}.yp-c .mint{color:#D8FBE7}.yp-c i{font-style:normal}",
 "motion": [{"target": ".t1 .ch", "tween": "fromTo", "at": 0.1, "from": {"opacity": 0}, "vars": {"opacity": 1, "duration": 0.01, "stagger": 0.033}}]}
```
Białe karty (szary podpis + pogrubiony tekst, obrót -2°), pędzel i dopiski: wzór w katalogu (SK/picker/nkb.html,
karta Yapping). Kapitaliki Rubik Mono One bez przecinków (krój o stałej szerokości robi z przecinka przerwę: "TO ,")
i poniżej brody (top 1170 do 1250px przy bliskim ujęciu).

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
