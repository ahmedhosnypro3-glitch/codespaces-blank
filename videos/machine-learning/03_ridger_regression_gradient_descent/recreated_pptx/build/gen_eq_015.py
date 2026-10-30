#!/usr/bin/env python3
"""Generate slide-015 equation PNGs: black body + green lambda-term overlays.
Green term span is found by substring search in the LaTeX source (not fixed indices)."""
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
  ("normal", r'(X^T X + \lambda I)W = X^T Y', 30, [], 229, 467),
  ("solution", r'\underline{W} = (X^T X + \lambda I)^{-1} X^T Y', 25, [], 553, 472),
]

def draw_pair(full_latex, seg_latex, fontsize):
    """Render full (magenta) + segment (cyan) on identical canvas; return buffer + masks."""
    fig = plt.figure(figsize=(16, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${full_latex}$", fontsize=fontsize, color="#FF00FF",
             ha="center", va="baseline")
    if seg_latex:
        fig.text(0.5, 0.5, f"${seg_latex}$", fontsize=fontsize, color="#00FFFF",
                 ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    r, g, b = buf[:,:,0].astype(int), buf[:,:,1].astype(int), buf[:,:,2].astype(int)
    magenta = (r > 200) & (g < 100) & (b > 200)
    cyan = (r < 100) & (g > 200) & (b > 200)
    return fig, buf, magenta, cyan

def render_full(full_latex, fontsize, color):
    """Render the full equation in one color; return tight RGBA image."""
    fig = plt.figure(figsize=(16, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${full_latex}$", fontsize=fontsize, color=color,
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0: raise SystemExit(f"no ink for {full_latex!r}")
    y0, y1 = max(rows[0]-PAD_PX, 0), min(rows[-1]+PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0]-PAD_PX, 0), min(cols[-1]+PAD_PX, buf.shape[1])
    img = Image.fromarray(buf[y0:y1, x0:x1])
    info = (x0, y0)
    plt.close(fig)
    return img, info

table = {}
for tag, latex, fs, green_segs, xf, yf in LATEX_EQS:
    base_img, (crop_x, crop_y) = render_full(latex, fs, BLACK)
    canvas = base_img.copy()
    for seg in green_segs:
        # Measure seg position on a probe canvas (identical layout)
        fig, buf, magenta, cyan = draw_pair(latex, seg, fs)
        srows = np.where(cyan.any(axis=1))[0]; scols = np.where(cyan.any(axis=0))[0]
        mrows = np.where(magenta.any(axis=1))[0]
        if not len(scols): raise SystemExit(f"segment {seg!r} not located")
        # Segment bbox in FIGURE px:
        st, sl, sb, sr = srows[0], scols[0], srows[-1]+1, scols[-1]+1
        # Figure crop origin for the BLACK render (same canvas layout):
        crop_fx = mrows[0]-PAD_PX
        crop_fy = np.where(magenta.any(axis=1))[0][0]-PAD_PX
        # position inside canvas:
        pos_x = sl - crop_fx
        pos_y = st - crop_fy
        seg_img = Image.fromarray(buf[st:sb, sl:sr])
        canvas.paste(seg_img, (int(pos_x), int(pos_y)), seg_img)
        plt.close(fig)
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
