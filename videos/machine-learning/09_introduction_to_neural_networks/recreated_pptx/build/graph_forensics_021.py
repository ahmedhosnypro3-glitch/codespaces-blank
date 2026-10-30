"""Forensic pass: plot-area margins, curve colours, tick-label ink, legend text pixels."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)

PANELS = {
    "TL": (121, 109, 400, 271),
    "TR": (564, 109, 842, 274),
    "BL": (122, 346, 400, 508),
    "BR": (564, 346, 842, 508),
}

for name, (x0, y0, x1, y1) in PANELS.items():
    print(f"\n##### {name} frame x[{x0},{x1}] y[{y0},{y1}] #####")
    sub = a[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
    h, w, _ = sub.shape
    r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    # any non-white, non-grid ink
    ink = (np.abs(sub - 255).max(axis=2) > 28)
    # strong red (curve) with loose threshold
    red = (r > 110) & (r - g > 45) & (r - b > 30)
    print("  curve-red px:", int(red.sum()))
    if red.sum():
        ys, xs = np.where(red)
        cols = sub[red]
        from collections import Counter
        print("   red bbox x", (x0 + 3 + xs.min(), x0 + 3 + xs.max()),
              "y", (y0 + 3 + ys.min(), y0 + 3 + ys.max()))
        print("   red colours:", Counter(map(tuple, (cols // 24 * 24))).most_common(4))
    # column profile of ALL ink to find where content sits
    prof = ink.sum(axis=0)
    runs = []
    prev = None
    for j in range(w):
        v = prof[j] > 0
        if v != prev:
            runs.append([j, j, v]); prev = v
    # report contiguous ink columns summary
    ink_cols = np.where(prof > 0)[0]
    if len(ink_cols):
        print("   ink cols:", x0 + 3 + ink_cols.min(), "..", x0 + 3 + ink_cols.max())
        # gaps
        gaps = []
        prev = None
        for c in ink_cols:
            if prev is not None and c - prev > 4:
                gaps.append((x0 + 3 + prev, x0 + 3 + c))
            prev = c
        print("   ink gaps (>4px):", gaps)
    ink_rows = np.where(ink.sum(axis=1) > 0)[0]
    if len(ink_rows):
        print("   ink rows:", y0 + 3 + ink_rows.min(), "..", y0 + 3 + ink_rows.max())

print("\n\n### BL legend region crop stats (px x 130..250, y 355..400) ###")
reg = a[355:400, 130:250]
from collections import Counter
c = Counter(map(tuple, reg.reshape(-1, 3) // 24 * 24))
print("  ", c.most_common(8))

print("\n### TR curve: loosest red sweep ###")
sub = a[112:272, 567:840]
r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
red = (r - g > 30) & (r - b > 25) & (r > 90)
ys, xs = np.where(red)
print("  n=", len(xs), "x", (567 + xs.min(), 567 + xs.max()) if len(xs) else None,
      "y", (112 + ys.min(), 112 + ys.max()) if len(ys) else None)
if len(xs):
    print("  colours:", Counter(map(tuple, (sub[red] // 24 * 24))).most_common(5))

print("\n### BR curve: loosest red sweep ###")
sub = a[349:505, 567:840]
r, g, b = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
red = (r - g > 25) & (r - b > 20) & (r > 90)
ys, xs = np.where(red)
print("  n=", len(xs), "x", (567 + xs.min(), 567 + xs.max()) if len(xs) else None,
      "y", (349 + ys.min(), 349 + ys.max()) if len(ys) else None)
if len(xs):
    print("  colours:", Counter(map(tuple, (sub[red] // 24 * 24))).most_common(5))
    for frac in (0.1, 0.3, 0.5, 0.7, 0.9):
        cx = int(frac * (sub.shape[1] - 1))
        col = np.where(red[:, cx])[0]
        if len(col):
            print(f"   col@{frac}: y [{349+col.min()},{349+col.max()}]")
