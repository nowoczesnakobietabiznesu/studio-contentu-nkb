#!/usr/bin/env bash
# Studio Contentu NKB: sprawdzanie i instalacja aktualizacji.
#
# Użycie:
#   bash sprawdz.sh            sprawdź (najwyżej raz dziennie; w pozostałe razy od razu kończy)
#   bash sprawdz.sh --teraz    sprawdź od razu, bez limitu raz dziennie
#   bash sprawdz.sh --instaluj zainstaluj najnowszą wersję (klientka powiedziała "tak")
#
# Linie wyniku (czyta je Claude):
#   STATUS aktualizacja BRAK <wersja>
#   STATUS aktualizacja DOSTEPNA <stara> -> <nowa> | <co nowego>
#   STATUS aktualizacja ZAINSTALOWANA <stara> -> <nowa> | <co nowego>
#   STATUS aktualizacja POMINIETA <powód>
#   STATUS aktualizacja RECZNIE <kroki>
#   STATUS wersja <wersja>

REPO_RAW="${NKB_REPO_RAW:-https://raw.githubusercontent.com/nowoczesnakobietabiznesu/studio-contentu-nkb/main}"  # zmienna tylko do testów
PLUGIN="studio-contentu-nkb"
MARKET="nkb-klub"

TU="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$TU/../../.." && pwd)"           # folder pluginu (tam jest .claude-plugin/plugin.json)
STAN="${HOME}/.nkb-studio"
mkdir -p "$STAN" 2>/dev/null

wersja_z() { grep -m1 '"version"' | sed -E 's/.*"version"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/'; }
nowsza() { [ "$1" != "$2" ] && [ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | tail -n1)" = "$2" ]; }  # czy $2 > $1

MOJA="$(wersja_z < "$ROOT/.claude-plugin/plugin.json" 2>/dev/null)"
[ -z "$MOJA" ] && { echo "STATUS aktualizacja POMINIETA nie znam wersji tej kopii"; exit 0; }
echo "STATUS wersja $MOJA"

# Informacja o licencji: raz na komputer, przy pierwszym użyciu Studia (i ponownie, gdy zmieni się wersja licencji).
LICENCJA_WERSJA="1"
if [ "$(cat "$STAN/licencja-pokazana" 2>/dev/null)" != "$LICENCJA_WERSJA" ]; then
  echo "STATUS licencja POKAZ | Korzystasz ze Studia Contentu NKB, stworzonego przez Elę Popardowską i Gosię Galbas w ramach Nowoczesnej Kobiety Biznesu. Treści, które tu stworzysz, są Twoje. Kopiowanie, udostępnianie i odsprzedaż Studia lub jego części bez naszej pisemnej zgody są zabronione. Korzystając ze Studia, akceptujesz licencję: https://github.com/nowoczesnakobietabiznesu/studio-contentu-nkb/blob/main/LICENSE.md"
  echo "$LICENCJA_WERSJA" > "$STAN/licencja-pokazana" 2>/dev/null
fi

TRYB="${1:-}"
DZIS="$(date +%F)"
if [ -z "$TRYB" ] && [ "$(cat "$STAN/ostatnie-sprawdzenie" 2>/dev/null)" = "$DZIS" ]; then
  echo "STATUS aktualizacja POMINIETA dzisiaj już sprawdzone"; exit 0
fi

NAJNOWSZA="$(curl -fsSL --max-time 8 "$REPO_RAW/$PLUGIN/.claude-plugin/plugin.json" 2>/dev/null | wersja_z)"
if [ -z "$NAJNOWSZA" ]; then
  echo "STATUS aktualizacja POMINIETA brak internetu albo GitHub nie odpowiada"; exit 0
fi
echo "$DZIS" > "$STAN/ostatnie-sprawdzenie" 2>/dev/null

co_nowego() {
  curl -fsSL --max-time 8 "$REPO_RAW/whats-new.json" 2>/dev/null \
    | grep -m1 "\"$1\"" | sed -E 's/^[[:space:]]*"[^"]+"[[:space:]]*:[[:space:]]*"(.*)",?[[:space:]]*$/\1/'
}

if ! nowsza "$MOJA" "$NAJNOWSZA"; then
  echo "STATUS aktualizacja BRAK $MOJA"; exit 0
fi

if [ "$TRYB" != "--instaluj" ]; then
  echo "STATUS aktualizacja DOSTEPNA $MOJA -> $NAJNOWSZA | $(co_nowego "$NAJNOWSZA")"; exit 0
fi

RECZNIE="W aplikacji Claude: + przy polu wiadomości -> Plugins -> Manage plugins -> nkb-klub -> Update. Albo w PowerShell/Terminalu, każda linia osobno: claude plugin marketplace update $MARKET   oraz   claude plugin update $PLUGIN@$MARKET"

CLAUDE_BIN=""
for k in "${CLAUDE_CODE_EXECPATH:-}" "$(command -v claude 2>/dev/null)" "$HOME/.local/bin/claude" "$HOME/.local/bin/claude.exe" "$HOME/.claude/local/claude"; do
  [ -n "$k" ] && [ -x "$k" ] && { CLAUDE_BIN="$k"; break; }
done
[ -z "$CLAUDE_BIN" ] && { echo "STATUS aktualizacja RECZNIE $RECZNIE"; exit 0; }

if "$CLAUDE_BIN" plugin marketplace update "$MARKET" >"$STAN/ostatnia-aktualizacja.log" 2>&1 \
   && "$CLAUDE_BIN" plugin update "$PLUGIN@$MARKET" >>"$STAN/ostatnia-aktualizacja.log" 2>&1; then
  echo "STATUS aktualizacja ZAINSTALOWANA $MOJA -> $NAJNOWSZA | $(co_nowego "$NAJNOWSZA")"
else
  echo "STATUS aktualizacja RECZNIE $RECZNIE   (szczegóły: $STAN/ostatnia-aktualizacja.log)"
fi
