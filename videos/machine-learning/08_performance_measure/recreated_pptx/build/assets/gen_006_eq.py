#!/usr/bin/env python3
"""Render slide 006 accuracy equation as a composed transparent PNG (600 dpi).

mathtext lacks \\textcolor, so colored segments are rendered separately and
stacked with PIL: red 'Accuracy =', dark-red stacked fraction, green over/under
braces with green italic labels.
Output: eq_006.png + eq_006.json (w_px,h_px,w_in,h_in).
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD = 10
HERE = os.path.dirname(os.path.abspath(__file__))
RED = "#C00000"
DRED = "#8B0000"
GREEN = "#1E9C17"
BLUE = "#222067"


def seg(latex, color, size=16):
    fig = plt.figure(figsize=(12, 3), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=size, color=color,
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - 4, 0), min(rows[-1] + 5, buf.shape[0])
    x0, x1 = max(cols[0] - 4, 0), min(cols[-1] + 5, buf.shape[1])
    return buf[y0:y1, x0:x1]


def paste(canvas, im, x, y):
    h, w = im.shape[:2]
    canvas[y:y + h, x:x + w] = np.where(
        im[:, :, 3:4] > 8, im, canvas[y:y + h, x:x + w])


def hbrace(width_px, over=True):
    """Horizontal curly brace of the given span: render a tall vertical '{'
    spanning two rows, crop to the glyph, rotate 90 deg, resize to width."""
    im = seg(r"\left\{\substack{TP+TN \\ TP+FP+TN+FN}\right.", GREEN, 15)
    a = im[:, :, 3]
    cols = (a > 8).sum(axis=0)
    runs, s = [], None
    for x in range(len(cols)):
        if cols[x] > 0 and s is None:
            s = x
        elif cols[x] == 0 and s is not None:
            runs.append((s, x - 1))
            s = None
    if s is not None:
        runs.append((s, len(cols) - 1))
    x0, x1 = runs[0]  # leftmost ink run = the brace glyph
    brace = Image.fromarray(im[:, x0:x1 + 1]).rotate(
        -90 if over else 90, expand=True, resample=Image.BICUBIC)
    w, h = brace.size
    nh = max(int(h * width_px / w), 6)
    brace = brace.resize((width_px, nh), Image.LANCZOS)
    return np.asarray(brace)


acc = seg(r"\mathbf{Accuracy\ =}", RED, 17)
num = seg(r"TP+TN", DRED, 15)
den = seg(r"TP+FP+TN+FN", DRED, 15)
lbl_top = seg(r"\mathit{Correctly\ Classified}", GREEN, 11)
lbl_bot = seg(r"\mathit{All\ Samples}", GREEN, 11)

frac_w = max(num.shape[1], den.shape[1]) + 30
ob = hbrace(frac_w, over=True)
ub = hbrace(frac_w, over=False)

acc_w = acc.shape[1]
GAP = 14
BAR_H = 7
ROW_GAP = 6

W = PAD + acc_w + GAP + frac_w + PAD
H = (PAD + lbl_top.shape[0] + ROW_GAP + ob.shape[0] + ROW_GAP + num.shape[0]
     + BAR_H + ROW_GAP + den.shape[0] + ROW_GAP + ub.shape[0] + ROW_GAP
     + lbl_bot.shape[0] + PAD)
canvas = np.zeros((H, W, 4), dtype=np.uint8)

fx = PAD + acc_w + GAP  # fraction column left
# top label centered over fraction
paste(canvas, lbl_top, fx + (frac_w - lbl_top.shape[1]) // 2, PAD)
y = PAD + lbl_top.shape[0] + ROW_GAP
paste(canvas, ob, fx + (frac_w - ob.shape[1]) // 2, y)
y += ob.shape[0] + ROW_GAP
paste(canvas, num, fx + (frac_w - num.shape[1]) // 2, y)
y += num.shape[0]
# blue fraction bar
canvas[y:y + BAR_H, fx:fx + frac_w, 3] = 255
bar = np.zeros((BAR_H, frac_w, 4), dtype=np.uint8)
bar[:, :, 0] = int(BLUE[1:3], 16); bar[:, :, 1] = int(BLUE[3:5], 16)
bar[:, :, 2] = int(BLUE[5:7], 16); bar[:, :, 3] = 255
canvas[y:y + BAR_H, fx:fx + frac_w] = bar
y += BAR_H + ROW_GAP
paste(canvas, den, fx + (frac_w - den.shape[1]) // 2, y)
y += den.shape[0] + ROW_GAP
paste(canvas, ub, fx + (frac_w - ub.shape[1]) // 2, y)
y += ub.shape[0] + ROW_GAP
paste(canvas, lbl_bot, fx + (frac_w - lbl_bot.shape[1]) // 2, y)
# 'Accuracy =' vertically centered on the fraction bar
bar_mid = PAD + lbl_top.shape[0] + ROW_GAP + ob.shape[0] + ROW_GAP \
    + num.shape[0] + BAR_H // 2
paste(canvas, acc, PAD, bar_mid - acc.shape[0] // 2)

out = os.path.join(HERE, "eq_006.png")
Image.fromarray(canvas).save(out)
info = {"path": out, "w_px": int(W), "h_px": int(H),
        "w_in": round(W / DPI, 5), "h_in": round(H / DPI, 5), "dpi": DPI}
with open(os.path.join(HERE, "eq_006.json"), "w") as f:
    json.dump(info, f)
print(json.dumps(info))
