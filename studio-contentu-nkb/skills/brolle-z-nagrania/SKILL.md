---
name: brolle-z-nagrania
description: Wycina z długiego nagrania wideo krótkie, wizualne b-rolle (zza kulis sesji zdjęciowej, nagranie ciągiem z telefonu, materiał z eventu, warsztatów lub nagrania produktu), które potem służą jako krótkie przebitki albo rolki z napisami na Instagramie. To NIE jest skill do długich formatów mówionych (nagrań, w których mówisz do kamery, podcastów, webinarów): liczy się obraz, nie to, co ktoś mówi. Sprawdza wymagane narzędzia, przegląda całe nagranie, proponuje najlepsze momenty, buduje lokalną stronę z odtwarzanymi podglądami do wyboru i wycina zatwierdzone fragmenty w 1080p co do klatki. Używaj ZAWSZE, gdy użytkowniczka mówi o pocięciu długiego filmu na kawałki, wyciągnięciu b-rolli, przebitek lub krótkich ujęć z nagrania, „mam 20 minut materiału z sesji”, „wytnij mi fragmenty na rolki”, „znajdź najlepsze momenty w tym wideo”, nawet jeśli nie użyje słowa „b-roll”. NIE używaj do montażu gotowej rolki z mówieniem do kamery, napisami i muzyką (to inna praca) ani do samej konwersji formatu pliku.
---

> **Studio Contentu NKB, zanim zaczniesz:** raz na rozmowę sprawdź aktualizacje tak, jak opisuje `../aktualizacja-studia/SKILL.md` (sekcja „Sprawdzenie”, skrypt `../aktualizacja-studia/scripts/sprawdz.sh` względem folderu tego skilla). Jeśli w trakcie pracy coś nie zadziała technicznie (błąd skryptu, brak pliku, narzędzie się wywala, nie da się zapisać pliku), zaproponuj klientce zgłoszenie problemu według `../zglos-problem/SKILL.md`.

# B-rolle z długiego nagrania

**Do czego jest ten skill:** do wizualnych b-rolli, czyli krótkich ujęć bez mówienia (ruch, detale, emocje,
kulisy), które klientka wykorzysta jako przebitki w rolce albo jako krótką rolkę z napisami. Jeśli
klientka chce pociąć długie nagranie, w którym mówi (rolkę do kamery, podcast, webinar, live), powiedz
jej wprost, że ten skill tego nie robi, bo wybiera ujęcia po obrazie, a nie po treści wypowiedzi.

Ten skill zamienia jedno długie nagranie w zestaw krótkich, czystych ujęć gotowych do montażu. Użytkowniczka nie musi przewijać 20–40 minut materiału: Ty przeglądasz całość, proponujesz najlepsze momenty, ona ogląda je jako prawdziwe wideo na lokalnej stronie, zaznacza wybrane i dopisuje uwagi, a Ty wycinasz to, co zatwierdziła.

Cały warsztat techniczny jest w `scripts/brolle.py` (Python, tylko biblioteka standardowa + ffmpeg). Korzystaj z niego zamiast pisać własne polecenia ffmpeg. Skrypt zawiera poprawki problemów, które wyszły w praktyce (opisane niżej w „Pułapkach”).

Pisz do użytkowniczki po polsku, prostym językiem, bez żargonu technicznego. Kiedy coś trwa dłużej (arkusze, podglądy, cięcie), uruchamiaj to w tle i krótko mów, co się dzieje.

Ścieżkę do skryptu oznaczam niżej jako `SKRYPT` (to `scripts/brolle.py` w folderze tego skilla). Python wywołuj jako `python`, a jeśli nie działa, jako `py` (Windows) albo `python3` (Mac, Linux).

## Krok 0. Sprawdzenie wymagań (przed pierwszą pracą)

Bez ffmpeg nic się nie uda, więc sprawdź to na samym początku, zanim cokolwiek obiecasz.

1. Sprawdź Pythona: `python --version`. Na Windows uwaga na `python3`, które często jest tylko skrótem do Microsoft Store i nic nie robi. Jeśli Pythona nie ma, zaproponuj instalację:
   - Windows: `winget install -e --id Python.Python.3.12`
   - Mac: `brew install python` albo instalator z python.org
