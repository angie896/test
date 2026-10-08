#!/usr/bin/env python3
"""
build_breakdown.py — JSON de desglose de arte → Excel con el formato de Angie.

Uso:
    python build_breakdown.py desglose.json salida.xlsx [--tracking] [--no-scenes]

--tracking   agrega columnas LEVEL / STATUS / ASSIGNMENT con menús desplegables
             (lo útil de la versión 2 del desglose).
--no-scenes  oculta la columna ESC. (números de escena).

Esquema del JSON: ver references/esquema_json.md
"""
import json
import sys
from collections import OrderedDict

from openpyxl import Workbook
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

# ---------------------------------------------------------------- estilo
MONO = "Courier New"
HEADER_FILL = PatternFill("solid", fgColor="3F3F3F")
BAND_FILLS = [PatternFill("solid", fgColor="D9D9D9"), PatternFill("solid", fgColor="F2F2F2")]
FINAL_FILL = PatternFill("solid", fgColor="F7F7F7")
THIN = Side(style="thin", color="7F7F7F")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
FLAG_COLOR = "C55A11"  # naranja: lo que Angie tiene que definir / verificar
ROW_HEIGHT = 80        # alto para pegar imágenes de referencia

CATEGORY_ORDER = ["SETS", "CHARACTERS", "PROPS", "GRAPHIC DESIGN",
                  "VEHICLES", "MAKEUP / SFX", "VFX"]
LEVELS = ["Easy", "Medium", "Hard"]
STATUSES = ["TO DO", "IN PROGRESS", "REVIEW", "DONE", "APPROVED"]


def columns(tracking, scenes):
    cols = [("CATEGORY", 16), ("☐", 5)]
    if scenes:
        cols.append(("ESC.", 9))
    cols += [("ITEM", 30), ("DESCRIPTION", 72), ("REFERENCE", 26), ("FINAL", 26)]
    if tracking:
        cols += [("LEVEL", 11), ("STATUS", 14), ("ASSIGNMENT", 14)]
    return cols


def rich_description(text):
    """Las líneas que empiezan con ⚠ van en naranja para que no se escapen."""
    if not text:
        return None
    if "⚠" not in text:
        return text
    normal = InlineFont(rFont=MONO, sz=9)
    flag = InlineFont(rFont=MONO, sz=9, color=FLAG_COLOR, b=True)
    parts = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        chunk = line + ("\n" if i < len(lines) - 1 else "")
        parts.append(TextBlock(flag if line.lstrip().startswith("⚠") else normal, chunk))
    return CellRichText(*parts)


