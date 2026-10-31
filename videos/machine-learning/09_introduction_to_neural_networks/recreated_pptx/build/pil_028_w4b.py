"""Targeted color-region map for slide_028 original + render (wave 4).

Locates discrete color families and their bounding boxes so the build can be
diffed against measured ground truth rather than assumptions.
"""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = Image.open(f"{V}/unique_slides/slide_028.jpg").convert("RGB")
REN = Image.open(f"{V}/recreated_pptx/build/slide_028_rendered-1.png").convert("RGB")
o = np.asarray(ORIG).astype(int)
r = np.asarray(REN).astype(int)
sc = r.shape[1] / o.shape[1]
print("scale render/orig =", round(sc, 4), "orig", o.shape, "render", r.shape)

FAMILIES = {
    "red/darkred": lambda R, G, B: (R > 130) & (G < 90) & (B < 90),
    "purple": lambda R, G, B: (R > 120) & (B > 120) & (G < R - 40) & (G < B - 20),
    "blue": lambda R, G, B: (B > 120) & (B > R + 30) & (B > G + 20),
    "green": lambda R, G, B: (G > 120) & (G > R + 20) & (G > B + 20),
    "orange": lambda R, G, B: (R > 200) & (G > 120) & (G < 200) & (B < 120),
    "black": lambda R, G, B: (R < 60) & (G < 60) & (B < 60),
    "yellow": lambda R, G, B: (R > 200) & (G > 190) & (B < 130),
}

for name, img, label in ((o, "ORIG", "orig"), (r, REN, "render")):
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    print(f"\n===== {label} (h={img.shape[0]}, w={img.shape[1]}) =====")
    for fam, test in FAMILIES.items():
        m = test(R, G, B)
        if m.sum() < 200:
            continue
        ys, xs = np.where(m)
        # density profile by 10 bands to separate multiple instances
        rows, cols = m.sum(axis=1), m.sum(axis=0)

        def bands(v, thr=3):
            out, st = [], None
            for i, x in enumerate(v):
                if x > thr and st is None:
                    st = i
                elif x <= thr and st is not None:
                    out.append((st, i - 1))
                    st = None
            if st is not None:
                out.append((st, len(v) - 1))
            return out

        rb = [(a, b) for a, b in bands(rows) if b - a >= 2]
        cb = [(a, b) for a, b in bands(cols) if b - a >= 2]
        print(f"  {fam:14s} px={m.sum():7d} bbox y[{ys.min()}..{ys.max()}] x[{xs.min()}..{xs.max()}]")
        print(f"      ybands({len(rb)}): {rb[:14]}")
        print(f"      xbands({len(cb)}): {cb[:14]}")
