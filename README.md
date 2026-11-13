# Klub NKB – narzędzia Claude

Pluginy do Claude dla członkiń Klubu Nowoczesna Kobieta Biznesu.

## Studio Contentu NKB

Twój zespół od treści na Instagram, po polsku i w Twoim głosie:

| Ekspertka | Co robi | Jak zacząć |
|---|---|---|
| **Phoebe** | strategia contentu i plan publikacji | „Phoebe, zrób mi strategię contentu” |
| **Veronica** | pomysły na treści z palącego problemu odbiorczyń | „pomysły na posty” |
| **Ashley** | 30 pomysłów na edukacyjne rolki | „pomysły na rolki” |
| **Zoe** | hooki, czyli pierwsze linijki, które zatrzymują scroll | „daj 5 hooków na rolkę o…” |
| **Dorothy** | skrypty do rolek | „napisz skrypt do rolki o…” |
| **Emily** | podpisy pod posty na Instagram | „napisz podpis pod post o…” |
| **Karuzele** | karuzele w Twoim brandingu: edukacyjne, z newsem, POV, storytelling, historie klientek i sprzedażowe, z 5 hookami na okładkę i slajdami wideo | „zrób karuzelę o…” |
| **Montaż rolek** | z surowych nagrań 9:16 robi gotową rolkę w Twoim stylu: najlepsze ujęcia, cięcie pauz, napisy, efekty, czysty dźwięk i wersje do trial reels | „zmontuj rolkę z nagrań w Pobranych” |
| **B-rolle z nagrania** | wycina z długiego nagrania krótkie, wizualne ujęcia na przebitki i rolki z napisami (nie do nagrań mówionych) | „wytnij b-rolle z tego nagrania” |

## Instalacja w aplikacji Claude

1. Otwórz aplikację Claude na komputerze i przejdź do zakładki **Code**.
2. Kliknij **+** obok pola wiadomości, potem **Plugins**, potem **Browse plugins**.
3. Kliknij **Add** w prawym górnym rogu, potem **Add marketplace**, potem **Add from a repository**.
4. Wklej ten link i kliknij **Sync**:

```
https://github.com/nowoczesnakobietabiznesu/studio-contentu-nkb
```

5. Zainstaluj **Studio Contentu NKB** z listy.
6. Otwórz nową rozmowę i napisz na przykład: `pomysły na rolki`.

## Instalacja z terminala

Tylko jeśli używasz Claude Code w Terminalu (Mac) albo w PowerShell (Windows). Wpisz to sama, nie w rozmowie z Claude. Każda linia osobno:

```bash
claude plugin marketplace add nowoczesnakobietabiznesu/studio-contentu-nkb
```

```bash
claude plugin install studio-contentu-nkb@nkb-klub
```

Na Windowsie najpierw zainstaluj [Git for Windows](https://git-scm.com/downloads).

## Masz już skill video-edit?

Jeśli wcześniej montowałaś rolki ze skillem **video-edit**, nie musisz zaczynać od zera. Przy pierwszym montażu
w Studiu Claude zapyta, czy przenieść Twój dopracowany styl z video-edit, i zrobi to za Ciebie.

Gdy pierwsza rolka w przeniesionym stylu będzie gotowa, Claude zaproponuje wyłączenie video-edit, żeby przy
montażu nie wybierał starego skilla zamiast Studia. Niczego nie usuwa: przenosi go tylko do folderu
`skills-wylaczone`, skąd w każdej chwili możesz go przywrócić.

## Aktualizacje

Poprawki i nowości przychodzą jako aktualizacje. Raz dziennie Claude sam sprawdza, czy jest nowa wersja, i pyta, czy ją zainstalować. Wystarczy odpowiedzieć „tak”, a potem otworzyć nową rozmowę.

Możesz też w każdej chwili napisać:

```
zaktualizuj studio
```

## Coś nie działa?

Napisz w rozmowie z Claude:

```
zgłoś problem
```

Claude zbierze informacje potrzebne do naprawy, pokaże Ci całe zgłoszenie i dopiero po Twojej zgodzie otworzy formularz. Nie wysyła niczego bez Twojej wiedzy.

---

© Nowoczesna Kobieta Biznesu. Autorki: Ela Popardowska i Gosia Galbas. Wyłącznie dla osób z wykupionym dostępem do Klubu NKB lub produktu Studio Contentu NKB, na warunkach [licencji](LICENSE.md) i zakupu. To, że pliki są publicznie widoczne, nie daje prawa do korzystania z nich. Kopiowanie, udostępnianie i odsprzedaż bez naszej pisemnej zgody są zabronione. Projekt niezależny, niezwiązany z Anthropic ani z Instagramem.
