#!/usr/bin/env python3
"""Regenerate slide-008 equation assets at the measured original sizes.

- eq_008_frac_v2.png:  stacked fraction TP/(TP+FP), rendered ~24pt so the placed
  height matches the original's ~44px fraction block.
- eq_008_worked_v2.png: two-line worked example, line 1 black
  "Precision = 10/(10+2)" (2D fraction), line 2 bold blue "= 83.3%".
600 dpi transparent PNGs; placed in the pptx at exact w=w_px/600 in.
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 8
OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"


def render_line(latex, fontsize, color):
    fig = plt.figure(figsize=(10, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="center", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    plt.close(fig)
    return buf[y0:y1, x0:x1]


def save(arr, name):
    im = Image.fromarray(arr)
    im.save(f"{OUT}/{name}")
    return {"path": f"{OUT}/{name}", "w_px": im.size[0], "h_px": im.size[1],
            "w_in": round(im.size[0] / DPI, 5), "h_in": round(im.size[1] / DPI, 5),
            "dpi": DPI}


frac = render_line(r"\frac{TP}{TP+FP}", 32, "#000000")
info_frac = save(frac, "eq_008_frac_v2.png")

l1 = render_line(r"\mathrm{Precision}=\frac{10}{10+2}", 18, "#000000")
l2 = render_line(r"\mathbf{=\,83.3\%}", 18, "#0070C0")
gap = 10
top_pad = 10
w = max(l1.shape[1], l2.shape[1])
h = top_pad + l1.shape[0] + gap + l2.shape[0]
canvas = np.zeros((h, w, 4), dtype=np.uint8)
canvas[top_pad:top_pad + l1.shape[0], 0:l1.shape[1]] = l1
# line 2 centered under line 1 (original: line2 indented/centered, not left-flush)
xoff2 = (l1.shape[1] - l2.shape[1]) // 2
canvas[top_pad + l1.shape[0] + gap:, xoff2:xoff2 + l2.shape[1]] = l2
info_worked = save(canvas, "eq_008_worked_v2.png")

print(json.dumps({"frac": info_frac, "worked": info_worked}))
