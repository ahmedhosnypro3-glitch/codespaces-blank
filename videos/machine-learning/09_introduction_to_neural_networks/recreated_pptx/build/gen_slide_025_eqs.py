#!/usr/bin/env python3
"""Render slide 025 equations as 2D PNGs (matplotlib mathtext, 600 dpi).

Piecewise unit-step definitions use a real stacked cases construct with a
left curly brace spanning both lines, matching the original slide's 2D format.
"""
import sys
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD_PX = 6


def render(mathtext, out, fontsize, color):
    fig = plt.figure(figsize=(12, 6), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${mathtext}$", fontsize=fontsize, color=color,
             ha="center", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {mathtext!r}")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    plt.close(fig)
    return {"path": out, "w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "w_in": round(float(x1 - x0) / DPI, 5), "h_in": round(float(y1 - y0) / DPI, 5),
            "dpi": DPI, "font_size_pt": fontsize, "color": color,
            "image": out.rsplit("/", 1)[-1], "mathtext": mathtext}


if __name__ == "__main__":
    outdir = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
              "09_introduction_to_neural_networks/recreated_pptx/build")
    fs = 20
    eqs = [
        # name, mathtext, out-file, color
        ("eq_s025_linear",
         r"F(x) = x",
         "eq_s025_linear.png", "#000000"),
        ("eq_s025_unipolar",
         r"F(x) = \mathrm{Uni-polar\ Unit\ Step} = \left\{ \substack{0 \ \ \mathrm{for}\ x < 0 \\ 1 \ \ \mathrm{for}\ x \geq 0} \right.",
         "eq_s025_unipolar.png", "#000000"),
        ("eq_s025_bipolar",
         r"F(x) = \mathrm{Bi-polar\ Unit\ Step} = \left\{ \substack{-1 \ \ \mathrm{for}\ x < 0 \\ 1 \ \ \mathrm{for}\ x \geq 0} \right.",
         "eq_s025_bipolar.png", "#000000"),
    ]
    results = []
    for name, mt, fn, color in eqs:
        info = render(mt, f"{outdir}/{fn}", fs, color)
        info["name"] = name
        results.append(info)
        print(json.dumps(info))
    with open(f"{outdir}/slide_025_equations.json", "w") as f:
        json.dump({"slide": "025", "equations": results}, f, indent=2)
