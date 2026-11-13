#!/usr/bin/env python3
"""Writes the NKB caption styles (catalog: "Stwórz swój styl") as presets: nkb-styles/<key>/style.json + style.md.
Run it after changing a spec here; the files it writes are what the skill ships. Values are on the 1080x1920 frame.
All of them sit at the bottom of the Reels safe zone (position 1470), as far from the face as the safe zone allows.
The accent is the NKB gold by default; a buyer's brand colour replaces "accent" (css uses var(--acc))."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ACC = '#CD9F38'
SHOW_SAID = {'tween': 'fromTo', 'from': {'opacity': 0}, 'vars': {'opacity': 1, 'duration': 0.15, 'ease': 'power1.out'}}
BASE = {'accent': ACC, 'position': 1470, 'margin': 108, 'align': 'center', 'lines': 1, 'mark': 'none', 'lit': 'none',
        'entrance': 'none'}

STYLES = {
 # ---- Spokojne
 'kinowe': ('Kinowe', 'spokojne', 'Klasyczne napisy jak w filmie. Całe zdanie naraz, bez podświetleń.', {
    'font': 'Poppins', 'weight': 400, 'size': 58, 'line_height': 1.4, 'color': '#FFFFFF',
    'shadow': '0 5px 14px rgba(0,0,0,.75)', 'words': 5, 'chars': 27}),
 'szept': ('Szept', 'spokojne', 'Kursywa Playfair, słowa wyłaniają się miękko jedno po drugim.', {
    'font': 'Playfair Display', 'weight': 500, 'italic': True, 'size': 93, 'line_height': 1.15, 'color': '#FFFFFF',
    'shadow': '0 9px 47px rgba(0,0,0,.4)', 'words': 3, 'chars': 16, 'css': '.cu .w{opacity:0}',
    'word_motion': {'tween': 'fromTo', 'from': {'opacity': 0, 'y': 22},
                    'vars': {'opacity': 1, 'y': 0, 'duration': 0.45, 'ease': 'power2.out'}}}),
 'cytat': ('Cytat', 'spokojne', 'Zdanie jak cytat w magazynie: polski cudzysłów i złota linia.', {
    'font': 'Cormorant Garamond', 'weight': 600, 'italic': True, 'size': 92, 'line_height': 1.08, 'color': '#F8F3EA',
    'shadow': '0 9px 56px rgba(0,0,0,.45)', 'words': 4, 'chars': 20, 'entrance': 'fade', 'dy': -36,
    'motion': [{'target': 'self', 'tween': 'from', 'vars': {'y': 28, 'duration': 0.7, 'ease': 'power2.out'}}],
    'css': ".cu::before{content:'';display:block;width:16%;height:3px;background:var(--acc);margin:0 auto 30px}"
           " .cu .ln:first-child::before{content:'\\201E'} .cu .ln:last-child::after{content:'\\201D'}"}),
 'szklo': ('Szkło', 'spokojne', 'Napis na matowej, przejrzystej kapsule. Czytelny na jasnym i ruchliwym tle.', {
    'font': 'Poppins', 'weight': 500, 'size': 69, 'line_height': 1.25, 'color': 'rgba(255,255,255,.78)',
    'accent': '#FFFFFF', 'lit': 'color', 'shadow': '0 2px 10px rgba(0,0,0,.2)', 'words': 4, 'chars': 20,
    'plate': {'color': 'rgba(255,255,255,.17)', 'radius': 999, 'pad': [19, 48], 'blur': 9},
    'css': '.cu .pl{border:4px solid rgba(255,255,255,.38)}'}),
 'kadr': ('Kadr', 'spokojne', 'Drobne, rozstrzelone kapitaliki z cienką złotą linią, jak w dokumencie.', {
    'font': 'Poppins', 'weight': 500, 'size': 44, 'tracking': 0.32, 'case': 'upper', 'line_height': 1.6,
    'color': '#FFFFFF', 'shadow': '0 5px 19px rgba(0,0,0,.6)', 'words': 4, 'chars': 26, 'entrance': 'fade',
    'dy': -32, 'motion': [{'target': 'self', 'tween': 'from', 'vars': {'y': 20, 'duration': 0.6, 'ease': 'power2.out'}}],
    'css': ".cu::before{content:'';display:block;width:9%;height:3px;background:var(--acc);margin:0 auto 28px}"}),
 # ---- Wyraziste (Złota nić: osobny plik, z pilota)
 'pieczatka': ('Pieczątka', 'wyraziste', 'Wersaliki, a kluczowe słowa dostają przechylony stempel w kolorze akcentu.', {
    'font': 'Poppins', 'weight': 800, 'size': 86, 'case': 'upper', 'line_height': 1.12, 'color': '#FFFFFF',
    'shadow': '0 9px 38px rgba(0,0,0,.45)', 'lit': 'pop', 'mark': 'highlight', 'lit_text': '#141414',
    'words': 3, 'chars': 16, 'css': '.cu .w.m{transform:rotate(-2.5deg)}'}),
 'obrys': ('Obrys', 'wyraziste', 'Słowa czekają jako sam kontur i wypełniają się, gdy je wypowiadasz.', {
    'font': 'Poppins', 'weight': 900, 'size': 88, 'case': 'upper', 'line_height': 1.05, 'color': '#FFFFFF',
    'stroke': {'color': '#FFFFFF', 'width': 6}, 'shadow': False, 'lit': 'color', 'words': 3, 'chars': 14,
    'css': '.cu .w{color:transparent}'}),
 'marker': ('Marker', 'wyraziste', 'Kremowa karteczka, a słowa kluczowe przejeżdża zakreślacz w kolorze akcentu.', {
    'font': 'Poppins', 'weight': 600, 'size': 73, 'line_height': 1.25, 'color': '#141414', 'shadow': False,
    'words': 4, 'chars': 20, 'plate': {'color': '#F8F3EA', 'radius': 14, 'pad': [17, 37]},
    'css': '.cu .pl{box-shadow:0 28px 85px -38px rgba(0,0,0,.5)}'
           ' .cu .w.m{background:linear-gradient(transparent 52%,color-mix(in srgb,var(--acc) 72%,transparent) 52%)'
           ' no-repeat 0 0/0% 100%}',
    'mark_motion': {'tween': 'to', 'vars': {'backgroundSize': '100% 100%', 'duration': 0.35, 'ease': 'power2.out'}}}),
 'etykieta': ('Etykieta', 'wyraziste', 'Każda fraza to osobna etykieta, a ta ze słowem kluczowym ma kolor akcentu.', {
    'font': 'Poppins', 'weight': 600, 'size': 64, 'line_height': 1.2, 'color': '#1E3E3A', 'shadow': False,
    'align': 'left', 'margin': 86, 'words': 3, 'chars': 18, 'entrance': 'fade',
    'plate': {'color': '#FFFFFF', 'radius': 22, 'pad': [14, 30]},
    'stack': {'keep': 2, 'gap': 22, 'dim': [0.72], 'scale': [1]},
    'motion': [{'target': 'self', 'tween': 'from', 'vars': {'x': -60, 'duration': 0.35, 'ease': 'power3.out'}}],
    'css': '.cu .pl{box-shadow:0 28px 75px -38px rgba(0,0,0,.5)} .cu:has(.w.m) .pl{background:var(--acc)}'
           ' .cu:has(.w.m) .w{color:#141414}'}),
 # ---- Dynamiczne
 'jedno-slowo': ('Jedno słowo', 'dynamiczne', 'Jedno duże słowo naraz, w rytmie mowy. Najszybszy styl.', {
    'font': 'Anton', 'weight': 400, 'size': 140, 'case': 'upper', 'line_height': 1.0, 'color': '#FFFFFF',
    'shadow': '0 14px 56px rgba(0,0,0,.45)', 'mark': 'accent', 'words': 1, 'chars': 30, 'margin': 60,
    'motion': [{'target': 'self', 'tween': 'fromTo', 'from': {'scale': 1.35, 'opacity': 0},
                'vars': {'scale': 1, 'opacity': 1, 'duration': 0.22, 'ease': 'power2.out'}}]}),
 'schody': ('Schody', 'dynamiczne', 'Nowa linia pojawia się na dole, poprzednie wspinają się w górę i bledną.', {
    'font': 'Poppins', 'weight': 700, 'size': 76, 'line_height': 1.15, 'color': '#FFFFFF',
    'shadow': '0 9px 38px rgba(0,0,0,.45)', 'mark': 'accent', 'words': 3, 'chars': 18,
    'stack': {'keep': 3, 'gap': 6, 'dim': [0.45, 0.18], 'scale': [0.86, 0.74]},
    'css': '.cu .w{opacity:0}', 'word_motion': SHOW_SAID}),
 'echo': ('Echo', 'dynamiczne', 'Kursywa z cieniem w kolorze akcentu, który dogania każde słowo.', {
    'font': 'Playfair Display', 'weight': 800, 'italic': True, 'size': 92, 'line_height': 1.12, 'color': '#FFFFFF',
    'shadow': '0.07em 0.07em 0 color-mix(in srgb,var(--acc) 80%,transparent)', 'words': 3, 'chars': 16,
    'css': '.cu .w{opacity:0}',
    'word_motion': {'tween': 'fromTo', 'from': {'opacity': 0, 'x': -10, 'y': -10},
                    'vars': {'opacity': 1, 'x': 0, 'y': 0, 'duration': 0.45, 'ease': 'power2.out'}}}),
 'naglowek': ('Nagłówek', 'dynamiczne', 'Duży szeryfowy nagłówek wyrównany do lewej, słowa wyjeżdżają od dołu.', {
    'font': 'Playfair Display', 'weight': 900, 'size': 104, 'line_height': 0.98, 'color': '#FFFFFF',
    'shadow': '0 14px 66px rgba(0,0,0,.4)', 'align': 'left', 'margin': 97, 'mark': 'accent', 'words': 2, 'chars': 13,
    'css': '.cu .w.m{font-style:italic} .cu .w{opacity:0}',
    'word_motion': {'tween': 'fromTo', 'from': {'opacity': 0, 'yPercent': 35},
                    'vars': {'opacity': 1, 'yPercent': 0, 'duration': 0.3, 'ease': 'power3.out'}}}),
 'maszynopis': ('Maszynopis', 'dynamiczne', 'Tekst wystukiwany jak na maszynie, na zielonym pasku z kursorem.', {
    'font': 'JetBrains Mono', 'weight': 500, 'size': 56, 'line_height': 1.4, 'color': '#F8F3EA', 'shadow': False,
    'mark': 'accent', 'entrance': 'type-on', 'words': 4, 'chars': 22,
    'plate': {'color': 'rgba(30,62,58,.92)', 'radius': 8, 'pad': [19, 35]},
    'css': ".cu .pl::after{content:'\\258D';color:var(--acc);margin-left:.08em}"}),
 # ---- Edytorskie
 'gabinet': ('Gabinet', 'edytorskie', 'Rozstrzelone kapitaliki, a słowa kluczowe przechodzą w kursywę Playfair.', {
    'font': 'Poppins', 'weight': 500, 'size': 52, 'tracking': 0.16, 'case': 'upper', 'line_height': 1.5,
    'color': '#FFFFFF', 'shadow': '0 5px 28px rgba(0,0,0,.5)', 'mark': 'accent', 'words': 3, 'chars': 20, 'dy': -44,
    'css': ".cu .w.m{font-family:'Playfair Display';font-style:italic;font-weight:500;font-size:1.8em;"
           "letter-spacing:0;text-transform:none;line-height:1} .cu .w{opacity:0}",
    'word_motion': {'tween': 'fromTo', 'from': {'opacity': 0}, 'vars': {'opacity': 1, 'duration': 0.3}}}),
 'duet': ('Duet', 'edytorskie', 'Dwie linie, dwa kroje: mała linia kapitalikami, pod nią duża kursywa.', {
    'font': 'Playfair Display', 'weight': 700, 'italic': True, 'size': 100, 'line_height': 1.02, 'color': '#FFFFFF',
    'shadow': '0 9px 47px rgba(0,0,0,.35)', 'lines': 2, 'words': 2, 'chars': 14,
    'css': ".cu .ln:first-child:not(:only-child){font:500 46px/1.6 Poppins;letter-spacing:.2em;text-transform:uppercase;"
           "text-shadow:0 5px 28px rgba(0,0,0,.5)} .cu .ln:last-child .w{color:var(--acc)} .cu .w{opacity:0}",
    'word_motion': {'tween': 'fromTo', 'from': {'opacity': 0, 'y': 18},
                    'vars': {'opacity': 1, 'y': 0, 'duration': 0.3, 'ease': 'power2.out'}}}),
 'liczby': ('Liczby', 'edytorskie', 'Liczby rosną do dużych cyfr Bodoni w kolorze akcentu, reszta zostaje drobna.', {
    'font': 'Poppins', 'weight': 500, 'size': 64, 'line_height': 1.3, 'color': '#FFFFFF',
    'shadow': '0 5px 28px rgba(0,0,0,.5)', 'words': 3, 'chars': 20, 'dy': -70,
    'css': ".cu .w.m-num{font:900 2.6em/.95 'Bodoni Moda';color:var(--acc)} .cu .w{opacity:0}",
    'word_motion': SHOW_SAID,
    'mark_motion': {'tween': 'fromTo', 'from': {'scale': 1.3}, 'vars': {'scale': 1, 'duration': 0.3, 'ease': 'back.out(2)'}}}),
 'notatki': ('Notatki', 'edytorskie', 'Odręczne pismo, a pod słowami kluczowymi rysuje się kreska w kolorze akcentu.', {
    'font': 'Caveat', 'weight': 700, 'size': 108, 'line_height': 1.05, 'color': '#FFFFFF',
    'shadow': '0 9px 28px rgba(0,0,0,.45)', 'words': 3, 'chars': 18,
    'css': '.cu .w.m{background:linear-gradient(var(--acc),var(--acc)) no-repeat 0 94%/0% 12px;padding-bottom:.08em}'
           ' .cu .w{opacity:0}',
    'word_motion': SHOW_SAID,
    'mark_motion': {'tween': 'to', 'vars': {'backgroundSize': '100% 12px', 'duration': 0.5, 'ease': 'power2.out'}}}),
 'wstega': ('Wstęga', 'edytorskie', 'Fraza na pochylonej, butelkowozielonej wstędze, która rozwija się od lewej.', {
    'font': 'Poppins', 'weight': 600, 'size': 69, 'line_height': 1.3, 'color': '#FFFFFF', 'shadow': False,
    'mark': 'accent', 'words': 4, 'chars': 20, 'plate': {'color': '#1E3E3A', 'radius': 0, 'pad': [17, 41]},
    'css': '.cu .pl{transform:skewX(-8deg);box-shadow:0 28px 75px -38px rgba(0,0,0,.6)} .cu .pl .w{transform:skewX(8deg)}',
    'motion': [{'target': '.pl', 'tween': 'fromTo', 'from': {'clipPath': 'inset(0 100% 0 0)'},
                'vars': {'clipPath': 'inset(0 0% 0 0)', 'duration': 0.4, 'ease': 'power2.out'}}]}),
}

for key, (name, fam, desc, spec) in STYLES.items():
    cap = {**BASE, **spec}
    d = os.path.join(HERE, key)
    os.makedirs(d, exist_ok=True)
    style = {'name': name, 'slug': key, 'nkb': {'kind': 'captions', 'family': fam, 'catalog': 'napis-' + key},
             'caption': cap, 'pace': 'jak w nagraniu, pauzy przycięte', 'sound': 'sam głos'}
    with open(os.path.join(d, 'style.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(style, fh, ensure_ascii=False, indent=1)
    font = f"{cap['font']} {cap.get('weight', '')}{' kursywa' if cap.get('italic') else ''}, {cap['size']} px"
    md = (f"# {name} (styl napisów NKB)\n\nZ katalogu stylów NKB, rodzina „{fam.capitalize()}”. {desc}\n\n"
          f"- Type: {font}.\n- Colour: akcent = kolor marki klientki (domyślnie złoto NKB {ACC}).\n"
          "- Captions: przy dolnej krawędzi strefy bezpiecznej (position 1470), jak najdalej od twarzy.\n"
          "- Pace: jak w nagraniu, pauzy przycięte.\n- Graphic elements: brak.\n- Sound: sam głos.\n\n"
          "## Standing notes\n- Napisy nie wchodzą na twarz: zostają przy dolnej krawędzi strefy bezpiecznej.\n")
    with open(os.path.join(d, 'style.md'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(md)
print(len(STYLES), 'stylów napisów zapisanych')
