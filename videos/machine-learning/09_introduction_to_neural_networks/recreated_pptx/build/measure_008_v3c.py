#!/usr/bin/env python3
"""Connected-component probes: panel edges, boundary lines, point dots, ? boxes, hatch regions."""
import numpy as np
from PIL import Image
from collections import deque

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.array(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def components(mask, min_n=40, label="", max_list=40):
    m = mask.copy()
    seen = np.zeros_like(m, dtype=bool)
    out = []
    ys0, xs0 = np.where(m)
    for y0, x0 in zip(ys0, xs0):
        if seen[y0, x0]:
            continue
        q = deque([(y0, x0)])
        seen[y0, x0] = True
        pix = []
        while q:
            y, x = q.popleft()
            pix.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True
                        q.append((yy, xx))
        if len(pix) >= min_n:
            ys = [p[0] for p in pix]
            xs = [p[1] for p in pix]
            out.append((min(xs), max(xs), min(ys), max(ys), len(pix),
                        sum(xs) / len(xs), sum(ys) / len(ys)))
    out.sort(key=lambda t: -t[4])
    print(f"--- {label} ({len(out)} comps >= {min_n}) ---")
    for c in out[:max_list]:
        print("   x %d-%d y %d-%d n=%d center (%.0f,%.0f)" % c)
    return out


pure_blue = (b > 190) & (r < 110) & (g < 130)
pure_green = (g > 130) & (r < 130) & (b < 150) & ((g - r) > 50) & ((g - b) > 40)
deep_red = (r > 150) & (g < 90) & (b < 90)
magenta = (r > 190) & (b > 170) & (g < 160) & ((r - g) > 60) & ((b - g) > 40)
yellow = (r > 235) & (g > 220) & (b < 120)

panel = np.zeros_like(pure_blue)
panel[110:500, 150:780] = True

components(pure_blue & panel, 40, "blue in panel", 25)
components(pure_green & panel, 40, "green in panel", 25)
components(deep_red & panel, 40, "deep red in panel", 30)
components(magenta, 30, "magenta", 15)
components(yellow, 100, "yellow", 10)

print("--- panel red border candidates ---")
for xx in range(140, 800):
    n = deep_red[120:500, xx].sum()
    if n > 120:
        print("  col", xx, n)
for yy in range(100, 520):
    n = deep_red[yy, 150:780].sum()
    if n > 120:
        print("  row", yy, n)

print("--- salmon density scan (34x32 windows) ---")
salmon = (r >= 246) & (g >= 205) & (g <= 240) & (b >= 185) & (b <= 225) & ((r - b) >= 22)
salmon[:110] = False
salmon[500:] = False
integ = salmon.astype(int)
integ = np.pad(integ, 1)
S = integ.cumsum(0).cumsum(1)
best = []
for yy in range(110, 470):
    for xx in range(150, 760):
        s = (S[yy + 32, xx + 34] - S[yy, xx + 34] - S[yy + 32, xx] + S[yy, xx])
        best.append((s, xx, yy))
best.sort(reverse=True)
shown = []
for s, xx, yy in best:
    if s < 500:
        break
    if all((xx - px) ** 2 + (yy - py) ** 2 > 30 ** 2 for px, py in shown):
        shown.append((xx, yy))
        print("  salmon box at x %d y %d (density %d)" % (xx, yy, s))
    if len(shown) >= 6:
        break

print("--- magenta ? near plot center ---")
mg = magenta & panel
ys, xs = np.where(mg)
for (yy, xx) in zip(ys, xs):
    if 250 < yy < 340 and 400 < xx < 520:
        print("   magenta px", (xx, yy), tuple(a[yy, xx]))
