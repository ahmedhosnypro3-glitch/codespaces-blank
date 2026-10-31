#!/usr/bin/env python3
"""b09 s018: label metrics both sides + orig green column profile."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), Image.LANCZOS)
    return np.asarray(im).astype(np.int16)

o, r = load("unique_slides/slide_018.jpg"), load("qa/slide018/attempt4/render-1.png")

def blue_m(a):
    return (a[:, :, 2] > 120) & (a[:, :, 0] < 120) & (a[:, :, 1] < 120)

print("== blue Output labels (x690..765) ==")
for name, a in (("orig", o), ("render", r)):
    m = blue_m(a)
    for y0, y1, lbl in ((70, 106, "Output1"), (106, 142, "Output2"), (142, 182, "Output3")):
        sub = m[y0:y1, 690:765]
        if not sub.any():
            print(f"  {name} {lbl}: none"); continue
        ys, xs = np.nonzero(sub)
        print(f"  {name} {lbl}: x {690+xs.min()}..{690+xs.max()} (w={xs.max()-xs.min()+1}) "
              f"y {y0+ys.min()}..{y0+ys.max()} (h={ys.max()-ys.min()+1}) n={int(sub.sum())}")

print("\n== orig blue label ASCII (x698..755, y76..94) ==")
mb = blue_m(o)
for y in range(76, 94):
    print(f" {y:3d} " + "".join("#" if mb[y, x] else "." for x in range(698, 756)))

print("\n== orig green column profile (x360..760) ==")
g = (o[:, :, 1] > 200) & (o[:, :, 0] > 130) & (o[:, :, 0] < 220) & (o[:, :, 2] > 120) & (o[:, :, 2] < 215)
row = ""
for x in range(360, 760, 10):
    row += f"{x}:{int(g[55:210, x:x+10].sum())} "
print(" ", row)

print("\n== orig green row profile within panel ==")
for y in range(55, 210, 5):
    n = int(g[y, 360:760].sum())
    if n:
        print(f"  y{y}: {n}")
