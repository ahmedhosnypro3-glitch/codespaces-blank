#!/usr/bin/env python3
"""Locate node circles + labels in slides 33/34 originals via color masks."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

n = sys.argv[1]
base = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
        "10_nn_training_and_example")
a = np.asarray(Image.open(f"{base}/unique_slides/slide_0{n}.jpg").convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
PX = 13.33 / 960.0
def inch(pxv): return pxv * PX

def report(mask, name, min_px=40, panel=None):
    lab, cnt = ndimage.label(mask)
    out = []
    for i in range(1, cnt + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px:
            continue
        if panel:
            cy = (ys.min() + ys.max()) / 2
            if not (panel[0] <= cy <= panel[1]):
                continue
        out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(ys)))
    print(f"-- {name}: {len(out)}")
    for c in sorted(out, key=lambda t: (t[1], t[0])):
        cx, cy = (c[0]+c[2])/2, (c[1]+c[3])/2
        print(f"   x={c[0]}-{c[2]} y={c[1]}-{c[3]} (w={c[2]-c[0]+1} h={c[3]-c[1]+1}) "
              f"center_px=({cx:.0f},{cy:.0f}) center_in=({inch(cx):.2f},{inch(cy):.2f}) px={c[4]}")

# pale yellow fill (hidden nodes): high r,g, b~180-210
pale_yellow = (r > 230) & (g > 220) & (b > 150) & (b < 215) & ((r - b) > 40)
# orange fill: r high, g mid, b low
orange = (r > 230) & (g > 120) & (g < 200) & (b < 110) & ((r - b) > 130)
# gold/yellow strong
strong_yellow = (r > 240) & (g > 190) & (b < 120) & ((r - b) > 140)
# cyan/light blue fill
cyan = (b > 150) & (g > 150) & (r < 180) & ((b - r) > 40)
# blue text/fill (royal)
blue = (b > 130) & ((b - r) > 50) & ((b - g) > 30)
# black nodes: very dark blobs that are roundish
black = (r < 70) & (g < 70) & (b < 70)
# red text/lines
red = (r > 120) & ((r - g) > 50) & ((r - b) > 40) & (g < 120)
# green
green = (g > 100) & ((g - r) > 30) & ((g - b) > 30)

print(f"=== slide {n} {W}x{H} ===")
if n == '33':
    report(pale_yellow, "PALE-YELLOW fill", 40)
    report(orange, "ORANGE fill", 40)
    report(strong_yellow, "STRONG YELLOW (badge?)", 40)
    report(cyan, "CYAN fill", 40)
    report(black, "BLACK blobs", 30)
    report(blue, "BLUE text", 25)
    report(red, "RED text/lines", 25)
else:
    # slide 34: network occupies top-right y<200, table y>200
    for m, nm in [(pale_yellow, "PALE-YELLOW"), (orange, "ORANGE"), (strong_yellow, "YELLOW"),
                  (cyan, "CYAN"), (black, "BLACK"), (blue, "BLUE text"), (red, "RED"), (green, "GREEN")]:
        report(m, nm + " [top y<200]", 25, panel=(0, 200))
        report(m, nm + " [bottom y>=200]", 25, panel=(200, 540))
