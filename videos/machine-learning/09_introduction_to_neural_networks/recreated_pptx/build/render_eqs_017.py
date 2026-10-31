#!/usr/bin/env python3
"""Render slide 017's three coloured text rows as 600 dpi transparent PNGs.

All anchors are measured from V/unique_slides/slide_017.jpg (960x540, 1px = 1pt).
Each token is drawn from its own TextPath and squeezed onto its measured ink
box, so the recreated ink lands on the original's pixels.
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.patches import PathPatch
from matplotlib.textpath import TextPath
from matplotlib.transforms import Affine2D
from PIL import Image

BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
DPI = 600
FONT = "DejaVu Sans"
BRACE_FONT = "DejaVu Serif"

RED = "#990D12"       # measured cores: name (144,3,9), brace (145,31,31), values (139,20,22)
BLACK = "#000000"     # measured cores: F / ( / ) / = / row-1 conditions
GREEN = "#008000"     # measured core: row-2 conditions (39,115,25)


def tok(text, color, left, top, width, size=18, weight="bold", style="normal"):
    return dict(text=text, color=color, left=left, top=top, width=width,
                size=size, weight=weight, style=style)


def _draw_token(ax, t):
    prop = FontProperties(family=FONT, weight=t["weight"], style=t["style"],
                          size=t["size"])
    path = TextPath((0, 0), t["text"], prop=prop)
    bb = path.get_extents()
    if bb.width <= 0:
        return
    sx = t["width"] / bb.width
    baseline = t["top"] + bb.y1
    trans = Affine2D.from_values(sx, 0.0, 0.0, -1.0,
                                 t["left"] - sx * bb.x0, baseline)
    patch = PathPatch(path, facecolor=t["color"], edgecolor="none",
                      transform=trans + ax.transData)
    ax.add_patch(patch)


def _draw_brace(ax, x0, x1, y0, y1, color):
    prop = FontProperties(family=BRACE_FONT, weight="normal", size=40)
    path = TextPath((0, 0), "{", prop=prop)
    bb = path.get_extents()
    sx = (x1 - x0) / bb.width
    sy = (y1 - y0) / bb.height
    trans = Affine2D.from_values(sx, 0.0, 0.0, -sy,
                                 x0 - sx * bb.x0, y1 + sy * bb.y0)
    ax.add_patch(PathPatch(path, facecolor=color, edgecolor="none",
                           transform=trans + ax.transData))


def render(out_path, region, tokens, brace=None):
    x0, y0, x1, y1 = region
    w = x1 - x0
    h = y1 - y0
    dev_w = int(round(w * DPI / 72.0))
    dev_h = int(round(h * DPI / 72.0))
    fig = plt.figure(figsize=(dev_w / DPI, dev_h / DPI), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)
    ax.axis("off")
    for t in tokens:
        _draw_token(ax, t)
    if brace:
        _draw_brace(ax, *brace)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)
    Image.fromarray(buf).save(out_path)
    return {
        "path": out_path,
        "region_px": [x0, y0, x1, y1],
        "dev_w_px": dev_w, "dev_h_px": dev_h,
        "w_in": round(dev_w / DPI, 6), "h_in": round(dev_h / DPI, 6),
        "dpi": DPI,
    }


def main():
    manifest = {}

    # ---- bottom-left: uni-polar unit step -------------------------------
    bl = [
        tok("F", BLACK, 124, 475, 11),
        tok("(", BLACK, 137, 472, 5),
        tok("x", RED, 144, 479, 9),
        tok(")", BLACK, 153, 472, 5),
        tok("=", BLACK, 160, 479, 11),
        tok("Uni-polar", RED, 173, 475, 66),
        tok("Unit", BLACK, 245, 475, 31),
        tok("Step", BLACK, 280, 475, 29),
        tok("=", BLACK, 311, 479, 10),
        tok("0", RED, 330, 469, 8),
        tok("1", RED, 330, 487, 6),
        tok("for", BLACK, 351, 468, 21, style="italic", weight="normal"),
        tok("x", BLACK, 373, 472, 9, style="italic", weight="normal"),
        tok("<", BLACK, 383, 471, 10, style="italic", weight="normal"),
        tok("0", BLACK, 395, 469, 8, style="italic", weight="normal"),
        tok("for", GREEN, 349, 486, 20, style="italic", weight="normal"),
        tok("x", GREEN, 372, 490, 9, style="italic", weight="normal"),
        tok(">=", GREEN, 382, 488, 11, style="italic", weight="normal"),
        tok("0", GREEN, 396, 487, 8, style="italic", weight="normal"),
    ]
    manifest["eq_017_unipolar"] = render(
        f"{BUILD_DIR}/eq_017_unipolar.png", (117, 459, 414, 507), bl,
        brace=(322, 327, 465, 504, RED))

    # ---- bottom-right: bi-polar unit step --------------------------------
    br = [
        tok("F", BLACK, 498, 475, 12),
        tok("(", BLACK, 511, 472, 5),
        tok("x", RED, 517, 479, 10),
        tok(")", BLACK, 527, 472, 5),
        tok("=", BLACK, 534, 479, 11),
        tok("Bi-polar", RED, 547, 475, 57),
        tok("Unit", BLACK, 610, 475, 30),
        tok("Step", BLACK, 644, 475, 30),
        tok("=", BLACK, 675, 479, 10),
        tok("-", RED, 695, 474, 10),
        tok("1", RED, 708, 469, 7),
        tok("1", RED, 695, 488, 6),
        tok("for", BLACK, 727, 469, 21, style="italic", weight="normal"),
        tok("x", BLACK, 751, 472, 8, style="italic", weight="normal"),
        tok("<", BLACK, 760, 471, 10, style="italic", weight="normal"),
        tok("0", BLACK, 771, 469, 8, style="italic", weight="normal"),
        tok("for", GREEN, 726, 487, 21, style="italic", weight="normal"),
        tok("x", GREEN, 748, 491, 9, style="italic", weight="normal"),
        tok(">=", GREEN, 758, 488, 12, style="italic", weight="normal"),
        tok("0", GREEN, 772, 487, 8, style="italic", weight="normal"),
    ]
    manifest["eq_017_bipolar"] = render(
        f"{BUILD_DIR}/eq_017_bipolar.png", (496, 459, 799, 507), br,
        brace=(687, 691, 465, 504, RED))

    # ---- top-right callout: F(x) = x   Linear (No Activation) -------------
    tr = [
        tok("F", BLACK, 613, 181, 8, weight="normal"),
        tok("(", BLACK, 622, 181, 7, weight="normal"),
        tok("x", RED, 632, 186, 9, weight="normal"),
        tok(")", BLACK, 641, 181, 5, weight="normal"),
        tok("=", BLACK, 649, 187, 10, weight="normal"),
        tok("x", RED, 661, 186, 9, weight="normal"),
        tok("Linear", RED, 730, 184, 45, size=16),
        tok("(No", BLACK, 781, 184, 25, size=14, style="italic", weight="normal"),
        tok("Activation)", BLACK, 808, 184, 72, size=14, style="italic", weight="normal"),
    ]
    manifest["eq_017_linear"] = render(
        f"{BUILD_DIR}/eq_017_linear.png", (605, 176, 884, 203), tr)

    with open(f"{BUILD_DIR}/eq_017_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    sys.exit(main())
