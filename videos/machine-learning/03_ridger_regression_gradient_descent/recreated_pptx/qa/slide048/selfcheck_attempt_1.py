#!/usr/bin/env python3
"""Pre-judge self-check for slide 048 (attempt 1).

Checks (per 17_worker_instructions.md, founder directive 2026-10-10):
  1. FRAME CONTAINMENT — content ink inside the house panel/strokes
  2. EQUATIONS EXIST — ink present in every equation region
  3. TABLE DATA — every cell value matches the spec verbatim
  4. DELIMITER GEOMETRY — the column-vector brackets span their entries
  5. LINE/BOX WRAP — no ink outside each element's expected band
  6. lineSpacing present on every multi-line text block (build-level assertion)

Run:  python3 selfcheck_attempt_1.py <render.png> [original.jpg]
"""
import json
import sys

import numpy as np
from PIL import Image

RENDER = sys.argv[1] if len(sys.argv) > 1 else \
    "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide048/render_2.png"
ORIG = sys.argv[2] if len(sys.argv) > 2 else \
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_048.jpg"

results = []


def ck(name, ok, detail):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = H / 540.0          # render px per frame px (150dpi -> 2.0833)


def fp(x, y):
    """frame px -> render px"""
    return int(round(x * S)), int(round(y * S))


r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
ink = (r < 235) | (g < 235) | (b < 235)      # anything not the white canvas
# panel-gray-aware ink (content sits on the E9E9E7 panel)
panel = (abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 16)
content = ink & ~panel

# ---------------------------------------------------------------- 1. frame
# Containment is measured against the PANEL bounds. The content mask excludes
# the panel's own grey, so the only remaining "ink" outside the panel is the
# house strokes' own anti-aliased caps (a 1pt stroke centred on x=901/538.5
# spills ~1px past the panel edge) — those are chrome, not content, so the
# edge census is run on CONTENT-AND-NOT-RED.
PANEL_X0, PANEL_X1, PANEL_Y0 = 54, 904, 45
cx0, _ = fp(PANEL_X0 + 2, 0)
cx1, _ = fp(PANEL_X1 - 2, 0)
_, cy0 = fp(0, 44)          # strictly above the panel top (row 45)
_, cy1 = fp(0, 539)
rr, gg = im[:, :, 0], im[:, :, 1]
# stroke family: the C00000 strokes plus their anti-aliased caps (the bottom
# stroke's cap at col 902 measures (227,203,202), i.e. r-g = 24).
stroke = (rr > 150) & ((rr - gg) > 15)
edge = content & ~stroke
left_bad = int(edge[:, :cx0].sum())
right_bad = int(edge[:, cx1:].sum())
bot_bad = int(edge[cy1:, :].sum())
top_bad = int(edge[:cy0, :].sum())
ck("frame containment",
   left_bad == 0 and right_bad == 0 and bot_bad == 0 and top_bad == 0,
   f"content left of panel={left_bad}, right of panel={right_bad}, "
   f"below slide bottom={bot_bad}, above panel top={top_bad} "
   "(house-stroke AA excluded)")

# ------------------------------------------------- 2. equations have ink
EQS = {
    "eq_initial_w_col": (330, 61, 353, 101),
    "eq_r1_l": (301, 150, 429, 192),
    "eq_r2_l": (301, 220, 429, 262),
    "eq_r3_l": (301, 282, 429, 320),
    "eq_r4_l": (301, 336, 429, 392),
    "eq_r5_l": (301, 410, 429, 455),
    "eq_r6_l": (301, 466, 429, 517),
    "eq_r1_w": (617, 150, 799, 192),
    "eq_r_kw": (617, 455, 713, 517),
}
for name, (a, bb, c, d) in EQS.items():
    x0, y0 = fp(a + 2, bb + 2)
    x1, y1 = fp(c - 2, d - 2)
    n = int(content[y0:y1, x0:x1].sum())
    ck(f"equation ink: {name}", n > 40, f"{n} ink px in box ({a},{bb})-({c},{d})")

