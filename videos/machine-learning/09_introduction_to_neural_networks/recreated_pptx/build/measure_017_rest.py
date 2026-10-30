#!/usr/bin/env python3
"""Remaining geometry for slide 017: top-right label box, title, graph internals,
and true RGB of the equation-box text regions."""
import numpy as np
from PIL import Image

SRC = "unique_slides/slide_017.jpg"
a = np.array(Image.open(SRC).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

PEACH = np.array([251, 234, 216])


def bbox(m, name):
    ys, xs = np.where(m)
    if len(ys) == 0:
        print(f"{name}: none")
        return
    print(f"{name}: rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} px={len(ys)}")


print("=== peach fill, top-right quadrant x560-900 y60-320 ===")
peach = (np.abs(a - PEACH).sum(axis=2) <= 26)
sub = peach[60:320, 560:900]
ys, xs = np.where(sub)
print("  peach bbox rows", ys.min() + 60, ys.max() + 60,
      "cols", xs.min() + 560, xs.max() + 560)
rowc = sub.sum(axis=1)
for i, v in enumerate(rowc):
    if v > 3:
        print(f"   y={i+60}: n={v}")

print("\n=== red outline near top-right label box ===")
red = (R > 110) & (G < 100) & (B < 100) & (R - G > 55) & (R - B > 55)
reg = red[60:320, 560:900]
ys, xs = np.where(reg)
print("  red bbox rows", ys.min() + 60, ys.max() + 60,
      "cols", xs.min() + 560, xs.max() + 560, "px", len(ys))
rowc = reg.sum(axis=1)
print("  rows with red:", [(int(i + 60), int(v)) for i, v in enumerate(rowc) if v > 3])
colc = reg.sum(axis=0)
print("  cols with red:", [(int(i + 560), int(v)) for i, v in enumerate(colc) if v > 2])

print("\n=== top-right box text ink ===")
black = (R < 95) & (G < 95) & (B < 95)
for (x0, x1, y0, y1, nm) in [(600, 820, 150, 230, "label text area")]:
    m = black[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {nm} black: rows {ys.min()+y0}-{ys.max()+y0} cols {xs.min()+x0}-{xs.max()+x0}")
        for y in range(y0, y1):
            rr = np.where(black[y, x0:x1])[0] + x0
            if len(rr):
                print(f"    y={y}: {rr.min()}-{rr.max()} n={len(rr)}")
    m2 = red[y0:y1, x0:x1]
    ys2, xs2 = np.where(m2)
    if len(ys2):
        print(f"  {nm} RED: rows {ys2.min()+y0}-{ys2.max()+y0} cols {xs2.min()+x0}-{xs2.max()+x0}")
        for y in range(y0, y1):
            rr = np.where(red[y, x0:x1])[0] + x0
            if len(rr):
                print(f"    y={y}: {rr.min()}-{rr.max()} n={len(rr)}")

print("\n=== TRUE RGB samples in bottom-left equation box ===")
samples = {
    "header F(x) x127-140 y476-490": (127, 140, 476, 490),
    "header mid x174-238 y477-486": (174, 238, 477, 486),
    "header right x247-308 y478-486": (247, 308, 478, 486),
    "brace x324-326 y480-500": (324, 326, 480, 500),
    "value0 x331-336 y472-484": (331, 336, 472, 484),
    "value1 x331-334 y489-497": (331, 334, 489, 497),
    "cond1 x352-404 y472-482": (352, 404, 472, 482),
    "cond2 x349-404 y490-499": (349, 404, 490, 499),
}
for nm, (x0, x1, y0, y1) in samples.items():
    reg = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    dark = reg[reg.sum(axis=1) < 600]
    print(f"  {nm}: darkest-5 mean RGB {dark.mean(axis=0).round(1) if len(dark) else 'n/a'} "
          f"n={len(dark)} min={dark.min(axis=0) if len(dark) else '-'}")

print("\n=== title (dark red) bbox ===")
darkred = (R > 90) & (R < 220) & (G < 90) & (B < 90) & (R - G > 50)
ys, xs = np.where(darkred[:120, :])
print("  rows", ys.min(), ys.max(), "cols", xs.min(), xs.max())
rowc = darkred[:120, :].sum(axis=1)
print("  rows with ink:", [(int(i), int(v)) for i, v in enumerate(rowc) if v > 2])
