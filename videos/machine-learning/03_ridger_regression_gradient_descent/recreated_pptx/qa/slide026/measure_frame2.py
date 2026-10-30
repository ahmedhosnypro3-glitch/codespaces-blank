#!/usr/bin/env python3
"""Pass-2 detailed PIL measurement of unique_slides/slide_026.jpg (960x540).
Sensitive masks + per-row word segmentation + color classification + underline
bar detection + Arial-metric wrap reconstruction.
Slide 26: 'Gradient Descent Solution' — blue-bordered white content box,
red section headers, blue algorithm steps [1]-[3], black Notes bullets.
"""
import numpy as np
from PIL import Image, ImageFont

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_026.jpg"
ARIAL = "/usr/share/fonts/TTF/Arial.TTF"
ARIALB = "/usr/share/fonts/TTF/Arialbd.TTF"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# ---- sensitive ink masks ---------------------------------------------------
# panel-gray background (233,233,231) e.g. title zone; ink = distance > 28
bg = np.array([233, 233, 231])
dist_panel = np.abs(im - bg).max(axis=2)
ink_panel = dist_panel > 28
# white box interior; ink = distance from 255 > 28
dist_white = 255 - im.min(axis=2)
ink_white = dist_white > 28

# color classes on ink (JPEG-tolerant)
red_ink = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
blue_ink = (b > 90) & ((b - r) > 40) & ((b - g) > 40)
dark_ink = (im.sum(axis=2) < 330)

def cls_of(y0, y1, x0, x1):
    """dominant color class + core color within a window"""
    win = (slice(y0, y1), slice(x0, x1))
    cnt = {"red": int(red_ink[win].sum()), "blue": int(blue_ink[win].sum()),
           "dark": int(dark_ink[win].sum())}
    dom = max(cnt, key=cnt.get)
    # core color = darkest ink px of the dominant class
    if dom == "red":
        mm = red_ink[win]
    elif dom == "blue":
        mm = blue_ink[win]
    else:
        mm = dark_ink[win]
    px = im[win][mm]
    if len(px):
        core = px[px.sum(axis=1).argmin()]
    else:
        core = None
    return dom, cnt, core

def runs_of(profile, gap=2):
    """contiguous runs (allow gap px of zero) from a 1-D bool profile"""
    idx = np.where(profile)[0]
    if not len(idx):
        return []
    out = []
    s = p = idx[0]
    for i in idx[1:]:
        if i > p + gap:
            out.append((s, p)); s = i
        p = i
    out.append((s, p))
    return out

def seg_words(mask_row, y0, y1, min_gap=3):
    """word segmentation: column profile of ink in rows y0..y1, runs with gaps>=min_gap"""
    prof = mask_row[y0:y1].any(axis=0)
    return runs_of(prof, gap=min_gap - 1)

def measure_band(name, y0, y1, x0, x1, inkm, pad_y=8, pad_x=8, min_gap=3, do_color=False):
    """ink bbox + word runs in a window"""
    win_ink = inkm[y0:y1, x0:x1]
    ys, xs = np.where(win_ink)
    print(f"\n== {name} (window y{y0}-{y1} x{x0}-{x1}) ==")
    if not len(ys):
        print("  NO INK")
        return
    gy0, gy1 = ys.min() + y0, ys.max() + y0
    gx0, gx1 = xs.min() + x0, xs.max() + x0
    print(f"  ink bbox y {gy0}-{gy1} (h={gy1-gy0+1})  x {gx0}-{gx1} (w={gx1-gx0+1})  center=({(gx0+gx1)/2:.1f},{(gy0+gy1)/2:.1f})")
    runs = seg_words(win_ink, 0, win_ink.shape[0], min_gap=min_gap)
    print(f"  {len(runs)} ink runs (gap>={min_gap}):")
    line = "   "
    for (s, e) in runs:
        seg = f"[{s+x0}-{e+x0}]"
        if len(line) + len(seg) > 100:
            print(line); line = "   "
        line += seg
    print(line)
    if do_color:
        # color classification per run
        for (s, e) in runs:
            dom, cnt, core = cls_of(gy0, gy1 + 1, s + x0, e + x0 + 1)
            print(f"    run x {s+x0}-{e+x0} w={e-s+1}: {dom} {cnt} core={core}")

