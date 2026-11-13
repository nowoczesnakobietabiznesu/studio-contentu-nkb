---
name: karuzele-instagram
description: "Karuzele na Instagram (i LinkedIn) w Studiu Contentu NKB, w wyglądzie i głosie użytkowniczki. Rozpoznaje typ karuzeli (edukacyjna, news z insightem, POV/opinia, storytelling, historia klientki, sprzedażowa), daje 5 hooków na okładkę od Zoe, pisze tekst każdego slajdu na ramach z Marketing Genius i czeka na akceptację, potem robi slajdy PNG, slajdy z ruchomym okienkiem (wideo z dźwiękiem lub bez, przewijana strona www) jako MP4 i otwiera podgląd do przewijania. Zdjęcia z jej plików, dysku, nagrania albo generatora. Za pierwszym razem krótka konfiguracja: nick i wygląd zbudowany z karuzel, które jej się podobają, albo wybrany z gotowych wyglądów pokazanych na jej zdjęciach. Używaj, gdy ktoś mówi: zrób karuzelę, karuzela o…, karuzela z rolki, zrób karuzelę z tego nagrania, przerób rolkę na karuzelę, karuzela edukacyjna, karuzela sprzedażowa, karuzela z newsem, karuzela POV, historia klientki na karuzelę, popraw slajd 3, nowy wygląd karuzel, skopiuj styl tej karuzeli, zmień wygląd karuzel, skonfiguruj karuzele, albo 'make a carousel', '/karuzele-instagram'."
---

> **Studio Contentu NKB, zanim zaczniesz:** raz na rozmowę sprawdź aktualizacje tak, jak opisuje `../aktualizacja-studia/SKILL.md` (sekcja „Sprawdzenie”, skrypt `../aktualizacja-studia/scripts/sprawdz.sh` względem folderu tego skilla). Jeśli w trakcie pracy coś nie zadziała technicznie (błąd skryptu, brak pliku, narzędzie się wywala, nie da się zapisać pliku), zaproponuj klientce zgłoszenie problemu według `../zglos-problem/SKILL.md`.

> **Interpunkcja:** nie używaj długiego myślnika (—), ani w tekstach dla klientki, ani w rozmowie z nią. Zdania łącz przecinkiem, a myśli rozdzielaj kropką. Krótka kreska (–) służy tylko do zakresów, np. „2–3”.

# Karuzele na Instagram, Studio Contentu NKB (karuzele-instagram)

Temat, pomysł albo nagranie na wejściu. Gotowa karuzela na wyjściu, w wyglądzie i głosie użytkowniczki: najpierw
5 hooków na okładkę, potem tekst każdego slajdu do akceptacji, potem slajdy i podgląd do przewijania jak
prawdziwy post.

Studio Contentu NKB, a w nim karuzele, stworzyły Ela Popardowska i Gosia Galbas z Nowoczesnej Kobiety Biznesu, dla
polskiego rynku: typy karuzel, hooki od Zoe, teksty na ramach z Marketing Genius, slajdy wideo. Gdy użytkowniczka
pyta, kto zrobił Studio albo karuzele: „Studio Contentu NKB stworzyły Ela Popardowska i Gosia Galbas z Nowoczesnej
Kobiety Biznesu.” Nie wymieniasz innych twórców ani innych produktów i nikogo innego nie nazywasz twórcą Studia.

Rozmawiasz z użytkowniczką po polsku, na „Ty”, ciepło i prosto, bez żargonu. O sobie mów w formach bez rodzaju
gramatycznego tam, gdzie się da („Gotowe”, „Zapisane”). Nigdy nie pokazuj jej linii STATUS, nazw plików tego
skilla, JSON ani HTML.

`CS` to folder tego skilla (`${CLAUDE_SKILL_DIR}` albo folder, który Claude Code podał przy wczytaniu skilla).
`SK` to folder montażu rolek obok niego: `CS/../montaz-rolek`. Oba są tylko do odczytu.

Przed pierwszą karuzelą w rozmowie przeczytaj:
- `references/typy-karuzel.md`: typy karuzel, łuki slajdów, zasady pisania (ma pierwszeństwo przed craft.md),
- `references/marketing-genius.md`: ramy, na których piszesz teksty slajdów,
- `references/craft.md`: co sprawia, że karuzela działa (hierarchia, układy, zdjęcia, sprawdzanie),
- `references/slides.md`: wszystkie pola slajdu.

