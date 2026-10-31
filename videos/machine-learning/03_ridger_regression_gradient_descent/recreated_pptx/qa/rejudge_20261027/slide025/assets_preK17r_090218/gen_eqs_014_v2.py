#!/usr/bin/env python3
"""Slide 014 equation assets v2 — measured colors from the original frame.

Final objective: dark 'J(W) = ', BLUE 1/2, dark '[', RED (Y-Yhat)^T(Y-Yhat),
dark ' + lambda ', GREEN W^T W, dark ']' — composed on a shared baseline.
Vectors: bare pmatrix (N x 1 subscript moved to PPTX text), both RED C00000.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

OUT = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
       "recreated_pptx/build/assets/")
DPI = 600
PAD = 8
DARK = "#1A1A1A"
BLUE = "#0000A8"
RED = "#C00000"
GREEN = "#3E7C34"

SEGS = [
    (r"J(W)\;=\;", DARK),
    (r"\frac{1}{2}\left[\right.", BLUE),
    (r"\left(Y-\hat{Y}\right)^{\top}\left(Y-\hat{Y}\right)", RED),
    (r"\;+\;\lambda\;", DARK),
    (r"\left.\,W^{\top}W\right]", GREEN),
]

FS = 17


def render_seg(latex, color):
    fig = plt.figure(figsize=(12, 3), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, "$" + latex + "$", fontsize=FS, color=color,
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    baseline = buf.shape[0] // 2          # va='baseline' anchor row
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, buf.shape[0])
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    plt.close(fig)
    return buf[y0:y1, x0:x1], baseline - y0


def compose(segs, out_name):
    parts = [render_seg(l, c) for l, c in segs]
    base = max(b for _, b in parts)
    asc = max(img.shape[0] - b for img, b in parts)
    H = base + asc
    W = sum(img.shape[1] for img, _ in parts)
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    xoff = 0
    for img, b in parts:
        canvas[base - b:base - b + img.shape[0], xoff:xoff + img.shape[1]] = img
        xoff += img.shape[1]
    ink = canvas[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, canvas.shape[0])
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, canvas.shape[1])
    Image.fromarray(canvas[y0:y1, x0:x1]).save(OUT + out_name)
    w_in, h_in = (x1 - x0) / DPI, (y1 - y0) / DPI
    print(f"{out_name}: {x1-x0}x{y1-y0}px = {w_in:.4f}x{h_in:.4f}in")
    return w_in, h_in


VEC_DEFS = {
    "eq_014_Yvec.png": [("y", "1"), ("y", "2"), (None, "\\vdots"), ("y", "n")],
    "eq_014_Yhatvec.png": [("\\hat{y}", "1"), ("\\hat{y}", "2"), (None, "\\vdots"), ("\\hat{y}", "n")],
}


def render_vector(entries, out_name, fs=16):
    ph = (len(entries) - 1) * 0.19
    top, bot = 0.85, 0.85 - ph
    fig = plt.figure(figsize=(3, 1.5), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ys = np.linspace(top, bot, len(entries))
    for y, (base, sub) in zip(ys, entries):
        if base is None:
            fig.text(0.52, y, "$" + sub + "$", fontsize=fs, color=RED,
                     ha="center", va="center")
        else:
            fig.text(0.5, y, "$" + base + "_{" + sub + "}$", fontsize=fs,
                     color=RED, ha="right", va="center")
    # tall parenthesis glyphs scaled to the stack height
    paren_h = ph * 1.15 + 0.35
    paren_fs = paren_h * 72 * 2.6
    paren_fs = 100
    fig.text(0.40, (top + bot) / 2, "(", fontsize=paren_fs, color=RED,
             ha="center", va="center", family="DejaVu Sans")
    fig.text(0.64, (top + bot) / 2, ")", fontsize=paren_fs, color=RED,
             ha="center", va="center", family="DejaVu Sans")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, buf.shape[0])
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(OUT + out_name)
    w_in, h_in = (x1 - x0) / DPI, (y1 - y0) / DPI
    print(f"{out_name}: {x1-x0}x{y1-y0}px = {w_in:.4f}x{h_in:.4f}in")
    return w_in, h_in


if __name__ == "__main__":
    info = {}
    info["eq_014_final"] = compose(SEGS, "eq_014_final.png")
    for name, entries in VEC_DEFS.items():
        info[name] = render_vector(entries, name)
    with open(OUT + "eq_index_014.json", "w") as f:
        json.dump(info, f, indent=1)
