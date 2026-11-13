---
name: zglos-problem
description: >
  Zgłaszanie problemów technicznych ze Studiem Contentu NKB do zespołu NKB. Zbiera to, co potrzebne do
  naprawy (wersja Studia, system, który skill, co się stało, treść błędu), pokazuje klientce całe zgłoszenie
  i dopiero po jej zgodzie otwiera formularz zgłoszeń. Używaj, gdy ktoś mówi: "zgłoś problem", "zgłoś błąd",
  "coś nie działa", "studio się wywala", "mam błąd", "wyślij zgłoszenie do NKB", "jak zgłosić problem",
  albo wpisuje /zglos-problem. Używaj też, gdy inny skill Studia trafił na błąd techniczny i klientka
  zgodziła się go zgłosić.
---

# Zgłoś problem – Studio Contentu NKB

Mówisz po polsku, ciepło i prosto. Klientka nie musi znać się na technice.

## Adresy zgłoszeń

- Formularz kontaktowy Klubu: `https://klub.nowoczesnakobietabiznesu.com/next/public/catalog/contact`
- E-mail: `info@nowoczesnakobietabiznesu.com`

## Krok 1. Zbierz informacje

Z tej rozmowy (bez dopytywania o to, co już wiesz):
- **Skill**: którego skilla Studia dotyczy problem (np. Emily, Phoebe).
- **Co robiła**: jednym-dwoma zdaniami, co klientka chciała zrobić.
- **Co się stało**: co poszło nie tak, z jej perspektywy.
- **Treść błędu**: dokładny komunikat błędu, jeśli był (najwyżej kilka linijek, bez ścieżek z nazwą użytkownika: zamień je na `~`).

Technicznie (uruchom w Bashu, jeśli możesz):
```bash
bash "<folder skilla aktualizacja-studia>/scripts/sprawdz.sh" --teraz | grep "STATUS wersja"; uname -s 2>/dev/null || echo Windows
```
To da **wersję Studia** i **system** (Windows / Darwin = Mac / Linux). Do tego **gdzie pracuje**: aplikacja Claude (Code albo Cowork) czy terminal, jeśli to wiesz.

Jeśli czegoś brakuje, zadaj **jedno** zbiorcze pytanie. Nie wypytuj w kółko.

## Krok 2. Pokaż zgłoszenie i zapytaj o zgodę

**Nigdy nie wysyłaj ani nie otwieraj niczego bez zgody.** Pokaż całe zgłoszenie tak, jak trafi do zespołu:

```
Studio Contentu NKB – zgłoszenie
Wersja: 1.0.0 | System: Windows | Gdzie: Claude, zakładka Code
Skill: Emily
Co robiłam: ...
Co się stało: ...
Treść błędu: ...
```

Zasady treści:
- **Bez danych osobowych i poufnych**: żadnych haseł, kluczy, danych klientów klientki, treści jej postów czy ofert. Tylko to, co potrzebne do naprawy.
- Klientka może dopisać lub usunąć, co chce.

Zapytaj: „Tak wygląda zgłoszenie. Wysłać je do zespołu NKB?”

## Krok 3. Wyślij (po zgodzie)

1. Skopiuj zgłoszenie do schowka:
   - Windows: zapisz tekst do pliku tymczasowego i `clip.exe < plik` (albo `Set-Clipboard` w PowerShell),
   - Mac: `pbcopy`, Linux: `xclip -selection clipboard` jeśli jest.
2. Otwórz formularz kontaktowy Klubu w przeglądarce (sam link, bez dopisywania czegokolwiek do adresu):
   `https://klub.nowoczesnakobietabiznesu.com/next/public/catalog/contact`
   - Windows: `start "" "<link>"` (cmd) albo `Start-Process "<link>"` (PowerShell), Mac: `open "<link>"`, Linux: `xdg-open "<link>"`.
3. Powiedz klientce: „Formularz kontaktowy Klubu jest otwarty w przeglądarce, a zgłoszenie masz w schowku. Wklej je w pole na treść wiadomości (Ctrl+V, na Macu Cmd+V), uzupełnij swoje dane kontaktowe i wyślij.”

Jeśli nie da się otworzyć przeglądarki albo skopiować: podaj link i zgłoszenie w bloku tekstu do ręcznego skopiowania. Jeśli formularz nie działa: niech wyśle zgłoszenie mailem na info@nowoczesnakobietabiznesu.com.

## Krok 4. Wróć do pracy

Jeśli da się obejść problem (np. zrobić tę samą rzecz inaczej), zaproponuj obejście. Nie obiecuj terminu naprawy. Powiedz tylko, że poprawka przyjdzie jako aktualizacja Studia i Claude sam zapyta, czy ją zainstalować.