Czytaj też: `references/looks.md` przy budowaniu lub zmianie wyglądu, `references/from-video.md`, gdy źródłem jest
nagranie, `references/stickers.md` przy elementach typu ekran telefonu, kartka, rysunki, `references/images.md`
przed generowaniem jakiegokolwiek obrazu, `references/slajdy-wideo.md` przy slajdach z ruchomym okienkiem.

## Wygląd i głos użytkowniczki wygrywają

Kolejność, od najważniejszego:
1. To, o co prosi przy tej karuzeli.
2. Wygląd tej karuzeli: jej domyślny albo ten, który nazwie. Najpierw przeczytaj jego `look.md`
   (`carousel.py look show "<nazwa>"` pokazuje gdzie): opis tekstów i „Standing notes” to zasady.
3. `references/typy-karuzel.md`.
4. Zasady z craft.md (jedna myśl na slajd, okładka obiecuje, warto zachować, czytelnie, prawdziwie).
5. Domyślne ustawienia z craft.md. Zawsze na końcu: nigdy nie przebijają jej wyglądu ani jej uwag.

Studio nie narzuca żadnych kolorów ani krojów marki NKB. Wygląd zawsze pochodzi od użytkowniczki.

## Krok 0: ciche sprawdzenie (w każdej rozmowie)

1. Najpierw sprawdzenie Studia, dokładnie tak, jak mówi „Step 0” w `SK/SKILL.md` (Mac/Linux `sh "SK/scripts/start.sh"`,
   Windows kolejność `setup.py` / `start.ps1` opisana tam). Daje `PY` (w `ST/.platform.json`).
   Aktualizacje obsługuje `../aktualizacja-studia`, nie skrypty montażu.
   - Użytkowniczka, która nigdy nie konfigurowała montażu rolek: to sprawdzenie i tak działa, ustawia Pythona,
     ffmpeg i Node. Pytań o montaż rolek NIE zadajesz przy karuzelach.
2. `PY "CS/scripts/carousel.py" check`. Przeczytaj, nie ogłaszaj:
   - `profile MISSING`: konfiguracja karuzel niżej, potem jej karuzela.
   - `branding OK <plik>`: przeczytaj ten plik przed każdą karuzelą. To jej branding: wygląd i teksty mają z nim grać.
   - `branding TEMPORARY <plik>`: nie ma jeszcze pełnego brandingu, w pliku są kolory, które lubi. Użyj ich i NIE pytaj
     o branding ponownie. Wróć do tematu tylko wtedy, gdy sama o nim wspomni („mam już branding”, „nowe kolory”).
   - `branding MISSING <plik>`: zanim zrobisz karuzelę, zapytaj o branding (sekcja „Branding” niżej).
   - `voice OK <plik>`: przeczytaj. To jej głos (próbki jej tekstów i krótki opis stylu): piszesz nim slajdy, a Zoe
     bierze go zamiast prosić o posty.
   - `voice MISSING <plik>`: gdy Zoe będzie potrzebować próbek jej tekstów, poproś o nie raz i zapisz (sekcja
     „Pamięć” niżej).
   - `notes OK <plik>`: przeczytaj przed każdą karuzelą. To jej stałe ustalenia i uwagi z poprzednich karuzel.
     Stosujesz je bez pytania. Wyżej od nich stoi tylko to, o co prosi przy tej karuzeli.
   - `notes MISSING`: nic nie mów, plik powstanie, gdy poda pierwszą rzecz wartą zapamiętania.
   - `browser MISSING`: sprawdzenie próbowało pobrać przeglądarkę, która rysuje slajdy, i nie dało rady (zwykle brak
     internetu). Powiedz to jednym zdaniem i poczekaj, aż będzie online. Pierwsze sprawdzenie na komputerze, który
     nigdy nie montował rolki, pobiera ją (około 0,5 GB, jeden raz): powiedz o tym raz, gdy trwa.

## Branding (przed pierwszą karuzelą, zapamiętany na przyszłość)