2. Uruchom: `python SKRYPT check --folder "<folder docelowy, jeśli już znany>"`. Skrypt sprawdza ffmpeg i ffprobe, potrzebne filtry, czcionkę do znaczników czasu i wolne miejsce. Przy braku podaje polecenie instalacji:
   - Windows: `winget install -e --id Gyan.FFmpeg` (po instalacji trzeba zamknąć i otworzyć aplikację, żeby system zobaczył ffmpeg)
   - Mac: `brew install ffmpeg`

Instalacja to pobieranie programu na komputer użytkowniczki, więc najpierw zapytaj ją wprost i poczekaj na wyraźne „tak”. Możesz też dać jej polecenie do samodzielnego uruchomienia. Jeśli `check` kończy się „wszystko gotowe”, nie opisuj szczegółów, tylko przejdź dalej.

## Krok 1. Ustalenia

Ustal (zapytaj tylko o to, czego nie wiesz z rozmowy):
- **Który plik** jest źródłem. Jeśli użytkowniczka nie zna ścieżki, poszukaj największych plików wideo w typowych miejscach (Pulpit, Pobrane, Wideo, folder z telefonu).
- **Folder docelowy** na gotowe b-rolle. Musi to być zwykły folder na dysku, np. `C:\Brolle` albo `~/Movies/Brolle`. Odradzaj folder synchronizowany z chmurą (OneDrive, iCloud, Dropbox), bo wysyłanie plików potrafi spowalniać komputer.
- **Wytyczne**, jeśli ma: jakie ujęcia (twarz, dłonie, ruch, detale stylizacji, śmiech), jak długie, ile sztuk. Jeśli nie ma, przyjmij: 15–25 propozycji po 3–8 sekund i powiedz o tym.

**Folder roboczy** (arkusze, podglądy, strona przeglądowa) załóż obok folderu docelowego, np. `C:\Brolle_przeglad`. Nie trzymaj go w folderze roboczym sesji ani w `AppData`: przeglądarka nie ma tam dostępu i strona się nie otworzy („Nie udało się uzyskać dostępu do pliku”).

## Krok 2. Parametry nagrania

`python SKRYPT info "<plik>"`

Zwróć uwagę na:
- **tylko_w_chmurze: true**: plik jest tylko w OneDrive lub podobnej usłudze, a odczyt wymusi pobranie całości (często kilkanaście GB). Zapytaj, zanim zaczniesz.
- **orientacja**: pionowa daje b-rolle 1080×1920, pozioma 1920×1080. Skrypt dobiera to sam.
- **dlugosc_s**: przy nagraniu dłuższym niż ok. 40 minut ustaw w kroku 3 `--co 3` albo `--co 4`, żeby arkuszy nie było za dużo.

Krótko powiedz użytkowniczce, co to za materiał (np. „24 minuty, pionowe, bardzo wysoka rozdzielczość”).

## Krok 3. Arkusze klatek

`python SKRYPT arkusze "<plik>" "<folder roboczy>/arkusze" --co 2` (w tle, przy dużych plikach to kilka minut)

Powstają obrazy z siatką miniatur (domyślnie klatka co 2 s), każda z czasem w rogu. Jeśli w `check` brakowało czcionki, czasu nie ma na miniaturach. Wtedy licz go z pozycji: arkusz N, kafelek K (od 0, wierszami) to `((N-1)*na_arkusz + K) * co` sekund.

## Krok 4. Przegląd i wybór kandydatów

Obejrzyj **wszystkie** arkusze, nie tylko początek. Najlepsze momenty bywają w środku i na końcu, a pominięcie części nagrania to najczęstszy powód, dla którego propozycje są słabsze, niż mogłyby być.

Co jest dobrym b-rollem:
- czysty kadr z główną osobą, bez osób trzecich (fotografa, asystentki, ręki z aparatem);
- moment z życiem: śmiech, ruch włosów, krok, gest, zmiana pozy, detal (dłonie, buty, faktura ubrania);
- stabilne ujęcie: kilka sekund bez szarpania kamery;
- ujęcia, które dają miejsce na tekst (dużo tła nad głową).

