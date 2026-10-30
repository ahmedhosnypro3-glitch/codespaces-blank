#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_040.jpg (960x540, 1px = 1pt = 1/72in).
Measures the title block (red/blue ink), the badge, the bottom-center icon, and
verifies the house chrome family geometry. Banked per the deck's measurement law.
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_040.jpg"
).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
print(f"frame: {W}x{H}")

def band(mask, name, min_count=6):
    rows = np.where(mask.sum(axis=1) >= min_count)[0]
    if not len(rows):
        print(f"{name}: none")
        return
    print(f"{name}: rows {rows.min()}..{rows.max()}")
    # per contiguous row group, report x extent
    groups = []
    start = rows[0]
    prev = rows[0]
    for y in rows[1:]:
        if y - prev > 3:
            groups.append((start, prev))
            start = y
        prev = y
    groups.append((start, prev))
    for (y0, y1) in groups:
        sub = mask[y0:y1 + 1, :]
        cols = np.where(sub.any(axis=0))[0]
        print(f"   band y {y0}..{y1}: x {cols.min()}..{cols.max()}  px={sub.sum()}")

# --- text ink masks -------------------------------------------------------
# Red text: r dominant. Blue text: b dominant. Thresholds set above the
# background: canvas white (255) + panel gray E9E9E7 (231,233,230).
red = (r > 120) & (r - g > 60) & (r - b > 60)
blue = (b > 120) & (b - r > 60) & (b - g > 40)
dark = (r + g + b) < 240
print("\n== TEXT INK ==")
band(red, "red ink")
band(blue, "blue ink")
band(dark, "dark ink (all, for icon/numeral)")

# --- title block core colors (sample cores) -------------------------------
def core_color(mask, name):
    ys, xs = np.where(mask)
    if not len(ys):
        return
    sel = (r[ys, xs] > 150) & (g[ys, xs] < 120)
    yy, xx = ys[sel], xs[sel]
    if len(yy):
        print(f"{name} core sample (median of strong px): "
              f"r={int(np.median(r[yy, xx]))} g={int(np.median(g[yy, xx]))} b={int(np.median(b[yy, xx]))}")
core_color(red, "red")

# --- badge (yellow FDFD96 + ring) ----------------------------------------
print("\n== BADGE ==")
yel = (r > 200) & (g > 200) & (b < 190) & (b > 60)
ys, xs = np.where(yel)
if len(ys):
    print(f"yellow mask: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} "
          f"count={len(ys)} center=({(xs.min()+xs.max())/2:.1f},{(ys.min()+ys.max())/2:.1f}) "
          f"w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1}")
pur = (b > 150) & (r > 70) & (r < 180) & (g < 130)
ys, xs = np.where(pur)
if len(ys):
    print(f"purple-ring mask: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} count={len(ys)}")

# --- badge numeral ink ----------------------------------------------------
print("\n== BADGE NUMERAL ==")
bx0, bx1, by0, by1 = 858, 895, 55, 92  # window around measured badge center (876,73) d~35
win = im[by0:by1, bx0:bx1]
dark = (win.sum(axis=2) < 330)
ys, xs = np.where(dark)
if len(ys):
    print(f"numeral ink in window: x {bx0+xs.min()}..{bx0+xs.max()} y {by0+ys.min()}..{by0+ys.max()} count={dark.sum()}")

# --- bottom-center icon ---------------------------------------------------
print("\n== BOTTOM-CENTER REGION (y 400..540, x 380..580) ==")
sub = im[400:540, 380:580]
# any non-gray, non-red ink (icon is white/black per spec)
lg = (abs(sub[:, :, 0] - 231) < 12) & (abs(sub[:, :, 1] - 233) < 12) & (abs(sub[:, :, 2] - 230) < 12)
redish = (sub[:, :, 0] > 120) & (sub[:, :, 0] - sub[:, :, 1] > 60)
other = ~lg & ~redish
ys, xs = np.where(other)
if len(ys):
    print(f"non-gray non-red ink: x {380+xs.min()}..{380+xs.max()} y {400+ys.min()}..{400+ys.max()} count={other.sum()}")
else:
    print("none found with that mask")

# --- chrome verification --------------------------------------------------
print("\n== CHROME ==")
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
band_rows = slice(65, 525)
cols = np.where(gray[band_rows].sum(axis=0) > (band_rows.stop - band_rows.start) * 0.5)[0]
if len(cols):
    print(f"panel gray: x {cols.min()}..{cols.max()} (canon 54..903)")
band_cols = slice(74, 134)
rows = np.where(gray[:, band_cols].sum(axis=1) > (band_cols.stop - band_cols.start) * 0.5)[0]
if len(rows):
    print(f"panel top (left band): y {rows.min()}..{rows.max()} (canon top 45, bottom at edge)")
redch = (r > 90) & (r - g > 40) & (r - b > 10)
bot = np.where(redch[533:, :].sum(axis=0) > 1)[0]
print(f"bottom stroke cols: {bot.min()}..{bot.max()} (canon 58..902)" if len(bot) else "bottom stroke: none")
mid = redch[250:290, :]
lcols = np.where(mid[:, :62].sum(axis=0) > 2)[0]
rcols = np.where(mid[:, 898:].sum(axis=0) > 2)[0] + 898
print(f"left stroke cols: {lcols.min()}..{lcols.max()} (canon 58-59)" if len(lcols) else "left stroke: none")
print(f"right stroke cols: {rcols.min()}..{rcols.max()} (canon 901)" if len(rcols) else "right stroke: none")
topband = redch[44:52, 80:880]
print(f"TOP BAND red px = {topband.sum()} (must be 0 for this deck)")
