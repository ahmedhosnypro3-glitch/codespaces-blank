#!/usr/bin/env python3
"""Independent PIL measurement of slide_021.jpg for the 021 build.
Banked values from the previous agent are annotated for cross-check."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
print("size", im.size)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = R.shape


def runs(vals, thr):
    out, start = [], None
    for i, v in enumerate(vals):
        if v > thr and start is None:
            start = i
        elif v <= thr and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(vals) - 1))
    return out


# ---- global long-line detection: find full-height columns / full-width rows that
#      are near a single saturated hue (red frame, blue frames, black bar).
def near(c, target, tol):
    return (R >= c[0] - tol) & (R <= c[0] + tol) & \
           (G >= c[1] - tol) & (G <= c[1] + tol) & \
           (B >= c[2] - tol) & (B <= c[2] + tol)


redish = (R - G > 40) & (R - B > 40)
blueish = (B - R > 40) & (B - G > 40)
dark = (R < 60) & (G < 60) & (B < 60)
pinkish = (R - B > 12) & (R > 200) & (G > 150) & (G < R) & (np.abs(G - B) < 45)

print("\n-- long red columns (>100 px):",
      [(i, int(redish[:, i].sum())) for i in range(W) if redish[:, i].sum() > 100])
print("-- long red rows (>100 px):",
      [(i, int(redish[i].sum())) for i in range(H) if redish[i].sum() > 100])
print("-- long blue columns (>100 px):",
      [(i, int(blueish[:, i].sum())) for i in range(W) if blueish[:, i].sum() > 100])
print("-- long blue rows (>100 px):",
      [(i, int(blueish[i].sum())) for i in range(H) if blueish[i].sum() > 100])
print("-- long dark rows (>400 px):",
      [(i, int(dark[i].sum())) for i in range(H) if dark[i].sum() > 400])
print("-- long dark columns (>400 px):",
      [(i, int(dark[:, i].sum())) for i in range(W) if dark[:, i].sum() > 400])

# ---- pink formula boxes: pinkish fill bounding boxes via row/col projections
pr = pinkish.sum(axis=1)
pc = pinkish.sum(axis=0)
print("\n-- pinkish row runs (>150):",
      [(s, e) for s, e in runs(pr, 150)])
print("-- pinkish col runs (>150):",
      [(s, e) for s, e in runs(pc, 150)])

# ---- pink box extents per quadrant
def quad(x0, x1, y0, y1):
    sub = pinkish[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs):
        return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())
    return None

for name, q in [("TL", (0, 480, 0, 270)), ("TR", (480, 960, 0, 270)),
                ("BL", (0, 480, 270, 540)), ("BR", (480, 960, 270, 540))]:
    print(f"  pink extents {name}:", quad(*q))

# ---- red border of pink boxes: redish pixels outside the outer frame
inner_red = redish.copy()
inner_red[42:518, 57:903] = False  # exclude outer frame
rr = inner_red.sum(axis=1)
rc = inner_red.sum(axis=0)
print("-- inner red row runs (>30):", [(s, e) for s, e in runs(rr, 30)])
print("-- inner red col runs (>30):", [(s, e) for s, e in runs(rc, 30)])

# ---- badge: yellow circle in top-right
yellow = (R > 240) & (G > 240) & (B < 200) & (B > 100)
ys, xs = np.nonzero(yellow)
if len(xs):
    print("\n-- yellow bbox:", xs.min(), xs.max(), ys.min(), ys.max(), "n=", len(xs))

# ---- sampled colors
print("\n-- sampled colors")
for label, (x, y) in [("bg mid-gap", (470, 200)), ("bg corner", (20, 20)),
                      ("pink fill TL", (200, 80)), ("pink fill TR", (700, 80)),
                      ("pink fill BL", (200, 310)), ("pink fill BR", (700, 310)),
                      ("plot white TL", (160, 200)), ("blue frame TL", (122, 190)),
                      ("red outer frame", (57, 300)),
                      ("badge fill", (876, 60)),
                      ("black bar", (200, 528)),
                      ("gridline TL", (260, 189))]:
    print(f"  {label} @({x},{y}) = {tuple(a[y, x])}")

# ---- blue graph frames (borders) extents
for name, (x0, y0, x1, y1) in [("TL", (0, 0, 480, 540)), ("TR", (480, 0, 960, 540)),
                               ("BL", (0, 0, 480, 540)), ("BR", (480, 0, 960, 540))]:
    sub = blueish[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs):
        print(f"  blue ink bbox {name}: x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}")
