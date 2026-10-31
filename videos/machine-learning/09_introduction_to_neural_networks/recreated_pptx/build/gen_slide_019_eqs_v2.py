#!/usr/bin/env python3
"""Slide 019 equation PNGs - 2D professional format (stacked fractions, real superscripts).

Ink colour corrected to #000000: PIL measurement of the original frame shows the
caption glyphs are predominantly dark/black (warm-tinted by JPEG) with only
partial red accents, while the v1 build painted every caption solid #C00000.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
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
    pb = probe.get_window_extent(renderer)
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
    info = {"path": os.path.basename(out), "w_px": int(x1 - x0), "h_px": int(h),
            "w_in": round(float(x1 - x0) / DPI, 5), "h_in": round(float(h) / DPI, 5),
            "baseline_px": int(baseline_row - y0),
            "baseline_frac": round(float(baseline_row - y0) / float(h), 5),
            "dpi": DPI, "fontsize_pt": fontsize, "color": color}
    plt.close(fig)
    return info


EQUATIONS = [
    ("sigmoid", r"f(x) = \mathrm{Sigmoid}(x) = \frac{1}{1+e^{-x}}"),
    ("tanh", r"f(x) = \tanh(x) = \frac{\sinh x}{\cosh x}"),
    ("tan", r"f(x) = \tan(x)"),
    ("arctan", r"f(x) = \tan^{-1}(x)"),
]

manifest = {}
for key, latex in EQUATIONS:
    out = f"{BUILD_DIR}/eq_{key}.png"
    info = render(latex, out, 16, "#000000")
    info["mathtext"] = latex
    manifest[f"eq_{key}"] = [info]
    with open(f"{BUILD_DIR}/eq_{key}.json", "w") as f:
        json.dump(info, f, indent=2)
    print(key, info["w_px"], "x", info["h_px"], "px")

with open(f"{BUILD_DIR}/eq_019_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
