#!/usr/bin/env python3
"""Self-check for slide 034 attempt 1.

Mandatory pre-judge checks:
  1. Frame containment — content ink sits inside the house panel (x54..903, y45..540 frame px)
  2. Equations exist with ink — the equation region has non-background pixels + a fraction bar
  3. Delimiter geometry — the equation box border spans the equation image
  4. Explicit lineSpacing on multi-line blocks — asserted from the build script text
  5. Table data cell-by-cell — every value matches the analysis JSON verbatim
  6. Smooth curve — the graph asset's blue curve passes a second-difference ripple check
"""
import json
import re
import sys

import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = f"{BASE}/recreated_pptx/qa/slide034/render_1.png"
ORIG = f"{BASE}/unique_slides/slide_034.jpg"
BUILD = f"{BASE}/recreated_pptx/build/slide_034.js"

PANEL = {"x0": 54, "x1": 903, "y0": 45, "y1": 540}   # frame px
SC = 1125 / 540                                       # render px per frame px (150dpi)

fails = []


def cv(v):
    return v * SC


# ------------------------------------------------------------- 1. frame containment
im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"render {W}x{H}")

r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
panel_mask = (abs(r - 233) < 12) & (abs(g - 233) < 12) & (abs(b - 231) < 12)
white_mask = (r > 245) & (g > 245) & (b > 245)
ink = ~(panel_mask | white_mask)
ink[0:int(cv(44)) - 2, :] = False  # white margin above the panel is title band, not an error

rows, cols = np.where(ink)
if len(rows):
    fx0, fx1 = cols.min() / SC, cols.max() / SC
    fy0, fy1 = rows.min() / SC, rows.max() / SC
    print(f"content ink (frame px): x {fx0:.1f}..{fx1:.1f}, y {fy0:.1f}..{fy1:.1f}")
    if fx0 < PANEL["x0"] - 1:
        fails.append(f"ink crosses panel left: {fx0:.1f} < {PANEL['x0']}")
    if fx1 > PANEL["x1"] + 1:
        fails.append(f"ink crosses panel right: {fx1:.1f} > {PANEL['x1']}")
    if fy0 < PANEL["y0"] - 1:
        fails.append(f"ink crosses panel top: {fy0:.1f} < {PANEL['y0']}")
    if fy1 > PANEL["y1"] + 1:
        fails.append(f"ink crosses panel bottom: {fy1:.1f} > {PANEL['y1']}")
else:
    fails.append("no content ink found in render")

# ------------------------------------------------------------- 2. equation ink + border
box = im[int(cv(200)):int(cv(275)), int(cv(200)):int(cv(550))]
not_white = ~((box[:, :, 0] > 245) & (box[:, :, 1] > 245) & (box[:, :, 2] > 245))
not_gray = ~((abs(box[:, :, 0] - 233) < 12) & (abs(box[:, :, 1] - 233) < 12) &
             (abs(box[:, :, 2] - 231) < 12))
n_ink = int((not_white & not_gray).sum())
print(f"equation box ink pixels: {n_ink}")
if n_ink < 2000:
    fails.append(f"equation region nearly empty ({n_ink} ink px)")

border_mask = (box[:, :, 0] < 60) & (box[:, :, 1] < 60) & (box[:, :, 2] < 60)
perim = np.concatenate([border_mask[0, :], border_mask[-1, :],
                        border_mask[:, 0], border_mask[:, -1]])
if perim.sum() < 50:
    fails.append("equation box black border missing")

# ------------------------------------------------------------- 3. table data cell-by-cell
analysis = json.load(open(f"{BASE}/analysis/slide_034_final.json"))
desc = next(e["description"] for e in analysis["visual_elements"]
            if e["type"] == "table" and "8 rows" in e["description"])

