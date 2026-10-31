#!/usr/bin/env python3
"""b09 s018: masked closed-loop check — fixed render vs original."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), Image.LANCZOS)
    return np.asarray(im).astype(np.int16)

o, r = load("unique_slides/slide_018.jpg"), load("qa/slide018/attempt4/render-1.png")

def box(img, rgb, tol, reg):
    sub = img[reg[1]:reg[3], reg[0]:reg[2]]
    m = np.ones(sub.shape[:2], bool)
    for i in range(3):
        m &= (sub[:, :, i] >= rgb[i] - tol) & (sub[:, :, i] <= rgb[i] + tol)
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return (reg[0] + xs.min(), reg[1] + ys.min(), reg[0] + xs.max(), reg[1] + ys.max())

RED = [(190, 0, 0), 45]
BLUE = [(30, 30, 170), 45]
GREEN = [(150, 215, 150), 30]
MAROON = [(150, 40, 40), 35]
DARK = [(70, 60, 40), 90]

CHECKS = [
    ("red '?'", RED, (860, 95, 905, 160)),
    ("error bar", RED, (750, 60, 780, 215)),
    ("blue Output", BLUE, (690, 50, 760, 215)),
    ("green sigma bands", GREEN, (360, 50, 750, 215)),
    ("maroon panel border", MAROON, (350, 50, 915, 220)),
    ("dark ink diagram", DARK, (360, 55, 745, 212)),
    ("class labels dark", DARK, (785, 55, 848, 215)),
    ("bottom magenta dots", [(150, 0, 130), 60], (360, 175, 625, 212)),
    ("train-data label", [(150, 20, 140), 60], (360, 185, 412, 205)),
]

print(f"{'region':22s} {'orig bbox':24s} {'render bbox':24s} {'dx0':>4s} {'dx1':>4s} {'dy0':>4s} {'dy1':>4s}")
for name, (rgb, tol), reg in CHECKS:
    bo, br = box(o, rgb, tol, reg), box(r, rgb, tol, reg)
    if not bo or not br:
        print(f"{name:22s} orig={bo} render={br}")
        continue
    d = (bo[0] - br[0], bo[2] - br[2], bo[1] - br[1], bo[3] - br[3])
    w_o, h_o = bo[2] - bo[0], bo[3] - bo[1]
    w_r, h_r = br[2] - br[0], br[3] - br[1]
    flag = "" if max(abs(v) for v in d) <= 4 else "  <-- OVER 4px"
    print(f"{name:22s} {str(bo):24s} {str(br):24s} {d[0]:4d} {d[1]:4d} {d[2]:4d} {d[3]:4d}"
          f"   size o{w_o}x{h_o} r{w_r}x{h_r}{flag}")
