#!/usr/bin/env python3
"""Measure slide_029.jpg (960x540, 1px=1pt): title text geometry, colors, pitch.

The slide's only content: 3 centered lines of bold red title text in the middle
band, plus house chrome (gray panel, red strokes, yellow badge).
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_029.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame {W}x{H}")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# red text mask (dark red C00000 family; JPEG may darken)
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
# exclude the border strokes region by scanning only the inner panel area,
# but report full extent first
ys, xs = np.where(red)
print(f"red ink total: {len(xs)} px, bbox x {xs.min()}-{xs.max()}, y {ys.min()}-{ys.max()}")

# Column profile of red ink excluding stroke columns (strokes at x~58-59, 901; bottom rows 537-539)
inner = red.copy()
inner[:, :75] = False
inner[:, 885:] = False
inner[530:, :] = False
inner[:45, :] = False
ys2, xs2 = np.where(inner)
print(f"TITLE red ink (panel interior, no strokes): {len(xs2)} px, bbox x {xs2.min()}-{xs2.max()}, y {ys2.min()}-{ys2.max()}")

# row profile -> line bands
rowsum = inner.sum(axis=1)
bands = []
in_band = False
for y in range(H):
    if rowsum[y] > 0 and not in_band:
        start = y; in_band = True
    elif rowsum[y] == 0 and in_band:
        bands.append((start, y - 1)); in_band = False
if in_band:
    bands.append((start, H - 1))
print(f"\nline bands (y0,y1, height, red px):")
prev = None
for (y0, y1) in bands:
    seg = inner[y0:y1 + 1]
    xs_l = np.where(seg.any(axis=0))[0]
    print(f"  y {y0}-{y1} h={y1 - y0 + 1} px, x {xs_l.min()}-{xs_l.max()} (w={xs_l.max() - xs_l.min() + 1}), "
          f"center_x={(xs_l.min() + xs_l.max()) / 2:.1f}, ink={seg.sum()}")
    if prev is not None:
        print(f"    pitch from prev band top: {y0 - prev}")
    prev = y0

# per-line color core (darkest red pixels in each band)
print("\nper-band red color core (median of strongly-red px):")
for (y0, y1) in bands:
    sel = inner[y0:y1 + 1]
    if sel.sum() < 10:
        continue
    rr = r[y0:y1 + 1][sel]; gg = g[y0:y1 + 1][sel]; bb = b[y0:y1 + 1][sel]
    med = (int(np.median(rr)), int(np.median(gg)), int(np.median(bb)))
    print(f"  band y {y0}-{y1}: median RGB {med}")

# cap-height / x-height estimate from the tallest band (line 1 has capitals E,O,M,V)
# Use column of a capital letter: measure ink height per band already printed.
# Font size estimate: Arial cap height ~ 0.716em -> pt ~= band_height / 0.716
for (y0, y1) in bands:
    hpx = y1 - y0 + 1
    print(f"  band y {y0}-{y1}: h={hpx}px -> font ~{hpx / 0.716:.1f}pt (if caps-only band)")

# also measure badge / panel / strokes for reference (chrome sanity on the original)
gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
band_rows = slice(65, 525)
cols = np.where(gray[band_rows].sum(axis=0) > 400)[0]
print(f"\nchrome ref: gray panel cols {cols.min()}-{cols.max()}")
yel = (r > 200) & (g > 200) & (b < 190)
pys, pxs = np.where(yel)
print(f"badge yellow bbox x {pxs.min()}-{pxs.max()}, y {pys.min()}-{pys.max()} "
      f"(center {(pxs.min() + pxs.max()) / 2:.1f},{(pys.min() + pys.max()) / 2:.1f}, d={pxs.max() - pxs.min() + 1})")

# background / panel color check at a quiet spot
print(f"\npanel color at (200,300): {tuple(im[300, 200])}")
print(f"canvas color at (20,270): {tuple(im[270, 20])}")
print(f"stroke color at (59,270): {tuple(im[270, 59])}")
print(f"bottom stroke at (480,538): {tuple(im[538, 480])}")
