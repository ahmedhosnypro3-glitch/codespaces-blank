#!/usr/bin/env python3
"""b09 s018: 150dpi-space closed-loop check + diagram column profiles."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    return im

oim = load("unique_slides/slide_018.jpg").resize((2001, 1125), Image.LANCZOS)
rim = load("qa/slide018/attempt4/render-1.png")
o = np.asarray(oim).astype(np.int16)
r = np.asarray(rim).astype(np.int16)
print("orig upscaled", o.shape, "render", r.shape)

def bbox(a, rgb, tol, reg):
    sub = a[reg[1]:reg[3], reg[0]:reg[2]]
    m = np.ones(sub.shape[:2], bool)
    for i in range(3):
        m &= (sub[:, :, i] >= rgb[i] - tol) & (sub[:, :, i] <= rgb[i] + tol)
    if not m.any():
        return None, 0
    ys, xs = np.nonzero(m)
    return (reg[0] + int(xs.min()), reg[1] + int(ys.min()),
            reg[0] + int(xs.max()), reg[1] + int(ys.max())), int(m.sum())

CHECKS = [
    ("red question", (190, 0, 0), 45, (1750, 200, 1900, 335)),
    ("error bar", (190, 0, 0), 45, (1560, 130, 1625, 450)),
    ("blue Output", (30, 30, 170), 45, (1450, 100, 1560, 450)),
    ("panel border maroon", (150, 40, 40), 35, (740, 130, 1940, 460)),
    ("cream panel fill", (239, 227, 208), 12, (740, 130, 1840, 440)),
    ("bottom magenta", (150, 0, 130), 60, (760, 370, 1300, 445)),
    ("train label", (130, 0, 120), 70, (750, 385, 860, 425)),
]

print(f"\n{'feature':20s} {'orig bbox (150dpi)':26s} {'render bbox':26s} {'dx0':>4s} {'dx1':>4s} {'dy0':>4s} {'dy1':>4s}")
for name, rgb, tol, reg in CHECKS:
    bo, no = bbox(o, rgb, tol, reg)
    br, nr = bbox(r, rgb, tol, reg)
    if not bo or not br:
        print(f"{name:20s} orig={bo}({no}) render={br}({nr}) -- mask miss")
        continue
    d = (bo[0] - br[0], bo[2] - br[2], bo[1] - br[1], bo[3] - br[3])
    flag = "" if max(abs(v) for v in d) <= 4 else "  <-- OVER 4px"
    print(f"{name:20s} {str(bo):26s} {str(br):26s} {d[0]:4d} {d[1]:4d} {d[2]:4d} {d[3]:4d}{flag}")

print("\n== diagram column ink profile (thr 560, x per 150dpi = orig x*2.08) ==")
for name, a in (("orig", o), ("render", r)):
    prof = []
    for x in range(740, 1900, 20):
        col = a[130:440, x:x + 20]
        prof.append((x, int((col.sum(2) < 560).sum())))
    print(name, " ".join(f"{x//1}:{n}" for x, n in prof))
