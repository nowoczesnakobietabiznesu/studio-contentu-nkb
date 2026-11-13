#!/usr/bin/env python3
"""Writes the NKB overall styles (catalog: "Wybieram gotowy styl") as presets: nkb-styles/<key>/style.json + style.md.
An overall style = a caption spec + the grade + always-on css / layers / reel motion, plus "Graphic elements" in
style.md: what Claude writes into each reel's plan.json from that reel's own words (titles, cards, words behind the
head). Values are on the 1080x1920 frame. Viral has its own files (made in the pilot)."""
import copy
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ACC = '#CD9F38'


def caption(key, **over):
    spec = copy.deepcopy(json.load(open(os.path.join(HERE, key, 'style.json'), encoding='utf-8'))['caption'])
    spec.update(over)
    return spec


BLUR_IN = [{'target': 'self', 'tween': 'fromTo', 'from': {'opacity': 0, 'filter': 'blur(14px)', 'y': 18},
            'vars': {'opacity': 1, 'filter': 'blur(0px)', 'y': 0, 'duration': 0.22, 'ease': 'power2.out'}}]

STYLES = {
 'salon': {
  'name': 'Salon', 'tag': 'Domowy styl NKB',
  'caption': caption('gabinet'), 'grade': 'sepia(.16) saturate(1.06) contrast(1.02)',
  'pace': 'spokojne, pauzy skrócone do 0,3 s', 'sound': 'miękkie kliknięcia, dzwonek na wezwaniu do działania',
  'md': ['Type: napisy Gabinet (rozstrzelone kapitaliki Poppins, słowa kluczowe kursywą Playfair w akcencie).',
         'Colour: ciepła korekta (sepia .16, saturate 1.06, contrast 1.02).',
         'Captions: przy dolnej krawędzi strefy bezpiecznej.'],
  'graphics': '''Przypięty tytuł u góry przez całą rolkę (warstwa bez from/to), z hooka TEJ rolki: krótki nadtytuł
(temat, 2–3 słowa) i tytuł (obietnica, do 28 znaków), oba z jej słów:
```json
{"id": "tytul", "anchor": "full", "in": "fade",
 "html": "<div class='sl-t'><span class='e'>AI w biznesie</span><span class='h'>Jak odzyskać wieczory</span></div>",
 "css": ".sl-t{position:absolute;left:86px;right:86px;top:236px;text-align:center;display:grid;gap:12px}.sl-t .e{font:500 39px/1 Poppins;letter-spacing:.28em;text-transform:uppercase;color:var(--acc)}.sl-t .h{font:italic 500 76px/1.1 'Playfair Display';color:#fff;text-shadow:0 9px 47px rgba(0,0,0,.35)}"}
```
Tytuł nie może zejść na czubek głowy: dół tytułu co najmniej 40 px nad `head.top` z `layout.json`.'''},

 'redakcja': {
  'name': 'Redakcja', 'tag': 'Rolka jak okładka magazynu',
  'caption': caption('cytat'), 'grade': 'sepia(.16) saturate(1.06) contrast(1.02)',
  'layers': [{'id': 'ramka', 'anchor': 'full', 'html': "<div class='rd-frame'></div>",
              'css': '.rd-frame{position:absolute;inset:0;box-shadow:inset 0 0 0 32px #F8F3EA}'}],
  'pace': 'spokojne', 'sound': 'szelest papieru przy zmianie sekcji',
  'md': ['Type: napisy Cytat (Cormorant Garamond kursywa w polskim cudzysłowie, złota linia).',
         'Colour: ciepła korekta, kremowa ramka 32 px dookoła kadru (warstwa stała).',
         'Captions: przy dolnej krawędzi strefy bezpiecznej.'],
  'graphics': '''Winieta jak na okładce: nazwa marki klientki (zapytaj raz i zapisz w „Standing notes”) i podpis z TĄ
rolką (miesiąc i rok albo temat), przez całą rolkę:
```json
{"id": "winieta", "anchor": "full", "in": "fade",
 "html": "<div class='rd-m'><span class='m'>Twoja marka</span><span class='i'>listopad 2026</span></div>",
 "css": ".rd-m{position:absolute;left:0;right:0;top:236px;text-align:center;display:grid;gap:13px}.rd-m .m{font:900 91px/1 'Bodoni Moda';letter-spacing:.04em;text-transform:uppercase;color:#fff;text-shadow:0 9px 56px rgba(0,0,0,.3)}.rd-m .i{font:500 35px/1 Poppins;letter-spacing:.24em;text-transform:uppercase;color:#fff;opacity:.85}"}
```
Nigdy wymyślony numer wydania. Długa nazwa marki: mniejszy krój, tak żeby zmieściła się w 980 px.'''},

 'lekcja': {
  'name': 'Lekcja', 'tag': 'Krok po kroku',
  'caption': caption('marker'), 'grade': 'brightness(1.07) saturate(1.08)',
  'pace': 'średnie, każdy krok to osobna część', 'sound': 'odhaczenie przy każdym kroku',
  'md': ['Type: napisy Marker (kremowa karteczka, zakreślacz w akcencie na słowach kluczowych).',
         'Colour: jasny, czysty obraz (brightness 1.07, saturate 1.08).',
         'Captions: przy dolnej krawędzi strefy bezpiecznej.'],
  'graphics': '''Etykieta kroku i pasek postępu w lewym górnym rogu, z kroków, które klientka SAMA wymienia
(„po pierwsze”, „krok drugi”), od słowa, które otwiera krok, do początku następnego. Bez kroków w nagraniu: bez etykiety.
```json
{"id": "krok1", "anchor": "full", "from": 0.4, "to": 6.0, "in": "pop",
 "html": "<div class='lk'><span class='c'>Krok 1 z 3</span><span class='p'><i class='on'></i><i></i><i></i></span></div>",
 "css": ".lk{position:absolute;left:65px;top:240px;display:flex;align-items:center;gap:27px}.lk .c{font:600 43px/1 Poppins;background:var(--acc);color:#141414;border-radius:999px;padding:17px 35px}.lk .p{display:flex;gap:13px}.lk .p i{width:76px;height:13px;border-radius:11px;background:rgba(255,255,255,.45)}.lk .p i.on{background:#fff}"}
```'''},

 'tempo': {
  'name': 'Tempo', 'tag': 'Szybko i do rzeczy',
  'caption': caption('jedno-slowo'), 'grade': 'contrast(1.16) saturate(1.18)',
  'motion': [{'on': 'cuts', 'target': '#root', 'tween': 'fromTo', 'from': {'filter': 'brightness(1.7)'},
              'vars': {'filter': 'brightness(1)', 'duration': 0.18}},
             {'on': 'marks', 'target': 'footage', 'tween': 'to',
              'vars': {'scale': 1.07, 'duration': 0.1, 'yoyo': True, 'repeat': 1, 'transformOrigin': '50% 35%'}}],
  'pace': 'szybkie: pauzy do 0,1 s, zbliżenie (zoom 1.2–1.3) co drugie cięcie w edl.json', 'sound': 'szum przejścia przy cięciach',
  'md': ['Type: napisy Jedno słowo (Anton, wersaliki, jedno słowo naraz).',
         'Colour: mocny kontrast i nasycenie.',
         'Motion: błysk na każdym cięciu, krótkie wejście kamery na każdym oznaczonym słowie (motion "on").'],
  'graphics': 'Brak stałych grafik. Tempo robią cięcia: zbliżenie co drugie cięcie (edl.json, zoom 1.2–1.3 na twarz).'},

 'pokaz': {
  'name': 'Pokaz', 'tag': 'Grafika u góry, Ty na dole',
  'caption': {'font': 'Poppins', 'weight': 800, 'size': 69, 'line_height': 1.1, 'tracking': -0.02, 'color': '#121212',
              'accent': ACC, 'shadow': False, 'mark': 'accent', 'lit': 'none', 'words': 2, 'chars': 16, 'lines': 1,
              'position': 730, 'margin': 76, 'align': 'center', 'entrance': 'none', 'avoid_face': False,
              'css': '.cu .w{opacity:0}',
              'word_motion': {'tween': 'fromTo', 'from': {'opacity': 0},
                              'vars': {'opacity': 1, 'duration': 0.1}}},
  'css': ('#root{background:radial-gradient(38% 7% at 84% 5%,rgba(52,64,54,.07),transparent 72%),'
          'radial-gradient(30% 5% at 70% 12%,rgba(52,64,54,.05),transparent 72%),#ECEDF0}'
          '#plate{position:absolute;inset:0;transform:translateY(365px);clip-path:inset(730px 0 0 0 round 85px 85px 0 0)}'
          '#cutw{transform:translateY(365px)}'),
  'layers': [{'id': 'wyciecie', 'anchor': 'behind', 'html': ''}],
  'pace': 'szybkie, nowa grafika mniej więcej co pół sekundy', 'sound': 'sam głos',
  'md': ['Layout: jasna, chłodna góra (#ECEDF0 z delikatnym cieniem liści), Ty w panelu z zaokrąglonymi górnymi rogami '
         '(krawędź y 1095, promień 85 px), obraz przesunięty o 365 px w dół, głowa z wycięcia wychodzi ponad krawędź.',
         'Type: czarny Poppins 800, 69 px, fraza buduje się słowo po słowie (z szarego do czarnego), słowa kluczowe w akcencie.',
         'Captions: y 730–800, między grafiką a głową. "avoid_face": false, bo twarz jest przesunięta przez styl.',
         'Needs: wycięcie postaci (rvm_cut.py); warstwa "wyciecie" włącza je w każdej rolce.'],
  'graphics': '''Karty interfejsu w pasie y 230–690 (65–1015 px w poziomie), zmieniane na każde NAZWANE słowo tej rolki
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
0.05 od chwili słowa), wiadomość z załącznikiem. Wzór: katalog stylów (karta Pokaz).'''},

 'kulisy': {
  'name': 'Kulisy', 'tag': 'Bez pokazywania twarzy',
  'caption': caption('maszynopis'), 'grade': 'sepia(.16) saturate(1.06) contrast(1.02)',
  'pace': 'średnie, przebitka co 2–3 s', 'sound': 'ciche stukanie klawiatury, szum tła',
  'md': ['Obraz: przebitki od klientki (biurko, kawa, ekran, ręce) zamiast twarzy; jej głos z nagrania leci dalej.',
         'Type: napisy Maszynopis (JetBrains Mono na zielonym pasku, pisanie litera po literze).',
         'Colour: ciepła korekta na przebitkach.'],
  'graphics': '''Przebitki: klientka podsyła krótkie nagrania (pionowe 9:16). Przytnij je ffmpegiem do 2–3 s, zapisz w
`<project>/assets/broll/` (1080x1920) i połóż jako pełnoekranowe warstwy jedna po drugiej, tak żeby pokryły całą rolkę:
```json
{"id": "przebitka1", "anchor": "full", "from": 0.0, "to": 2.0,
 "media": {"src": "assets/broll/biurko.mp4", "x": 0, "y": 0, "w": 1080}, "css": "#ly0 video{filter:sepia(.16) saturate(1.06) contrast(1.02)}"}
```
Kolejność: od szerokiego ujęcia do zbliżeń, bez dwóch podobnych obok siebie. Bez przebitek nie da się zrobić tego
stylu: poproś o 3–6 krótkich nagrań.'''},

 'notatnik': {
  'name': 'Notatnik', 'tag': 'Jasno, z kursywą i dopiskami',
  'caption': {'font': 'Instrument Serif', 'weight': 400, 'italic': True, 'size': 120, 'line_height': 1.0,
              'color': '#FFF8EF', 'accent': ACC, 'shadow': '0 6px 26px rgba(0,0,0,.3)', 'mark': 'none',
              'lit': 'none', 'words': 3, 'chars': 18, 'lines': 2, 'position': 1470, 'margin': 108, 'align': 'center',
              'entrance': 'none',
              'css': ".cu .ln:first-child:not(:only-child){font:500 56px/1.3 Inter;font-style:normal;text-transform:lowercase;"
                     "text-shadow:0 6px 22px rgba(0,0,0,.4)} .cu .ln:last-child .w{color:var(--acc)} .cu .w{opacity:0}",
              'word_motion': {'tween': 'fromTo', 'from': {'opacity': 0, 'y': 14},
                              'vars': {'opacity': 1, 'y': 0, 'duration': 0.3, 'ease': 'power2.out'}}},
  'grade': 'brightness(1.07) saturate(1.08)',
  'pace': 'spokojne, naturalne pauzy zostają', 'sound': 'sam głos',
  'md': ['Type: drobne małe litery Inter 500 (kremowe) i pod nimi linia kursywą Instrument Serif w akcencie.',
         'Colour: jasny, czysty i neutralny (brightness 1.07, saturate 1.08), bez sepii i winiety.',
         'Captions: dwie linie przy dolnej krawędzi strefy bezpiecznej.'],
  'graphics': '''Iskierki ✦ w akcencie obok kursywy na słowach kluczowych i odręczny dopisek Caveat ze strzałką, który
klientka MÓWI albo który komentuje jej słowa („za darmo!” przy „darmowym”), najwyżej jeden na 8–10 s:
```json
{"id": "iskry1", "anchor": "full", "from": 2.9, "to": 3.76,
 "html": "<span class='spk a'>✦</span><span class='spk b'>✦</span>",
 "css": ".spk{position:absolute;color:var(--acc);font:400 65px/1 Poppins;text-shadow:0 0 22px rgba(255,255,255,.5)}.spk.a{left:130px;top:1150px}.spk.b{right:130px;top:1270px}",
 "motion": [{"target": ".spk", "tween": "fromTo", "from": {"scale": 0.7, "opacity": 0.25}, "vars": {"scale": 1.1, "opacity": 1, "duration": 0.55, "yoyo": true, "repeat": 3, "stagger": 0.2}}]}
```'''},

 'elegancki': {
  'name': 'Elegancki', 'tag': 'Studio wywiadu',
  'caption': {'font': 'DM Serif Display', 'weight': 400, 'size': 112, 'line_height': 1.0, 'case': 'lower',
              'color': '#F7F4EE', 'accent': ACC, 'shadow': '0 6px 26px rgba(0,0,0,.45)', 'mark': 'none',
              'lit': 'none', 'words': 2, 'chars': 14, 'lines': 2, 'position': 1470, 'margin': 108, 'align': 'center',
              'entrance': 'none',
              'css': ".cu .ln:first-child:not(:only-child){font:500 35px/1.8 Montserrat;letter-spacing:.32em;"
                     "text-transform:uppercase;text-shadow:0 4px 17px rgba(0,0,0,.5)} .cu .w.m{font-style:italic} .cu .w{opacity:0}",
              'word_motion': {'tween': 'fromTo', 'from': {'opacity': 0, 'yPercent': 55, 'filter': 'blur(8px)'},
                              'vars': {'opacity': 1, 'yPercent': 0, 'filter': 'blur(0px)', 'duration': 0.5,
                                       'ease': 'expo.out'}}},
  'grade': 'contrast(1.06) saturate(1.04)',
  'motion': [{'on': 'start', 'target': 'footage', 'tween': 'to',
              'vars': {'scale': 1.05, 'duration': 30, 'ease': 'none', 'transformOrigin': '50% 35%'}}],
  'pace': 'wolne, powolny najazd zamiast cięć z uderzeniem', 'sound': 'sam głos',
  'md': ['Type: drobne rozstrzelone kapitaliki Montserrat 500 i pod nimi duże małe litery DM Serif Display.',
         'Colour: naturalny, lekki kontrast (jak Viral).',
         'Motion: słowa wysuwają się z rozmycia; powolny najazd kamery przez całą rolkę.'],
  'graphics': '''Jeden przelot światła na otwarcie (0–1,1 s):
```json
{"id": "swiatlo", "anchor": "full", "from": 0.0, "to": 1.1, "html": "<div class='el-sw'></div>",
 "css": ".el-sw{position:absolute;top:-200px;bottom:-200px;left:0;width:430px;background:linear-gradient(90deg,transparent,rgba(255,240,215,.35),transparent);mix-blend-mode:screen}",
 "motion": [{"target": ".el-sw", "tween": "fromTo", "from": {"x": -520, "skewX": -18}, "vars": {"x": 1300, "skewX": -18, "duration": 1.1, "ease": "power2.out"}}]}
```'''},

 'yapping': {
  'name': 'Yapping', 'tag': 'Krem, mięta i mieszane kroje',
  'caption': {'font': 'Instrument Serif', 'weight': 400, 'size': 56, 'line_height': 1.0, 'color': '#F4F1EA',
              'accent': '#D8FBE7', 'shadow': '0 3px 15px rgba(0,0,0,.4)', 'mark': 'none', 'lit': 'none',
              'words': 1, 'chars': 30, 'lines': 1, 'position': 845, 'margin': 80, 'align': 'left',
              'entrance': 'none', 'avoid_face': False},
  'grade': 'contrast(.97) brightness(1.02)',
  'pace': 'cięcia zdanie po zdaniu (1–2,3 s), przy każdym cięciu inna wielkość kadru: 1.0 / 1.3 / 1.7 przy planie '
          'średnim, 1.0 / 1.12 / 1.25 przy bliskim ujęciu (głowa nigdy nie wychodzi poza kadr, sprawdź check.jpg)',
  'sound': 'sam głos, 3–4 ciche dzwonki na nagrodę, ciche stukanie pod pisanym tekstem',
  'md': ['Type: bieżące słowo Instrument Serif 56 px z lewej (x 80, y 845), zawsze na wierzchu.',
         'Colour: naturalny, krem #FCF5BC i mięta #D8FBE7 na zmianę w kompozycjach.',
         'Kompozycje (warstwy na rolkę): tytuł szeryfem za głową, grube kapitaliki Rubik Mono One pisane litera po '
         'literze, białe karty, pędzel Caveat Brush, odręczne dopiski Patrick Hand.',
         'Kolory stałe (krem i mięta): kolor marki ich nie zmienia.',
         'Needs: wycięcie postaci (rvm_cut.py) tylko wtedy, gdy któraś kompozycja idzie za głowę.'],
  'graphics': '''Jedna kompozycja naraz, z jej słów. Tytuł z hooka za głową od 0 s, tylko gdy nad głową jest miejsce
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
i poniżej brody (top 1170 do 1250px przy bliskim ujęciu).'''},
}

