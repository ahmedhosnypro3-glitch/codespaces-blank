#!/usr/bin/env python3
"""Connected-component geometry for slide_025.jpg (PIL/numpy only)."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

COLORS = {
    "red": (r > 140) & (r - g > 45) & (r - b > 45),
    "blue": (b > 140) & (b - r > 45) & (b - g > 35),
    "green": (g > 110) & (g - r > 35) & (g - b > 35),
    "purple": (r > 90) & (b > 90) & (r - g > 25) & (b - g > 25),
    "orange": (r > 200) & (g > 120) & (g < 200) & (b < 110),
    "yellow": (r > 200) & (g > 200) & (b < 170),
    "dark": a.mean(axis=2) < 110,
}


def components(mask, min_px=25):
    """Simple 8-connectivity flood fill (iterative, no scipy)."""
    lab = np.zeros(mask.shape, dtype=np.int32)
    cur = 0
    out = []
    Hm, Wm = mask.shape
    for y in range(Hm):
        for x in range(Wm):
            if mask[y, x] and lab[y, x] == 0:
                cur += 1
                stack = [(y, x)]
                lab[y, x] = cur
                pix = []
                while stack:
                    cy, cx = stack.pop()
                    pix.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < Hm and 0 <= nx < Wm and mask[ny, nx] and lab[ny, nx] == 0:
                                lab[ny, nx] = cur
                                stack.append((ny, nx))
                ys = [p[0] for p in pix]
                xs = [p[1] for p in pix]
                if len(pix) >= min_px:
                    out.append((min(xs), min(ys), max(xs), max(ys), len(pix)))
    return out


def dump(name, mask, min_px=40, limit=40):
    comps = sorted(components(mask, min_px), key=lambda c: (c[1], c[0]))
    print(f"\n### {name}  ({len(comps)} comps >= {min_px}px)")
    for (x0, y0, x1, y1, n) in comps[:limit]:
        print(f"   bbox x {x0}-{x1} (w={x1-x0+1})  y {y0}-{y1} (h={y1-y0+1})  px={n}"
              f"   [in] x {x0/72:.2f}-{x1/72:.2f} y {y0/72:.2f}-{y1/72:.2f}")


for name in ["red", "blue", "green", "purple", "orange", "yellow"]:
    dump(name, COLORS[name])

print("\n### title-band red components (rows 40..110)")
rb = COLORS["red"].copy()
rb[:40] = False
rb[110:] = False
dump("red_title", rb, 30, 20)

print("\n### right-edge red (cols 820..960)")
rc = COLORS["red"].copy()
rc[:, :820] = False
dump("red_right", rc, 30, 20)
