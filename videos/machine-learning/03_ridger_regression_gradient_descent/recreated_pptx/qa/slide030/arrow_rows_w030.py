#!/usr/bin/env python3
"""Slide 030: per-row red-ink x-extents in the arrow neighbourhood (frame px).

Prints, for the render and the original, every row's red-ink x-range inside
x=140..225, y=296..356 so the arrowhead tips, shaft edges and head-to-head
span can be compared as numbers (no model judgement).
"""
import numpy as np
from PIL import Image

V = "videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide030"


def redish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r - g > 60) & (r - b > 40) & (r > 110)


def pinkish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 200) & (r - g > 18) & (r - b > 18) & (g > 150) & (b > 150)


def dump(label, path, sx, sy, W, H):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    x0, x1, y0, y1 = 140, 225, 296, 356
    X0, Y0, X1, Y1 = int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy)
    sub = im[Y0:Y1, X0:X1]
    rm, pm = redish(sub), pinkish(sub)
    print(f"-- {label} (px window {X0},{Y0}..{X1},{Y1})")
    for i in range(sub.shape[0]):
        y = round((Y0 + i) / sy, 1)
        xs = np.where(rm[i])[0]
        pxs = np.where(pm[i])[0]
        if not len(xs) and not len(pxs):
            continue
        s = ""
        if len(xs):
            runs = []
            start = prev = xs[0]
            for x in xs[1:]:
                if x == prev + 1:
                    prev = x
                    continue
                runs.append((start, prev))
                start = prev = x
            runs.append((start, prev))
            s = "red runs(frame x): " + " ".join(
                f"{round((a+X0)/sx,1)}..{round((b+X0)/sx,1)}" for a, b in runs)
        if len(pxs):
            s += f"  [pink px={len(pxs)} x {round((pxs.min()+X0)/sx,1)}..{round((pxs.max()+X0)/sx,1)}]"
        print(f"   y={y:6.1f}  {s}")


dump("render", f"{Q}/render_6.png", 2001 / 960.0, 1125 / 540.0, 2001, 1125)
print()
dump("orig", f"{V}/unique_slides/slide_030.jpg", 1.0, 1.0, 960, 540)
