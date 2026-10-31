#!/usr/bin/env python3
"""Baseline-aware segment renderer + canvas compositor for slide 023 equations.
Wide 20in canvas (6000px) keeps the probe-erase trick of the certified
scripts/render_eq_wide.py from ever eating equation ink."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

plt.rcParams["mathtext.fontset"] = "stix"
BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
DPI = 600
PAD = 10
MANIFEST = {}


def seg(kind, text, color, fs, family="DejaVu Sans", weight="normal"):
    """Render one text/mathtext segment. Returns img + baseline row from top."""
    fig = plt.figure(figsize=(20, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    if kind == "math":
        fig.text(0.5, 0.5, f"${text}$", fontsize=fs, color=color,
                 ha="center", va="baseline")
    else:
        fig.text(0.5, 0.5, text, fontsize=fs, color=color, ha="center",
                 va="baseline", fontfamily=family, fontweight=weight)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, buf.shape[0])
    fig_half = 2.0
    baseline_row = int(round((1.0 - 0.5) * buf.shape[0]))
    base = baseline_row - y0
    plt.close(fig)
    return {"img": Image.fromarray(buf[y0:y1, x0:x1]), "base": base}


def _paste(canvas, img, x, y_top):
    """Alpha-composite img onto canvas at (x, y_top), clipping to canvas bounds."""
    cx0, cy0 = max(x, 0), max(y_top, 0)
    cx1 = min(x + img.width, canvas.shape[1])
    cy1 = min(y_top + img.height, canvas.shape[0])
    if cx1 <= cx0 or cy1 <= cy0:
        return
    sx, sy = cx0 - x, cy0 - y_top
    sub = np.asarray(img).astype(np.float32)[sy:sy + (cy1 - cy0), sx:sx + (cx1 - cx0)]
    a = sub[:, :, 3:4] / 255.0
    reg = canvas[cy0:cy1, cx0:cx1].astype(np.float32)
    canvas[cy0:cy1, cx0:cx1, :3] = (reg[:, :, :3] * (1 - a) + sub[:, :, :3] * a)
    canvas[cy0:cy1, cx0:cx1, 3] = np.maximum(canvas[cy0:cy1, cx0:cx1, 3], sub[:, :, 3])


def canvas_place(items, pad=8):
    """items: [(img, base, x_or_None, baseline_row)] pasted left-to-right
    on rows; returns PIL RGBA image. x_or_None -> sequential."""
    hmax = max(i[1]["img"].height + i[3] for i in items)
    xs, x = [], 0
    for it in items:
        if it[2] is None:
            xs.append(x); x += it[1]["img"].width + pad
        else:
            xs.append(it[2])
    w = max(xs[i] + items[i][1]["img"].width for i in range(len(items)))
    canvas = np.zeros((hmax, w, 4), dtype=np.uint8)
    for i, it in enumerate(items):
        _paste(canvas, it[1]["img"], xs[i], it[3] - it[1]["base"])
    return Image.fromarray(canvas)


def save(img, name):
    p = f"{BUILD_DIR}/{name}.png"
    img.save(p)
    MANIFEST[name] = {"image": name + ".png", "w_px": img.width, "h_px": img.height,
                      "w_in": round(img.width / DPI, 5), "h_in": round(img.height / DPI, 5),
                      "dpi": DPI}
    return p


def write_manifest(fname):
    with open(f"{BUILD_DIR}/{fname}", "w") as fh:
        json.dump(MANIFEST, fh, indent=2)
    print(json.dumps(MANIFEST, indent=2))


def trim(img):
    a = np.asarray(img)
    ink = a[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if not len(rows):
        return img
    return Image.fromarray(a[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1])
