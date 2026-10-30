#!/usr/bin/env python3
"""Pass 4: per-column band analysis (dots), curve centerlines, arrowheads,
tiny valley arrow, text row profiles, empirical font matching."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
blue = (b - r > 45) & (b > 110)  # curve+dots (border is b-r~90 but darker; both catch)

print("== LEFT PANEL: per-column blue bands (dot = tall band) ==")
# region: inside border, left of divider ~475
lmask = blue[:, :476].copy()
lmask[:140, :] = False; lmask[462:, :] = False
dotsL = []
x = 100
while x < 476:
    col = np.where(lmask[:, x])[0]
    if len(col):
        # contiguous bands in this column
        bands = []
        s = col[0]; p = col[0]
        for yy in col[1:]:
            if yy > p + 2:
                bands.append((s, p)); s = yy
            p = yy
        bands.append((s, p))
        if len(bands) == 1 and (bands[0][1] - bands[0][0]) >= 7:
            dotsL.append((x, (bands[0][0] + bands[0][1]) / 2, bands[0][1] - bands[0][0] + 1))
    x += 1
# cluster dot columns
print("  tall-band columns (x, y-mid, band-h):")
cl = []
for d in dotsL:
    if cl and d[0] - cl[-1][-1][0] <= 2:
        cl[-1].append(d)
    else:
        cl.append([d])
for grp in cl:
    xs = [d[0] for d in grp]; ys = [d[1] for d in grp]; hs = [d[2] for d in grp]
    if len(xs) >= 2:
        print(f"    DOT: cx={sum(xs)/len(xs):.1f} cy={sum(ys)/len(ys):.1f} "
              f"cols {min(xs)}-{max(xs)} h~{max(hs)}")
    else:
        print(f"    single {grp}")

print("\n== RIGHT PANEL: per-column blue bands ==")
rmask = blue.copy()
rmask[:, :480] = False; rmask[:, 855:] = False
rmask[:140, :] = False; rmask[462:, :] = False
dotsR = []
x = 480
while x < 855:
    col = np.where(rmask[:, x])[0]
    if len(col):
        bands = []
        s = col[0]; p = col[0]
        for yy in col[1:]:
            if yy > p + 2:
                bands.append((s, p)); s = yy
            p = yy
        bands.append((s, p))
        if len(bands) == 1 and (bands[0][1] - bands[0][0]) >= 8:
            dotsR.append((x, (bands[0][0] + bands[0][1]) / 2, bands[0][1] - bands[0][0] + 1))
    x += 1
cl = []
for d in dotsR:
    if cl and d[0] - cl[-1][-1][0] <= 2:
        cl[-1].append(d)
    else:
        cl.append([d])
for grp in cl:
    xs = [d[0] for d in grp]; ys = [d[1] for d in grp]; hs = [d[2] for d in grp]
    if len(xs) >= 2:
        print(f"    DOT: cx={sum(xs)/len(xs):.1f} cy={sum(ys)/len(ys):.1f} "
              f"cols {min(xs)}-{max(xs)} h~{max(hs)}")
    else:
        print(f"    single {grp}")

print("\n== CURVE CENTERLINES (every 8 cols; single-band columns only) ==")
def trace(mask, x0, x1, label):
    pts = []
    for x in range(x0, x1):
        col = np.where(mask[:, x])[0]
        if len(col):
            bands = []
            s = col[0]; p = col[0]
            for yy in col[1:]:
                if yy > p + 2:
                    bands.append((s, p)); s = yy
                p = yy
            bands.append((s, p))
            if len(bands) == 1:
                pts.append((x, (bands[0][0] + bands[0][1]) / 2))
    print(f"  {label}: {len(pts)} pts")
    step = max(1, len(pts) // 24)
    print("   ", " ".join(f"({p[0]},{p[1]:.0f})" for p in pts[::step]))
    return pts

lm2 = blue.copy(); lm2[:, :150] = False; lm2[:, 480:] = False; lm2[:150, :] = False; lm2[448:, :] = False
ptsL = trace(lm2, 150, 480, "LEFT curve")
rm2 = blue.copy(); rm2[:, :480] = False; rm2[:, 850:] = False; rm2[:150, :] = False; rm2[448:, :] = False
ptsR = trace(rm2, 480, 850, "RIGHT curve")

print("\n== Y-AXIS TOP ARROWHEADS ==")
red_ink = (r > 120) & ((r - g) > 40) & ((r - b) > 40)
for label_, (x0, x1, y0, y1) in [("LEFT ytop", (145, 175, 200, 225)), ("RIGHT ytop", (498, 528, 196, 222))]:
    print(f"  {label_}:")
    for yy in range(y0, y1):
        row = np.where(red_ink[yy, x0:x1])[0]
        if len(row):
            print(f"    y={yy}: x {x0+row.min()}-{x0+row.max()} n={len(row)}")

print("\n== TINY BLACK ARROW near left valley (loose dark scan x 230..300, y 415..465) ==")
darkish = (r < 150) & (g < 150) & (b < 150) & ((r + g + b) < 420)
for yy in range(415, 465):
    row = np.where(darkish[yy, 230:300])[0]
    if len(row):
        print(f"  y={yy}: x {230+row.min()}-{230+row.max()} n={len(row)}")

print("\n== HEADING ROW PROFILES ==")
darkm = (r < 120) & (g < 120) & (b < 120)
for label_, (x0, x1) in [("LEFT heading", (235, 380)), ("RIGHT heading", (585, 726))]:
    print(f"  {label_}:")
    for yy in range(184, 204):
        row = np.where(darkm[yy, x0:x1])[0]
        if len(row):
            print(f"    y={yy}: x {x0+row.min()}-{x0+row.max()} n={len(row)}")

print("\n== LOSS LABEL ROW PROFILES ==")
for label_, (x0, x1, y0, y1) in [("left Loss", (118, 150, 218, 234)), ("right Loss", (472, 502, 214, 230))]:
    print(f"  {label_}:")
    for yy in range(y0, y1):
        row = np.where(darkm[yy, x0:x1])[0]
        if len(row):
            print(f"    y={yy}: x {x0+row.min()}-{x0+row.max()} n={len(row)}")

print("\n== VALUE-OF-WEIGHT LABEL PROFILES ==")
for label_, (x0, x1, y0, y1) in [("left VoW", (255, 460, 442, 464)), ("right VoW", (705, 805, 446, 465))]:
    print(f"  {label_}:")
    for yy in range(y0, y1):
        row = np.where(darkm[yy, x0:x1])[0]
        if len(row):
            print(f"    y={yy}: x {x0+row.min()}-{x0+row.max()} n={len(row)}")

print("\n== EMPIRICAL FONT MATCH (Liberation Sans == Arial metrics proxy) ==")
import glob
cands = glob.glob("/usr/share/fonts/**/LiberationSans-[Rr]egular.ttf", recursive=True) + \
        glob.glob("/usr/share/fonts/**/LiberationSans-[Bb]old.ttf", recursive=True)
print("  fonts found:", cands[:4])


def ink_metrics(text, fontpath, size_pt, bold=False):
    f = ImageFont.truetype(fontpath, size_pt)
    img = Image.new("L", (1400, 160), 255)
    dr = ImageDraw.Draw(img)
    dr.text((20, 30), text, font=f, fill=0)
    arr = np.asarray(img)
    ys, xs = np.where(arr < 128)
    if not len(ys):
        return None
    return xs.max() - xs.min() + 1, ys.min(), ys.max(), xs.min(), xs.max()


if cands:
    reg = [c for c in cands if "egular" in c][0]
    bold_ = [c for c in cands if "old" in c][0]
    for size in (22, 24, 26, 28, 30):
        w, y0, y1, _, _ = ink_metrics("Effect of small and large Learning Rate", bold_, size)
        print(f"  TITLE bold {size}pt: ink w={w} h={y1-y0+1} ytop={30+y0} (target w=499 h=30)")
    for size in (12, 13, 14, 15, 16):
        w, y0, y1, _, _ = ink_metrics("Small Learning Rate", bold_, size)
        print(f"  HEADING bold {size}pt: ink w={w} h={y1-y0+1} (target w=134 h~12)")
    for size in (9, 10, 11):
        w, y0, y1, _, _ = ink_metrics("Value of weight", reg, size)
        print(f"  VoW reg {size}pt: w={w} h={y1-y0+1} (target w=88 h~13)")
        w, y0, y1, _, _ = ink_metrics("Loss", reg, size)
        print(f"  Loss reg {size}pt: w={w} h={y1-y0+1} (target w=23 h~7)")
