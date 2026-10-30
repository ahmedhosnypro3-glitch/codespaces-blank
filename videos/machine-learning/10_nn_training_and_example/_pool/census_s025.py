#!/usr/bin/env python3
"""Census of colored blobs in slide_025.jpg for measured-blob reconstruction."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")
a = np.asarray(img).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

MASKS = {
    "red": (r > 140) & (r - g > 45) & (r - b > 45),
    "blue": (b > 140) & (b - r > 45) & (b - g > 35),
    "green": (g > 110) & (g - r > 35) & (g - b > 35),
    "purple": (r > 90) & (b > 90) & (r - g > 25) & (b - g > 25),
    "orange": (r > 200) & (g > 120) & (g < 200) & (b < 110),
    "yellow": (r > 200) & (g > 200) & (b < 170),
}


def components(mask, min_px=30):
    lab = np.zeros(mask.shape, np.int32)
    cur = 0
    out = []
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if mask[y, x] and lab[y, x] == 0:
                cur += 1
                st = [(y, x)]
                lab[y, x] = cur
                pix = []
                while st:
                    cy, cx = st.pop()
                    pix.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if (0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1]
                                    and mask[ny, nx] and lab[ny, nx] == 0):
                                lab[ny, nx] = cur
                                st.append((ny, nx))
                if len(pix) >= min_px:
                    ys = [p[0] for p in pix]
                    xs = [p[1] for p in pix]
                    out.append((min(xs), min(ys), max(xs), max(ys), len(pix)))
    return out


def show(name, region=None, min_px=30):
    m = MASKS[name].copy()
    if region:
        x0, y0, x1, y1 = region
        m2 = np.zeros_like(m)
        m2[y0:y1, x0:x1] = m[y0:y1, x0:x1]
        m = m2
    print(f"\n### {name} region={region}")
    for (x0, y0, x1, y1, n) in sorted(components(m, min_px), key=lambda c: (c[1], c[0])):
        w, h = x1 - x0 + 1, y1 - y0 + 1
        fill = n / (w * h)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        print(f"   x {x0}-{x1} y {y0}-{y1} w={w} h={h} px={n} fill={fill:.2f}"
              f" | in x {x0/72:.2f}-{x1/72:.2f} y {y0/72:.2f}-{y1/72:.2f}"
              f" c=({cx/72:.2f},{cy/72:.2f})")


for c in ["red", "blue", "green", "purple", "orange", "yellow"]:
    show(c, region=(340, 330, 960, 540), min_px=40)

print("\n### center diagram region (x 300..960, y 120..320)")
for c in ["red", "blue", "green", "purple", "orange", "yellow"]:
    show(c, region=(300, 120, 960, 320), min_px=60)

print("\n### left column region (x 40..310, y 150..320)")
for c in ["red", "blue", "green", "purple", "orange", "yellow", ]:
    show(c, region=(40, 150, 310, 320), min_px=40)
