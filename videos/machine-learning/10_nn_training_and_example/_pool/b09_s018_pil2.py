#!/usr/bin/env python3
"""b09 s018 closed-loop PIL: original 960x540 vs render resampled to 960x540."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
SRC = NS + "unique_slides/slide_018.jpg"
RND = NS + "qa/slide018/rejudge/attempt2/render-1.png"

def arr(path, resample):
    im = Image.open(path).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), resample)
    a = np.asarray(im).astype(np.int16)
    return a, a.sum(2)

o, os_ = arr(SRC, Image.LANCZOS)
r, rs = arr(RND, Image.LANCZOS)
print("orig", o.shape, "render", r.shape)

REGIONS = [
    ("diagram_band", (360, 55, 745, 212)),
    ("output_labels", (743, 55, 800, 212)),
    ("error_bar", (748, 55, 795, 212)),
    ("class_col", (793, 55, 845, 212)),
    ("equation", (825, 85, 905, 175)),
    ("input_label", (355, 178, 415, 208)),
    ("bottom_train", (360, 178, 620, 215)),
]

def ink(a, s, reg, thr=420):
    x0, y0, x1, y1 = reg
    sub = s[y0:y1, x0:x1]
    m = sub < thr
    if not m.any():
        return None, 0
    ys, xs = np.nonzero(m)
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max()), int(m.sum())

print("\n-- dark ink bbox (orig px coords) --")
print(f"{'region':15s} {'orig bbox':26s} {'n':>5s} {'render bbox':26s} {'n':>5s} {'dx':>4s} {'dy':>4s}")
for name, reg in REGIONS:
    bo, no = ink(o, os_, reg)
    br, nr = ink(r, rs, reg)
    if bo and br:
        print(f"{name:15s} {str(bo):26s} {no:5d} {str(br):26s} {nr:5d} {bo[0]-br[0]:4d} {bo[1]-br[1]:4d}")
    else:
        print(f"{name:15s} orig={bo} render={br} (one side empty)")

COLORS = [("sigma_green", (184, 232, 168)), ("error_red", (204, 0, 0)),
          ("magenta_dot", (204, 0, 204)), ("output_blue", (32, 32, 192)),
          ("pink_box", (240, 192, 216)), ("orange_box", (255, 243, 196))]

def cbbox(a, rgb, tol=26):
    m = (np.abs(a - np.array(rgb)).max(2) <= tol)
    if not m.any():
        return None, 0
    ys, xs = np.nonzero(m)
    return (xs.min(), ys.min(), xs.max(), ys.max()), int(m.sum())

print("\n-- colour feature bbox --")
for name, rgb in COLORS:
    bo, no = cbbox(o, rgb)
    br, nr = cbbox(r, rgb)
    print(f"{name:13s} {str(bo):26s} {no:6d} {str(br):26s} {nr:6d}")
