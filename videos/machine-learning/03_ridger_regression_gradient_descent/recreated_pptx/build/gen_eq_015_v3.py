#!/usr/bin/env python3
"""Generate slide-015 equation PNGs v3: clean black base + green lambda overlays.

Green segments per the original frame's per-symbol colour census (probe_015_colors.py):
eq1_l1/l2/l3, deriv_l1/l2, normal, solution carry a green \\lambda term; the
peach/redbox equations are plain black.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 8
BUILD = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BUILD, "assets")

BLACK = "#000000"
GREEN = "#2E9B57"

LATEX_EQS = [
  ("eq1_l1", r'J(W)=\frac{1}{2}(Y-\hat{Y})^T(Y-\hat{Y})+\frac{1}{2}\lambda W^T W = \frac{1}{2}(Y-XW)^T(Y-XW)+\frac{1}{2}\lambda W^T W',
   17, [r'\lambda W^T W'], 97, 104),
  ("eq1_l2", r'J(W)=\frac{1}{2}[Y^T Y + (XW)^T(XW) - Y^T(XW) - (XW)^T Y]+\frac{1}{2}\lambda W^T W',
   18, [r'\lambda W^T W'], 97, 163),
  ("eq1_l3", r'J(W)=\frac{1}{2}[Y^T Y + (XW)^T(XW) - 2(XW)^T Y]+\frac{1}{2}\lambda W^T W',
   18, [r'\lambda W^T W'], 97, 216),
  ("redbox_eq", r'\frac{\partial J(W)}{\partial W} = 0', 26, [], 81, 282),
  ("peach_eq", r'\frac{\partial W^T W}{\partial W} = 2W', 19, [], 791, 298),
  ("deriv_l1", r'\frac{\partial J(W)}{\partial W} = 0 = \frac{1}{2}[(XW)^T(X) + (X)^T(XW) - 2(X)^T Y]+\lambda W',
   22, [r'\lambda W'], 79, 350),
  ("deriv_l2", r'\frac{\partial J(W)}{\partial W} = 0 = \frac{1}{2}[2X^T X W - 2 X^T Y]+\lambda I W',
   21, [r'\lambda I W'], 79, 415),
  ("normal", r'(X^T X + \lambda I)W = X^T Y', 30, [r'\lambda I'], 229, 467),
  ("solution", r'\underline{W} = (X^T X + \lambda I)^{-1} X^T Y', 25, [r'\lambda I'], 553, 472),
]

def render_equation(latex, fontsize, color):
    fig = plt.figure(figsize=(16, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0: raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0]-PAD_PX, 0), min(rows[-1]+PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0]-PAD_PX, 0), min(cols[-1]+PAD_PX, buf.shape[1])
    img = Image.fromarray(buf[y0:y1, x0:x1])
    left_ink = cols[0]
    top_ink = rows[0]
    plt.close(fig)
    return img, left_ink, top_ink

def find_segment_offset(full_latex, seg_latex, fontsize):
    fig = plt.figure(figsize=(16, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${full_latex}$", fontsize=fontsize, color="#000000",
             ha="center", va="baseline")
    fig.text(0.5, 0.5, f"${seg_latex}$", fontsize=fontsize, color="#FFFFFF",
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    black_ink = (buf[:,:,0] < 50) & (buf[:,:,1] < 50) & (buf[:,:,2] < 50) & (buf[:,:,3] > 8)
    white_ink = (buf[:,:,0] > 200) & (buf[:,:,1] > 200) & (buf[:,:,2] > 200) & (buf[:,:,3] > 8)
    full_cols = np.where(black_ink.any(axis=0))[0]
    seg_cols = np.where(white_ink.any(axis=0))[0]
    if not len(full_cols) or not len(seg_cols):
        raise SystemExit(f"could not locate full/seg columns")
    full_left = full_cols[0]
    seg_left = seg_cols[0]
    plt.close(fig)
    return seg_left - full_left

table = {}
for tag, latex, fs, green_segs, xf, yf in LATEX_EQS:
    base_img, base_left, base_top = render_equation(latex, fs, BLACK)
    canvas = base_img.copy()
    for seg in green_segs:
        dx = find_segment_offset(latex, seg, fs)
        seg_img, seg_left, seg_top = render_equation(seg, fs, GREEN)
        pos_x = dx
        pos_y = seg_top - base_top
        canvas.paste(seg_img, (int(pos_x), int(pos_y)), seg_img)
    png = os.path.join(ASSETS, f"eq_015_{tag}_c.png")
    canvas.save(png)
    size = canvas.size
    table[tag] = {"png": png, "w_in": round(size[0]/DPI, 5), "h_in": round(size[1]/DPI, 5),
                  "x_frame": xf, "y_frame": yf, "fontsize_pt": fs,
                  "w_pt": int(size[0]/DPI*72), "h_pt": int(size[1]/DPI*72)}
    print(tag, table[tag])

with open(os.path.join(ASSETS, "eq015_table_c.json"), "w") as f:
    json.dump(table, f, indent=1)
print("WROTE", os.path.join(ASSETS, "eq015_table_c.json"))
