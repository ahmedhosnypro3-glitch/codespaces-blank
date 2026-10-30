#!/usr/bin/env python3
"""Render colored mathtext equations by compositing black base + green highlights."""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 8

def to_py(obj):
    if isinstance(obj, (np.integer, np.floating)):
        return obj.item()
    if isinstance(obj, dict):
        return {k: to_py(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_py(v) for v in obj]
    return obj

def render_black(latex, out, fontsize, color="#000000"):
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
    baseline_row = int(np.where(ink[:, int(pb.x0):int(pb.x1)].any(axis=1))[0][-1])
    ink[:, :int(pb.x1)+20] = False
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r}")
    y0, y1 = max(rows[0]-PAD_PX, 0), min(rows[-1]+PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0]-PAD_PX, 0), min(cols[-1]+PAD_PX, buf.shape[1])
    img = Image.fromarray(buf[y0:y1, x0:x1])
    h = y1 - y0
    plt.close(fig)
    return img, {"w_px": int(x1-x0), "h_px": int(h), "baseline_px": int(baseline_row - y0),
                 "w_in": round(float(x1-x0)/DPI, 5), "h_in": round(float(h)/DPI, 5),
                 "baseline_frac": round(float(baseline_row - y0)/float(h), 5),
                 "dpi": DPI, "fontsize_pt": fontsize, "color": color}

if __name__ == "__main__":
    # Fix deriv_l2 to include "I"
    latex = r'\frac{\partial J(W)}{\partial W} = 0 = \frac{1}{2}[2X^T X W - 2 X^T Y]+\lambda I W'
    out = 'videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/eq_015_deriv_l2_fixed.png'
    img, info = render_black(latex, out, 21, "#000000")
    img.save(out)
    print(json.dumps(to_py({**info, "path": out})))
