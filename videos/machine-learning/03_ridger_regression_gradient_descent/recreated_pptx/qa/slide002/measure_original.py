#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_002.jpg (960x540, 1px=1pt).

Measures: canvas/panel/stroke chrome (vs house_chrome.js law), the two-line
red title (per-line ink bbox, cap height -> font size), the badge disc,
and the plus-sign artifact. All numbers in frame px.
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_002.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
print(f"frame {W}x{H}")

def stats(name, mask):
    ys, xs = np.where(mask)
    if not len(ys):
        print(f"{name}: NONE")
        return None
    print(f"{name}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(ys)}")
    return (xs.min(), xs.max(), ys.min(), ys.max())

# --- chrome: what does THIS frame's own chrome look like? ---
# corner colors
for label, (yy, xx) in {
    "corner TL (5,5)": (5, 5), "corner TR (5,954)": (5, 954),
    "panel mid (400,300)": (400, 300), "panel mid-left (300,70)": (300, 70),
    "above panel (20,480)": (20, 480), "left margin (300,20)": (300, 20),
    "right margin (300,950)": (300, 950),
}.items():
    print(f"  {label}: rgb={tuple(IM[yy, xx])}")

# gray panel mask (E9E9E7 ~ (233,233,231))
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
stats("gray panel", gray)

# red strokes (dark-maroon JPEG family + C00000)
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
top = red[0:50, :]
print(f"top band red px: {top.sum()}")
bot = red[520:, :]
ys, xs = np.where(bot)
if len(xs):
    print(f"bottom stroke: x {xs.min()}..{xs.max()}  y {ys.min()}+520..{ys.max()}+520")
midl = red[250:290, 0:100]
ys, xs = np.where(midl)
if len(xs):
    print(f"left stroke @mid: x {xs.min()}..{xs.max()}  y {ys.min()+250}..{ys.max()+250}")
midr = red[250:290, 900:960]
ys, xs = np.where(midr)
if len(xs):
    print(f"right stroke @mid: x {900+xs.min()}..{900+xs.max()}  y {ys.min()+250}..{ys.max()+250}")

# --- badge: yellow disc ---
yel = (r > 200) & (g > 200) & (b < 190)
bb = stats("badge yellow", yel)
if bb:
    xs0, xs1, ys0, ys1 = bb
    print(f"  badge center=({(xs0+xs1)/2:.1f},{(ys0+ys1)/2:.1f}) d={(xs1-xs0+1)}x{(ys1-ys0+1)}")
    # sample ring color around the disc edge
    cx, cy = int((xs0 + xs1) / 2), int((ys0 + ys1) / 2)
    rad = (xs1 - xs0) / 2
    ring = []
    import math
    for a in range(0, 360, 30):
        x = int(cx + rad * math.cos(math.radians(a)))
        y = int(cy + rad * math.sin(math.radians(a)))
        if 0 <= x < W and 0 <= y < H:
            ring.append(tuple(IM[y, x]))
    print(f"  ring samples: {ring}")

# --- title: red text (FF0000-ish; JPEG may darken) ---
# title red: strong red, more permissive than stroke mask but g/b low
tit = (r > 150) & (g < 110) & (b < 110)
ys, xs = np.where(tit)
if len(ys):
    print(f"\ntitle red ink: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(ys)}")
    # row profile to find the two line bands
    rowsum = tit.sum(axis=1)
    rows = np.where(rowsum > 0)[0]
    # segment into bands separated by >=3 empty rows
    bands = []
    start = rows[0]
    prev = rows[0]
    for y in rows[1:]:
        if y - prev > 3:
            bands.append((start, prev))
            start = y
        prev = y
    bands.append((start, prev))
    for i, (y0, y1) in enumerate(bands):
        band = tit[y0:y1 + 1, :]
        bys, bxs = np.where(band)
        print(f"  line {i+1}: y {y0}..{y1} (h={y1-y0+1})  x {bxs.min()}..{bxs.max()} (w={bxs.max()-bxs.min()+1})")
        # column profile within band to find word gaps
        colsum = band.sum(axis=0)
        # print gap structure: runs of empty columns inside the band
        gaps = []
        in_gap = False
        for x in range(bxs.min(), bxs.max() + 1):
            if colsum[x] == 0 and not in_gap:
                in_gap = True
                gs = x
            elif colsum[x] > 0 and in_gap:
                in_gap = False
                if x - gs >= 5:
                    gaps.append((gs, x - 1))
        if in_gap:
            gaps.append((gs, bxs.max()))
        print(f"    word gaps (>=5px): {gaps}")
    # sample title ink color (core pixels)
    core = np.where(tit)
    cr = r[core].mean()
    print(f"  title ink mean rgb: ({cr:.0f},{g[core].mean():.0f},{b[core].mean():.0f})")
else:
    print("NO title red ink found")

# --- plus sign: gray artifact near top-center-right (x 749-806, y 43-65 per spec) ---
# gray ~ 808080: low saturation, mid value
grayish = (abs(r - g) < 25) & (abs(g - b) < 25) & (r > 60) & (r < 200)
zone = grayish[20:120, 700:860]
ys, xs = np.where(zone)
if len(ys):
    print(f"\ngrayish zone (y20-120,x700-860): x {700+xs.min()}..{700+xs.max()}  y {20+ys.min()}..{20+ys.max()}  n={len(ys)}")
    # connected structure: row and column profiles
    rp = zone.sum(axis=1)
    cp = zone.sum(axis=0)
    print(f"  row profile nonzero rows: {[20+y for y in np.where(rp>0)[0]]}")
    print(f"  col profile nonzero cols: {[700+x for x in np.where(cp>0)[0]]}")
else:
    print("\nno grayish ink in plus-sign zone")

# full slide: any other ink outside known regions? (non-bg, non-panel, non-chrome)
other = (~(gray | yel | red | (r > 200) & (g > 200) & (b > 200))) & (~grayish)
ys, xs = np.where(other[60:500, :])
if len(ys):
    print(f"\n'other' ink in content zone: n={len(ys)} sample x {xs.min()}..{xs.max()} y {60+ys.min()}..{60+ys.max()}")
