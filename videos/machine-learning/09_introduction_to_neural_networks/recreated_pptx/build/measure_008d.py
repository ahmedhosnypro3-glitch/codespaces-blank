#!/usr/bin/env python3
"""Targeted sampling of the ORIGINAL slide_008 frame: cluster colors, line colors, box fills."""
import numpy as np
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
im = Image.open(ORIG).convert("RGB").resize((960, 540), Image.LANCZOS)
a = np.asarray(im).astype(int)

def sample(name, x, y, half=14):
    box = a[y - half:y + half, x - half:x + half].reshape(-1, 3)
    med = np.median(box, axis=0)
    print(f"  {name:22s} @({x:3d},{y:3d})  median RGB={tuple(int(v) for v in med)}  "
          f"frac_sat={(box.max(axis=1)-box.min(axis=1)).mean()/255:.2f}")
    return med

print("=== cluster centers (vision-measured) ===")
sample("C1 green upper", 480, 210)
sample("C2 blue right", 630, 360)
sample("C3 red lower-left", 380, 390)
print("=== decision line midpoints ===")
sample("d1 red mid", 445, 340)
sample("d2 blue mid", 535, 315)
sample("d3 green mid", 495, 375)
print("=== yellow label boxes ===")
sample("yellow C1", 558, 162)
sample("yellow C2", 630, 306)
sample("yellow C3", 294, 402)
print("=== orange ? boxes ===")
for i, (x, y) in enumerate([(285, 320), (475, 365), (685, 240), (490, 490)], 1):
    sample(f"orange ? #{i}", x, y)
print("=== boxes outside plot ===")
sample("Undefined box", 95, 145)
sample("New Class box", 775, 380)
print("=== plot corner probes ===")
for nm, (x, y) in {"TL": (175, 120), "TR": (790, 120), "BL": (175, 510), "BR": (790, 510),
                   "top-mid": (480, 120), "bot-mid": (480, 510), "left-mid": (175, 315),
                   "right-mid": (790, 315)}.items():
    sample(f"frame {nm}", x, y)
print("=== background samples ===")
for nm, (x, y) in {"slide bg top-left": (20, 20), "slide bg top-right": (940, 20),
                   "below plot": (480, 530), "left of plot": (60, 315),
                   "right of plot": (930, 315)}.items():
    sample(nm, x, y)
print("=== title text sample ===")
sample("title center", 480, 65, half=20)
sample("title left-run red", 200, 65, half=12)
sample("title blue run", 480, 65, half=8)

# scan for pale purple / pale green boxes anywhere on slide
print("\n=== scan: pale green #d5f5e3 / pale purple #d7bde2 proximity ===")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mint = (g > r + 6) & (g > b + 4) & (g > 120) & (r > 150)
purple = (b > g + 8) & (r > g) & (b > 150) & (r > 120)
for nm, m in [("mint", mint), ("purple", purple)]:
    ys, xs = np.nonzero(m)
    if not len(xs):
        print(f"  {nm}: none"); continue
    print(f"  {nm}: n={len(xs)} bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
    # histogram of x in 40px buckets
    import collections
    c = collections.Counter(int(x // 40) for x in xs)
    print("     x buckets:", sorted(c.items()))
    c2 = collections.Counter(int(y // 40) for y in ys)
    print("     y buckets:", sorted(c2.items()))
