#!/usr/bin/env python3
"""Slide 006 equation assets, PIL-adjudicated against the original frame.

Original eq box (unique_slides/slide_006.jpg, 1px = 1pt):
  blue frame (64,233)-(443,368); red enclosure (70,273)-(422,330) wraps ONLY
  the equation; green braces + red italic captions sit OUTSIDE it; equation ink
  black with a BLUE fraction bar (measured (33,26,103)).
Outputs (600 dpi, placed at exact size w = px/600 in):
  eq_006b.png         "Accuracy =" + stacked fraction, black, blue bar,
                      fitted into 336x46 pt (2800x383 px canvas)
  brace_006_over.png  green overbrace, fitted into 73x17 pt
  brace_006_under.png green underbrace, fitted into 220x16 pt
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
HERE = os.path.dirname(os.path.abspath(__file__))
BLACK = "#000000"
GREEN = "#1E9C17"
BLUE = "#222067"


def seg(latex, color, size=40):
    fig = plt.figure(figsize=(12, 3), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=size, color=color,
             ha="center", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    return buf[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]


def fit(im, w_px, h_px):
    """Resize ink-preserving crop to fit inside w_px x h_px, center on canvas."""
    h, w = im.shape[:2]
    scale = min(w_px / w, h_px / h)
    nw, nh = max(int(w * scale), 1), max(int(h * scale), 1)
    resized = np.asarray(Image.fromarray(im).resize((nw, nh), Image.LANCZOS))
    canvas = np.zeros((h_px, w_px, 4), dtype=np.uint8)
    y0 = (h_px - nh) // 2
    x0 = (w_px - nw) // 2
    canvas[y0:y0 + nh, x0:x0 + nw] = resized
    return canvas


def pad_to(im, w):
    if im.shape[1] >= w:
        return im
    out = np.zeros((im.shape[0], w, 4), dtype=np.uint8)
    x0 = (w - im.shape[1]) // 2
    out[:, x0:x0 + im.shape[1]] = im
    return out


def equation():
    acc = seg(r"\mathrm{Accuracy}\ =", BLACK)
    num = seg(r"TP+TN", BLACK)
    den = seg(r"TP+FP+TN+FN", BLACK)
    gap = 18
    bar_h = 26
    frac_w = max(num.shape[1], den.shape[1])
    num = pad_to(num, frac_w)
    den = pad_to(den, frac_w)
    bar = np.zeros((bar_h, frac_w, 4), dtype=np.uint8)
    bar[:, :, 0] = 0x22
    bar[:, :, 1] = 0x20
    bar[:, :, 2] = 0x67
    bar[:, :, 3] = 255
    frac = np.concatenate([num, np.full((gap, frac_w, 4), 0, dtype=np.uint8),
                           bar, np.full((gap, frac_w, 4), 0, dtype=np.uint8), den])
    total = frac.shape[0]
    h = max(acc.shape[0], total)
    w = acc.shape[1] + 40 + frac_w
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    ay = (h - acc.shape[0]) // 2
    canvas[ay:ay + acc.shape[0], :acc.shape[1]] = acc
    fx = acc.shape[1] + 40
    fy = (h - total) // 2
    canvas[fy:fy + total, fx:fx + frac_w] = frac
    out = fit(canvas, 2800, 383)
    Image.fromarray(out).save(os.path.join(HERE, "eq_006b.png"))
    print("eq_006b.png", out.shape)


def brace(over, w_px, h_px, name):
    # mathtext has no \overbrace: render a tall '{' and rotate it horizontal
    im = seg(r"\left\{\rule{0pt}{2.2em}\right.", GREEN, 60)
    pil = Image.fromarray(im).rotate(90 if not over else -90, expand=True)
    out = fit(np.asarray(pil), w_px, h_px)
    Image.fromarray(out).save(os.path.join(HERE, name))
    print(name, out.shape)


def main():
    equation()
    brace(True, int(73 / 72 * DPI), int(17 / 72 * DPI), "brace_006_over.png")
    brace(False, int(220 / 72 * DPI), int(16 / 72 * DPI), "brace_006_under.png")


if __name__ == "__main__":
    main()
