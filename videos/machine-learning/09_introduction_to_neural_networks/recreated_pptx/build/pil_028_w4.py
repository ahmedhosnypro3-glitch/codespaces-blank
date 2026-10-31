"""Fresh PIL ground-truth for slide 028: original frame vs recreated render (wave 4)."""
import sys
from collections import Counter
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = Image.open(f"{V}/unique_slides/slide_028.jpg").convert("RGB")
REN = Image.open(f"{V}/recreated_pptx/build/slide_028_rendered-1.png").convert("RGB")
W, H = ORIG.size
print("orig size", ORIG.size, "render size", REN.size, "xscale", round(REN.size[0] / W, 4))

o = np.asarray(ORIG).astype(int)
r = np.asarray(REN).astype(int)

for name, img in (("ORIG", o), ("RENDER", r)):
    print(f"\n--- {name} ---")
    print("mean RGB", img.reshape(-1, 3).mean(axis=0).round(1))
    sample = img[::4, ::4].reshape(-1, 3)
    cc = Counter(map(tuple, sample))
    print("most common colors:", cc.most_common(6))

    bg = np.array(cc.most_common(1)[0][0])
    d = np.abs(img - bg).max(axis=2)
    ink = d > 28
    rows, cols = ink.sum(axis=1), ink.sum(axis=0)

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

    print(f"bg={bg} ink frac={round(ink.mean(), 4)}")
    print("ROW bands:")
    for a, b in bands(rows):
        if b - a >= 2:
            print(f"  y {a:4d}..{b:4d}  h={b - a + 1:4d}  peak={rows[a:b + 1].max()}")
    print("COL bands:")
    for a, b in bands(cols):
        if b - a >= 2:
            print(f"  x {a:4d}..{b:4d}  w={b - a + 1:4d}  peak={cols[a:b + 1].max()}")
