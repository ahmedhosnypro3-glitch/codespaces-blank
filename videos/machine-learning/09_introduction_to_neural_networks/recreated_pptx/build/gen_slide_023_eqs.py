#!/usr/bin/env python3
"""Generate slide_023 equation PNGs using matplotlib mathtext at 600dpi.
Equations rendered as 2D/Professional Format: stacked fractions, proper superscripts, left braces for piecewise.
"""
import json
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
DPI = 600
PAD_PX = 8

def render(latex, out, fontsize, color):
    """Render single mathtext string to tight transparent PNG, return manifest info."""
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

# --- Build manifest ---
manifest = {}

# Row 1: Uni-polar Unit Step
# f(x) = Uni-polar Unit Step = { 0 for x<0 ; 1 for x≥0 }
info = render(r"f(x) = \mathrm{Uni\text{-}polar~Unit~Step} = \left\{ 0\ \ \mathrm{for}\ x<0 \\ 1\ \ \mathrm{for}\ x\ge 0 \right\}", 
              f"{BUILD_DIR}/eq_023_unipolar.png", 14, "#000000")
manifest["eq_023_unipolar"] = [info]

# Row 1 derivative: f'(x) = { 0 for x≠0 ; ? for x=0 }
info = render(r"f'(x) = \left\{ 0\ \ \mathrm{for}\ x\neq 0 \\ ?\ \ \mathrm{for}\ x=0 \right\}", 
              f"{BUILD_DIR}/eq_023_unipolar_deriv.png", 14, "#000000")
manifest["eq_023_unipolar_deriv"] = [info]

# Row 2: Bi-polar Unit Step
info = render(r"f(x) = \mathrm{Bi\text{-}polar~Unit~Step} = \left\{ -1\ \ \mathrm{for}\ x<0 \\ 1\ \ \mathrm{for}\ x\ge 0 \right\}", 
              f"{BUILD_DIR}/eq_023_bipolar.png", 14, "#000000")
manifest["eq_023_bipolar"] = [info]

# Row 2 derivative: f'(x) = { 0 for x≠0 ; ? for x=0 }
info = render(r"f'(x) = \left\{ 0\ \ \mathrm{for}\ x\neq 0 \\ ?\ \ \mathrm{for}\ x=0 \right\}", 
              f"{BUILD_DIR}/eq_023_bipolar_deriv.png", 14, "#000000")
manifest["eq_023_bipolar_deriv"] = [info]

# Row 3: Sigmoid
# f(x) = Sigmoid(x) = 1/(1+e^{-x}) — with stacked fraction
info = render(r"f(x) = \mathrm{Sigmoid}(x) = \frac{1}{1+e^{-x}}", 
              f"{BUILD_DIR}/eq_023_sigmoid.png", 14, "#000000")
manifest["eq_023_sigmoid"] = [info]

# Row 3 derivative: f'(x) = f(x)(1-f(x))
info = render(r"f'(x) = f(x)(1-f(x))", 
              f"{BUILD_DIR}/eq_023_sigmoid_deriv.png", 14, "#0000FF")
manifest["eq_023_sigmoid_deriv"] = [info]

# Row 4: tanh
# f(x) = tanh(x) = sinh x / cosh x — stacked fraction
info = render(r"f(x) = \tanh(x) = \frac{\sinh x}{\cosh x}", 
              f"{BUILD_DIR}/eq_023_tanh.png", 14, "#000000")
manifest["eq_023_tanh"] = [info]

# Row 4 derivative: f'(x) = 1-f(x)^2
info = render(r"f'(x) = 1-f(x)^2", 
              f"{BUILD_DIR}/eq_023_tanh_deriv.png", 14, "#0000FF")
manifest["eq_023_tanh_deriv"] = [info]

# Row 5: tan^{-1}(x)  (this is arctan, not tanh — slide has it)
info = render(r"f(x) = \tan^{-1}(x)", 
              f"{BUILD_DIR}/eq_023_arctan.png", 14, "#000000")
manifest["eq_023_arctan"] = [info]

# Row 5 derivative: f'(x) = 1/(x^2+1)
info = render(r"f'(x) = \frac{1}{x^2+1}", 
              f"{BUILD_DIR}/eq_023_arctan_deriv.png", 14, "#CC0000")
manifest["eq_023_arctan_deriv"] = [info]

with open(f"{BUILD_DIR}/eq_023_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(json.dumps(manifest, indent=2))