#!/usr/bin/env python3
"""Render piecewise equations as 2D PNGs for slide 017.
Uni-polar: F(x) = Uni-polar Unit Step = { 0 for x<0 ; 1 for x>=0 }
Bi-polar:  F(x) = Bi-polar Unit Step = { -1 for x<0 ; 1 for x>=0 }

The equation name part is plain text (rendered separately in the build);
the case stack is rendered as mathtext with a left brace.
"""
import json
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 8


def render(latex, out, fontsize, color):
    fig = plt.figure(figsize=(10, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    eq = fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
                  ha="center", va="baseline")
    probe = fig.text(0.15, 0.5, "x", fontsize=fontsize, color=color,
                     ha="center", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    px0, px1 = max(int(pb.x0) - 2, 0), int(pb.x1) + 2
    baseline_row = int(np.where(ink[:, px0:px1].any(axis=1))[0][-1])
    ink[:, :px1 + 20] = False
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    h = y1 - y0
    info = {"path": out, "w_px": int(x1 - x0), "h_px": int(h),
            "w_in": round(float(x1 - x0) / DPI, 5), "h_in": round(float(h) / DPI, 5),
            "baseline_px": int(baseline_row - y0),
            "baseline_frac": round(float(baseline_row - y0) / float(h), 5),
            "dpi": DPI, "fontsize_pt": fontsize, "color": color}
    plt.close(fig)
    return info


if __name__ == "__main__":
    which = sys.argv[1]
    fs = 12
    if which == "unipolar":
        latex = r"0\ \ \mathrm{for}\ x<0" + " \\ " + r"1\ \ \mathrm{for}\ x\ge 0"
        out = sys.argv[2]
        info = render(r"\left\{ " + latex + r" \right.", out, fs, "#000000")
    elif which == "bipolar":
        latex = r"-1\ \ \mathrm{for}\ x<0" + " \\ " + r"1\ \ \mathrm{for}\ x\ge 0"
        out = sys.argv[2]
        info = render(r"\left\{ " + latex + r" \right.", out, fs, "#000000")
    elif which == "linear":
        out = sys.argv[2]
        info = render(r"F(x) = x", out, fs, "#000000")
    print(json.dumps(info))
