#!/usr/bin/env python3
"""Measure slide_014 original frame: panel boxes, node colors, weight label colors,
equation line bands, threshold box position."""
import numpy as np
from PIL import Image
from collections import Counter

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"image {W}x{H}")

def near(px, hexs, tol=42):
    r, g, b = hexs
    return (abs(px[0]-r) <= tol) & (abs(px[1]-g) <= tol) & (abs(px[2]-b) <= tol)

def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"  {label}: NONE")
        return None
    print(f"  {label}: x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] n={len(xs)}")
    return (xs.min(), ys.min(), xs.max(), ys.max())

print("\n=== global color census (top 14) ===")
flat = a.reshape(-1, 3)
cnt = Counter(map(tuple, flat[::7]))
for c, n in cnt.most_common(14):
    print(f"  #{c[0]:02X}{c[1]:02X}{c[2]:02X}  {n}")

# --- white panels ---
white = (a[:, :, 0] > 246) & (a[:, :, 1] > 246) & (a[:, :, 2] > 246)
print("\n=== white panel regions ===")
lbl = np.zeros_like(white, dtype=int)
from scipy import ndimage
lab, n = ndimage.label(white)
sizes = ndimage.sum(white, lab, range(1, n + 1))
order = np.argsort(sizes)[::-1]
for i in order[:8]:
    if sizes[i] < 1500:
        break
    ys, xs = np.where(lab == i + 1)
    print(f"  panel#{i+1}: x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={int(sizes[i])}")

print("\n=== colored circles / labels ===")
for name, hexs, tol in [
    ("cyan/teal node", (0x99, 0xCC, 0xCC), 55),
    ("cyan2", (0x66, 0xCC, 0xCC), 45),
    ("red C00000", (0xC0, 0x00, 0x00), 50),
    ("red FF0000", (0xFF, 0x00, 0x00), 45),
    ("green 008000", (0x00, 0x80, 0x00), 45),
    ("blue 0000FF", (0x00, 0x00, 0xFF), 45),
    ("purple D0B0D0", (0xD0, 0xB0, 0xD0), 40),
    ("yellow FFD700", (0xFF, 0xD7, 0x00), 50),
]:
    m = near(a, hexs, tol)
    m[:0, :] = False
    print(f"-- {name}")
    bbox(m, name)
    # split into components to find distinct blobs
    lab2, n2 = ndimage.label(m)
    if n2:
        sizes2 = ndimage.sum(m, lab2, range(1, n2 + 1))
        keep = [i for i in np.argsort(sizes2)[::-1][:6] if sizes2[i] > 120]
        for i in keep:
            ys, xs = np.where(lab2 == i + 1)
            print(f"     blob x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}] px={int(sizes2[i])}")

print("\n=== equation panel: dark-ink row profile (x 30..470) ===")
dark = (a.sum(axis=2) < 330)
band = dark[:, 30:470]
prof = band.sum(axis=1)
runs = []
inrun = False
for y in range(H):
    if prof[y] >= 3 and not inrun:
        inrun, start = True, y
    elif prof[y] < 3 and inrun:
        inrun = False
        runs.append((start, y - 1, int(prof[start:y].max())))
if inrun:
    runs.append((start, H - 1, int(prof[start:H].max())))
for r in runs:
    if 250 < r[0] < 520:
        print(f"  ink band y[{r[0]}..{r[1]}] h={r[1]-r[0]+1} maxpx={r[2]}")