Czego unikać albo co oznaczać w opisie:
- puste kadry, osoba wychodząca z kadru, ktoś przechodzący przed obiektywem;
- **błysk lampy studyjnej**: pojedyncza, prawie biała klatka; nie zaczynaj ani nie kończ fragmentu w takim miejscu;
- elementy, które mogą przeszkadzać: statyw lub podstawa lampy w rogu, napis lub logo studia (np. na lustrze), kable na podłodze;
- ujęcia bardziej intymne (bielizna, odsłonięte ciało): nie pomijaj ich z góry, tylko rzeczowo zaznacz to w opisie i zostaw decyzję użytkowniczce.

**Grupy** służą tylko do tego, żeby użytkowniczce łatwiej było przeglądać propozycje (strona pokazuje je jako filtry). Dobierz podział do konkretnego materiału, wybierając to, czym propozycje najwyraźniej się od siebie różnią:
- miejsce, tło lub scena (np. „Przy oknie”, „Jasne tło”, „Na zewnątrz”);
- strój lub stylizacja, jeśli w nagraniu jest ich kilka;
- rodzaj kadru (np. „Cała sylwetka”, „Półpostać”, „Zbliżenia i detale”);
- rodzaj ujęcia (np. „Ruch”, „Statyczne pozy”, „Emocje i śmiech”);
- etap nagrania (np. „Początek”, „Środek”, „Koniec”), gdy nic innego nie dzieli materiału sensownie.

Przy jednym miejscu i jednej stylizacji grupuj według kadru albo rodzaju ujęcia. Jeśli żaden podział nie pomaga (np. 8 podobnych propozycji), pomiń grupy: zostaw puste `"grupy": {}` i nie wpisuj pola `grupa`, a strona nie pokaże filtrów. Zwykle wystarczą 2–5 grup. Nazywaj je tak, żeby użytkowniczka od razu wiedziała, co w nich jest.

Zapisz kandydatów w `<folder roboczy>/fragmenty.json`:

```json
{
  "tytul": "Przegląd b-rolli",
  "opis_nagrania": "Nagranie 24 min, pionowe.",
  "zapas": 1.5,
  "grupy": {"A": "Cała sylwetka", "B": "Zbliżenia i detale", "C": "Ruch"},
  "fragmenty": [
    {"id": 1, "start": 20, "koniec": 26, "grupa": "A", "tytul": "Ręce na biodrach", "opis": "Pełna postać, lekki uśmiech. W lewym dolnym rogu widać podstawę lampy."}
  ]
}
```

Czasy podawaj w sekundach od początku nagrania. Opis ma być krótki i konkretny: co widać, do czego się nada, co ewentualnie przeszkadza.

## Krok 5. Podglądy i strona przeglądowa

1. `python SKRYPT podglady "<plik>" "<folder roboczy>/fragmenty.json" "<folder roboczy>"` (w tle). Każdy podgląd ma zapas (domyślnie 1,5 s) z przodu i z tyłu, żeby było widać, co dzieje się tuż przed i po.
2. `python SKRYPT strona "<folder roboczy>/fragmenty.json" "<folder roboczy>" --otworz`

Strona otwiera się w domyślnej przeglądarce. Ma odtwarzacz po lewej i opis po prawej, filtry grup, plakietkę „zapas”/„fragment”, pole „Biorę”, miejsce na uwagi i przycisk „Kopiuj mój wybór”. Wybór zapisuje się w przeglądarce, więc użytkowniczka może zrobić przerwę.