def underline_bars(name, y0, y1, x0, x1):
    """detect solid horizontal bars (underline candidates) in a window"""
    print(f"\n== underline-bar scan in {name} (y{y0}-{y1} x{x0}-{x1}) ==")
    for colname, m in (("red", red_ink), ("blue", blue_ink), ("dark", dark_ink)):
        sub = m[y0:y1, x0:x1]
        for yy in range(sub.shape[0]):
            row = sub[yy]
            rs = runs_of(row, gap=0)
            for (s, e) in rs:
                w_ = e - s + 1
                if w_ >= 18 and row[s:e + 1].mean() > 0.75:
                    print(f"  {colname} bar: y {y0+yy} x {x0+s}-{x0+e} (w={w_}, fill={row[s:e+1].mean():.2f})")

# ---- 1. TITLE (rows 40..100, gray panel; exclude badge halo window) --------
title_ink = ink_panel.copy()
title_ink[:, 845:] = False   # exclude badge x 860-893 + halo
title_ink[:, :60] = False    # exclude left chrome stroke zone
measure_band("TITLE 'Gradient Descent Solution'", 40, 100, 0, 960, title_ink, min_gap=4)
# title word runs + per-run color + core
win = (slice(40, 100), slice(60, 845))
ys, xs = np.where(title_ink[win])
if len(ys):
    print("title core colors (darkest 5 ink px):")
    px = im[win][title_ink[win]]
    order = px.sum(axis=1).argsort()[:5]
    for p in px[order]:
        print("   ", tuple(p))

# ---- 2. CONTENT BOX border --------------------------------------------------
print("\n== CONTENT BOX border ==")
# use blue mask; borders are the 2-3px solid lines
colprof = blue_ink.sum(axis=0)
rowprof = blue_ink.sum(axis=1)
print("cols with >150 blue px:", [x for x in range(W) if colprof[x] > 150])
print("rows with >150 blue px:", [y for y in range(H) if rowprof[y] > 150])
# left/right border x centers, top/bottom border y centers + thickness
for lbl, prof, rng in (("left col", colprof, range(70, 100)), ("right col", colprof, range(850, 880)),
                       ("top row", rowprof, range(80, 105)), ("bottom row", rowprof, range(485, 510))):
    heavy = [v for v in rng if prof[v] > 150]
    print(f"  {lbl}: heavy {heavy}")

# ---- 3. GD HEADER (red, rows 105..135) --------------------------------------
measure_band("GD HEADER (red)", 105, 135, 90, 860, ink_white & (red_ink | (dist_white > 28)), min_gap=4, do_color=False)
# clean: measure red only in that window
hdr = (slice(105, 135), slice(90, 860))
ys, xs = np.where(ink_white[hdr])
if len(ys):
    print(f"  red-ink bbox: y {ys.min()+105}-{ys.max()+105} x {xs.min()+90}-{xs.max()+90}")

# ---- 4. BLUE ALGORITHM ROWS --------------------------------------------------
ROWS = {"A(line[1])": (138, 168), "B(line[2] r1)": (172, 202), "C(line[2] r2)": (205, 236), "D(line[3])": (238, 268)}
for name, (y0, y1) in ROWS.items():
    measure_band(f"BLUE ROW {name}", y0, y1, 90, 860, ink_white, min_gap=4, do_color=True)

# per-column dominant color along row C to find red segment boundary
print("\n== ROW C per-column color classification ==")
y0, y1 = 205, 236
winR = (slice(y0, y1), slice(90, 860))
prof_red = red_ink[winR].sum(axis=0)
prof_blue = blue_ink[winR].sum(axis=0)
prof_dark = dark_ink[winR].sum(axis=0)
# columns with ink
anyink = ink_white[winR].any(axis=0)
segs = runs_of(anyink, gap=2)
print(f"  row C ink runs: {len(segs)}")
# classify each run
for (s, e) in segs:
    rc, bc, dc = prof_red[s:e+1].sum(), prof_blue[s:e+1].sum(), prof_dark[s:e+1].sum()
    dom = max((rc, 'red'), (bc, 'blue'), (dc, 'dark'), key=lambda t: t[0])
    print(f"  run x {s+90}-{e+90} w={e-s+1}: red={rc} blue={bc} dark={dc} -> {dom[1]}")

# same classification for rows B and D
for nm, (y0, y1) in (("ROW B", (172, 202)), ("ROW D", (238, 268))):
    print(f"\n== {nm} per-column color classification ==")
    winR = (slice(y0, y1), slice(90, 860))
    prof_red = red_ink[winR].sum(axis=0)
    prof_blue = blue_ink[winR].sum(axis=0)
    anyink = ink_white[winR].any(axis=0)
    segs = runs_of(anyink, gap=2)
    for (s, e) in segs:
        rc, bc = prof_red[s:e+1].sum(), prof_blue[s:e+1].sum()
        print(f"  run x {s+90}-{e+90} w={e-s+1}: red={rc} blue={bc} -> {'red' if rc > bc else 'blue'}")

