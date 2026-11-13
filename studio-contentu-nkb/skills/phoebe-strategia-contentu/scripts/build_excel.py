#!/usr/bin/env python3
"""
Buduje sformatowany plik Excel z planem contentu na social media.

Tworzy trzy arkusze:
  1. Kalendarz publikacji: Dzień/Data, Platforma, Format, Filar, Temat, Hook, CTA, Status
  2. Banka tematów: Filar, Temat/Tytuł, Obiekcja, Format, Platforma
  3. Mechaniki: Typ, Narzędzie, Przykładowe pytanie, Częstotliwość

Użycie:
    python build_excel.py dane.json plan-contentu-marka.xlsx

Format pliku JSON (wszystkie sekcje opcjonalne, pomijane arkusze nie powstają):
{
  "marka": "Nazwa marki",
  "kalendarz": [
    {"dzien": "Poniedziałek", "platforma": "Instagram", "format": "Rolka",
     "filar": "Edukacja", "temat": "3 błędy w X", "hook": "Większość robi to źle...",
     "cta": "Zapisz post", "status": ""}
  ],
  "banka_tematow": [
    {"filar": "Edukacja", "temat": "Jak zacząć X", "obiekcja": "Nie dam rady",
     "format": "Karuzela", "platforma": "Instagram"}
  ],
  "mechaniki": [
    {"typ": "Stories", "narzedzie": "Ankieta tak/nie",
     "pytanie": "Czy zdarza Ci się X?", "czestotliwosc": "2x w tygodniu"}
  ]
}

Jeśli openpyxl nie jest zainstalowany:
    pip install openpyxl --break-system-packages
"""

import json
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HEADER_FILL = PatternFill(start_color="6C4F8C", end_color="6C4F8C", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=14, color="3D2A5C")
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center")
THIN = Side(style="thin", color="D9D2E9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def style_header(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.border = BORDER


def autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def add_sheet(wb, title, headers, rows, keys, widths):
    ws = wb.create_sheet(title=title)
    ws.cell(row=1, column=1, value=title).font = TITLE_FONT
    header_row = 3
    for i, h in enumerate(headers, start=1):
        ws.cell(row=header_row, column=i, value=h)
    style_header(ws, header_row, len(headers))
    r = header_row + 1
    for item in rows:
        for i, k in enumerate(keys, start=1):
            cell = ws.cell(row=r, column=i, value=item.get(k, ""))
            cell.alignment = WRAP
            cell.border = BORDER
        r += 1
    autosize(ws, widths)
    ws.freeze_panes = ws.cell(row=header_row + 1, column=1)
    last_col = get_column_letter(len(headers))
    ws.auto_filter.ref = f"A{header_row}:{last_col}{max(r - 1, header_row)}"
    return ws


def main():
    if len(sys.argv) < 3:
        print("Użycie: python build_excel.py dane.json wyjscie.xlsx")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)

    wb = Workbook()
    wb.remove(wb.active)

    if data.get("kalendarz"):
        add_sheet(
            wb, "Kalendarz publikacji",
            ["Dzień / Data", "Platforma", "Format", "Filar", "Temat", "Hook", "CTA", "Status"],
            data["kalendarz"],
            ["dzien", "platforma", "format", "filar", "temat", "hook", "cta", "status"],
            [16, 14, 14, 18, 34, 34, 24, 12],
        )

    if data.get("banka_tematow"):
        add_sheet(
            wb, "Banka tematów",
            ["Filar", "Temat / Tytuł", "Obiekcja którą rozbraja", "Format", "Platforma"],
            data["banka_tematow"],
            ["filar", "temat", "obiekcja", "format", "platforma"],
            [18, 40, 32, 14, 14],
        )

    if data.get("mechaniki"):
        add_sheet(
            wb, "Mechaniki angażowania",
            ["Typ", "Narzędzie", "Przykładowe pytanie", "Częstotliwość"],
            data["mechaniki"],
            ["typ", "narzedzie", "pytanie", "czestotliwosc"],
            [18, 24, 44, 18],
        )

    if not wb.sheetnames:
        wb.create_sheet("Plan")  # nie zostawiaj pustego skoroszytu

    wb.save(sys.argv[2])
    print(f"Zapisano: {sys.argv[2]}")


if __name__ == "__main__":
    main()
