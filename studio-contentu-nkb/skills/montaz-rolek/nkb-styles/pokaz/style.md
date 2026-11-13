# Pokaz (styl całościowy NKB)

Z katalogu stylów NKB: Grafika u góry, Ty na dole.

- Layout: jasna, chłodna góra (#ECEDF0 z delikatnym cieniem liści), Ty w panelu z zaokrąglonymi górnymi rogami (krawędź y 1095, promień 85 px), obraz przesunięty o 365 px w dół, głowa z wycięcia wychodzi ponad krawędź.
- Type: czarny Poppins 800, 69 px, fraza buduje się słowo po słowie (z szarego do czarnego), słowa kluczowe w akcencie.
- Captions: y 730–800, między grafiką a głową. "avoid_face": false, bo twarz jest przesunięta przez styl.
- Needs: wycięcie postaci (rvm_cut.py); warstwa "wyciecie" włącza je w każdej rolce.
- Pace: szybkie, nowa grafika mniej więcej co pół sekundy.
- Sound: sam głos.
- Akcent = kolor marki klientki (domyślnie złoto NKB #CD9F38); w css i warstwach var(--acc).

## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)
Karty interfejsu w pasie y 230–690 (65–1015 px w poziomie), zmieniane na każde NAZWANE słowo tej rolki
(narzędzie, rzecz, liczba): jedna warstwa na scenę, od słowa do następnej sceny, wejście z rozmycia. Każda karta to
prawdziwa rzecz z jej słów albo ogólny zamiennik: nigdy cudze logo ani wymyślone dane.
```json
{"id": "scena1", "anchor": "full", "from": 0.15, "to": 2.45,
 "html": "<div class='pk-ui'><div class='pk-grid'><div class='pk-card'><span class='k'>Zasada 1</span><span class='t'>Kontekst</span></div><div class='pk-card'><span class='k'>Zasada 2</span><span class='t'>Rola</span></div></div></div>",
 "css": ".pk-ui{position:absolute;left:65px;right:65px;top:230px;height:460px;display:flex;align-items:center;justify-content:center}.pk-grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;width:100%}.pk-card{background:#fff;border-radius:26px;box-shadow:0 15px 43px -17px rgba(20,24,30,.28),0 0 0 1px rgba(20,24,30,.05);padding:28px 32px;display:grid;gap:11px;font-family:Poppins;color:#141414}.pk-card .k{font:500 27px/1 Poppins;letter-spacing:.14em;text-transform:uppercase;color:#8a8f98}.pk-card .t{font:700 45px/1.1 Poppins}",
 "motion": [{"target": ".pk-card", "tween": "fromTo", "from": {"opacity": 0, "filter": "blur(8px)", "y": 30}, "vars": {"opacity": 1, "filter": "blur(0px)", "y": 0, "duration": 0.15, "ease": "power2.out", "stagger": 0.13}}]}
```
Inne sceny tego samego typu: okładka poradnika (ciemna karta 3:4 z tytułem kursywą i naklejką w akcencie), pole
komentarza ze słowem wpisywanym znak po znaku (litery jako `<span class='ch'>`, motion `.ch` opacity 0→1 ze stagger
0.05 od chwili słowa), wiadomość z załącznikiem. Wzór: katalog stylów (karta Pokaz).

## Standing notes
- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.