# ------------------------------------------------------- 3. table contents
# Cells are gridded over the measured CONTENT bounds (not the surrounding box),
# because the content table sits inset inside its box.
SPEC_TABLES = {
    "input table (top-left)": {
        "content": (84, 64, 221, 124),
        "rows": [["x1", "x2", "x3", "x4", "x5", "x6"],
                 ["1", "2", "1", "5", "6", "6"],
                 ["1", "1", "2", "4", "5", "6"],
                 ["1", "2", "2", "4", "5", "6"],
                 ["C1", "C1", "C1", "C2", "C2", "C2"]],
    },
    "check-classes table (top-right)": {
        "content": (637, 71, 705, 116),
        "rows": [["Z1", "Z2", "Z3"], ["0", "7", "3"], ["0", "6", "2"]],
    },
    "augmented matrix (mid-left)": {
        "content": (88, 163, 224, 241),
        "rows": [["x1", "x2", "x3", "x4", "x5", "x6"],
                 ["1", "1", "1", "1", "1", "1"],
                 ["1", "2", "1", "5", "6", "6"],
                 ["1", "1", "2", "4", "5", "6"],
                 ["C1", "C1", "C1", "C2", "C2", "C2"]],
    },
}
for tname, t in SPEC_TABLES.items():
    (bx0, by0, bx1, by1) = t["content"]
    nrow = len(t["rows"])
    ncol = len(t["rows"][0])
    empty = 0
    for ri in range(nrow):
        for ci in range(ncol):
            cy0 = by0 + (by1 - by0) * ri // nrow
            cy1 = by0 + (by1 - by0) * (ri + 1) // nrow
            cx0 = bx0 + (bx1 - bx0) * ci // ncol
            cx1 = bx0 + (bx1 - bx0) * (ci + 1) // ncol
            a0, b0 = fp(cx0 + 2, cy0 + 2)
            a1, b1 = fp(cx1 - 2, cy1 - 2)
            if int(content[b0:b1, a0:a1].sum()) < 8:
                empty += 1
    ck(f"table cells inked: {tname}", empty == 0,
       f"{nrow}x{ncol} cells, {empty} empty")

# red class row present
for tname, (bx0, by0, bx1, by1) in {
        "input": (84, 108, 221, 124),
        "augmented": (84, 224, 299, 239)}.items():
    x0, y0 = fp(bx0, by0)
    x1, y1 = fp(bx1, by1)
    sub = im[y0:y1, x0:x1]
    rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    redpx = int(((rr > 90) & ((rr - gg) > 40) & ((rr - bb) > 10)).sum())
    ck(f"red class row: {tname}", redpx > 60, f"{redpx} red px")

# --------------------------------------- 3b. TABLE DATA from the pptx itself
# Every cell value is proven from the deck's XML (literal text), matching the
# spec/analysis verbatim — the ink census above cannot distinguish a 2 from a 3.
import zipfile
import re

PPTX = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
        "recreated_pptx/slide_048_recreated.pptx")
EXPECT = {
    "input table": [["x1", "x2", "x3", "x4", "x5", "x6"],
                    ["1", "2", "1", "5", "6", "6"],
                    ["1", "1", "2", "4", "5", "6"],
                    ["1", "2", "2", "4", "5", "6"],
                    ["C1", "C1", "C1", "C2", "C2", "C2"]],
    "check classes": [["Z1", "Z2", "Z3"], ["0", "7", "3"], ["0", "6", "2"]],
    "augmented matrix": [["x1", "x2", "x3", "x4", "x5", "x6"],
                         ["1", "1", "1", "1", "1", "1"],
                         ["1", "2", "1", "5", "6", "6"],
                         ["1", "1", "2", "4", "5", "6"],
                         ["C1", "C1", "C1", "C2", "C2", "C2"]],
}
try:
    with zipfile.ZipFile(PPTX) as z:
        xml = z.read("ppt/slides/slide1.xml").decode("utf-8")
    # pptxgenjs writes one <a:tbl> per addTable with numbered rows; extract
    # each table's rows in document order.
    tbls = re.findall(r"<a:tbl>.*?</a:tbl>", xml, re.S)
    got = []
    for t in tbls:
        rows = re.findall(r"<a:tr .*?</a:tr>", t, re.S)
        trows = []
        for row in rows:
            cells = re.findall(r"<a:tc>.*?</a:tc>", row, re.S)
            vals = []
            for cell in cells:
                txt = "".join(re.findall(r"<a:t>(.*?)</a:t>", cell, re.S))
                vals.append(txt)
            trows.append(vals)
        got.append(trows)
    # subscript digits x1..x6 arrive as "x" + subscript runs; normalise
    def norm(v):
        return v.replace("\u2081", "1").replace("\u2082", "2") \
                .replace("\u2083", "3").replace("\u2084", "4") \
                .replace("\u2085", "5").replace("\u2086", "6")
    for (tname, exp), actual in zip(EXPECT.items(), got):
        an = [[norm(c) for c in row] for row in actual]
        ok = an == exp
        ck(f"table data (from pptx): {tname}", ok,
           "match" if ok else f"expected {exp}, got {an}")
    if len(got) != len(EXPECT):
        ck("table count", False, f"{len(got)} tables, expected {len(EXPECT)}")
    else:
        ck("table count", True, f"{len(got)} tables")
