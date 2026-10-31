#!/usr/bin/env python3
"""Column-vector eq assets for slide 027: fixed-size rows stacked tightly with PIL."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_027"
DPI = 600
PAD = 6
MAROON = "#7B241C"


def render_row(latex, color, pt):
    fig = plt.figure(figsize=(6.0, 2.0), dpi=DPI)
    fig.patch.set_alpha(0.0)
    t = fig.text(0.02, 0.5, f"${latex}$", fontsize=pt, color=color, ha="left", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    al = buf[..., 3]
    ys, xs = np.where(al > 10)
    y0, y1 = max(ys.min() - PAD, 0), min(ys.max() + PAD + 1, buf.shape[0])
    x0, x1 = max(xs.min() - PAD, 0), min(xs.max() + PAD + 1, buf.shape[1])
    return buf[y0:y1, x0:x1]


def stack(name, rows, color, pt, rowgap=14):
    parts = [render_row(r, color, pt) for r in rows]
    w = max(p.shape[1] for p in parts)
    h = sum(p.shape[0] for p in parts) + rowgap * (len(parts) - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = 0
    for p in parts:
        x = (w - p.shape[1]) // 2
        canvas[y:y + p.shape[0], x:x + p.shape[1]] = p
        y += p.shape[0] + rowgap
    out = f"{BASE}/{name}.png"
    Image.fromarray(canvas).save(out)
    info = {"path": out, "w_px": int(w), "h_px": int(h),
            "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5),
            "dpi": DPI, "fontsize_pt": [pt] * len(rows), "rows": [f"{color}:{r}" for r in rows]}
    with open(out + ".json", "w") as fh:
        json.dump(info, fh, indent=2)
    print("OK", name, w, h, info["w_in"], info["h_in"])


stack("eq_veca", [r"a_{1}", r"a_{2}"], MAROON, 24, rowgap=12)
stack("eq_vecb", [r"b_{1}", r"b_{2}"], MAROON, 24, rowgap=12)
stack("eq_phib", [r"b_{1}^{2}", r"b_{2}^{2}", r"\sqrt{2}b_{1}b_{2}", r"\sqrt{2}b_{1}", r"\sqrt{2}b_{2}", r"1"], MAROON, 17, rowgap=30)
stack("eq_phix", [r"x_{1}^{2}", r"x_{2}^{2}", r"\sqrt{2}x_{1}x_{2}", r"\sqrt{2}x_{1}", r"\sqrt{2}x_{2}", r"1"], MAROON, 17, rowgap=30)