def row_height(text, chars_per_line=75, pt_per_line=11.5):
    """Alto mínimo para pegar imágenes; crece si la descripción es larga."""
    lines = sum(max(1, -(-len(l) // chars_per_line)) for l in (text or "").split("\n"))
    return max(ROW_HEIGHT, lines * pt_per_line + 12)


def group_items(items):
    groups = OrderedDict()
    order = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    for it in sorted(items, key=lambda x: order.get(x["category"].upper(), 99)):
        groups.setdefault(it["category"].upper(), []).append(it)
    return groups


def write_sheet(ws, title, items, tracking, scenes):
    cols = columns(tracking, scenes)
    ws.sheet_view.showGridLines = False
    idx = {name: i + 1 for i, (name, _) in enumerate(cols)}
    for i, (_, width) in enumerate(cols, start=1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = width

    # Fila 1: título fusionado hasta DESCRIPTION, luego encabezados.
    desc_col = idx["DESCRIPTION"]
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=desc_col)
    ws.cell(1, 1, title)
    for name, col in idx.items():
        if col > desc_col:
            ws.cell(1, col, name)
    for col in range(1, len(cols) + 1):
        c = ws.cell(1, col)
        c.fill, c.border, c.alignment = HEADER_FILL, BORDER, CENTER
        c.font = Font(name=MONO, bold=True, color="FFFFFF", size=10)
    ws.row_dimensions[1].height = 22
    ws.freeze_panes = "A2"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:1"

    row = 2
    for band, (category, its) in enumerate(group_items(items).items()):
        fill = BAND_FILLS[band % 2]
        start = row
        for it in its:
            ws.row_dimensions[row].height = row_height(it.get("description", ""))
            values = {
                "☐": "☐",
                "ESC.": it.get("scenes", ""),
                "ITEM": it["item"],
                "DESCRIPTION": rich_description(it.get("description", "")),
                "LEVEL": it.get("level"),
                "STATUS": it.get("status") or ("TO DO" if tracking else None),
                "ASSIGNMENT": it.get("assignment"),
            }
            for name, col in idx.items():
                c = ws.cell(row, col)
                if name in values and values[name] not in (None, ""):
                    c.value = values[name]
                c.border, c.alignment = BORDER, CENTER
                c.fill = FINAL_FILL if name == "FINAL" else fill
                c.font = Font(name=MONO, size=9)
            box = ws.cell(row, idx["☐"])
            box.font = Font(name="Arial", size=14, color="1F4E79")
            row += 1
        # Celda de categoría fusionada (bordes en cada celda subyacente).
        for r in range(start, row):
            c = ws.cell(r, 1)
            c.border, c.fill = BORDER, fill
        ws.merge_cells(start_row=start, start_column=1, end_row=row - 1, end_column=1)
        cat = ws.cell(start, 1, category)
        cat.font = Font(name=MONO, bold=True, size=9)
        cat.alignment = CENTER

    if tracking and row > 2:
        for name, options in (("LEVEL", LEVELS), ("STATUS", STATUSES)):
            dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"',
                                allow_blank=True)
            ws.add_data_validation(dv)
            letter = ws.cell(1, idx[name]).column_letter
            dv.add(f"{letter}2:{letter}{row - 1}")

    # Leyenda debajo de la tabla.
    legend = ws.cell(row + 1, 1, "⚠ naranja = continuidad no escrita en el guion o dato "
                                 "inferido: definir o verificar. REFERENCE y FINAL se "
                                 "llenan a mano.")
    legend.font = Font(name=MONO, size=8, italic=True, color=FLAG_COLOR)


def sets_master(wb, sheets, tracking):
    """Para series o películas con varias unidades: todas las locaciones en un solo lugar."""
    merged = OrderedDict()
    for sh in sheets:
        for it in sh["items"]:
            if it["category"].upper() != "SETS":
                continue
            key = it["item"].strip().lower()
            entry = merged.setdefault(key, {"category": "SETS", "item": it["item"],
                                            "scenes": [], "description": []})
            entry["scenes"].append(f'{sh["name"]}: {it.get("scenes", "")}'.strip(": "))
            if it.get("description"):
                entry["description"].append(f'[{sh["name"]}] {it["description"]}')
    items = [{**e, "scenes": "\n".join(e["scenes"]),
              "description": "\n".join(e["description"])} for e in merged.values()]
    write_sheet(wb.create_sheet("SETS MASTER", 0), "SETS MASTER — todas las locaciones",
                items, tracking, scenes=True)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) != 2:
        sys.exit(__doc__)
    src, out = args
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    opts = data.get("options", {})
    tracking = "--tracking" in flags or opts.get("tracking", False)
    scenes = "--no-scenes" not in flags and opts.get("scenes", True)

    wb = Workbook()
    wb.remove(wb.active)
    sheets = data["sheets"]
    for sh in sheets:
        ws = wb.create_sheet(sh["name"][:31])
        write_sheet(ws, sh.get("title", f'BREAKDOWN {sh["name"]}'), sh["items"],
                    tracking, scenes)
    if len(sheets) > 1:
        sets_master(wb, sheets, tracking)
    wb.save(out)
    n = sum(len(s["items"]) for s in sheets)
    print(f"OK → {out}  ({len(sheets)} hoja(s), {n} ítems, tracking={tracking})")


if __name__ == "__main__":
    main()
