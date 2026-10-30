"""Adjudication v5b — color-separated ink analysis of slide 004 original."""
from PIL import Image
import numpy as np

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"

o = Image.open(ORIG).convert("RGB")
a = np.asarray(o).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# ink classes
red   = (R > 110) & (R - G > 55) & (R - B > 55)
blue  = (B > 100) & (B - R > 30) & (B - G > 15)
black = (R < 110) & (G < 110) & (B < 110) & ~(red | blue)
print("counts: red", int(red.sum()), "blue", int(blue.sum()), "black", int(black.sum()))


def bbox(mask, x0, x1, y0, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if not len(ys):
        return None
    return (int(xs.min())+x0, int(ys.min())+y0, int(xs.max())+x0, int(ys.max())+y0)


def rowbands(mask, x0, x1, y0, y1, gap=4, minpx=2):
    sub = mask[y0:y1, x0:x1]
    cnt = sub.sum(axis=1)
    bands = []
    cur = None
    for i, c in enumerate(cnt):
        if c >= minpx:
            if cur is None or i - cur[1] < gap:
                cur = [cur[0] if cur else i, i]
            else:
                bands.append((cur[0]+y0, cur[1]+y0)); cur = [i, i]
        else:
            if cur is not None and i - cur[1] >= gap:
                bands.append((cur[0]+y0, cur[1]+y0)); cur = None
    if cur is not None:
        bands.append((cur[0]+y0, cur[1]+y0))
    return bands


def colbands(mask, x0, x1, y0, y1, gap=8, minpx=2):
    sub = mask[y0:y1, x0:x1]
    cnt = sub.sum(axis=0)
    bands = []
    cur = None
    for i, c in enumerate(cnt):
        if c >= minpx:
            if cur is None or i - cur[1] < gap:
                cur = [cur[0] if cur else i, i]
            else:
                bands.append((cur[0]+x0, cur[1]+x0)); cur = [i, i]
        else:
            if cur is not None and i - cur[1] >= gap:
                bands.append((cur[0]+x0, cur[1]+x0)); cur = None
    if cur is not None:
        bands.append((cur[0]+x0, cur[1]+x0))
    return bands


print()
print("=" * 74)
print("TOP BOXES — colour-separated row bands (interior only, borders excluded)")
print("=" * 74)
for name, ix0, ix1, iy0, iy1 in [
    ("LEFT  Let Y  box",   84, 392, 103, 219),
    ("RIGHT Let Yh box", 431, 742, 103, 219),
]:
    print(f"\n--- {name}  interior x{ix0}..{ix1} y{iy0}..{iy1} ---")
    for mask, label in [(black, "BLACK"), (red, "RED"), (blue, "BLUE")]:
        rb = rowbands(mask, ix0, ix1, iy0, iy1)
        if not rb:
            continue
        print(f"  {label} row bands: {rb}")
        for (y0, y1) in rb:
            print(f"      y{y0}..{y1}  bbox={bbox(mask, ix0, ix1, y0, y1+2)}  cols={colbands(mask, ix0, ix1, y0, y1+2)}")
