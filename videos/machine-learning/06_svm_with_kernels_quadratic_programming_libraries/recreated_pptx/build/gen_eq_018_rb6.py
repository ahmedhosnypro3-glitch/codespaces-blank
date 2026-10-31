#!/usr/bin/env python3
"""Slide 018 mapping equation PNGs, rb6. render_math.py crops with unflipped
window extents (wrong for tall multi-row stacks), so this renders each '||'
color:latex segment into ONE figure on a shared baseline (eq_render_fix.py
approach) and crops the full buffer by actual ink bbox."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
DPI = 600
PAD = 8


def parse_row(row):
    segs = []
    for part in row.split("||"):
        head = part.split("\\", 1)[0]
        if ":" in head:
            color, latex = part.split(":", 1)
        else:
            color, latex = "#333333", part
        segs.append((color if color.startswith("#") else "#" + color, latex))
    return segs


def measure(segs, pt):
    fig = plt.figure(figsize=(40, 6), dpi=72)
    r = fig.canvas.get_renderer()
    widths = []
    for color, latex in segs:
        t = fig.text(0.01, 0.5, f"${latex}$", fontsize=pt, ha="left", va="baseline")
        widths.append(t.get_window_extent(renderer=r).width / 72.0)
        t.remove()
    plt.close(fig)
    return widths


def render(row, pt):
    segs = parse_row(row)
    widths = measure(segs, pt)
    total = sum(widths)
    margin = 0.25
    fig_w = total + 2 * margin
    fig_h = max(1.2, min(8.0, total * 0.45 + 1.0))
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=DPI)
    fig.patch.set_alpha(0.0)
    x = margin / fig_w
    for (color, latex), w in zip(segs, widths):
        fig.text(x, 0.5, f"${latex}$", fontsize=pt, color=color,
                 ha="left", va="baseline")
        x += (w + 0.03) / fig_w
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    ink = buf[:, :, 3] > 10
    ys, xs = np.nonzero(ink)
    y0, y1 = max(ys.min() - PAD, 0), min(ys.max() + PAD + 1, buf.shape[0])
    x0, x1 = max(xs.min() - PAD, 0), min(xs.max() + PAD + 1, buf.shape[1])
    return buf[y0:y1, x0:x1]


def save(name, row, pt, max_w_in, max_h_in):
    canvas = render(row, pt)
    h_in, w_in = canvas.shape[0] / DPI, canvas.shape[1] / DPI
    while (w_in > max_w_in or h_in > max_h_in) and pt > 6:
        pt *= 0.94
        canvas = render(row, pt)
        h_in, w_in = canvas.shape[0] / DPI, canvas.shape[1] / DPI
    out = f"{BASE}/eq_018/{name}.png"
    Image.fromarray(canvas).save(out)
    info = {"path": f"eq_018/{name}.png", "w_px": int(canvas.shape[1]),
            "h_px": int(canvas.shape[0]), "w_in": round(w_in, 5),
            "h_in": round(h_in, 5), "dpi": DPI, "fontsize_pt": [pt], "rows": [row]}
    with open(out + ".json", "w") as f:
        json.dump(info, f, indent=2)
    print(json.dumps(info))


save("eq18_map_rb6",
     "#000000:\\boldsymbol{Z}||#CC0000:\\ \\Rightarrow\\ ||#0000CC:\\phi||#000000:(\\boldsymbol{Z})",
     24, 1.15, 0.30)
save("eq18_colvec_rb6",
     "#000000:\\boldsymbol{Z}=\\left(\\substack{x\\\\y}\\right)||#CC0000:\\ \\Rightarrow\\ ||#000000:\\left(\\substack{x^{2}\\\\y^{2}\\\\ \\sqrt{2xy}}\\right)",
     28, 2.38, 0.86)