for key, st in STYLES.items():
    d = os.path.join(HERE, key)
    os.makedirs(d, exist_ok=True)
    out = {'name': st['name'], 'slug': key, 'nkb': {'kind': 'overall', 'catalog': 'styl-' + key, 'tag': st['tag']},
           'caption': st['caption']}
    for k in ('grade', 'css', 'layers', 'motion'):
        if st.get(k):
            out[k] = st[k]
    out['pace'], out['sound'] = st['pace'], st['sound']
    if any(l.get('anchor') == 'behind' for l in st.get('layers') or []):
        out['nkb']['needs'] = ['clean cutout (rvm_cut.py)']
    with open(os.path.join(d, 'style.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    md = (f"# {st['name']} (styl całościowy NKB)\n\nZ katalogu stylów NKB: {st['tag']}.\n\n"
          + ''.join(f'- {line}\n' for line in st['md'])
          + f"- Pace: {st['pace']}.\n- Sound: {st['sound']}.\n"
          + ('' if key == 'yapping' else
             f"- Akcent = kolor marki klientki (domyślnie złoto NKB {ACC}); w css i warstwach var(--acc).\n")
          + "\n## Graphic elements (piszesz je w plan.json każdej rolki, z jej słów)\n"
          + st['graphics'] + '\n\n## Standing notes\n- Tekst na ekranie: tylko słowa klientki albo ogólny zamiennik.\n')
    with open(os.path.join(d, 'style.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(md)
print(len(STYLES), 'stylów całościowych zapisanych')
