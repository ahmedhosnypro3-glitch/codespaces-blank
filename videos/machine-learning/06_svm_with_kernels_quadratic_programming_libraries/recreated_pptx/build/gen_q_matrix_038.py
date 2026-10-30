#!/usr/bin/env python3
"""Render the 4x4 Q matrix with spanning square brackets for slide 038.
Brackets are drawn as vector lines (spanning all four rows), numbers set in the
CM math font. Transparent PNG at 600 dpi.
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
       "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_038/q_matrix.png")

ROWS = [
    ["4.5", "12.5", "-72", "-84.5"],
    ["12.5", "40.5", "-264.5", "-312.5"],
    ["-72", "-264.5", "2178", "2664.5"],
    ["-84.5", "-312.5", "2664.5", "3280.5"],
]
FS = 18
COL_W = 1.5
ROW_H = 0.55

fig = plt.figure(figsize=(COL_W * 4 + 1.2, ROW_H * 4 + 0.5), dpi=DPI)
fig.patch.set_alpha(0.0)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, COL_W * 4 + 1.2)
ax.set_ylim(0, ROW_H * 4 + 0.5)
ax.axis("off")

for r, row in enumerate(ROWS):
    for c, val in enumerate(row):
        ax.text(0.9 + c * COL_W + COL_W / 2 - 0.1, (3 - r) * ROW_H + ROW_H / 2 + 0.02,
                f"${val}$", fontsize=FS, color="#000000", ha="center", va="center")

# square brackets spanning all four rows
x_l, x_r = 0.25, 0.9 + 3 * COL_W + COL_W - 0.55
y_b, y_t = 0.12, ROW_H * 4 + 0.08
tick = 0.22
for x, sgn in ((x_l, 1), (x_r, -1)):
    ax.plot([x, x], [y_b, y_t], color="#000000", linewidth=1.6)
    ax.plot([x, x + sgn * tick], [y_b, y_b], color="#000000", linewidth=1.6)
    ax.plot([x, x + sgn * tick], [y_t, y_t], color="#000000", linewidth=1.6)

fig.canvas.draw()
buf = np.asarray(fig.canvas.buffer_rgba())
ink = buf[:, :, 3] > 8
rows = np.where(ink.any(axis=1))[0]
cols = np.where(ink.any(axis=0))[0]
y0, y1 = max(rows[0] - 8, 0), min(rows[-1] + 8, buf.shape[0])
x0, x1 = max(cols[0] - 8, 0), min(cols[-1] + 8, buf.shape[1])
os.makedirs(os.path.dirname(OUT), exist_ok=True)
Image.fromarray(buf[y0:y1, x0:x1]).save(OUT)
print(json.dumps({"path": OUT, "w_px": int(x1 - x0), "h_px": int(y1 - y0),
                  "w_in": round((x1 - x0) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5)}))
