#!/usr/bin/env python3
"""Render slide_023 equations as 2D PNGs (mathtext, 600dpi, tight trim).

Equations for the five activation-function rows:
  row1 left : Uni-polar Unit Step piecewise { 0 for x<0 ; 1 for x>=0 }
  row1 right: f'(x) piecewise { 0 for x!=0 ; ? for x=0 }
  row2 left : Bi-polar Unit Step piecewise { -1 for x<0 ; 1 for x>=0 }
  row2 right: f'(x) piecewise { 0 for x!=0 ; ? for x=0 }
  row3 left : f(x) = Sigmoid(x) = 1 / (1 + e^{-x})
  row3 right: f'(x) = f(x) (1 - f(x))
  row4 left : f(x) = tanh(x) = sinh x / cosh x
  row4 right: f'(x) = 1 - f(x)^2
  row5 left : f(x) = tan^{-1}(x)
  row5 right: f'(x) = 1/(x^2 + 1)
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
BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"


def render(latex, out, fontsize, color):
    fig = plt.figure(figsize=(10, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    eq = fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
                  ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r} (mathtext parse error?)")
    y0, y1 = max(rows[0] - PAD_PX, 0), min(rows[-1] + PAD_PX, buf.shape[0])
    x0, x1 = max(cols[0] - PAD_PX, 0), min(cols[-1] + PAD_PX, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    h = y1 - y0
    baseline_row = rows[-1]
    info = {"path": out, "w_px": int(x1 - x0), "h_px": int(h),
            "w_in": round(float(x1 - x0) / DPI, 5), "h_in": round(float(h) / DPI, 5),
            "baseline_px": int(baseline_row - y0),
            "baseline_frac": round(float(baseline_row - y0) / float(h), 5),
            "dpi": DPI, "fontsize_pt": fontsize, "color": color}
    plt.close(fig)
    return info


def render_piecewise(cases, out_path, fontsize_val=14, fontsize_cond=11, brace_size=48,
                     value_color="#000000"):
    """cases = list of (value, condition) tuples."""
    n = len(cases)
    fig = plt.figure(figsize=(6, n * 0.6), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    for i, (val, cond) in enumerate(cases):
        y = 0.85 - i * (0.85 / (n + 0.5))
        ax.text(0.35, y, val, fontsize=fontsize_val, color=value_color, ha='center', va='center')
        ax.text(0.42, y, f"for {cond}", fontsize=fontsize_cond, color="#000000", ha='left', va='center')
    brace_y = 0.85 - (n - 1) * (0.85 / (n + 0.5)) / 2
    ax.text(0.18, brace_y, "{", fontsize=brace_size, color="#000000", ha='center', va='center')
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - 8, 0), min(rows[-1] + 8, buf.shape[0])
    x0, x1 = max(cols[0] - 8, 0), min(cols[-1] + 8, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out_path)
    plt.close(fig)
    h = y1 - y0
    return {
        "path": out_path, "w_px": int(x1 - x0), "h_px": int(h),
        "w_in": round(float(x1 - x0) / DPI, 5), "h_in": round(float(h) / DPI, 5),
        "baseline_px": int(brace_y * buf.shape[0] - y0),
        "baseline_frac": round(float(brace_y * buf.shape[0] - y0) / float(h), 5),
        "dpi": DPI, "fontsize_pt": fontsize_val, "color": "#000000"
    }


def main():
    manifest = {}
    fs = 14

    # Row 1 left: uni-polar unit step piecewise
    manifest["eq_s023_unipolar"] = [render_piecewise(
        [("0", "x<0"), ("1", "x\\ge 0")], f"{BUILD_DIR}/eq_s023_unipolar.png")]

    # Row 2 left: bi-polar unit step piecewise
    manifest["eq_s023_bipolar"] = [render_piecewise(
        [("-1", "x<0"), ("1", "x\\ge 0")], f"{BUILD_DIR}/eq_s023_bipolar.png")]

    # Rows 1-2 right: derivative piecewise with green ?
    manifest["eq_s023_step_deriv"] = [render_piecewise(
        [("0", "x\\neq 0"), ("?", "x=0")], f"{BUILD_DIR}/eq_s023_step_deriv.png",
        value_color="#00B000")]

    # Row 3 left: sigmoid
    manifest["eq_s023_sigmoid"] = [render(
        r"f(x) = \mathrm{Sigmoid}(x) = \frac{1}{1+e^{-x}}",
        f"{BUILD_DIR}/eq_s023_sigmoid.png", fs, "#000000")]

    # Row 3 right
    manifest["eq_s023_sigmoid_deriv"] = [render(
        r"f'(x) = f(x)\,(1 - f(x))",
        f"{BUILD_DIR}/eq_s023_sigmoid_deriv.png", fs, "#000000")]

    # Row 4 left: tanh = sinh/cosh
    manifest["eq_s023_tanh"] = [render(
        r"f(x) = \tanh(x) = \frac{\sinh x}{\cosh x}",
        f"{BUILD_DIR}/eq_s023_tanh.png", fs, "#000000")]

    # Row 4 right
    manifest["eq_s023_tanh_deriv"] = [render(
        r"f'(x) = 1 - f(x)^{2}",
        f"{BUILD_DIR}/eq_s023_tanh_deriv.png", fs, "#000000")]

    # Row 5 left: arctan
    manifest["eq_s023_arctan"] = [render(
        r"f(x) = \tan^{-1}(x)",
        f"{BUILD_DIR}/eq_s023_arctan.png", fs, "#000000")]

    # Row 5 right
    manifest["eq_s023_arctan_deriv"] = [render(
        r"f'(x) = \frac{1}{x^{2}+1}",
        f"{BUILD_DIR}/eq_s023_arctan_deriv.png", fs, "#000000")]

    with open(f"{BUILD_DIR}/eq_s023_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
