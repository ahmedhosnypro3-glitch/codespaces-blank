#!/usr/bin/env python3
"""b09 s018: full-res ASCII of original label + eq, and eq PNG intrinsic bbox."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
o = np.asarray(Image.open(NS + "unique_slides/slide_018.jpg").convert("RGB")).astype(np.int16)
os_ = o.sum(2)

def amap(reg, thr, step=1, ymin=0):
    x0, y0, x1, y1 = reg
    print(f"\n== {reg} thr={thr} step={step} ==")
    print("     " + "".join(str((x // 10) % 10) for x in range(x0, x1, step)))
    for y in range(y0, y1, step):
        print(f"{y:4d} " + "".join("#" if os_[y, x] < thr else ("." if os_[y, x] < 700 else " ")
                                   for x in range(x0, x1, step)))

amap((360, 186, 415, 204), 560, 1)
amap((826, 100, 900, 155), 520, 1)
amap((826, 100, 900, 155), 700, 1)

eq = np.asarray(Image.open(NS + "recreated_pptx/build/eq_s18b.png").convert("RGBA"))
print("\neq_s18b.png size", eq.shape)
alpha = eq[:, :, 3]
if alpha.max() < 255:
    print("has transparency; ink bbox by alpha")
    ys, xs = np.nonzero(alpha > 60)
    if len(xs):
        print("alpha>60 bbox:", xs.min(), ys.min(), xs.max(), ys.max())
rgb = eq[:, :, :3].astype(np.int16)
ink = (rgb.sum(2) < 520) & (alpha > 60)
ys, xs = np.nonzero(ink)
print("rgb-ink bbox:", xs.min(), ys.min(), xs.max(), ys.max(), "-> w,h =", xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)
