#!/usr/bin/env python3
"""eq_025 rb5 assets for slide_025: one figure per equation, segments drawn
left-to-right on a shared baseline, tight-cropped to ink, 600 dpi.
rb5: fit each equation to FILL its spec box (scale up or down,
min(maxw/w, maxh/h)); taller column stacks via zero-width struts."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_025")
DPI = 600
PAD = 6
matplotlib.rcParams["mathtext.fontset"] = "cm"
R, B, K = "#CC0000", "#0033CC", "#000000"


def seg_width(latex, color, pt):
    fig = plt.figure(figsize=(30, 10), dpi=72)
    t = fig.text(0.02, 0.5, f"${latex}$", fontsize=pt, color=color,
                 ha="left", va="baseline")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    plt.close(fig)
    return bb.width / 72.0


def render_row(segs, pt):
    widths = [seg_width(l, c, pt) for c, l in segs]
    gap = 0.02
    total = sum(widths) + gap * len(segs)
    fig_w = max(total * 1.3 + 0.5, 1.0)
    fig_h = max(2.0, pt / 72.0 * 4.5)
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    fig.patch.set_alpha(0.0)
    x = 0.25 / fig_w
    for (c, l), w in zip(segs, widths):
        fig.text(x, 0.5, f"${l}$", fontsize=pt, color=c, ha="left", va="baseline")
        x += (w + gap) / fig_w
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    ink = buf[:, :, 3] > 40
    ys, xs = np.where(ink)
    return buf[max(ys.min() - PAD, 0):ys.max() + PAD + 1,
               max(xs.min() - PAD, 0):xs.max() + PAD + 1]


def fit(segs, size, maxw, maxh):
    pt = size
    canvas = render_row(segs, pt)
    for _ in range(14):
        w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
        s = min(maxw / w_in, maxh / h_in)
        if abs(s - 1.0) < 0.015:
            break
        pt *= s * 0.995
        canvas = render_row(segs, pt)
    return canvas, pt


STACK2 = lambda top, bot: f"\\binom{{{top}}}{{{bot}}}"
STACK3 = lambda a, b, c: f"\\binom{{{a}}}{{{STACK2(b, c)}}}"

# spec boxes [x0,y0,x1,y1] normalized -> inches on 13.33 x 7.5
BX = lambda r: ((r[2] - r[0]) * 13.33, (r[3] - r[1]) * 7.5)

EQS = {
    # E1 [0.071,0.161,0.198,0.243]: a = (a1/a2)   b = (b1/b2)
    "e1": ([(R, "a"), (K, "\\;=\\;"), (R, STACK2("a_1", "a_2")),
             (K, "\\;\\;\\;\\;"), (B, "b"), (K, "\\;=\\;"),
             (B, STACK2("b_1", "b_2"))], [0.071, 0.161, 0.198, 0.243]),
    # E2 [0.069,0.259,0.521,0.363]: a^T b = [a1 a2 | b1/b2]^12 = (a1b1+a2b2)^2 = ...
    "e2": ([(R, "a^{T}"), (B, "b"), (K, "\\;=\\;"),
             (K, "[\\;"), (R, "a_1\\;\\;a_2"), (K, "\\;|\\;"),
             (B, STACK2("b_1", "b_2")), (K, "\\;]^{12}\\;=\\;("),
             (R, "a_1"), (B, "b_1"), (K, "\\;+\\;"), (R, "a_2"), (B, "b_2"),
             (K, ")^{2}\\;=\\;"),
             (R, "a_1^{2}"), (B, "b_1^{2}"), (K, "\\;+\\;"),
             (R, "a_2^{2}"), (B, "b_2^{2}"), (K, "\\;+\\;2\\;"),
             (R, "a_1"), (B, "b_1"), (R, "a_2"), (B, "b_2")], [0.069, 0.259, 0.521, 0.363]),
    # E3 [0.069,0.380,0.458,0.541]: [a^T b]^2 = [a1^2 a2^2 sqrt2 a1a2 | b-col] = phi(a)^T phi(b)
    "e3": ([(K, "["), (R, "a^{T}"), (B, "b"), (K, "]^{2}\\;=\\;["),
             (R, "a_1^{2}\\;\\;a_2^{2}\\;\\;\\sqrt{2}\\,a_1a_2"), (K, "\\;|\\;"),
             (B, STACK3("b_1^{2}", "b_2^{2}", "\\sqrt{2}\\,b_1b_2")),
             (K, "\\;]\\;=\\;"), (K, "\\varphi(a)^{T}"), (B, "\\varphi(b)")], [0.069, 0.380, 0.458, 0.541]),
    # E4 [0.513,0.374,0.783,0.520]: Where: phi(x) =def (x1/x2) => (x1^2/x2^2/sqrt2 x1x2)^T
    "e4": ([(K, "Where:\\;\\varphi(x)\\;\\equiv\\;"),
             (K, STACK2("x_1", "x_2")),
             (R, "\\;\\Rightarrow\\;"),
             (K, f"{STACK3('x_1^{2}','x_2^{2}','\\sqrt{2}\\,x_1x_2')}^{{T}}")], [0.513, 0.374, 0.783, 0.520]),
    # E5 [0.644,0.520,0.732,0.550]: red "2D => 3D"
    "e5": ([(R, "\\mathbf{2D}\\;\\Rightarrow\\;\\mathbf{3D}")], [0.644, 0.520, 0.732, 0.550]),
}

manifest = {}
for name, (segs, region) in EQS.items():
    maxw, maxh = BX(region)
    canvas, pt = fit(segs, 16, maxw, maxh)
    fn = f"{name}_rb5.png"
    Image.fromarray(canvas).save(os.path.join(OUT, fn))
    manifest[name] = {
        "file": fn, "path": os.path.join(OUT, fn),
        "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
        "w_in": round(canvas.shape[1] / DPI, 5), "h_in": round(canvas.shape[0] / DPI, 5),
        "pt": round(pt, 2), "box": region,
    }
    print(name, manifest[name]["w_in"], manifest[name]["h_in"], manifest[name]["pt"])

with open(os.path.join(OUT, "manifest_rb5.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
