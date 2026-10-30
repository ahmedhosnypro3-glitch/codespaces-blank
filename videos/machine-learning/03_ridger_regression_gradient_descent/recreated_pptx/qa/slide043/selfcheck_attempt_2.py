#!/usr/bin/env python3
"""MANDATORY pre-judge selfcheck — slide 043 attempt 2 render (render_2.png).
Prints measured numbers for: frame containment, equation ink presence, delimiter
geometry, table data presence, line/box wrap, crop-pair scale audit.
Run: python3 selfcheck_attempt_2.py"""
import json
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = V + "/recreated_pptx/qa/slide043"
SX, SY = 2001 / 960.0, 1125 / 540.0

O = np.asarray(Image.open(V + "/unique_slides/slide_043.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(Q + "/render_2.png").convert("RGB")).astype(int)


def ink(a):
    lum = a.sum(2) / 3.0
    sat = a.max(2) - a.min(2)
    return (lum < 175) | (sat > 45)


def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def rbox(x0, y0, x1, y1):
    """ink bbox inside a frame-px window of the render"""
    m = ink(R[int(y0 * SY):int(y1 * SY), int(x0 * SX):int(x1 * SX)])
    b = bbox(m)
    if b is None:
        return None
    return (round(b[0] / SX + x0, 1), round(b[1] / SY + y0, 1),
            round(b[2] / SX + x0, 1), round(b[3] / SY + y0, 1))


fails = []

# 1. FRAME CONTAINMENT -------------------------------------------------------
panel_ink = rbox(60, 47, 900, 537)
ok = panel_ink and panel_ink[0] >= 57 and panel_ink[2] <= 902 and panel_ink[1] >= 45 and panel_ink[3] <= 539
print("1 frame containment: content ink bbox (frame px) =", panel_ink,
      "->", "PASS" if ok else "FAIL")
if not ok:
    fails.append("frame containment")

# 2. EQUATION INK PRESENCE ---------------------------------------------------
bands = [(150, 200), (215, 265), (278, 325), (345, 395), (411, 456), (477, 522)]
for i, (y0, y1) in enumerate(bands):
    d = rbox(280, y0, 478, y1)
    w = rbox(616, y0, 812, y1)
    po = int(ink(O[y0:y1, 280:478]).sum())
    pr = int(ink(R[int(y0 * SY):int(y1 * SY), int(280 * SX):int(478 * SX)]).sum())
    print(f"2 band {i+1}: d-eq ink bbox={d}  W-eq ink bbox={w}  "
          f"orig_ink={po} render_ink={pr} ratio={pr/max(po,1):.2f} ->",
          "PASS" if d and w and pr > 0 else "FAIL")
    if not (d and w and pr > 0):
        fails.append(f"empty equation band {i+1}")

# 3. DELIMITER GEOMETRY ------------------------------------------------------
# initial-W "brackets" vs the text they are supposed to enclose / do enclose
init_strokes = rbox(328, 58, 334, 108)
init_strokes2 = rbox(428, 58, 434, 108)
step = rbox(330, 58, 460, 90)
vec = rbox(331, 68, 428, 105)
print("3a initial-W bracket strokes:", init_strokes, init_strokes2,
      "| Step text bbox:", step, "| interior ink bbox:", vec)
overlap = step and init_strokes and step[0] <= 332
print("3a verdict:", "FAIL (Step text starts inside/at the left bracket x330.5; "
      "vector has no enclosing delimiter)" if overlap else "PASS")
if overlap:
    fails.append("initial-W delimiter")
# top-right matrix: each column must be ONE tall paren over 2 entries
for cx, name in [(605, "col1"), (628, "col2"), (650, "col3")]:
    b = rbox(cx - 10, 78, cx + 10, 112)
    print(f"3b matrix {name}: ink bbox={b}")
print("3b verdict: see judge transcript (render draws separate one-line parens "
      "per entry, not one paren spanning the two-entry vector)")
fails.append("matrix delimiter")
# aug vectors: paren extent vs entry extent
for cx in (99, 122, 144, 166, 189, 212):
    b = rbox(cx - 9, 180, cx + 9, 226)
    print(f"3c aug {cx}: ink bbox={b}")

# 4. TABLE DATA PRESENCE -----------------------------------------------------
cols = [94, 117, 139, 161, 184, 206]
missing = []
for ri, y in enumerate((69, 84, 98, 118)):
    row = []
    for cx in cols:
        b = rbox(cx - 9, y - 7, cx + 9, y + 8)
        row.append(1 if b else 0)
        if not b:
            missing.append((ri, cx))
    print(f"4 top-left table row {ri+1} cell ink:", row)
print("4 verdict:", "PASS (18/18 cells inked)" if not missing else f"FAIL missing {missing}")
if missing:
    fails.append("table cells")
# class-row colours (frame: C1 red, C2 blue)
cr = R[int(112 * SY):int(125 * SY), int(88 * SX):int(218 * SX)]
red = int(((cr[:, :, 0] > 90) & (cr[:, :, 0] - cr[:, :, 1] > 40)).sum())
blue = int(((cr[:, :, 2] > 90) & (cr[:, :, 2] - cr[:, :, 0] > 40)).sum())
print(f"4b top-left class row colour px: red={red} blue={blue} ->",
      "FAIL (frame has red C1 + blue C2; render is black)" if red + blue < 20 else "PASS")
if red + blue < 20:
    fails.append("class-row colour")

# 5. LINE / BOX WRAP ---------------------------------------------------------
box_r = 246
head = rbox(80, 145, 280, 162)
print("5a aug heading bbox:", head, "| box right edge x=246 ->",
      "FAIL overflow" if head and head[2] > box_r else "PASS")
if head and head[2] > box_r:
    fails.append("aug heading overflow")
itbox = rbox(80, 272, 260, 312)
print("5b iteration block bbox:", itbox, "| frame box x84..245 y277..307")
# decision text vs d-equation collision: count ink overlap column band
for i, (y0, y1) in enumerate(bands):
    dec = rbox(470, y0, 625, y1)
    print(f"5c band {i+1} decision-zone ink bbox:", dec)

# 6. CROP-PAIR SCALE AUDIT ---------------------------------------------------
cr = Image.open(Q + "/crop_2_eqstack_render.png")
co = Image.open(Q + "/crop_2_eqstack_orig.png")
sx = cr.size[0] / 591.0
sy = cr.size[1] / 402.0
print(f"6 crop_2_eqstack: render_crop={cr.size} orig_crop={co.size} "
      f"region=591x402 frame px; effective px/frame: x={sx:.4f} y={sy:.4f}; "
      f"render dpi scale=({SX:.4f},{SY:.4f}) ->",
      "PASS" if abs(sx - SX) < 0.005 and abs(sy - SY) < 0.005 and cr.size == co.size else "FAIL")

print("\nSELFCHECK RESULT: FAIL — unfixed defects:", len(fails))
for f in fails:
    print("  -", f)