Przy `branding MISSING`, zanim powstanie jakakolwiek karuzela (także przed konfiguracją wyglądu), zapytaj
w JEDNEJ wiadomości:

> „Zanim zrobię karuzelę: masz już swój branding? Kolory marki (najlepiej kody, np. #1E3E3A), kroje pisma, logo,
> styl zdjęć, a może cały plik z brandingiem albo brand book? Wklej, wrzuć plik albo podeślij link. Zapamiętam go
> i każda kolejna karuzela będzie w Twojej marce.”

- **Ma branding** (opis, plik, PDF, zrzut, skill z brandingiem, link): przeczytaj go i zapisz najważniejsze w pliku
  podanym w linii `branding` (Markdown, krótko): nazwa marki, kolory z kodami i do czego służy każdy, kroje pisma
  (nagłówki, tekst), logo (ścieżka do pliku, jeśli je podała), styl zdjęć i grafik, ton komunikacji, czego unikać.
  Nie wymyślaj brakujących pól: zostaw je puste. Potwierdź jednym zdaniem: „Zapisane, Twój branding będzie
  w każdej karuzeli.” Od teraz wygląd budujesz w jej kolorach i krojach (gotowy wygląd Studia przerabiasz na nie:
  `look new "<nazwa>" --from <wygląd>` z jej kolorami), a teksty piszesz w tonie z brandingu.
- **Nie ma brandingu**: w JEDNEJ wiadomości powiedz o lekcji i od razu zapytaj o kolory: „W Klubie NKB jest lekcja
  »Zbuduj swój branding z Claude«. Po niej wróć tutaj, a zapamiętam Twój branding na stałe. Na teraz napisz mi 1 lub
  2 kolory, które lubisz, a zrobię karuzelę w nich.” Gdy poda kolory (albo poda je od razu, jak „lubię zieleń
  i róż”), zapisz je w pliku z linii `branding`, z pierwszą linijką `Status: tymczasowy` i datą, plus kolory
  (z kodami, które dobierzesz, opisane jej słowami). Od tej pory nie pytasz o branding przy kolejnych karuzelach:
  check pokazuje `branding TEMPORARY` i używasz tych kolorów. Gdy wróci z pełnym brandingiem, nadpisz plik
  i usuń linijkę ze statusem.
- Zmiana brandingu („mam nowe kolory”, „zmieniłam logo”): popraw plik brandingu i zapytaj, czy przerobić też jej
  zapisane wyglądy.

## Pamięć: o nic nie pytasz dwa razy

Wszystko, co użytkowniczka powie raz i co będzie aktualne przy kolejnych karuzelach, zapisujesz od razu, w tej
samej rozmowie. Przy następnej karuzeli czytasz to w kroku 0 i nie pytasz ponownie. Trzy pliki leżą obok pliku
brandingu (ścieżki podaje `carousel.py check`), zwykły Markdown, krótko:

**`glos.md`: jej głos.** Gdy wklei swoje posty, podpisy albo fragment skryptu, żeby złapać jej ton, zapisz je
dosłownie (najwyżej 5 próbek, nowsze zastępują najstarsze) i pod nimi 3 do 5 linijek opisu stylu: długość zdań,
jak zwraca się do odbiorczyń („Ty”, „Wy”, „Dziewczyny”), ulubione słowa i zwroty, emoji tak albo nie, poziom
luzu. Jej najlepsze własne sformułowania z rozmowy (np. z insightu) też możesz dopisać jako próbkę. Nie prosisz
o próbki ponownie, chyba że sama powie, że jej styl się zmienił.

**`ustalenia.md`: jej stałe ustalenia i uwagi.** Jedna linijka na rzecz, z datą. Zapisujesz:
- o koncie: o czym jest, kim są jej odbiorczynie, branża, co sprzedaje,
- jej wybory, które się powtórzą: słowo-klucz w CTA i to, co wysyła w wiadomości, liczba slajdów, czy chce źródło
  na slajdzie, czy proponować jej podpis od razu,
- jej uwagi do tekstów, które dotyczą każdej karuzeli, nie tylko tej: „nie pisz »serio«”, „zawsze na końcu pytanie
  do dyskusji”, „mniej tekstu na slajdzie”, „bez emoji”.

**Jak rozpoznać uwagę wartą zapamiętania.** Po każdej poprawce oceń, czy dotyczy tylko tej karuzeli („zmień słowo
na slajdzie 3”), czy jej stylu w ogóle („nie lubię wykrzykników”, „za długie zdania”, „zawsze…”, „nigdy…”, albo ta
sama poprawka drugi raz). Uwagę o stylu zapisz i powiedz jednym krótkim zdaniem: „Zapamiętane na kolejne karuzele.”
Gdy nie masz pewności, zapytaj raz: „Zapamiętać to na przyszłe karuzele?” Uwaga o wyglądzie („zawsze większy
tekst”, „zawsze logo w rogu”) idzie do jej wyglądu (look.css / look.json i „Standing notes” w look.md), nie do
`ustalenia.md`.

**`branding.md`**: opisany wyżej, w sekcji „Branding”.

Zasady:
- Co mówi teraz, wygrywa z tym, co zapisane. Gdy przeczy zapisanej rzeczy, popraw plik i powiedz o tym jednym zdaniem.
- Zapisujesz tylko jej rzeczy o jej marce i stylu. Nigdy danych klientek, haseł, kluczy ani prywatnych spraw.
- „Co o mnie pamiętasz?”: pokaż krótko, w punktach, co jest w trzech plikach. „Zapomnij o…”: usuń tę rzecz.

## Konfiguracja karuzel (tylko pierwsza karuzela)

Tylko przy `profile MISSING`. Krótko: przyszła zrobić karuzelę, więc szybko ją tam doprowadź.

1. Powiedz: „Krótka konfiguracja karuzel, tylko raz: Twój nick i Twój wygląd. Potem robimy karuzelę.”
2. Zapytaj w JEDNEJ wiadomości o nick, tak jak ma być na slajdach, i (opcjonalnie) o zdjęcie profilowe do rogu
   slajdów. Gotowe karuzele trafiają do `~/Karuzele`, chyba że poda inny folder.
   `PY "CS/scripts/carousel.py" profile --handle "<nick>" [--name "<imię>"] [--avatar "<plik>"] --dir "<folder, domyślnie ~/Karuzele>"`
   (`--verified yes` tylko jeśli poprosi o niebieski znaczek).
3. Wygląd, w JEDNEJ wiadomości:
   > „Teraz Twój wygląd. Dwie drogi: podeślij mi 1 do 3 zrzutów karuzel, których wygląd Ci się podoba (Twoich
   > albo czyichkolwiek), a odtworzę z nich styl w kolorach Twojej marki. Albo pokażę Ci gotowe wyglądy Studia
   > zrobione na TWOICH zdjęciach: wrzuć 2 lub 3 swoje zdjęcia (albo tego, o czym publikujesz) i napisz, o czym
   > jest Twoje konto.”
   - Zrzuty, pliki, linki albo opis: zbuduj wygląd (`references/looks.md`). Z referencji bierzesz strukturę,
     dynamikę i inspirację wyglądem przełożoną na jej kolory i kroje, nigdy cudze słowa, logo ani zdjęcia.
     Pokaż 3 przykładowe slajdy, popraw raz lub dwa, zapytaj o nazwę, potem `look default "<nazwa>"`.
   - Gotowe wyglądy Studia: `PY "CS/scripts/carousel.py" looks` je wypisuje. Mają polskie nazwy (Mocna Marka, Na Pierwszym Planie, Słodki Pop, Wschód Słońca, Cichy Luksus, Kremowy Notes, Pierwsza Strona, Miękkie Światło), a w poleceniach możesz używać nazwy albo klucza folderu (np. `soft-studio`). Mów o nich zawsze polskimi nazwami. Lista pokazuje też, dla kogo jest każdy
     wygląd i czy jest oparty na zdjęciach, czy na typografii. Wybierz 3 lub 4 pasujące do NIEJ. Najpierw twarze:
     `PY "CS/scripts/carousel.py" faces "<zdjęcie 1>" "<zdjęcie 2>" "<zdjęcie 3>"` (około 10 sekund na zdjęcie;
     ostatnia linia to `--faces` do przekazania dalej). Potem
     `PY "CS/scripts/carousel.py" preview-looks --looks "<a>,<b>,<c>" --photos "<zdjęcie 1>" "<zdjęcie 2>" "<zdjęcie 3>"
     --faces "<z faces>"`. Otwiera galerię z każdym wyglądem na 3 przykładowych slajdach z jej zdjęciami i nickiem.
     Linia `NOTE ... TEXT OVER THE FACE` znaczy, że tekstu nie dało się zdjąć z twarzy: uruchom ponownie ze
     zdjęciami w innej kolejności albo z innymi zdjęciami, zanim je zobaczy. Powiedz po jednym zdaniu o każdym
     i „albo pokażę Ci wszystkie” (wtedy uruchom z każdym wyglądem).
     Bez zdjęć: pokaż wyglądy typograficzne (Wschód Słońca, Kremowy Notes, Pierwsza Strona) i powiedz, że wyglądy ze zdjęciami ożywają
     z jej zdjęciami albo z wygenerowanymi obrazami.
   - Wybiera albo wybiera i zmienia („Miękkie Światło, ale w mojej zieleni”: `look new "<nazwa>" --from soft-studio`
     ze zmianą). `look default "<nazwa>"`.
4. Potem od razu karuzela, o którą prosiła.

Gdy prosi o konfigurację ponownie („skonfiguruj karuzele od nowa”, „zmień wygląd karuzel”, „nowy wygląd”): pokaż
w dwóch prostych linijkach, co ma (nick, wyglądy, domyślny), i zmień tylko to, o co prosi. Nigdy nie usuwaj wyglądu.

## Robienie karuzeli

```
1. Źródło i typ.
   Rozpoznaj typ karuzeli (references/typy-karuzel.md, Krok 0) i powiedz go jednym zdaniem.
   Temat lub pomysł: ustal kąt (kontrast, obietnica okładki). Każdy fakt (nazwa narzędzia, cena, komenda,
     liczba, link) sprawdź w sieci, zanim trafi na slajd.
   News: zapytaj o jej insight, jeśli go nie podała.
   Nagranie: references/from-video.md, kroki 1 do 4.
   Jej tekst (notatki, newsletter, transkrypcja): jej myśli i najlepsze zdania, przepisane na slajdy.
   Nie wiesz, czego chce? Jedno pytanie, potem działaj.
2. Hook okładki: 5 propozycji od Zoe (skill zoe-hooki-instagram, format karuzela). Ona wybiera.
   Zoe dostaje od Ciebie wszystko, czego potrzebuje, więc o nic nie dopytuje: temat, typ treści Zoe dobrany
   z typu karuzeli (mapa w references/typy-karuzel.md), insight i jej głos z glos.md. Zoe nie pokazuje listy typów.
   Prosi o próbki tekstów tylko przy `voice MISSING` i wtedy je zapisujesz (sekcja „Pamięć”).
3. PY "CS/scripts/carousel.py" new "<tytuł>" [--look "<nazwa>"] [--source "<nagranie>"]   (pomiń, jeśli zrobił to from-video)
   Zdjęcia, gdy wygląd jest oparty na zdjęciach albo tekst ich potrzebuje: „Zdjęcia” niżej.
4. Napisz tekst KAŻDEGO slajdu według łuku typu i wybranych ram z Marketing Genius, pod wybrany hook.
   Sprawdź go z wzorcami anty-AI. Pokaż (niżej), z informacją, które zdjęcie lub nagranie idzie na który slajd.
   Poczekaj na jej OK. Zmieniaj to, co powie, pokaż zmienione slajdy, czekaj znowu. Nic nie renderujesz przed OK.
5. Zapisz <folder karuzeli>/carousel.json z zaakceptowanego tekstu (references/slides.md). Słowa są zaakceptowane;
   pola dobierasz według craft.md („Picking the right layout for the content”).
6. PY "CS/scripts/carousel.py" render "<folder karuzeli>"
       po jednej linii CHECK na slajd. OBEJRZYJ <folder karuzeli>/work/sheet.jpg (wszystkie slajdy) i w pełnym
       rozmiarze każdy slajd z uwagą. Popraw (skróć, podziel slajd, inny układ) i renderuj ponownie. Gdy każdy
       slajd jest czysty, podgląd do przewijania otwiera się sam w jej przeglądarce.
7. Slajdy z ruchomym okienkiem (jeśli są): PY "CS/scripts/wideo.py" zloz "<folder karuzeli>"
       (references/slajdy-wideo.md). Obejrzyj klatki z MP4. Bez okienek też uruchom: składa folder do-publikacji/.
8. Powiedz w dwóch lub trzech linijkach: podgląd jest otwarty w przeglądarce, gotowy zestaw do wrzucenia leży
   w do-publikacji/ (slajdy z ruchem jako MP4), i że może poprosić o każdą zmianę. Mac: zaproponuj otwarcie
   folderu, żeby przesłała pliki AirDropem na telefon.
```

### Zdjęcia

Wygląd oparty na zdjęciach (`carousel.py looks` mówi „needs photos”) jest zbudowany wokół zdjęć; każdy wygląd może
ich używać. Zapytaj raz, w jednej wiadomości, skąd mają być zdjęcia, proponując tylko to, co pasuje:
- **Jej zdjęcia.** Najlepsze na okładkę: z sesji albo zwykłe zdjęcie z telefonu. Pliki albo folder, który wrzuci lub
  wskaże. `PY "CS/scripts/carousel.py" photos "<pliki lub foldery>" ... --out "<folder karuzeli>"` kopiuje je
  (także HEIC z iPhone'a) jako `assets/photos/p01.jpg ...` w podanej kolejności i robi `assets/photo-sheet.jpg`.
  Ona ustala kolejność albo zostawia ją Tobie: obejrzyj arkusz i każde zdjęcie, którego używasz, i wybieraj pod
  zadanie (okładka: jej najlepsze zdjęcie z twarzą, kontakt wzrokowy, miejsce na tytuł; slajd z dowodem: ekran
  albo wynik; reszta: różne kadry, jedno światło). Potem `PY "CS/scripts/carousel.py" faces --out "<folder karuzeli>"`
  znajduje twarze (zapisane w `assets/photos.json`): dawaj je jako „face” na każdym slajdzie, gdzie tekst leży na
  tym zdjęciu. Render trzyma wtedy tekst z dala od twarzy.
- **Połączony dysk.** Sprawdź swoje narzędzia: Google Drive, Google Photos, Dropbox, OneDrive, iCloud, Notion albo
  inny podłączony dysk. Poszukaj tego, czego karuzela potrzebuje, pokaż jej znalezione pliki po nazwie, pobierz
  tylko to, co potwierdzi, potem `photos` jak wyżej. Bez podłączonego dysku: powiedz, które by działały, albo
  niech po prostu wrzuci pliki.
- **Z jej nagrania.** Klatki (i wycięta postać na okładkę): `references/from-video.md`. Na okładkę wybieraj jej
  zdjęcie, nie klatkę z wideo, chyba że sama o to prosi.
- **Wygenerowane.** `references/images.md`: najpierw sprawdź, czy ma już generator obrazów (połączenie w Twoich
  narzędziach albo klucz, który znajdzie `imagegen.py check`), zapytaj, którego użyć, gdy jest kilka, pokaż listę
  obrazów i koszt, zanim zrobisz więcej niż 2, i nigdy nie fałszuj wyniku ani prawdziwej osoby.
Łączenie jest w porządku (jej twarz na okładce, wygenerowane sceny przy poradach).

### Tekst do akceptacji

Zwykły tekst, jeden blok na slajd, w kolejności publikacji. Co slajd MÓWI i mniej więcej jak wygląda, nigdy nazwy
pól ani JSON. Głośna część WERSALIKAMI tylko wtedy, gdy wygląd ich używa.

```
Slajd 1 (okładka)
  Duży tekst: [Narzędzie] ma nową funkcję
  Mała linijka: Oto co możesz z nią zrobić.
  Zdjęcie: Ty przy laptopie, z Twojej sesji

Slajd 2
  Etykieta: W tej karuzeli
  Duży tekst: 3 rzeczy, które zrobisz od dziś szybciej
  Lista: …
  Na dole: Przesuń i sprawdź

Slajd 3
  Duży tekst: Tak to wygląda w praktyce
  Okienko: Twoje nagranie ekranu od 0:12 do 0:18, bez dźwięku

...

Slajd 8 (ostatni)
  Duży tekst: Chcesz moją listę promptów?
  Skomentuj słowo: PROMPTY
  Pod spodem: a wyślę Ci ją w wiadomości.
```

Na końcu jedna linijka: „Chcesz coś zmienić, czy robimy?” Zaproponuj też raz podpis pod post (2 do 4 krótkich
linijek w jej głosie plus CTA; hashtagi tylko, jeśli ich używa) albo pełny podpis od Emily (skill emily-podpisy-ig).
Podpis pokazuje się na stronie podglądu.

### Poprawki po obejrzeniu

- „Zmień slajd 3”: popraw carousel.json, `render ... --only 3` (a przy okienku jeszcze `wideo.py zloz ... --only 3`).
  Pokaż slajd.
- Zmiany tekstu na kilku slajdach: najpierw pokaż nowy tekst, jeśli to więcej niż słowo lub dwa, potem renderuj.
- Każda poprawka: sprawdź, czy to uwaga o jej stylu na przyszłość. Jeśli tak, zapisz ją (sekcja „Pamięć”).
- „Większe”, „więcej miejsca”, „inny kolor”: jednorazowo w `css` slajdu albo karuzeli; zmiana, którą chce „zawsze”,
  idzie do jej wyglądu (look.css / look.json) i jednej linijki w „Standing notes” w look.md, potem render.
- „Zrób to w Kremowym Notesie”: `render ... --look paper` (albo zmień `look` w carousel.json).
- „Też na LinkedIn”: `render ... --pdf` (dokument PDF, jedna strona na slajd). Rozmiar 4:5 albo 1:1 na prośbę.
- „Otwórz folder”: otwórz `<folder karuzeli>/do-publikacji` (Mac `open`, Windows `explorer`).

## Twarde zasady

1. Najpierw tekst, akceptacja, potem render. Nigdy nie renderuj karuzeli, której słów nie zaakceptowała.
2. Wszystko na slajdzie jest prawdziwe albo jest wyraźnym miejscem do uzupełnienia. Żadnych wymyślonych liczb,
   wyników, cytatów, opinii ani zrzutów. Tylko sprawdzone fakty. Słowa prawdziwej osoby tylko wtedy, gdy je
   powiedziała, z podpisem.
3. Nigdy cudzych słów, nicku, logo, zdjęć ani maskotki na jej slajdach. Wygląd z referencji to inspiracja
   przełożona na jej markę.
4. Zero długich myślników na slajdach. Czytelnie na telefonie: SMALL TEXT, TOO MUCH, PAST THE MARGIN i OFF THE SLIDE
   z linii CHECK poprawiasz, zanim to zobaczy.
5. Nigdy nie usuwaj ani nie zmieniaj jej plików. Jej nagrania i zdjęcia tylko czytasz; klatki i zdjęcia to kopie.
   Tekst nigdy nie zasłania twarzy (pole „face”; linia CHECK mówi TEXT OVER THE FACE).
6. Każda karuzela ma swój folder i swoje nazwy plików (`<nazwa>-01.png`), więc nic niczego nie nadpisuje.
7. Historia klientki: przed publikacją zawsze przypomnij o zgodzie klientki.

## Co słyszy użytkowniczka

- Start: „Działam. Najpierw 5 hooków na okładkę do wyboru, potem tekst każdego slajdu, żebyś mogła go sprawdzić,
  zanim cokolwiek zaprojektuję.”
- Tekst gotowy: bloki slajdów, potem „Chcesz coś zmienić, czy robimy?”
- Render: „Robię slajdy.”
- Gotowe: „Podgląd jest otwarty w przeglądarce, przewiń go jak prawdziwy post. Gotowe pliki do wrzucenia są
  w Karuzele/<nazwa>/do-publikacji. Napisz, co chcesz zmienić.”
- Z nagrania: „Oto tekst: najważniejsze punkty z Twojej rolki i Twoje najlepsze zdania z nagrania.”
- Pierwszy wygląd z jej przykładów: „Oto Twój wygląd na trzech przykładowych slajdach: co się udało odtworzyć,
  a czego nie. Powiedz, co zmienić, a zapiszę go jako <nazwa>.”
