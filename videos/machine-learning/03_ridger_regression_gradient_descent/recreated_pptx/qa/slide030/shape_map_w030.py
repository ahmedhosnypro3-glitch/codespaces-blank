#!/usr/bin/env python3
"""Slide 030: frame-px ASCII shape map of the arrow + callout bands
(worker w030-finish-20261024c).

Prints the two images side by side at ONE CHARACTER PER FRAME PIXEL so the
arrowhead geometry, shaft width and tilt can be compared directly without any
model judgement. Red-class pixels only; the table's pale pink fill is excluded.
"""
import numpy as np
from PIL import Image

V = "videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide030"

rend = np.asarray(Image.open(f"{Q}/render_6.png").convert("RGB")).astype(int)
orig = np.asarray(Image.open(f"{V}/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
RW, RH = rend.shape[1], rend.shape[0]
SXR, SYR = RW / 960.0, RH / 540.0


def redish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r - g > 60) & (r - b > 40) & (r > 110)


def pinkish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 200) & (r - g > 18) & (r - b > 18) & (g > 150) & (b > 150)


def to_frames(im, sx, sy, box):
    """Block-average an image region down to ONE CELL PER FRAME PXEL (960x540)."""
    x0, y0, x1, y1 = box
    X0, Y0, X1, Y1 = int(round(x0 * sx)), int(round(y0 * sy)), int(round(x1 * sx)), int(round(y1 * sy))
    sub = im[Y0:Y1, X0:X1].astype(float)
    h, w = sub.shape[:2]
    fh, fw = int(round(h / sy)), int(round(w / sx))
    if (fh, fw) != (h, w):
        out = np.zeros((fh, fw, 3))
        for i in range(fh):
            for j in range(fw):
                ys = slice(int(round(i * sy)), max(int(round((i + 1) * sy)), int(round(i * sy)) + 1))
                xs = slice(int(round(j * sx)), max(int(round((j + 1) * sx)), int(round(j * sx)) + 1))
                out[i, j] = sub[ys, xs].reshape(-1, 3).mean(axis=0)
        return out
    return sub


def frame_grid(im, sx, sy, box):
    """Classify each frame-px cell of the region ('#', '.', ' ')."""
    sub = to_frames(im, sx, sy, box)
    a = sub.astype(int)
    rm, pm = redish(a), pinkish(a)
    rows = []
    for i in range(rm.shape[0]):
        rows.append("".join("#" if rm[i, j] else ("." if pm[i, j] else " ") for j in range(rm.shape[1])))
    return rows


BOX = (158, 298, 200, 352)
r = frame_grid(rend, SXR, SYR, BOX)
o = frame_grid(orig, 1.0, 1.0, BOX)
print(f"== arrow shape map, frame px x{BOX[0]}..{BOX[2]} y{BOX[1]}..{BOX[3]} "
      f"(# = red ink, . = pale fill) ==")
print(f"{'RENDER':<44}| ORIGINAL")
for i in range(max(len(r), len(o))):
    rr = "".join(r[i]) if i < len(r) else ""
    oo = "".join(o[i]) if i < len(o) else ""
    y = BOX[1] + i
    mark = ""
    if rr.replace(" ", "") != oo.replace(" ", ""):
        mark = "  <-- differs"
    print(f"y={y:3d} {rr:<42}| {oo}{mark}")

print("\n== callout band map (purple=#, light text=o, other=.): frame px x320..585, y288..324 ==")


def callout_map(im, sx, sy):
    sub = to_frames(im, sx, sy, (320, 288, 585, 324)).astype(int)
    r_, g_, b_ = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    purple = (r_ - g_ > 25) & (b_ - g_ > 25) & (b_ > 120)
    light = (r_ > 200) & (g_ > 200) & (b_ > 200)
    return ["".join("#" if purple[i, j] else ("o" if light[i, j] else ".") for j in range(purple.shape[1]))
            for i in range(purple.shape[0])]


rc = callout_map(rend, SXR, SYR)
oc = callout_map(orig, 1.0, 1.0)
for i in range(max(len(rc), len(oc))):
    a = "".join(rc[i]) if i < len(rc) else ""
    b = "".join(oc[i]) if i < len(oc) else ""
    print(f"y={288+i:3d} {a[:44]:<44}| {b}")
print("\nSHAPE MAP DONE")