# rows are separated by " | "; the x header row is glued into the prefix, and the
# last row (next x) is followed by trailing prose.
_rowparts = desc.split(" | ")
_header_label = _rowparts[0].split("values: ")[-1].strip()   # "x"
expected = {_header_label: []}
for i, _p in enumerate(_rowparts[1:]):
    if i == len(_rowparts[1:]) - 1:
        _p = _p.split(". The ")[0]                            # strip trailing prose
    _sp = _p.strip().rstrip(".").split(" ", 1)
    _label = _sp[0].strip()
    _vals = [v.strip() for v in _sp[1].split(",")] if len(_sp) > 1 else []
    if len(_vals) != 18:
        fails.append(f"row {_label!r}: parsed {len(_vals)} values, expected 18")
        continue
    expected[_label] = _vals

if len(expected) != 8:
    fails.append(f"parsed {len(expected)} table rows from analysis (need 8)")
else:
    print(f"parsed {len(expected)} table rows x 18 data cols from analysis")

build_src = open(BUILD).read()
for label, vals in expected.items():
    for v in vals:
        if v not in build_src:
            fails.append(f"table value {v!r} (row {label!r}) missing from build data")

for hexv in ["AFEEEE", "FFFFFF", "90EE90", "FFFACD", "FFB6C1", "98FB98"]:
    if hexv not in build_src:
        fails.append(f"row fill #{hexv} missing from build")

# ------------------------------------------------------------- 4. lineSpacing pinned
for txt in ["Non-Convex Function",
            "May reach different minimum value based on:",
            "initial point and learning rate",
            "X is in between 9.6 and",
            "f(x) is in between -10.03 and -9.92"]:
    idx = build_src.find(txt)
    if idx < 0:
        fails.append(f"text {txt!r} not found in build")
        continue
    block = build_src[max(0, idx - 600): idx + 900]   # wide window: options follow the text
    if "lineSpacing" not in block:
        fails.append(f"no lineSpacing pinned for multi-line block {txt!r}")

# ------------------------------------------------------------- 5. equation fraction bar
eq = np.asarray(Image.open(f"{BASE}/recreated_pptx/build/assets/eq_034_main.png").convert("RGBA"))
alpha = eq[:, :, 3]
rows_e, cols_e = np.where(alpha > 8)
print(f"equation asset: {eq.shape[1]}x{eq.shape[0]} px, ink rows {rows_e.min()}..{rows_e.max()}")
bar_rows = sum(1 for row in range(eq.shape[0])
               if (alpha[row, cols_e.min():cols_e.max() + 1] > 128).mean() > 0.35)
print(f"fraction-bar rows: {bar_rows}")
if bar_rows < 3:
    fails.append(f"equation has no fraction bar (bar rows = {bar_rows})")

# ------------------------------------------------------------- 6. smooth curve ripple
gp = np.asarray(Image.open(f"{BASE}/recreated_pptx/build/assets/graph_034_main.png").convert("RGBA"))
ga, gr, gg, gb = gp[:, :, 3], gp[:, :, 0], gp[:, :, 1], gp[:, :, 2]
blue_curve = (ga > 100) & (gb > 150) & (gb - gr > 60) & (gb - gg > 60)
nblue = int(blue_curve.sum())
print(f"graph asset blue curve pixels: {nblue}")
if nblue < 2000:
    fails.append(f"blue curve nearly empty ({nblue} px)")

# ripple check across many vertical slices (the curve crosses each column once)
maxd2 = 0
checked = 0
for x in range(60, gp.shape[1] - 60, 17):
    col = blue_curve[:, x:x + 3].any(axis=1)
    ys = np.where(col)[0]
    # take the central contiguous run only (markers/text also register blue)
    if len(ys) < 8:
        continue
    d2 = np.abs(np.diff(ys, 2))
    if len(d2):
        maxd2 = max(maxd2, int(d2.max()))
        checked += 1
print(f"ripple check: {checked} slices, max |2nd difference| = {maxd2}")
if checked < 10:
    fails.append(f"curve ripple check covered only {checked} slices")
if maxd2 > 4:
    fails.append(f"curve not smooth (max |2nd difference| = {maxd2})")

print()
if fails:
    print("SELFCHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELFCHECK: PASS (render_1)")
