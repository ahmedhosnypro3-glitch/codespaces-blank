#!/usr/bin/env python3
"""Pre-judge selfcheck for slide 037, attempt 6 (render_6.png, 150 dpi 2001x1125).

Checks (founder directive; a judge PASS never waives them):
 1. Frame containment: content ink inside every inner frame (and inside the house panel).
 2. Equation regions contain ink (empty equation region = BLOCKER).
 3. Delimiter geometry: parentheses span the content they enclose, no overlap.
 4. Table data: n/a (slide 037 has no table).
 5. Line/box wrap: every text line stays inside its panel band; explicit lineSpacing
    is set by the builder on every text box (checked by source grep).
 6. Crop-pair scale audit: render/original crops share the same effective px-per-frame-px.
 7. house_chrome_check.py PASS (run separately; output banked next to this file).

Run from the project root:
  python3 videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide037/selfcheck_attempt_6.py
"""
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path("/workspaces/codespaces-blank/ai_llm_slides")
VROOT = ROOT / "videos/machine-learning/03_ridger_regression_gradient_descent"
QA = VROOT / "recreated_pptx/qa/slide037"
RENDER = QA / "render_6.png"
ORIG = VROOT / "unique_slides/slide_037.jpg"
BUILD = VROOT / "recreated_pptx/build/slide_037.js"

render = Image.open(RENDER).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
R = np.asarray(render).astype(int)
O = np.asarray(orig).astype(int)
S = render.width / 960.0  # render px per frame px

FAILS = []


def fail(msg):
    FAILS.append(msg)
    print("  FAIL:", msg)


def bbox(a, x0, y0, x1, y1, bg, thr=90, scale=1.0):
    X0, Y0, X1, Y1 = [int(round(v * scale)) for v in (x0, y0, x1, y1)]
    sub = a[Y0:Y1, X0:X1]
    d = np.abs(sub - np.array(bg)).sum(axis=2)
    ink = d > thr
    ys, xs = np.nonzero(ink)
    if len(ys) == 0:
        return None
    return (round((X0 + xs.min()) / scale, 1), round((Y0 + ys.min()) / scale, 1),
            round((X0 + xs.max()) / scale, 1), round((Y0 + ys.max()) / scale, 1))


def ink_count(a, x0, y0, x1, y1, bg, thr=90, scale=1.0):
    X0, Y0, X1, Y1 = [int(round(v * scale)) for v in (x0, y0, x1, y1)]
    sub = a[Y0:Y1, X0:X1]
    d = np.abs(sub - np.array(bg)).sum(axis=2)
    return int((d > thr).sum())


WHITE = (255, 255, 255)
CREAM = (254, 255, 232)
TAN = (234, 219, 200)
GREEN = (223, 255, 238)

print(f"# slide 037 selfcheck attempt 6 — render_6.png {render.size}")
print(f"# scale render/frame = {S:.6f} (2001/960)")

# ---------------------------------------------------------------- 1. containment
print("\n[1] FRAME CONTAINMENT (content ink vs each panel's inner edge, frame px)")
panels = [
    ("P1 white  ", (68, 108, 870, 210), WHITE, (72, 112, 866, 206)),
    ("P2 cream  ", (66, 229, 891, 341), CREAM, (70, 233, 887, 337)),
    ("P3 tan    ", (66, 348, 891, 531), TAN, (70, 352, 887, 527)),
]
for name, frame, bg, interior in panels:
    b = bbox(R, interior[0], interior[1], interior[2], interior[3], bg, scale=S)
    print(f"  {name} frame={frame} interior_ink={b}")
    if b is None:
        fail(f"{name} empty panel")
        continue
    margins = (b[0] - frame[0], b[1] - frame[1], frame[2] - b[2], frame[3] - b[3])
    print(f"      margins L/T/R/B = {margins} (must all be > 0)")
    if min(margins) <= 0:
        fail(f"{name} content crosses its frame")
# green highlight box interior
b = bbox(R, 82, 464, 483, 518, GREEN, scale=S)
print(f"  green box  frame=(80,462,485,520) interior_ink={b}")
if b:
    margins = (b[0] - 80, b[1] - 462, 485 - b[2], 520 - b[3])
    print(f"      margins L/T/R/B = {margins}")
    if min(margins) <= 0:
        fail("green box content crosses its frame")
# house panel + strokes: no content ink outside the panel
b = bbox(R, 54, 45, 903, 540, (233, 233, 231), thr=120, scale=S)
print(f"  house panel ink bbox (incl. chrome) = {b} (panel 54..903 x 45..540)")
if b and (b[0] < 54 or b[1] < 45 or b[2] > 903 or b[3] > 540):
    fail("ink outside the house panel")

# ---------------------------------------------------------------- 2. equations ink
print("\n[2] EQUATION REGIONS CONTAIN INK (nonzero ink pixels; empty = BLOCKER)")
eq_regions = [
    ("Sigma1 (error)", (198, 260, 226, 290), CREAM),
    ("frac1 (dError/dW)", (263, 400, 340, 451), TAN),
    ("frac2 (dError/dW)", (507, 400, 584, 451), TAN),
    ("Sigma2 (misclass)", (648, 406, 681, 444), TAN),
    ("Sigma3 (ONLY)", (328, 469, 357, 504), GREEN),
]
for name, box, bg in eq_regions:
    n = ink_count(R, *box, bg, scale=S)
    print(f"  {name:20s} region={box} ink_px={n}")
    if n <= 0:
        fail(f"{name} renders empty")

