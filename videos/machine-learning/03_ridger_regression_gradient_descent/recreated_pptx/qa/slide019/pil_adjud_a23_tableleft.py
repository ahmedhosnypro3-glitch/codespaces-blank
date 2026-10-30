#!/usr/bin/env python3
"""PIL adjudication of crop_23_table_left MAJORs (attempt 23, render_23).

MAJOR 1: "y-row highlight does not cover the row's cells in IMG1 (render);
          60/80/100 sit on white, yellow only in gaps; original shows the
          y-row cells filled."
MAJOR 2: "outlier-vector delimiter: render = heavy black square bracket,
          original = large thin parentheses."

Measures, in ORIGINAL frame px (render scaled x2.0833):
  A. dominant background color inside each y-row cell (groups 1-3, all 3
     columns) in BOTH images
  B. outlier delimiter ink: column histogram + per-row centroid (bracket =
     constant-x stroke, paren = curved), stroke color, vertical extent
     vs the three stacked entries
"""
from PIL import Image
from collections import Counter

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = Image.open(f"{BASE}/unique_slides/slide_019.jpg").convert("RGB")
rend = Image.open(f"{BASE}/recreated_pptx/qa/slide019/render_23.png").convert("RGB")
OW, OH = orig.size
RW, RH = rend.size
SX, SY = RW / OW, RH / OH
print(f"orig {orig.size} render {rend.size} scale {SX:.4f}/{SY:.4f}")

def bg_mode(img, x0, y0, x1, y1, skip_dark=140):
    """dominant quantized color of pixels that are NOT dark ink"""
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = img.getpixel((x, y))
            if r < skip_dark and g < skip_dark and b < skip_dark:
                continue  # ink
            c[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
    return c.most_common(3)

# A. y-row cells. Render layout: NO REG x0=124 v0=266 colW=38; RIDGE3 x0=384
# v0=526 colW=38; RIDGE10 x0=644 v0=786 colW=36. y-row text gy+69..gy+87,
# gy in [205, 310, 420]. Sample cell interiors away from centered text.
gy_groups = [205, 310, 420]
cells = []
for gy in gy_groups:
    for (v0, colW, label) in [(266, 38, "NOREG"), (526, 38, "RIDGE3"), (786, 36, "RIDGE10")]:
        for ti in range(3):
            cx0 = v0 + ti * colW
            cells.append((label, gy, ti, cx0 + 4, gy + 72, cx0 + colW - 4, gy + 78))
print("\n== A. y-row cell background (mode, top3) ==")
for (label, gy, ti, x0, y0, x1, y1) in cells:
    om = bg_mode(orig, x0, y0, x1, y1)
    rm = bg_mode(rend, int(x0 * SX), int(y0 * SY), int(x1 * SX), int(y1 * SY))
    print(f"  g{gy} {label:7s} T{ti+1} orig={om[0][0]} x{om[0][1]}  render={rm[0][0]} x{rm[0][1]}")

# also the y-label cell (x0+96=220..268) and one band-only gap for reference
print("  -- reference: band-only zone x660..680 y280..290 (between cells) --")
print("   orig:", bg_mode(orig, 660, 280, 680, 290), " render:", bg_mode(rend, int(660*SX), int(280*SY), int(680*SX), int(290*SY)))

# B. outlier delimiter, group 1: entries at tops 199/219/269 (frame), text
# x84..114. Delimiter ink zone: x58..82, y192..300.
def ink_columns(img, x0, y0, x1, y1, scale=1):
    rows = {}
    colhist = Counter()
    colors = Counter()
    for y in range(y0, y1):
        xs = []
        for x in range(x0, x1):
            r, g, b = img.getpixel((x, y))
            if r < 130 and g < 130 and b < 130:
                xs.append(x)
                colors[(r // 32 * 32, g // 32 * 32, b // 32 * 32)] += 1
        if xs:
            rows[y] = (min(xs), max(xs), len(xs))
            for x in xs:
                colhist[x] += 1
    return rows, colhist, colors

print("\n== B. outlier delimiter ORIGINAL frame x58..82 y192..300 ==")
rows_o, hist_o, col_o = ink_columns(orig, 58, 192, 82, 300)
ys_o = sorted(rows_o)
if ys_o:
    print(f"  ink y-extent {ys_o[0]}..{ys_o[-1]}  ({len(ys_o)} rows)")
    span = [ys_o[i+1]-ys_o[i] for i in range(len(ys_o)-1)]
    print(f"  gaps>3px: {[(ys_o[i], ys_o[i+1]) for i in range(len(span)) if span[i] > 3]}")
    samp = [ys_o[0], ys_o[len(ys_o)//4], ys_o[len(ys_o)//2], 3*ys_o[len(ys_o)//4]//2 if False else ys_o[3*len(ys_o)//4], ys_o[-1]]
    for y in samp:
        print(f"    y={y}: x {rows_o[y][0]}..{rows_o[y][1]} w={rows_o[y][2]}")
    top = hist_o.most_common(5)
    print(f"  top ink columns: {top}")
    print(f"  ink color modes: {col_o.most_common(4)}")

print("\n== B2. outlier delimiter RENDER x58..82 (scaled) y192..300 ==")
rx0, ry0, rx1, ry1 = int(58*SX), int(192*SY), int(82*SX), int(300*SY)
rows_r, hist_r, col_r = ink_columns(rend, rx0, ry0, rx1, ry1)
ys_r = sorted(rows_r)
if ys_r:
    print(f"  ink y-extent {ys_r[0]}..{ys_r[-1]} ({len(ys_r)} rows) [frame {ys_r[0]/SY:.0f}..{ys_r[-1]/SY:.0f}]")
    span = [ys_r[i+1]-ys_r[i] for i in range(len(ys_r)-1)]
    print(f"  gaps>3px: {[(ys_r[i], ys_r[i+1]) for i in range(len(span)) if span[i] > 3]}")
    for y in [ys_r[0], ys_r[len(ys_r)//2], ys_r[-1]]:
        print(f"    y={y} (frame {y/SY:.0f}): x {rows_r[y][0]}..{rows_r[y][1]} w={rows_r[y][2]}")
    print(f"  top ink columns: {[(x, n) for x, n in hist_r.most_common(5)]} [frame x: {[round(x/SX,1) for x,_ in hist_r.most_common(5)]}]")
    print(f"  ink color modes: {col_r.most_common(4)}")

# C. does the ORIGINAL bracket span entry 3 (the 22 at y269..285)?
print("\n== C. original outlier entry ink rows (x84..114) group 1 ==")
rows_e, _, col_e = ink_columns(orig, 84, 190, 116, 300)
ys_e = sorted(rows_e)
runs = []
if ys_e:
    start = prev = ys_e[0]
    for y in ys_e[1:]:
        if y - prev > 3:
            runs.append((start, prev)); start = y
        prev = y
    runs.append((start, prev))
print(f"  entry ink runs (frame y): {runs}")