Powiedz jej krótko, jak z niej korzystać, ile jest propozycji w każdej grupie i co warto sprawdzić (np. „w #6 widać napis studia”). Jeśli strona się nie otwiera, prawie zawsze winne jest miejsce folderu (patrz krok 1).

## Krok 6. Odczytanie wyboru

Użytkowniczka wkleja tekst w formie `#3 01:12–01:20 Tytuł | uwagi: ...`. Uwagi dotyczące sekund odnoszą się do **odtwarzacza podglądu**, bo to on był przed jej oczami. Przeliczaj tak:

- czas w oryginale = `(start − zapas) + sekunda z odtwarzacza`
- „wytnij zapas” albo brak uwag: `start` do `koniec`
- „zostaw zapas z przodu”: `start − zapas` do `koniec`
- „zostaw zapas z tyłu” albo „na końcu”: koniec przesuwa się na `koniec + zapas`
- „zacznij od X sekundy”: start = `(start − zapas) + X`; koniec bez zmian, chyba że dopisała coś o końcu
- „skróć do X sekundy”: koniec = `(start − zapas) + X`

Pokaż tabelę: numer, nazwa, czas w oryginale (z dziesiątymi sekundy), długość, a przy nietypowych uwagach krótką adnotację, jak je zrozumiałaś. Jeśli jakaś uwaga da się odczytać na dwa sposoby, napisz wprost, jak ją rozumiesz, i zapytaj o ten jeden fragment. Resztę możesz w tym czasie wyciąć.

Zapisz listę cięć w `<folder roboczy>/ciecia.json`:

```json
[
  {"id": 1, "start": 20.0, "koniec": 26.0, "nazwa": "rece_na_biodrach"},
  {"id": 4, "start": 110.5, "koniec": 118.0, "nazwa": "dlon_na_biodrze"}
]
```

`nazwa` pisz małymi literami, bez polskich znaków i spacji, żeby pliki dobrze działały w każdym programie.

## Krok 7. Cięcie i weryfikacja

`python SKRYPT tnij "<plik>" "<folder roboczy>/ciecia.json" "<folder docelowy>" --robocze "<folder roboczy>"` (w tle)

Skrypt wycina każdy fragment co do klatki w 1080p (H.264, wysoka jakość), sprawdza długość i liczbę klatek każdego pliku i robi arkusz pierwszych klatek `pierwsze_klatki.jpg`.

Potem:
1. Przeczytaj wynik. Przy „PROBLEM” uruchom cięcie tego fragmentu jeszcze raz, a jeśli dalej źle, powiedz o tym otwarcie.
2. **Obejrzyj** `pierwsze_klatki.jpg` i wymień rzeczy widoczne w kadrze, które mogą przeszkadzać (fragment fotografa, lampa, czubek buta przy krawędzi). Zaproponuj poprawkę: przesunięcie startu o ułamek sekundy albo przycięcie kadru w programie do montażu.
3. Podsumuj: ile plików, gdzie leżą, ile ważą razem.

Rób tylko wersję 1080p. Wyższa rozdzielczość jest niepotrzebna na Instagramie, a ponowne kodowanie np. 8K trwa bardzo długo i przy szybkich ustawieniach wychodzi słabiej niż oryginał. Jeśli użytkowniczka wprost poprosi o wyższą rozdzielczość, użyj `--krotszy-bok 2160` (4K) i uprzedź, że potrwa to dłużej.

Na tym skill się kończy. Nie usuwaj ani nie przenoś oryginału ani folderu roboczego z własnej inicjatywy. Folder roboczy zostaje na dysku, żeby można było wrócić do podglądów i dociąć coś jeszcze. Co z nim zrobić, decyduje użytkowniczka osobno.

## Pułapki (skąd wzięły się te zasady)

- **Dekoder sprzętowy (`-hwaccel`) przy dużych plikach HEVC potrafi przerwać pracę w połowie** i zostawić ucięty plik bez błędu w kodzie wyjścia. Dlatego skrypt dekoduje programowo i liczy klatki w każdym pliku.
- **Cięcie bez ponownego kodowania (`-c copy`)** trafia tylko w klatki kluczowe, czyli zwykle co ok. 1 s. Za mało, gdy trzeba ominąć np. fotografa w kadrze. Dlatego tniemy z kodowaniem.
- **Strona w folderze `AppData` lub w folderze sesji się nie otworzy**, bo przeglądarka nie ma tam dostępu.
- **Arkusze z dekodowaniem tylko klatek kluczowych** są szybkie, ale działają tylko wtedy, gdy klatki kluczowe występują co najwyżej co tyle sekund, co odstęp arkusza. Skrypt sprawdza to sam i w razie potrzeby dekoduje całość (wolniej).
