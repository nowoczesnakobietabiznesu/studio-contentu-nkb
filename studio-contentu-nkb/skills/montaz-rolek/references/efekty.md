# Efekty: lista dla klubowiczki

Efekty klubowiczka ogląda i zaznacza w katalogu stylów, pod stylami napisów ("Stwórz swój styl", sekcja "Dodaj
efekty"): każdy efekt gra tam jako gotowa rolka nagrana w Studiu, a ona zaznacza tyle, ile chce. Gdy pyta, jakie
efekty może mieć ("jakie są efekty", "co mogę dodać", "zmień efekty"), otwórz katalog od razu na efektach:
`PY "SK/scripts/picker.py" --tab effects --until-saved`. Woli w rozmowie? Pokaż jej tę listę: grupy niżej, jedna
linijka na efekt, polska nazwa i co robi. Kolumn z kluczem i wymaganiami jej nie pokazuj, służą Tobie. Gdy pyta o
jedną grupę albo o konkretny cel ("coś na liczby", "coś na listę kroków"), pokaż tylko pasujące. Jej nagrania znasz:
od razu powiedz, które efekty przy jej ujęciach odpadną (np. przy zbliżeniu twarzy wszystkie z "plan średni").
Innych efektów niż te z listy Studio nie ma i nie pokazujesz.

Zapis jej wyboru w rozmowie: `PY "SK/scripts/effects.py" set <klucze>` (albo `add`, `remove`, `clear`, `auto`,
`show`). Polska nazwa z tej listy też działa jako klucz. Katalog zapisuje do tego samego pliku.

**Nie wybrała żadnego efektu = dobierasz sama.** Pusta lista to nie "bez efektów": `footage_check.py` sprawdza wtedy
wszystkie efekty, a Ty bierzesz 1 do 3, które pasują do tego nagrania i jego zdań (SKILL.md, "Effects"). "Bez
efektów" mówi tylko `effects.py clear`.

**Wybrała efekt, który nie pasuje do nagrania = mówisz jej to przed montażem**, jednym prostym zdaniem z powodem
("Wybrałaś Klony, ale do tego nagrania nie pasują: potrzebują szerokiego kadru, a to jest zbliżenie. Montuję bez
nich."). Tak samo, gdy ujęcie pasuje, ale żadne zdanie nie daje efektowi treści (Licznik bez liczby w nagraniu).
Efekt to propozycja: użyj go tylko tam, gdzie pasuje do zdania i do ujęcia.

Czas: efekty z wycięciem postaci liczą je tylko dla swoich kilku sekund, na komputerze bez Apple Silicon to kilka
minut na efekt. Powiedz to, zanim zaczniesz. Część efektów przy pierwszym użyciu dociąga mały pakiet
(`setup.py --fx <klucz>`).

Skróty w kolumnie "Wymaga": **każde ujęcie** = działa też przy zbliżeniu twarzy; **plan średni** = widać Cię od pasa
albo szerzej, nie samo zbliżenie; **statyw** = kamera stoi nieruchomo; **ściana nad głową / obok / po bokach** = wolne
miejsce na ścianie w tym miejscu; **jej materiał** = coś, co musi dać (zdjęcia, nagranie ekranu, liczby).

## Grafiki na ekranie (szybkie, bez wycinania postaci)
| Efekt | Klucz | Co robi | Wymaga |
|---|---|---|---|
| Rozsypane słowa | `depth-scatter` | Pierwsze słowa rolki lądują po kolei w różnych rozmiarach. | każde ujęcie; otwarcie 2 do 6 słów |
| Wielka liczba | `stat-stack` | Liczba, którą mówisz, wielka na piersi, z małym podpisem pod spodem. | każde ujęcie; liczba w zdaniu |
| Kropki postępu | `dot-counter` | Rząd kropek: ile rzeczy będzie i przy której jesteś. | każde ujęcie; liczba od 2 do 8 |
| Pigułki listy | `chip-row` | Przy wyliczaniu pod napisami pojawia się pigułka na każdą rzecz. | każde ujęcie; lista 2 do 4 rzeczy |
| Pole promptu | `prompt-box` | Szklane pole, w które sam wpisuje się prompt, który mówisz. | każde ujęcie; polecenie do ok. 60 znaków |
| Proces na karcie | `serif-flow` | Ciemna karta, na której krok po kroku rozpisuje się Twój proces. | każde ujęcie; 2 do 4 kroków |
| Okno montażu | `pull-back-reveal` | Wideo zmniejsza się do okna aplikacji: odhaczana lista, oś ujęć, licznik. | każde ujęcie |

## Karty, listy i liczby
| Efekt | Klucz | Co robi | Wymaga |
|---|---|---|---|
| Lista kroków | `checklist` | Na ścianie buduje się karta, a kroki odhaczają się, gdy je mówisz. | każde ujęcie; 2 do 4 kroków |
| Komentarz | `comment-bubble` | Wpisuje się komentarz ze słowem-kluczem i pojawia się Twoja odpowiedź. | każde ujęcie; słowo do komentarza |
| Telefon | `phone-mockup` | Obok Ciebie wlatuje telefon z ekranem aplikacji. | każde ujęcie, bez chodzenia; jej nagranie ekranu albo obrazek |
| Karty z danymi | `the-stack` | Karty z liczbami i paskami nad Tobą, Ty w okienku pod nimi. | każde ujęcie; jej liczby |
| Licznik | `odometer` | Liczba kręci się cyfra po cyfrze jak licznik. | każde ujęcie; prawdziwa liczba |
| Stop-klatka z podpisami | `freeze-and-label` | Obraz zamiera, a podpisy ze strzałkami wskazują na Ciebie. | każde ujęcie; podpisy |
| Przed i po | `before-and-after` | Linia przesuwa się przez kadr i odsłania wersję po montażu. | każde ujęcie |
| Płonąca oś | `timeline-burn` | Oś montażowa składa się przed Tobą i na Twoje słowo się zapala. | plan średni |
| Spadające klocki | `word-pile` | Wymieniane rzeczy spadają jak klocki, odbijają się od głowy i odlatują. | każde ujęcie, bez chodzenia |

## Na ścianie za Tobą
| Efekt | Klucz | Co robi | Wymaga |
|---|---|---|---|
| Ściana okładek | `couch-wall` | Okładki Twoich rolek układają się w siatkę na ścianie. | plan średni; ściana nad głową; jej okładki (min. 4) |
| Ściana słów | `type-wall` | Wielkie słowa przesuwają się za Tobą i zmieniają na Twoje słowa. | plan średni; statyw; ściana nad głową |
| Ściana nagłówków | `headline-wall` | Ściana zapełnia się nagłówkami i postami, słowo-klucz podświetlone. | plan średni; ściana obok |
| Rosnący wykres | `chart-grow` | Na ścianie rysuje się wykres i wystrzeliwuje na Twoje słowo. | plan średni; ściana po bokach |
| Skreślane nazwy | `knockout-tiles` | Nazwy lądują na ścianie po jednej, potem są skreślane i strącane. | plan średni; ściana obok |
| Tapeta ze słowa | `scene-text` | Słowo drukuje się na ścianie jak tapeta, potem lądują na nim dwa duże słowa. | każde ujęcie, bez chodzenia; ściana obok |
| Neon | `neon-sign` | Twoje hasło jako neon na ścianie: miga, zapala się, pokój ciemnieje. | plan średni; ściana obok |
| Szklane słowo | `glass-type` | Jedno słowo z grubego szkła na ścianie, załamuje światło. | każde ujęcie, bez chodzenia; ściana nad głową |
| Okładka magazynu | `cover-story` | Kadr staje się okładką: tytuł za głową, ramka, podpisy. | każde ujęcie, bez chodzenia; ściana nad głową |
| Szklane panele | `spatial-glass` | Trzy matowe szyby unoszą się wokół Ciebie, po jednej na krok. | każde ujęcie, bez chodzenia; ściana obok |

## Ty w roli głównej
| Efekt | Klucz | Co robi | Wymaga |
|---|---|---|---|
| Orbita | `orbit` | Twoje rolki krążą wokół Ciebie, z przodu i z tyłu. | plan średni, bez chodzenia; jej okładki (min. 4) |
| Ekran za Tobą | `ui-world` | Za Tobą ekran aplikacji na cały kadr. | plan średni, bez chodzenia; jej zrzut albo opis ekranu |
| Wyjście z ramki | `frame-break` | Wideo zmniejsza się do karty, a głowa i ręce z niej wychodzą. | plan średni |
| Zielone tło | `green-screen` | Jesteś mała na dole kadru, a za Tobą to, o czym mówisz. | plan średni; jej wideo albo zdjęcie tematu |
| Klony | `clone` | Obok pojawiają się Twoje kopie, a na puentę mówicie razem. | plan szeroki; statyw; wolne miejsce po obu stronach |
| Okno w sylwetce | `inside-out` | W Twojej sylwetce gra wybrane nagranie, potem odwrotnie. | każde ujęcie, bez chodzenia; jej nagranie albo zdjęcie |
| Kolaż z papieru | `paper-cut` | Pokój zmienia się w podarty papier, a hasło układa się z wycinanych liter. | każde ujęcie, bez chodzenia |
| Kredowy kontur | `doodle-boil` | Kreda obrysowuje Twoją sylwetkę i rysuje doodle na wybrane słowa. | każde ujęcie, bez chodzenia |
| Kod | `code-scan` | Obraz zamienia się w kod, Ty jesteś jaśniejszą postacią, terminal pisze dwie linijki. | każde ujęcie, bez chodzenia |
| Naklejka | `freeze-sticker` | Twoja stop-klatka staje się naklejką z odręcznymi dopiskami. | każde ujęcie; dopiski |
| Przyklejona etykieta | `sticky-text` | Etykieta przyklejona do Ciebie, rusza się razem z Tobą. | każde ujęcie |

## Światło i kamera
| Efekt | Klucz | Co robi | Wymaga |
|---|---|---|---|
| Najazd | `digital-zoom` | Powolny najazd na twarz, szarpnięcie na słowo, odjazd. | każde ujęcie |
| Zaciemnienie | `blackout` | Pokój przygasa na Twoje zdanie, słowo wpada za głowę, światło wraca. | każde ujęcie |
| Ostrość na tytuł | `rack-focus` | Ostrość przeskakuje z Ciebie na tytuł i z powrotem. | każde ujęcie, bez chodzenia |
| Przejście przez Ciebie | `zoom-through-cut` | Kamera wjeżdża w Ciebie i wyjeżdża w następnym ujęciu. | dwa ujęcia jedno po drugim |
| Pękające szkło | `shatter-3d` | Kadr pęka na kafelki, drga na słowo i rozpada się jak szkło. | każde ujęcie, bez chodzenia |