# underline scans for blue rows (below glyph band)
underline_bars("blue row B zone", 172, 205, 90, 860)
underline_bars("blue row C zone", 205, 238, 90, 860)
underline_bars("blue row D zone", 238, 272, 90, 860)

# ---- 5. NOTES HEADER + NOTES ROWS ---------------------------------------------
measure_band("NOTES HEADER", 300, 335, 90, 860, ink_white, min_gap=4)
NOTES = {"N1": (338, 366), "N2": (372, 400), "N3": (437, 465), "N4": (471, 499)}
for name, (y0, y1) in NOTES.items():
    measure_band(f"NOTES ROW {name}", y0, y1, 88, 860, ink_white, min_gap=4)
underline_bars("notes row N3 zone", 437, 470, 88, 860)
underline_bars("notes row N4 zone", 471, 502, 88, 860)

# ---- 6. core colors per class -------------------------------------------------
print("\n== CORE COLORS ==")
for nm, m, win2 in (
    ("title red", red_ink, (slice(48, 100), slice(150, 845))),
    ("gd header red", red_ink, (slice(105, 135), slice(90, 860))),
    ("notes hdr red", red_ink, (slice(300, 335), slice(90, 860))),
    ("blue text", blue_ink, (slice(138, 268), slice(90, 860))),
    ("notes dark", dark_ink, (slice(338, 499), slice(88, 860))),
    ("box border blue", blue_ink, (slice(85, 505), slice(70, 880))),
):
    px = im[win2][m[win2]]
    if len(px):
        core = px[px.sum(axis=1).argmin()]
        med = np.median(px, axis=0)
        print(f"  {nm}: darkest={tuple(core)} median={tuple(int(v) for v in med)} n={len(px)}")

# ---- 7. unaccounted ink census (white box interior + panel) -------------------
print("\n== UNACCOUNTED INK (white box interior rows 93..497, x 85..861) ==")
# ink rows in box interior
prof = ink_white[:, 85:861].sum(axis=1)
bands = runs_of(prof > 0, gap=3)
for (y0, y1) in bands:
    if 90 <= y0 <= 500:
        cols = np.where(ink_white[y0:y1+1, 85:861].any(axis=0))[0]
        print(f"  ink band y {y0}-{y1} h={y1-y0+1} x {cols.min()+85}-{cols.max()+85}")

print("\n== panel-zone ink outside box (title row band census) ==")
prof = ink_panel[:, 60:845].sum(axis=1)
bands = runs_of(prof > 0, gap=3)
for (y0, y1) in bands:
    if y1 < 95 or y0 > 495:
        cols = np.where(ink_panel[y0:y1+1, 60:845].any(axis=0))[0]
        print(f"  ink band y {y0}-{y1} x {cols.min()+60}-{cols.max()+60}")

# ---- 8. Arial metric wrap reconstruction -------------------------------------
print("\n== ARIAL METRIC RECONSTRUCTION ==")
L2 = "[2] Update the weights by moving along the direction of negative gradient of Loss function (w.r.t. W) (moving step is a hyper parameter, AKA Learning Rate)"
L1 = "[1] Start with initial Random Weights (W)"
L3 = "[3] Stop when the gradient is almost zero (this is at the minimum value of the function)"
N1 = "Least Squares Linear regression objective function is a convex function (even with regularizer). This means it has ONE Minimum (good news )."
N2 = "GD will approximately find this minimum value but at a variable number of steps depending on the used Learning Rate"
BOLD2 = ["negative gradient", "Loss function", "w.r.t. W", "moving step is a hyper parameter", "AKA Learning Rate"]

def advance(text, size, bold=False):
    f = ImageFont.truetype(ARIALB if bold else ARIAL, size)
    return f.getlength(text)

for size in (14, 15, 16, 17):
    # measure mixed bold/regular line 2 at this size with wrap candidates
    print(f"  --- size {size}pt ---")
    print(f"  L1 reg: {advance(L1, size):.0f}px / bold: {advance(L1, size, True):.0f}px (measured row A w~323)")
    # try wrap points on space boundaries
    words = L2.split()
    for cutoff in range(8, len(words)):
        r1 = " ".join(words[:cutoff]); r2 = " ".join(words[cutoff:])
        w1 = advance(r1, size)  # approx (mixed bold not modeled yet)
        w2 = advance(r2, size)
        if 700 < w1 < 800 and 400 < w2 < 560:
            print(f"  wrap@{cutoff}: r1 w={w1:.0f} '{r1[:50]}...' r2 w={w2:.0f} '{r2[:40]}...'")
