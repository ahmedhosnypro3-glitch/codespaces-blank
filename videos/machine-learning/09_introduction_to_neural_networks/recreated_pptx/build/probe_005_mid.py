from PIL import Image
import numpy as np
from scipy import ndimage
import sys

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

white = (R > 244) & (G > 244) & (B > 244)
blue = (B - R > 60) & (B - G > 50) & (B > 90)
red = (R - G > 60) & (R - B > 60) & (R > 120)
dark = (~white) & (R < 140) & (G < 140) & (B < 140)
ink = (~white)


def runs_in_col(x, y0, y1, mask):
    col = mask[y0:y1 + 1, x]
    out = []
    start = None
    for i, v in enumerate(col):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((y0 + start, y0 + i - 1)); start = None
    if start is not None:
        out.append((y0 + start, y1))
    return out


print("=== LEFT PANEL: bracket column vertical ink runs (all non-white) ===")
for x in [116, 117, 118, 139, 140, 248, 249, 250, 271, 272, 273]:
    print(f"  x={x}: {runs_in_col(x, 90, 250, ink)}")

print("\n=== RIGHT PANEL: bracket column vertical ink runs ===")
for x in [591, 592, 593, 618, 619, 620]:
    print(f"  x={x}: {runs_in_col(x, 90, 250, ink)}")

print("\n=== MIDDLE BAND x 520..780: blue ink column counts (y 255..340) ===")
for x in range(520, 781):
    n = int(blue[255:341, x].sum())
    if n >= 8:
        print(f"  x={x}: blue={n} runs={runs_in_col(x, 255, 340, blue)}")

print("\n=== MIDDLE BAND x 520..800: any-ink tall columns (>=40 of 86 rows) ===")
for x in range(520, 801):
    n = int(ink[255:341, x].sum())
    if n >= 40:
        print(f"  x={x}: ink={n} runs={runs_in_col(x, 255, 340, ink)}")

print("\n=== MIDDLE BAND: all components (dark+blue+red), y 250..345 ===")
comp = ink.copy()
comp[250:346, :] = comp[250:346, :]
lab, n = ndimage.label(ndimage.binary_closing(comp[250:346], np.ones((3, 3))))
objs = ndimage.find_objects(lab)
rows = []
for i, sl in enumerate(objs):
    ys, xs = sl
    cnt = int((lab[sl] == i + 1).sum())
    if cnt < 8:
        continue
    y0, y1 = ys.start + 250, ys.stop + 249
    x0, x1 = xs.start, xs.stop - 1
    cls = []
    for name, m in (("R", red), ("B", blue), ("K", dark)):
        c = int(m[y0:y1 + 1, x0:x1 + 1].sum())
        if c > 5:
            cls.append(f"{name}{c}")
    rows.append((y0, x0, x1, y1, cnt, ",".join(cls)))
rows.sort()
for r in rows:
    print(f"  y[{r[0]:3d}..{r[3]:3d}] x[{r[1]:3d}..{r[2]:3d}] px={r[4]:4d} {r[5]}")
