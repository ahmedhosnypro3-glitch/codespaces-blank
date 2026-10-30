#!/usr/bin/env python3
"""Self-check for slide 033 attempt 1: render vs original frame.
Measures key elements against the ORIGINAL frame (frame px) at 150dpi render scale.
1px frame = 1pt; render scale = 2001/960 = 2.084375 render-px per frame-px.
"""
import sys
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide033/render_1.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
OH, OW = o.shape[:2]
RH, RW = r.shape[:2]
S = RH / 540.0   # render px per frame px (should be ~2.084)
print(f"orig {OW}x{OH}  render {RW}x{RH}  scale={S:.4f}")
fails = []

def cv(v):  # frame px -> render px
    return int(round(v * S))

def rr(v):  # render px -> frame px
    return v / S

# ---------- helper masks on the RENDER ----------
R_r, R_g, R_b = r[:, :, 0], r[:, :, 1], r[:, :, 2]
O_r, O_g, O_b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

def red_mask(a_r, a_g, a_b):
    return (a_r > 90) & ((a_r - a_g) > 40) & ((a_r - a_b) > 10)

def green_mask(a_r, a_g, a_b):
    return (a_g > 100) & ((a_g - a_r) > 25) & ((a_g - a_b) > 25)

def purple_mask(a_r, a_g, a_b):
    return (a_g < 140) & (a_b > 130) & (a_b - a_g > 25) & (a_r < 180) & (a_b - a_r > 25)

def yellow_mask(a_r, a_g, a_b):
    return (a_r > 200) & (a_g > 200) & (a_b < 190)

def gray_mask(a_r, a_g, a_b):
    return (np.abs(a_r - 233) < 16) & (np.abs(a_g - 233) < 16) & (np.abs(a_b - 231) < 18)

# ---------- 0. smoothness of the green curve (second-difference ripple) ----------
# Extract the green curve centreline from the render and check ripple.
cur = green_mask(R_r, R_g, R_b)
ys, xs = np.where(cur)
if len(ys) < 50:
    fails.append(f"green curve: only {len(ys)} px found on render")
else:
    print(f"green ink on render: rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}  ({len(ys)} px)")
    # group by column, take median y -> centreline; then second-difference ripple
    col = {}
    for y, x in zip(ys, xs):
        col.setdefault(int(x), []).append(int(y))
    cx = sorted(col)
    cy = np.array([np.median(col[c]) for c in cx], dtype=float)
    if len(cy) > 10:
        d2 = np.diff(cy, 2)
        ripple = float(np.nanstd(d2))
        print(f"curve cols {cx[0]}..{cx[-1]} ({len(cx)} cols); second-diff std={ripple:.3f}px "
              f"max|d2|={np.nanmax(np.abs(d2)):.3f}px")
        if ripple > 2.5:
            fails.append(f"curve second-difference ripple {ripple:.2f}px > 2.5px — not smooth")
        else:
            print("  -> curve appears smooth (ripple within tolerance)")

# ---------- 1. house chrome ----------
# panel gray extent on render
g = gray_mask(R_r, R_g, R_b)
cols = np.where(g.sum(axis=0) > RH * 0.3)[0]
rows_ = np.where(g[:, 100:180].sum(axis=1) > 80)[0]
if not len(cols) or not len(rows_):
    fails.append("panel gray not found on render")
else:
    fx0, fx1 = rr(cols.min()), rr(cols.max())
    fy0 = rr(rows_.min())
    print(f"panel: x {fx0:.0f}..{fx1:.0f} (canon 54..903), top y {fy0:.0f} (canon 45)")
    if abs(fx0 - 54) > 5 or abs(fx1 - 903) > 5:
        fails.append(f"panel x {fx0:.0f}..{fx1:.0f} vs 54..903")
    if abs(fy0 - 45) > 5:
        fails.append(f"panel top {fy0:.0f} vs 45")

# no top stroke
red_r = red_mask(R_r, R_g, R_b)
top_band = red_r[int(cv(44)): int(cv(52)), int(cv(80)): int(cv(880))]
print(f"top-band red px: {int(top_band.sum())} (must be ~0, no top stroke)")
if top_band.sum() > 30:
    fails.append(f"TOP STROKE PRESENT: {int(top_band.sum())} red px")

# badge
yel = yellow_mask(R_r, R_g, R_b)
ys, xs = np.where(yel[int(cv(40)):int(cv(110)), int(cv(830)):int(cv(925))])
if len(ys):
    bcx = 830 + xs.mean(); bcy = 40 + ys.mean()
    bw = xs.max() - xs.min() + 1
    print(f"badge: center ({rr(bcx):.0f},{rr(bcy):.0f}) d~{rr(bw):.0f} (canon 876,73 d35)")
    if abs(rr(bcx) - 876) > 5 or abs(rr(bcy) - 73) > 5:
        fails.append(f"badge center {rr(bcx):.0f},{rr(bcy):.0f} vs 876,73")

