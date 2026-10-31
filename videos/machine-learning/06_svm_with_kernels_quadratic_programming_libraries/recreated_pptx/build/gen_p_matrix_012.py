#!/usr/bin/env python3
"""Slide 012 P matrix: red 'P =' label, large blue round parentheses flanking a
4x4 matrix of navy numerals. Tight transparent PNG at 600 dpi.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
OUT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_012/p_matrix.png")

ROWS = [
    ["2", "4", "-11", "-12"],
    ["4", "8", "-22", "-24"],
    ["-11", "-22", "65", "72"],
    ["-12", "-24", "72", "80"],
]
RED = "#CC0000"
BLUE = "#0000CC"
NAVY = "#002060"
FS = 12
COL_W = 0.50
ROW_H = 0.30

fig = plt.figure(figsize=(0.75 + COL_W * 4 + 0.55, ROW_H * 4 + 0.30), dpi=DPI)
fig.patch.set_alpha(0.0)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 0.75 + COL_W * 4 + 0.55)
ax.set_ylim(0, ROW_H * 4 + 0.30)
ax.axis("off")

ax.text(0.03, ROW_H * 2 + 0.06, r"$P\;=$", fontsize=14, color=RED, ha="left", va="center")

x0 = 0.80
for r, row in enumerate(ROWS):
    for c, val in enumerate(row):
        ax.text(x0 + c * COL_W + COL_W / 2, (3 - r) * ROW_H + ROW_H / 2 + 0.03,
                f"${val}$", fontsize=FS, color=NAVY, ha="center", va="center")

# large round parentheses spanning all four rows (drawn as arcs)
y_b, y_t = 0.06, ROW_H * 4 + 0.16
y_m = (y_b + y_t) / 2
for x, flip in ((x0 - 0.12, 1), (x0 + 3 * COL_W + COL_W + 0.02, -1)):
    th = np.linspace(-0.32 * np.pi, 0.32 * np.pi, 60)
    rr = (y_t - y_b) / 2
    ax.plot(x + flip * 0.10 * np.cos(th), y_m + rr * np.sin(th),
            color=BLUE, linewidth=2.2)

fig.canvas.draw()
buf = np.asarray(fig.canvas.buffer_rgba())
ink = buf[:, :, 3] > 8
rows = np.where(ink.any(axis=1))[0]
cols = np.where(ink.any(axis=0))[0]
y0, y1 = max(rows[0] - 8, 0), min(rows[-1] + 8, buf.shape[0])
x0c, x1c = max(cols[0] - 8, 0), min(cols[-1] + 8, buf.shape[1])
os.makedirs(os.path.dirname(OUT), exist_ok=True)
Image.fromarray(buf[y0:y1, x0c:x1c]).save(OUT)
print(json.dumps({"path": OUT, "w_px": int(x1c - x0c), "h_px": int(y1 - y0),
                  "w_in": round((x1c - x0c) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5)}))
