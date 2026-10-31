#!/usr/bin/env python3
"""Render the three slide-006 equations as 600 dpi transparent PNGs with the
original's red ink preserved: the X in d_j(X) and the bias term b_j * 1.

Each equation is drawn as colour segments with matplotlib mathtext and composited
left-to-right on a shared baseline, so the result is ONE image per equation
(e.g. eq_s006_d1.png) usable by pptxgenjs addImage() at w = px/600 in.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

BUILD = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
DPI = 600
PAD = 8

# target ink width in original-frame px (960 px == 13.33 in == 960 pt, so 1 px == 1 pt)
TARGET_PX = {"eq_s006_d1": 359, "eq_s006_d2": 349, "eq_s006_dm": 345}

BLACK = "#000000"
RED = "#b51e31"   # measured ink rgb(181,30,49) of the original's red terms

SEGMENTS = {
    "eq_s006_d1": [(r"d_1(", BLACK), (r"X", RED),
                   (r") = W_1^T X = w_{11}x_1 + w_{12}x_2 + ", BLACK),
                   (r".....", BLACK), (r" + w_{1n}x_n + ", BLACK), (r"b_1 * 1", RED)],
    "eq_s006_d2": [(r"d_2(", BLACK), (r"X", RED),
                   (r") = W_2^T X = w_{21}x_1 + w_{22}x_2 + ", BLACK),
                   (r".....", BLACK), (r" + w_{2n}x_n + ", BLACK), (r"b_2 * 1", RED)],
    "eq_s006_dm": [(r"d_m(", BLACK), (r"X", RED),
                   (r") = W_m^T X = w_{m1}x_1 + w_{m2}x_2 + ", BLACK),
                   (r".....", BLACK), (r" + w_{mn}x_n + ", BLACK), (r"b_m * 1", RED)],
}

MATHTEXT = {k: "".join(s for s, _ in v) for k, v in SEGMENTS.items()}


def render_seg(latex, color, fontsize):
    """One mathtext segment -> (cropped RGBA array, row range, baseline row)."""
    fig = plt.figure(figsize=(8, 3), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fontsize, color=color,
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    ink = buf[:, :, 3] > 8
    ys, xs = np.where(ink)
    sub = buf[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
    plt.close(fig)
    return sub, ys[0], ys[-1] + 1, int(ys[-1])


def compose(segs, fontsize):
    """Lay the colour segments side by side on a shared baseline; return the image."""
    crops = [render_seg(latex, color, fontsize) for latex, color in segs]
    top = min(c[1] for c in crops)
    bottom = max(c[2] for c in crops)
    width = sum(c[0].shape[1] for c in crops) + PAD * 2
    height = bottom - top + 1 + PAD * 2
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    xcur = PAD
    for sub, r0, r1, _base in crops:
        y = (r0 - top) + PAD
        canvas[y:y + sub.shape[0], xcur:xcur + sub.shape[1]] = sub
        xcur += sub.shape[1]
    alpha = canvas[:, :, 3]
    cols = np.where(alpha.any(axis=0))[0]
    return canvas[:, cols[0]:cols[-1] + 1]


def main():
    results = []
    for name, segs in SEGMENTS.items():
        target = TARGET_PX[name]
        fs = 15.0
        for _ in range(15):
            w = sum(render_seg(l, c, fs)[0].shape[1] for l, c in segs)
            if abs(w - target) / target < 0.01:
                break
            fs *= target / w
        canvas = compose(segs, fs)
        h, w = canvas.shape[0], canvas.shape[1]
        Image.fromarray(canvas).save(BUILD / f"{name}.png")
        results.append({
            "name": name,
            "mathtext": MATHTEXT[name],
            "image": f"{name}.png",
            "font_size_pt": round(fs, 3),
            "color": "#000000",
            "sidecar": {
                "path": str(BUILD / f"{name}.png"),
                "w_px": int(w), "h_px": int(h),
                "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5),
                "dpi": DPI, "fontsize_pt": round(fs, 3),
                "color": "#000000",
            },
        })
        print(f"{name}: font {fs:.2f} pt, ink {w} px ({w / DPI * 72:.1f} pt wide), h {h} px")

    with open(BUILD / "slide_006_equations.json", "w") as f:
        json.dump({"slide": "006", "equations": results}, f, indent=2)
    print("wrote slide_006_equations.json")


if __name__ == "__main__":
    main()
