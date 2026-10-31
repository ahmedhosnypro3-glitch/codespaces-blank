#!/usr/bin/env python3
"""Focused probe 2: arrow colors, fan-in lines, input column, equation glyph colors."""
from PIL import Image
import numpy as np
from scipy import ndimage
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)


def px(x, y):
    return tuple(a[y, x])


print("=== arrow pixel samples ===")
for name, y in (("top(186)", 186), ("mid(319)", 319), ("bot(455)", 455)):
    print(f" {name}: sum->box samples:",
          [(x, px(x, y)) for x in (705, 710, 715, 719)])
    print(f" {name}: box->label samples:",
          [(x, px(x, y)) for x in (770, 780, 790, 798)])

print("\n=== fan-in diagonal samples (input x~430 -> sum x~690) ===")
for y_in, y_sum, col in ((212, 186, "red(top)"), (240, 186, "red(top)"), (285, 186, "red(top)"),
                         (332, 186, "red(top)"), (418, 186, "red-bias)"),
                         (231, 320, "blue(mid)"), (282, 320, "blue(mid)"), (366, 320, "blue-bias)"),
                         (255, 455, "green(bot)"), (300, 455, "green(bot)"), (432, 455, "green-bias)")):
    ts = np.linspace(0, 1, 9)
    pts = []
    for t in ts:
        x = int(round(430 + (690 - 430) * t))
        y = int(round(y_in + (y_sum - y_in) * t))
        pts.append((x, y, px(x, y)))
    print(f" {col} in_y={y_in}: " + " ".join(f"{x},{y}:{c[0]},{c[1]},{c[2]}" for x, y, c in pts))

print("\n=== input column: dark blobs x 380-450 ===")
d = a.sum(axis=2) < 400
d2 = d.copy(); d2[:, :380] = False; d2[:, 450:] = False
lab, n = ndimage.label(d2, structure=np.ones((3, 3)))
rows = {}
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 6:
        continue
    rows[(xs.min(), xs.max(), ys.min(), ys.max())] = len(ys)
for k in sorted(rows, key=lambda k: k[2]):
    print(f"   x {k[0]}-{k[1]} y {k[2]}-{k[3]} area {rows[k]}")

print("\n=== equation line 1: per-column dark color (black vs red) ===")
sub = a[108:126, 79:440]
for x in range(sub.shape[1]):
    col = sub[:, x]
    m = col.sum(axis=1) < 400
    if m.sum() < 2:
        continue
    c = col[m].mean(axis=0)
    kind = "RED" if (c[0] > 120 and c[1] < 110 and c[2] < 110) else "black"
    print(f"   x={79+x:3d} {kind:5s} mean rgb {tuple(c.round().astype(int))} n={int(m.sum())}")

print("\n=== weight label extents (loose color, x 440-700) ===")
def extents(name, pred):
    m = pred.copy()
    m[:, :440] = False
    m[:, 700:] = False
    m[:150, :] = False
    m[487:, :] = False
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    got = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 12:
            continue
        got.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys)))
    got.sort(key=lambda t: t[1])
    print(f" {name}: {len(got)} blobs")
    for g in got:
        print(f"    x {g[0]}-{g[2]} y {g[1]}-{g[3]} area {g[4]}")

red = (a[:, :, 0] > 130) & (a[:, :, 1] < 120) & (a[:, :, 2] < 120)
blue = (a[:, :, 2] > 130) & (a[:, :, 0] < 140) & (a[:, :, 1] < 130)
green = (a[:, :, 1] > 90) & (a[:, :, 0] < 120) & (a[:, :, 2] < 120)
extents("RED weights", red)
extents("BLUE weights", blue)
extents("GREEN weights", green)
