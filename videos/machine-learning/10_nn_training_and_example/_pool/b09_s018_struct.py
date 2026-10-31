#!/usr/bin/env python3
"""b09 s018: original-side structure probes for the render's gaps."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
o = np.asarray(Image.open(NS + "unique_slides/slide_018.jpg").convert("RGB")).astype(np.int16)

def amap(reg, step=1, thr=620, mode="dark"):
    x0, y0, x1, y1 = reg
    print(f"\n== {reg} mode={mode} thr={thr} step={step} ==")
    print("     " + "".join(str((x // 10) % 10) for x in range(x0, x1, step)))
    for y in range(y0, y1, step):
        row = ""
        for x in range(x0, x1, step):
            p = o[y, x]
            if mode == "red":
                row += "R" if (p[0] > 140 and p[1] < 110 and p[2] < 110) else "."
            elif mode == "maroon":
                row += "M" if (p[0] > 120 and p[0] < 215 and p[1] < 100 and p[2] < 100) else "."
            elif mode == "blue":
                row += "B" if (p[0] < 110 and p[1] < 110 and p[2] > 120) else "."
            else:
                row += "#" if p.sum() < thr else "."
        print(f"{y:4d} {row}")

amap((752, 60, 786, 200), 1, mode="red")
amap((396, 52, 420, 76), 1, mode="maroon")
amap((694, 74, 750, 100), 1, mode="blue")
amap((860, 50, 915, 76), 1, mode="maroon")

print("\n== blue label row extents in orig (x690..760) ==")
for y0, y1 in ((70, 105), (105, 140), (140, 180)):
    sub = o[y0:y1, 690:760]
    m = (sub[:, :, 0] < 120) & (sub[:, :, 1] < 120) & (sub[:, :, 2] > 120)
    if m.any():
        ys, xs = np.nonzero(m)
        print(f"  y{y0}-{y1}: x {690+xs.min()}..{690+xs.max()} (w={xs.max()-xs.min()+1}) rows {y0+ys.min()}..{y0+ys.max()}")
