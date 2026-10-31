#!/usr/bin/env python3
"""One-shot confirmation of the small annotation box bounds on slide_008.jpg."""
import numpy as np
from PIL import Image
from collections import deque

P = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def comps(mask, min_area=40):
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    for y in range(H):
        for x in range(W):
            if mask[y, x] and not seen[y, x]:
                q = deque([(y, x)]); seen[y, x] = True; n = 0
                x0 = x1 = x; y0 = y1 = y
                while q:
                    cy, cx = q.popleft(); n += 1
                    x0, x1 = min(x0, cx), max(x1, cx)
                    y0, y1 = min(y0, cy), max(y1, cy)
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny,nx] and not seen[ny,nx]:
                            seen[ny,nx] = True; q.append((ny,nx))
                if n >= min_area:
                    out.append((x0, y0, x1, y1, n))
    return out


def sq(name, mask, lo, hi):
    print(f"--- {name} ---")
    for c in comps(mask, 40):
        w, h = c[2] - c[0], c[3] - c[1]
        if lo <= w <= hi and lo <= h <= hi:
            print(f"  x {c[0]}-{c[2]}  y {c[1]}-{c[3]}  w{w} h{h} n={c[4]}")


# salmon "?" boxes: pale pink fill, away from the panel borders
salmon = (R > 232) & (G > 198) & (G < 240) & (B > 188) & (B < 232) & (R - B > 15)
mask = salmon.copy(); mask[:126, :] = False; mask[500:, :] = False
mask[:, :200] = False; mask[:, 600:] = False
sq("? boxes (salmon)", mask, 22, 48)

# yellow C tags, away from badge
yel = (R > 200) & (G > 190) & (B < 150) & (R - B > 70)
m2 = yel.copy(); m2[:150, :] = False; m2[90:, :] = False
sq("C tags (yellow)", m2, 20, 60)

# magenta: New Class box / tiny ?
mag = (R > 130) & (B > 130) & (G < R - 45) & (G < B - 45)
m3 = mag.copy(); m3[:200, :] = False; m3[:, :600] = False
sq("New Class (magenta)", m3, 15, 90)

# magenta tiny ? anywhere in the panel
m4 = mag.copy(); m4[:200, :] = False; m4[:, 600:] = False
sq("magenta in panel", m4, 3, 20)

# +ve text: small black clusters
blk = (R < 90) & (G < 90) & (B < 90)
m5 = blk.copy(); m5[:130, :] = False; m5[505:, :] = False
m5[:, :200] = False
sq("black text clusters in panel", m5, 15, 60)
