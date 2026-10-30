#!/usr/bin/env python3
"""Render a LaTeX (mathtext) equation to a tight transparent PNG (serif math fontset).

Usage: python3 render_eq_serif.py '<latex>' out.png <fontsize_pt> <hexcolor>
Prints JSON: {path,w_px,h_px,w_in,h_in,baseline_px,baseline_frac,dpi,fontsize_pt,color}
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
PAD_PX = 8


def render(latex, out, fontsize, color):
    fig = plt.figure(figsize=(12, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="center", va="baseline")
    probe = fig.text(0.15, 0.5, "x", fontsize=fontsize, color=color,
                     ha="center", va="baseline")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pb = probe.get_window_extent(renderer=renderer)
    buf = np.asarray(fig.canvas.buffer_rgba())
    px0, px1 = max(int(pb.x0) - 2, 0), int(pb.x1) + 2
    baseline_row = int(np.where(buf[:, :, 3][:, px0:px1].any(axis=1))[0][-1])
    ink = buf[:, :, 3] > 8
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
            "w_in": round(float(x1 - x0) / DPI, 5), "h_in": round(h / DPI, 5),
            "baseline_px": int(baseline_row - y0),
            "baseline_frac": round(float(baseline_row - y0) / float(h), 5),
            "dpi": DPI, "fontsize_pt": fontsize, "color": color}
    plt.close(fig)
    return info


if __name__ == "__main__":
    latex, out, fs, color = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    print(json.dumps(render(latex, out, fs, color)))