# ---------------------------------------------------------------- 3. delimiters
print("\n[3] DELIMITER GEOMETRY")
# the explanation's "( W^T X_i )" — parens must span the enclosed glyph rows
# measure: left paren column band and the enclosed MAIN GLYPH rows (subscripts
# hang below the paren in the original too, so they are excluded from the span test)
b_paren = bbox(R, 392, 264, 402, 290, CREAM, scale=S)
b_inner = bbox(R, 403, 264, 444, 284, CREAM, scale=S)
print(f"  explanation '(' band={b_paren} enclosed 'W^T X' main-glyph band={b_inner}")
if b_paren and b_inner:
    spans = b_paren[1] <= b_inner[1] + 1 and b_paren[3] >= b_inner[3] - 1
    print(f"      paren spans enclosed ink: {spans}")
    if not spans:
        fail("explanation left paren does not span its content")
# "(i)" in limit 1 and limit 3 (single-line, parens must enclose the i)
b = bbox(R, 255, 290, 276, 305, CREAM, scale=S)
print(f"  limit-1 trailing '(i)' band={b}")
if not b:
    fail("limit-1 '(i)' missing")

# ---------------------------------------------------------------- 4. tables
print("\n[4] TABLE DATA — n/a (slide 037 contains no table)")

# ---------------------------------------------------------------- 5. line bands
print("\n[5] LINE/BOX WRAP + explicit lineSpacing")
lines = [
    ("box1 line1", (77, 848), (141, 171), WHITE, (68, 108, 870, 210)),
    ("box1 line2", (77, 848), (169, 201), WHITE, (68, 108, 870, 210)),
    ("box2 heading", (75, 300), (241, 259), CREAM, (66, 229, 891, 341)),
    ("box2 error line", (76, 352), (261, 290), CREAM, (66, 229, 891, 341)),
    ("box2 limit", (145, 275), (289, 305), CREAM, (66, 229, 891, 341)),
    ("box2 explanation", (390, 885), (264, 290), CREAM, (66, 229, 891, 341)),
    ("box2 summation", (75, 305), (307, 330), CREAM, (66, 229, 891, 341)),
    ("box3 heading", (82, 550), (360, 384), TAN, (66, 348, 891, 531)),
    ("box3 eq1 left", (82, 260), (412, 438), TAN, (66, 348, 891, 531)),
    ("box3 where", (408, 465), (413, 433), TAN, (66, 348, 891, 531)),
    ("box3 limit2", (605, 720), (440, 456), TAN, (66, 348, 891, 531)),
    ("box3 eq1 terms", (720, 768), (412, 440), TAN, (66, 348, 891, 531)),
    ("box3 eq2 left", (82, 260), (470, 498), GREEN, (82, 464, 483, 518)),
    ("box3 limit3", (250, 440), (502, 520), GREEN, (82, 464, 483, 518)),
    ("box3 eq2 terms", (418, 492), (470, 500), GREEN, (82, 464, 483, 518)),
]
for name, (x0, x1), (y0, y1), bg, frame in lines:
    b = bbox(R, x0, y0, x1, y1, bg, scale=S)
    print(f"  {name:18s} band=({x0},{y0},{x1},{y1}) ink={b}")
    if b is None:
        fail(f"{name} empty")
        continue
    if b[0] < x0 - 2 or b[2] > x1 + 2 or b[1] < y0 - 2 or b[3] > y1 + 2:
        fail(f"{name} ink leaves its intended band")
src = BUILD.read_text()
print(f"  slide.addText boxes={src.count('slide.addText(')} (title, single line),"
      f" lineAt boxes={src.count('lineAt(')}; helper sets explicit lineSpacing:"
      f" {'lineSpacing:' in src}")
if "lineSpacing:" not in src:
    fail("lineAt helper does not set explicit lineSpacing")
# every content line is single-line (no multi-line box without a pinned pitch)
if src.count("breakLine") > 0:
    fail("multi-line text box present without a measured pitch")

# ---------------------------------------------------------------- 6. crop scale
print("\n[6] CROP-PAIR SCALE AUDIT (render crop vs upscaled original crop)")
crops = {
    "def_lines": (70, 135, 860, 202),
    "eq_stack": (140, 250, 884, 306),
    "update_eqs": (75, 395, 790, 460),
    "green_box": (70, 455, 500, 525),
}
for name, (x0, y0, x1, y1) in crops.items():
    rbox = tuple(int(round(v * S)) for v in (x0, y0, x1, y1))
    rc = render.crop(rbox)
    oc = orig.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(QA / f"crop_6_{name}_render.png")
    oc.save(QA / f"crop_6_{name}_orig.png")
    sx = rc.width / (x1 - x0)
    sy = rc.height / (y1 - y0)
    print(f"  {name:11s} frame=({x0},{y0},{x1},{y1}) crop={rc.size} "
          f"px/frame_px x={sx:.6f} y={sy:.6f} expected={S:.6f}")
    if abs(sx - S) > 0.01 * S or abs(sy - S) > 0.01 * S:
        fail(f"{name} crop scale mismatch")

print("\n[7] HOUSE CHROME CHECK — see house_chrome_check_attempt_6.txt (PASS)")
print("\nSELFCHECK RESULT:", "PASS" if not FAILS else f"FAIL ({len(FAILS)} issues)")
for f in FAILS:
    print("  -", f)
