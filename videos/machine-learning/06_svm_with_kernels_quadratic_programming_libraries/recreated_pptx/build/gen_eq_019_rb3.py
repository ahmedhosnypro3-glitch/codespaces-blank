#!/usr/bin/env python3
"""Slide 019 equation, wave-3 re-render: STIX mathtext (clear a/b/phi/equiv/Rightarrow
glyphs) at 600 dpi tight transparent PNG -> eq_019/eq19_kernel_rb3.png + .json sidecar."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["mathtext.default"] = "it"

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "eq_019", "eq19_kernel_rb3.png")
DPI = 600
SIZE = 44.0
MAXW_IN = 8.53
MAXH_IN = 0.43

ROW = [
    ("#CC0000", r"\boldsymbol{a}^{T}\boldsymbol{b}"),
    ("#0000CC", r"\ \Rightarrow\ "),
    ("#000000", r"\mathrm{map\ to}\ "),
    ("#009900", r"\boldsymbol{\phi(a)}\ "),
    ("#000000", r"\mathrm{and}\ "),
    ("#009900", r"\boldsymbol{\phi(b)}"),
    ("#0000CC", r"\ \Rightarrow\ "),
    ("#009900", r"\boldsymbol{\phi(a)}^{T}\boldsymbol{\phi(b)}"),
    ("#000000", r"\ \equiv\ "),
    ("#009900", r"\boldsymbol{K}"),
    ("#CC0000", r"\boldsymbol{(a,\ b)}"),
]


def measure(size):
    fig = plt.figure(figsize=(24, 4), dpi=DPI)
    fig.patch.set_alpha(0)
    rend = fig.canvas.get_renderer()
    segs = []
    for color, latex in ROW:
        t = fig.text(0, 0, f"${latex}$", fontsize=size, color=color)
        bb = t.get_window_extent(renderer=rend)
        segs.append([color, latex, bb.width, bb.height])
        t.remove()
    plt.close(fig)
    return segs


segs = measure(SIZE)
wpx = sum(s[2] for s in segs)
hpx = max(s[3] for s in segs)
scale = min(1.0, MAXW_IN * DPI / (wpx + 12), MAXH_IN * DPI / (hpx + 12))
size2 = SIZE * scale
if scale < 1.0:
    segs = measure(size2)
    wpx = sum(s[2] for s in segs)
    hpx = max(s[3] for s in segs)

W = int(wpx) + 12
H = int(hpx) + 12
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
fig.patch.set_alpha(0)
x = 6.0
for color, latex, w, h in segs:
    fig.text(x / W, 6.0 / H, f"${latex}$", fontsize=size2, color=color,
             ha="left", va="baseline")
    x += w
fig.canvas.draw()
buf = np.asarray(fig.canvas.buffer_rgba()).copy()
plt.close(fig)
img = Image.fromarray(buf)
bbox = img.split()[3].getbbox()
img = img.crop(bbox)
img.save(OUT)
meta = {
    "path": OUT,
    "w_px": img.size[0],
    "h_px": img.size[1],
    "w_in": img.size[0] / DPI,
    "h_in": img.size[1] / DPI,
    "dpi": DPI,
    "fontsize_pt": [size2],
    "fontset": "stix",
    "rows": ["||".join(f"{c}:{l}" for c, l in ROW)],
}
with open(OUT + ".json", "w") as f:
    json.dump(meta, f, indent=2)
print(OUT, img.size, round(img.size[0] / DPI, 4), "x", round(img.size[1] / DPI, 4), "in")