# ---------- 2. content presence vs original ----------
def ext(mask, x0, y0, x1, y1, label):
    """ink extent in frame px inside a frame-space window"""
    sub = mask[cv(y0):cv(y1), cv(x0):cv(x1)]
    ys, xs = np.where(sub)
    if not len(ys):
        print(f"{label}: NO INK in window")
        return None
    fx0e = x0 + xs.min() / S; fx1e = x0 + xs.max() / S
    fy0e = y0 + ys.min() / S; fy1e = y0 + ys.max() / S
    print(f"{label}: rows {fy0e:.0f}..{fy1e:.0f} cols {fx0e:.0f}..{fx1e:.0f} ({int(sub.sum())} px)")
    return fx0e, fy0e, fx1e, fy1e

print("--- content on ORIGINAL ---")
og_red = ext(red_mask(O_r, O_g, O_b), 330, 60, 620, 140, "title red (orig)")
og_blue = ((O_b > 200) & (O_r < 80) & (O_g < 80))
sub = og_blue[cv(80):cv(140), cv(330):cv(620)]
ys_, xs_ = np.where(sub)
if len(ys_):
    print(f"subtitle blue (orig): rows {80+ys_.min()/S:.0f}..{80+ys_.max()/S:.0f} cols {330+xs_.min()/S:.0f}..{330+xs_.max()/S:.0f}")
og_green = ext(green_mask(O_r, O_g, O_b), 615, 120, 930, 330, "green curve (orig)")
og_pur = ext(purple_mask(O_r, O_g, O_b), 615, 250, 930, 340, "purple callout (orig)")
o_yel = ext(yellow_mask(O_r, O_g, O_b), 615, 100, 930, 340, "yellow (orig, plot area)")

print("--- content on RENDER ---")
rg_red = ext(red_mask(R_r, R_g, R_b), 60, 60, 940, 540, "red (render)")
rg_green = ext(green_mask(R_r, R_g, R_b), 60, 60, 940, 540, "green curve (render)")
rg_pur = ext(purple_mask(R_r, R_g, R_b), 60, 60, 940, 540, "purple (render)")

def find(e, name, tol=12):
    if e is None:
        fails.append(f"{name}: missing on one side")
        return
    return e

# ---------- 3. table structure on the render ----------
# 17 columns, 9 rows: check vertical gridline count by scanning the table band
print("--- table grid on render ---")
band = slice(cv(335), cv(515))
# count columns whose column has strong vertical-line ink (dark, low variance)
colscore = []
for c in range(cv(20), cv(940), 3):
    colpix = r[band, c]
    lum = colpix.sum(axis=1)
    # a gridline column is mostly uniform dark-ish OR mostly uniform fill with few transitions
    dark = (lum < 300).mean()
    colscore.append((c, dark))
# count vertical gridlines via transitions along a data row
trow = cv(370)
cols_tr = []
for c in range(cv(20), cv(940)):
    a = r[trow, c]; b = r[trow, c+1]
    d = abs(int(a[0])-int(b[0])) + abs(int(a[1])-int(b[1])) + abs(int(a[2])-int(b[2]))
    if d > 90:
        cols_tr.append(c)
print(f"row {trow//1} strong vertical transitions at render cols: {[int(rr(c)) for c in cols_tr][:25]} (frame px)")

# horizontal gridlines via transitions along a data column
tcol = cv(300)
rows_tr = []
for y in range(cv(330), cv(520)):
    a = r[y, tcol]; b = r[y+1, tcol]
    d = abs(int(a[0])-int(b[0])) + abs(int(a[1])-int(b[1])) + abs(int(a[2])-int(b[2]))
    if d > 90:
        rows_tr.append(y)
print(f"col {tcol//1} strong horizontal transitions at render rows: {[int(rr(y)) for y in rows_tr][:20]} (frame px)")

# table extent (any ink in the bottom band)
sub_ink = (r[cv(330):cv(520), cv(20):cv(940)].sum(axis=2) < 700)
ys_, xs_ = np.where(sub_ink)
if len(ys_):
    print(f"table ink extent: rows {330+ys_.min()/S:.0f}..{330+ys_.max()/S:.0f} cols {20+xs_.min()/S:.0f}..{20+xs_.max()/S:.0f}")
    if 330 + ys_.max()/S > 530:
        fails.append(f"table ink spills past y={330+ys_.max()/S:.0f} (bottom panel is 540, must stay inside)")

# ---------- 4. equation image present ----------
print("--- equation asset ---")
import os
eq = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/eq_033_main.png"
if os.path.exists(eq):
    eim = Image.open(eq)
    print(f"eq_033_main.png {eim.size} mode={eim.mode}")
    if eim.mode != "RGBA":
        fails.append(f"equation PNG mode {eim.mode} (want RGBA transparent)")
else:
    fails.append("equation PNG missing")

# verify the equation image is embedded in the render at the expected box
eqwin = r[cv(185):cv(230), cv(360):cv(640)]
darkish = (eqwin.sum(axis=2) < 650).sum()
print(f"equation window darkish px: {int(darkish)}")
if darkish < 200:
    fails.append("equation region nearly empty on render — image may not have embedded")

# ---------- 5. frame containment of every content block ----------
print("--- containment ---")
# title / subtitle must stay left of the plot (x<600)
sub_dark = (r[cv(60):cv(140), cv(560):cv(940)].sum(axis=2) < 600)
n = int(sub_dark.sum())
print(f"ink in cols 560-940 rows 60-140 (plot-side of title block): {n} px")
if n > 400:
    fails.append(f"title/subtitle ink crosses into plot region ({n} px)")

print()
if fails:
    print("SELFCHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELFCHECK: PASS")