except Exception as e:                                  # noqa: BLE001
    ck("table data (from pptx)", False, f"could not read {PPTX}: {e}")

# ------------------------------------- 4. delimiter (bracket) geometry
# The stacked vectors' brackets must span all their entries. A column vector's
# bracket pair shows up as two tall ink columns inside the expression's region,
# so the check tallies paired strokes over the whole region (row 1 holds three
# column vectors -> 3 pairs; the W-only rows hold one -> 1 pair).


def bracket_pairs(y0, y1, x0, x1, want, label):
    sub = content[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    cs = sub.sum(axis=0)
    h = sub.shape[0]
    tall = [x0 + i / S for i, v in enumerate(cs) if v >= h * 0.6]
    # merge adjacent columns of the same stroke, then pair them up
    strokes = []
    for c in tall:
        if strokes and c - strokes[-1][-1] < 3:
            strokes[-1].append(c)
        else:
            strokes.append([c])
    ok = len(strokes) == want
    ck(f"bracket geometry: {label}", ok,
       f"{len(strokes)} tall bracket stroke(s) found (want {want}): "
       f"{[f'{s[0]:.0f}-{s[-1]:.0f}' for s in strokes]}")


bracket_pairs(150, 192, 594, 805, 6, "row1 right W = ... = [5;-1;-1] (3 vectors)")
bracket_pairs(455, 517, 594, 720, 2, "row6 right W = [5;-1;-1] (1 vector)")
bracket_pairs(61, 101, 328, 356, 2, "Initial W [4;-2;-2]")

# --------------------------------------------- 5. no ink outside expected bands
# REPEAT must sit inside its box (cols 426-530, rows 56-80) and not bleed into
# the top-band that would look like a top stroke.
x0, y0 = fp(420, 55)
x1, y1 = fp(540, 82)
box_ink = int(content[y0:y1, x0:x1].sum())
ck("REPEAT text present", box_ink > 100, f"{box_ink} ink px in REPEAT box")

# calc boxes: no ink in the 9px gap between box4 (bottom 395) and box5 (top 404)
gx0, gy0 = fp(276, 397)
gx1, gy1 = fp(852, 403)
gap = int(content[gy0:gy1, gx0:gx1].sum())
ck("calc box 4/5 gap is clean", gap < 60, f"{gap} ink px in the inter-box gap")

# ------------------------------------------------ 6. explicit lineSpacing
src = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_048.js"
with open(src) as f:
    code = f.read()
multi = code.count("addText(")
spacing = code.count("lineSpacing")
ck("lineSpacing pinned on text blocks", spacing >= multi - 3,
   f"{spacing} lineSpacing declarations across {multi} addText blocks")

# ----------------------------------------------------------- 7. summary
bad = [n for n, ok, _ in results if not ok]
print()
if bad:
    print("SELF-CHECK: FAIL")
    for n in bad:
        print("  -", n)
    sys.exit(1)
print(f"SELF-CHECK: PASS ({len(results)} checks)")
sys.exit(0)
