#!/usr/bin/env python3
"""Slide 049 — tall-paren PNG generator (aug table + Z block, 044-cert pattern).

Frame-measured on unique_slides/slide_049.jpg (960x540, 1px = 1pt):
  aug-table column parens: ink y181..223 (h44.5), bow D=1.0pt, stroke ~1.5px, DGRAY 909090
  Z-block column parens:   ink y88..118 (h30),   bow D=1.0pt, stroke ~1.5px, DGRAY
  top-table column parens: ink y77..107 (h30),   bow D=1.0pt, stroke ~1.5px, DGRAY
Build places ink_left/lp and ink_right/rp on the frame's bow columns
(aug lp [93.5,115.5,137.5,160.5,182.5,205.5] / rp [106.5,128.5,151.5,173.5,196.5,218.5];
 Z bows (641.5,655.5)(664.5,677.5)(686.5,699.5); top2 lp [89.78,111.18,133.45,155.89,
 178.84,201.21] / rp [102.42,124.72,147.12,170.07,192.45,214.74] sub-pixel bow
 centroids, qa/slide049/parenA_15c.out; A gray signature == D's certified 909090).
"""
import json, os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parens049")
os.makedirs(OUT, exist_ok=True)
DPI = 600
PAD = 0.5

# (name, S_pt, inkH_pt, D_pt, color)
CLASSES = [
    ("aug",  1.5, 44.5, 1.0, "909090"),
    ("z49",  1.5, 30.0, 1.0, "909090"),
    ("top2", 1.5, 30.0, 1.0, "909090"),
]


def bezier_x(t, x_tip, x_ctrl):
    return (1 - t) ** 2 * x_tip + 2 * (1 - t) * t * x_ctrl + t ** 2 * x_tip


def render(name, S, inkH, D, color):
    W = S + D + 2 * PAD
    H = inkH + 2 * PAD
    for side in ("lp", "rp"):
        if side == "lp":
            x_bulge = PAD + S / 2.0
            x_tip = x_bulge + D
        else:
            x_bulge = W - PAD - S / 2.0
            x_tip = x_bulge - D
        x_ctrl = 2 * x_bulge - x_tip
        t = np.linspace(0.0, 1.0, 400)
        xs = bezier_x(t, x_tip, x_ctrl)
        ys = np.linspace(PAD + S / 2.0, H - PAD - S / 2.0, 400)
        fig = plt.figure(figsize=(W / 72.0, H / 72.0))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, W)
        ax.set_ylim(0, H)
        ax.axis("off")
        ax.plot(xs, ys, lw=S, color="#" + color, solid_capstyle="round",
                solid_joinstyle="round")
        path = f"{OUT}/paren_{name}_{side}.png"
        fig.savefig(path, dpi=DPI, transparent=True)
        plt.close(fig)
        a = np.array(Image.open(path))[:, :, 3]
        ys_i, xs_i = np.nonzero(a > 30)
        sidecar = {
            "px_w": a.shape[1], "px_h": a.shape[0],
            "ink_left_px": int(xs_i.min()), "ink_right_px": int(xs_i.max()),
            "ink_top_px": int(int(np.min(ys_i))), "ink_bot_px": int(int(np.max(ys_i))),
            "S_pt": S, "D_pt": D, "inkH_pt": inkH, "color": color, "side": side,
            "ink_band_pt": name,
            "pt_per_px": 72.0 / DPI,
        }
        json.dump(sidecar, open(path.replace(".png", ".json"), "w"), indent=1)


for name, S, inkH, D, color in CLASSES:
    render(name, S, inkH, D, color)
print("DONE ->", OUT)
