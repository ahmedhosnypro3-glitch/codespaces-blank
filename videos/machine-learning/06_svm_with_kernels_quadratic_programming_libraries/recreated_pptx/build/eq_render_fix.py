#!/usr/bin/env python3
"""Single-figure multi-segment mathtext renderer -> tight transparent PNG.

render_math.render_row crops each segment separately and then top-aligns
the crops, which drops superscripts to the wrong height in composed rows.
This module instead draws every '||'-separated COLOR:latex segment into ONE
figure on a shared baseline (fig.text va="baseline") and crops the whole
canvas once, so superscripts/subscripts keep their true positions.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
PAD = 8


def parse_row(row):
    segs = []
    for part in row.split("||"):
        head = part.split("\\", 1)[0]
        if ":" in head:
            color, latex = part.split(":", 1)
        else:
            color, latex = "#333333", part
        segs.append((color if color.startswith("#") else "#" + color, latex))
    return segs


def _measure(segs, pt):
    fig = plt.figure(figsize=(40, 6), dpi=72)
    r = fig.canvas.get_renderer()
    widths = []
    for color, latex in segs:
        t = fig.text(0.01, 0.5, f"${latex}$", fontsize=pt, ha="left", va="baseline")
        widths.append(t.get_window_extent(renderer=r).width / 72.0)
        t.remove()
    plt.close(fig)
    return widths


def render_row(row, pt):
    segs = parse_row(row)
    widths = _measure(segs, pt)
    total = sum(widths)
    margin = 0.25
    fig_w = total + 2 * margin
    fig_h = max(1.2, min(6.0, total * 0.30 + 0.8))
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    fig.patch.set_alpha(0.0)
    x = margin / fig_w
    for (color, latex), w in zip(segs, widths):
        fig.text(x, 0.5, f"${latex}$", fontsize=pt, color=color,
                 ha="left", va="baseline")
        x += (w + 0.03) / fig_w
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    ink = buf[:, :, 3] > 10
    ys, xs = np.nonzero(ink)
    if len(ys) == 0:
        raise SystemExit(f"no ink for row {row!r}")
    y0, y1 = max(ys.min() - PAD, 0), min(ys.max() + PAD + 1, buf.shape[0])
    x0, x1 = max(xs.min() - PAD, 0), min(xs.max() + PAD + 1, buf.shape[1])
    return buf[y0:y1, x0:x1]


def save_png(row, pt, path):
    canvas = render_row(row, pt)
    Image.fromarray(canvas).save(path)
    return canvas.shape[1] / DPI, canvas.shape[0] / DPI
