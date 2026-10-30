#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_024.jpg (960x540, 1px=1pt).
Measure: title/subtitle text bboxes + colors, badge, bottom icon, border strokes.
Everything derived from pixels; print a structured report."""
from PIL import Image
import sys

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_024.jpg"
im = Image.open(FRAME).convert("RGB")
W, H = im.size
px = im.load()
print(f"size: {W}x{H}")

# --- helper: ink masks ---
def ink_bbox(mask_fn, region=None):
    xs, ys = [], []
    x0, y0, x1, y1 = region or (0, 0, W, H)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if mask_fn(px[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys), len(xs))

def is_red(c):
    r, g, b = c
    return r > 110 and g < 90 and b < 90 and (r - max(g, b)) > 50

def is_dark_text(c):
    r, g, b = c
    return r < 120 and g < 120 and b < 120

def is_darkish(c):
    r, g, b = c
    return r < 150 and g < 150 and b < 150

# scan rows for red text bands (title + subtitle) — inside panel x 60..900, y 46..537
print("\n--- red ink (text) row bands, x in 60..900, y in 46..537 ---")
rows = []
for y in range(46, 537):
    cnt = sum(1 for x in range(60, 900) if is_red(px[x, y]))
    rows.append((y, cnt))
# find contiguous bands with cnt > 0
bands = []
cur = None
for y, cnt in rows:
    if cnt > 0:
        if cur is None:
            cur = [y, y, cnt]
        else:
            cur[1] = y; cur[2] += cnt
    else:
        if cur is not None:
            bands.append(cur); cur = None
if cur: bands.append(cur)
for b in bands:
    y0, y1, tot = b
    bb = ink_bbox(is_red, (60, y0, 900, y1 + 1))
    print(f"red band y {y0}..{y1}  inkbbox={bb}")

# measure gap between bands
print("\nband structure (y0,y1):")
coords = [(b[0], b[1]) for b in bands]
print(coords)

# --- colors ---
print("\n--- sampled colors ---")
def sample(cx, cy, r=2):
    rs, gs, bs = [], [], []
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            c = px[cx + dx, cy + dy]
            rs.append(c[0]); gs.append(c[1]); bs.append(c[2])
    return (sum(rs)//len(rs), sum(gs)//len(gs), sum(bs)//len(bs))

print("panel bg (300,300):", sample(300, 300))
print("canvas left margin (20,300):", sample(20, 300))

# --- badge region: circle near top-right. Whole-deck law: center (876,73) d=35 ---
print("\n--- badge window 855..900 x 50..100 ---")
for y in range(50, 100, 4):
    line = ""
    for x in range(855, 900, 2):
        c = px[x, y]
        if is_red(c): line += "R"
        elif c[0] > 230 and c[1] > 230 and c[2] > 130: line += "Y"  # yellow fill
        elif c[0] < 130 and c[0] > 60 and c[2] > 150: line += "P"  # purple ring
        elif sum(c) < 250: line += "#"  # dark ink
        else: line += "."
    print(f"{y:3d} {line}")

# badge ink colors
print("badge fill sample (876,73):", sample(876, 73, 1))
print("badge ring sample (876,57):", sample(876, 57, 1))
# numeral ink: dark pixels inside badge
nd = ink_bbox(lambda c: sum(c) < 300, (860, 58, 893, 90))
print("numeral dark ink bbox inside badge:", nd)

# --- bottom icon region: bottom-center ---
print("\n--- bottom icon window y 495..539, x 420..540 ---")
bb = ink_bbox(lambda c: sum(c) < 420, (400, 490, 560, 538))
print("dark ink bbox (sum<420) bottom center:", bb)
bb2 = ink_bbox(lambda c: sum(c) < 500, (400, 490, 560, 538))
print("dark ink bbox (sum<500) bottom center:", bb2)
# ASCII map of the icon area
for y in range(495, 540, 2):
    line = ""
    for x in range(440, 500, 1):
        c = px[x, y]
        line += "#" if sum(c) < 480 else ("+" if sum(c) < 620 else ".")
    print(f"{y:3d} {line}")

# --- strokes check (house chrome sanity on THIS frame) ---
print("\n--- stroke check ---")
def col_has_red(x, y0, y1):
    return sum(1 for y in range(y0, y1) if is_red(px[x, y]))
print("left stroke col 58-60 red count:", [col_has_red(x, 46, 539) for x in (57, 58, 59, 60)])
print("right stroke col 900-903:", [col_has_red(x, 46, 539) for x in (899, 900, 901, 902)])
def row_has_red(y, x0, x1):
    return sum(1 for x in range(x0, x1) if is_red(px[x, y]))
print("bottom stroke rows 536-539:", [row_has_red(y, 58, 902) for y in (536, 537, 538, 539)])
print("top band y46..50 red count (should be 0, no top stroke):", [row_has_red(y, 60, 900) for y in range(45, 52)])

# --- title/subtitle exact colors ---
print("\n--- text color cores ---")
# title band: use first band bbox from earlier; sample darkest red px
for (y0, y1) in coords:
    cores = []
    for y in range(y0, y1 + 1):
        for x in range(60, 900):
            c = px[x, y]
            if is_red(c):
                cores.append(c)
    if cores:
        rs = sorted(c[0] for c in cores); mid = cores[len(cores)//2]
        print(f"band y{y0}..{y1}: n={len(cores)} median_core={mid}")
