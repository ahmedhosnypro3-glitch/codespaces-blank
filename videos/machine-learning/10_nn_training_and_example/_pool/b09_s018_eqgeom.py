#!/usr/bin/env python3
"""b09 s018: precise eq/label geometry orig vs render + render ASCII of bottom band."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), Image.LANCZOS)
    return np.asarray(im).astype(np.int16)

o, r = load("unique_slides/slide_018.jpg"), load("qa/slide018/rejudge/attempt2/render-1.png")
oe, re = o.sum(2), r.sum(2)

def ink_bbox(a, reg, thr):
    x0, y0, x1, y1 = reg
    m = a[y0:y1, x0:x1] < thr
    if not m.any():
        return None, 0
    ys, xs = np.nonzero(m)
    return (int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max()), int(y0 + ys.max())), int(m.sum())

for thr in (420, 520, 620):
    bo, _ = ink_bbox(oe, (820, 80, 910, 180), thr)
    br, _ = ink_bbox(re, (820, 80, 910, 180), thr)
    wo = (bo[2] - bo[0], bo[3] - bo[1]) if bo else None
    wr = (br[2] - br[0], br[3] - br[1]) if br else None
    print(f"thr={thr} orig_bbox={bo} w/h={wo} | render_bbox={br} w/h={wr}")

print("\n-- input-label text bbox, thr 560, x355..410 y185..205 --")
bo, no = ink_bbox(oe, (355, 185, 412, 205), 560)
br, nr = ink_bbox(re, (355, 185, 412, 205), 560)
print("orig  ", bo, no, "render", br, nr)
print("orig  colors row y=195 x368..400:",
      [tuple(o[195, x]) for x in range(368, 400, 4)])
print("render colors row y=195 x368..400:",
      [tuple(r[195, x]) for x in range(368, 400, 4)])

print("\n-- render bottom band ASCII (x360..620 y180..212, step 4) --")
for y in range(180, 212, 4):
    row = "".join("#" if re[y, x] < 520 else ("+" if re[y, x] < 700 else ".")
                  for x in range(360, 620, 4))
    print(f"{y:4d} {row}")

print("\n-- original bottom band ASCII (x360..620 y180..212, step 4) --")
for y in range(180, 212, 4):
    row = "".join("#" if oe[y, x] < 520 else ("+" if oe[y, x] < 700 else ".")
                  for x in range(360, 620, 4))
    print(f"{y:4d} {row}")
