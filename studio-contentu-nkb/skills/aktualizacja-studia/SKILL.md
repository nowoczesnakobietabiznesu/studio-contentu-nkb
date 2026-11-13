---
name: aktualizacja-studia
description: >
  Aktualizacje Studia Contentu NKB. Sprawdza, czy na GitHubie jest nowsza wersja pluginu, mówi klientce
  co nowego i po jej zgodzie instaluje aktualizację. Pozostałe skille Studia uruchamiają to sprawdzenie
  same, raz dziennie. Używaj, gdy ktoś mówi: "zaktualizuj studio", "aktualizacja studia", "czy jest nowa
  wersja", "jaką mam wersję studia", "co nowego w studiu", albo wpisuje /aktualizacja-studia.
---

# Aktualizacja Studia Contentu NKB

Mówisz do klientki po polsku, prosto, bez technicznego żargonu. Nie pokazuj jej komend ani linii STATUS.

## Sprawdzenie (na starcie każdego skilla Studia)

Uruchom w Bashu, podając pełną ścieżkę do skryptu z folderu tego skilla:

```bash
bash "<folder tego skilla>/scripts/sprawdz.sh"
```

Skrypt sam pilnuje, żeby pytać najwyżej raz dziennie. Gdy klientka sama prosi o sprawdzenie, dodaj `--teraz`.

Co zrobić z wynikiem:

- `STATUS licencja POKAZ | tekst`: to pierwsze użycie Studia na tym komputerze. Rób swoje zadanie normalnie, a na samym
  końcu swojej najbliższej odpowiedzi dopisz, po linii odstępu, **dokładnie ten tekst, słowo w słowo**, kursywą, z linkiem.
  Nie skracaj go, nie parafrazuj i nie komentuj. Pokazujesz go tylko ten jeden raz (skrypt sam pilnuje, żeby się nie powtarzał).
- `BRAK` albo `POMINIETA`: nic nie mów (chyba że klientka pytała, wtedy: „Masz najnowszą wersję, X.Y.Z.”) i wracaj do zadania.
- `DOSTEPNA stara -> nowa | opis`: zanim zaczniesz właściwe zadanie, zapytaj jednym zdaniem:
  „Jest nowa wersja Studia Contentu (nowa): *opis*. Zainstalować? To zajmie chwilę.”
  - **Tak**: uruchom `bash "<folder tego skilla>/scripts/sprawdz.sh" --instaluj`.
  - **Nie**: wracaj do zadania i nie pytaj ponownie w tej rozmowie.
- `ZAINSTALOWANA`: powiedz „Gotowe, masz wersję X.Y.Z. Otwórz nową rozmowę, żeby Claude wczytał nową wersję.” i zakończ. W nowej rozmowie klientka wraca do tego, co robiła.
- `RECZNIE kroki`: automat się nie udał. Przekaż klientce kroki prostymi słowami, krok po kroku. Jeśli i to nie pomoże, zaproponuj zgłoszenie problemu (skill **zglos-problem**).

Jeśli nie możesz uruchomić Basha (np. środowisko go nie ma), pomiń sprawdzenie bez komentarza i rób swoje.
