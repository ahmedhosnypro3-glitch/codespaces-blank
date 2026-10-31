#!/usr/bin/env python3
"""Connected-component measurements of small coloured boxes on slide_008.jpg."""
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
                q = deque([(y, x)])
                seen[y, x] = True
                pts = []
                while q:
                    cy, cx = q.popleft()
                    pts.append((cy, cx))
                    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        ny, nx = cy+dy, cx+dx
                        if 0 <= ny < H and 0 <= nx < W and mask[ny,nx] and not seen[ny,nx]:
                            seen[ny,nx] = True
                            q.append((ny,nx))
                if len(pts) >= min_area:
                    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                    out.append((min(xs), min(ys), max(xs), max(ys), len(pts)))
    return out


yellow = (R > 200) & (G > 190) & (B < 150) & (R - B > 70)
print("=== YELLOW components (C tags / badge) ===")
for c in sorted(comps(yellow, 60), key=lambda c: c[1]):
    print(f"  x {c[0]}-{c[2]}  y {c[1]}-{c[3]}  n={c[4]}")

salmon = (R > 235) & (G > 195) & (G < 235) & (B > 185) & (B < 228) & (R - B > 20)
print("=== SALMON components (? boxes) ===")
for c in sorted(comps(salmon, 120), key=lambda c: c[1]):
    print(f"  x {c[0]}-{c[2]}  y {c[1]}-{c[3]}  n={c[4]}")

mag = (R > 130) & (B > 130) & (G < R - 45) & (G < B - 45)
print("=== MAGENTA components (New Class / badge ring / tiny ?) ===")
for c in sorted(comps(mag, 15), key=lambda c: c[1]):
    print(f"  x {c[0]}-{c[2]}  y {c[1]}-{c[3]}  n={c[4]}")

blue = (B > 140) & (B - R > 80) & (B - G > 60)
print("=== PURE BLUE components (Undefined box + leaders, d2 label) ===")
for c in sorted(comps(blue, 25), key=lambda c: c[1]):
    print(f"  x {c[0]}-{c[2]}  y {c[1]}-{c[3]}  n={c[4]}")

# the Undefined box border is pure blue; isolate x<200 region
print("=== BLUE pixels in x 60..200, y 120..190 (Undefined box) ===")
m = np.zeros_like(blue); m[120:190, 60:200] = True
for c in sorted(comps(blue & m, 8), key=lambda c: c[1]):
    print(f"  x {c[0]}-{c[2]}  y {c[1]}-{c[3]}  n={c[4]}")
