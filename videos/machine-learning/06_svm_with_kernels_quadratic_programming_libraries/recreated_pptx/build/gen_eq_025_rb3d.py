#!/usr/bin/env python3
"""Wave-3 fix: eq_025/*_rb3d.png — one-figure-per-row mathtext at 600 dpi.

Segment widths probed at 72 dpi (cheap), final row rendered in a single
600-dpi figure with all segments on a common baseline, then cropped to ink.
Point size shrinks until ink fits the target box.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_025")
os.makedirs(OUT, exist_ok=True)

R, B, K = "#CC0000", "#0033CC", "#000000"

EQS = {
    "e1": ("||".join([
        f"{R}:a", f"{K}:\\;=\\;", f"{R}:\\left(\\substack{{a_1\\\\a_2}}\\right)",
        f"{K}:\\;\\;", f"{B}:b", f"{K}:\\;=\\;",
        f"{B}:\\left(\\substack{{b_1\\\\b_2}}\\right)",
    ]), 22, 2.50, 0.62),
    "e2": ("||".join([
        f"{R}:a^{{T}}", f"{B}:b", f"{K}:\\;=\\;",
        f"{R}:[\\;a_1\\;\\;a_2", f"{K}:\\;|\\;",
        f"{B}:\\substack{{b_1\\\\b_2}}\\;]^{{12}}",
        f"{K}:\\;=\\;(",
        f"{R}:a_1", f"{B}:b_1", f"{K}:\\;+\\;", f"{R}:a_2", f"{B}:b_2",
        f"{K}:)^{{2}}\\;=\\;",
        f"{R}:a_1^{{2}}", f"{B}:b_1^{{2}}", f"{K}:\\;+\\;",
        f"{R}:a_2^{{2}}", f"{B}:b_2^{{2}}", f"{K}:\\;+\\;2\\;",
        f"{R}:a_1", f"{B}:b_1", f"{R}:a_2", f"{B}:b_2",
    ]), 22, 6.00, 0.75),
    "e3": ("||".join([
        f"{K}:[", f"{R}:a^{{T}}", f"{B}:b", f"{K}:]^{{2}}\\;=\\;",
        f"{K}:[\\;", f"{R}:a_1^{{2}}\\;\\;a_2^{{2}}\\;\\;\\sqrt{{2}}\\,a_1a_2",
        f"{K}:\\;|\\;",
        f"{B}:\\substack{{b_1^{{2}}\\\\b_2^{{2}}\\\\sqrt{{2}}\\,b_1b_2}}",
        f"{K}:\\;]\\;=\\;",
        f"{K}:\\varphi(a)^{{T}}", f"{B}:\\varphi(b)",
    ]), 22, 5.00, 1.10),
    "e4": ("||".join([
        f"{K}:Where:\\;\\varphi(x)\\;\\equiv\\;",
        f"{K}:\\left(\\substack{{x_1\\\\x_2}}\\right)",
        f"{R}:\\;\\Rightarrow\\;",
        f"{K}:\\left(\\substack{{x_1^{{2}}\\\\x_2^{{2}}\\\\sqrt{{2}}\\,x_1x_2}}\\right)^{{T}}",
    ]), 22, 3.20, 1.00),
    "e5": (f"{R}:\\mathbf{{2D\\;\\Rightarrow\\;3D}}", 22, 1.00, 0.22),
}


def parse_row(row):
    segs = []
    for part in row.split("||"):
        color, latex = part.split(":", 1)
        segs.append((color if color.startswith("#") else "#" + color, latex))
    return segs


def seg_width_in(latex, color, pt):
    fig = plt.figure(figsize=(max(2.0, len(latex) * pt / 72.0), 2.0), dpi=72)
    fig.patch.set_alpha(0.0)
    t = fig.text(0.01, 0.5, f"${latex}$", fontsize=pt, color=color,
                 ha="left", va="baseline")
    fig.canvas.draw()
    ext = t.get_window_extent(renderer=fig.canvas.get_renderer())
    plt.close(fig)
    return ext.width / 72.0


def render_row_direct(segs, widths, pt, gap_in=0.04):
    total_w = sum(widths) + gap_in * (len(segs) - 1)
    fig_w = total_w + 0.6
    fig_h = pt / 72.0 * 4.5 + 0.6
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.patch.set_facecolor("none")
    x = 0.3 / fig_w
    y = 0.3 / fig_h
    for (c, l), w in zip(segs, widths):
        fig.text(x, y, f"${l}$", fontsize=pt, color=c, ha="left", va="baseline")
        x += (w + gap_in) / fig_w
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    ink = buf[:, :, 3] > 0
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    pad = 8
    r0, r1 = max(rows.min() - pad, 0), min(rows.max() + pad + 1, buf.shape[0])
    c0, c1 = max(cols.min() - pad, 0), min(cols.max() + pad + 1, buf.shape[1])
    return buf[r0:r1, c0:c1]


def fit(row, size, maxw, maxh, min_pt=7.0):
    segs = parse_row(row)
    pt = size
    for _ in range(14):
        widths = [seg_width_in(l, c, pt) for c, l in segs]
        canvas = render_row_direct(segs, widths, pt)
        w_in, h_in = canvas.shape[1] / DPI, canvas.shape[0] / DPI
        if w_in <= maxw and h_in <= maxh:
            break
        pt = max(min_pt, pt * 0.94)
    return canvas, pt


manifest = {}
for name, (row, size, maxw, maxh) in EQS.items():
    canvas, pt = fit(row, size, maxw, maxh)
    fn = f"{name}_rb3d.png"
    Image.fromarray(canvas).save(os.path.join(OUT, fn))
    manifest[name] = {
        "file": fn, "path": os.path.join(OUT, fn),
        "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
        "w_in": round(canvas.shape[1] / DPI, 5), "h_in": round(canvas.shape[0] / DPI, 5),
        "pt": round(pt, 2),
    }
    print(name, manifest[name]["w_in"], manifest[name]["h_in"], manifest[name]["pt"], flush=True)

with open(os.path.join(OUT, "manifest_rb3d.json"), "w") as fh:
    json.dump(manifest, fh, indent=2)
