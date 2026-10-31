#!/usr/bin/env python3
"""Slide 012 P matrix, compact variant sized to fit the blue box
(3.39 x 1.39 in): red 'P =', blue arc parentheses, 4x4 navy numerals."""
import json
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

ROWS = [["2", "4", "-11", "-12"], ["4", "8", "-22", "-24"],
        ["-11", "-22", "65", "72"], ["-12", "-24", "72", "80"]]
RED, BLUE, NAVY = "#CC0000", "#0000CC", "#002060"
FS, COL_W, ROW_H = 11, 0.46, 0.26

fig = plt.figure(figsize=(0.70 + COL_W * 4 + 0.50, ROW_H * 4 + 0.26), dpi=DPI)
fig.patch.set_alpha(0.0)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 0.70 + COL_W * 4 + 0.50)
ax.set_ylim(0, ROW_H * 4 + 0.26)
ax.axis("off")
ax.text(0.03, ROW_H * 2 + 0.05, r"$P\;=$", fontsize=13, color=RED, ha="left", va="center")

x0 = 0.74
for r, row in enumerate(ROWS):
    for c, val in enumerate(row):
        ax.text(x0 + c * COL_W + COL_W / 2, (3 - r) * ROW_H + ROW_H / 2 + 0.02,
                f"${val}$", fontsize=FS, color=NAVY, ha="center", va="center")

y_b, y_t = 0.05, ROW_H * 4 + 0.14
y_m = (y_b + y_t) / 2
for x, flip in ((x0 - 0.11, 1), (x0 + 3 * COL_W + COL_W + 0.02, -1)):
    th = np.linspace(-0.32 * np.pi, 0.32 * np.pi, 60)
    rr = (y_t - y_b) / 2
    ax.plot(x + flip * 0.09 * np.cos(th), y_m + rr * np.sin(th),
            color=BLUE, linewidth=2.0)

fig.canvas.draw()
buf = np.asarray(fig.canvas.buffer_rgba())
ink = buf[:, :, 3] > 8
rows = np.where(ink.any(axis=1))[0]
cols = np.where(ink.any(axis=0))[0]
pad = 8
y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad, buf.shape[0])
x0p, x1p = max(cols[0] - pad, 0), min(cols[-1] + pad, buf.shape[1])
Image.fromarray(buf[y0:y1, x0p:x1p]).save(OUT)
meta = {"path": OUT, "w_px": int(x1p - x0p), "h_px": int(y1 - y0),
        "w_in": round((x1p - x0p) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5)}
with open(OUT.replace(".png", ".json"), "w") as fh:
    json.dump(meta, fh)
print("p_matrix", meta["w_in"], "x", meta["h_in"])
