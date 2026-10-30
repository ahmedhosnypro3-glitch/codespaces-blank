#!/usr/bin/env python3
"""Slide 041 — tall-paren PNG generator (lefttable crop FAIL, attempt 1).

The frame's delimiters are bowed 1-1.5px paren glyphs (PIL thr205 scans:
tips/straight-vline w0.75 rendered them as "straight vertical rules" — a
MAJOR delimiter-glyph substitution per the zoomed crop judge). Replaces them
per P3 (patterns.md): ONE quadratic-Bezier centerline PNG per delimiter at
600dpi, placed from the sidecar ink bbox so ink lands exactly on the anchors.

Geometry measured on unique_slides/slide_041.jpg (960x540, 1px = 1pt):
  table cols (x1..x6): ink y78..106 (h28), bow D=1.0pt, stroke ~1.5px
  W vector parens:      ink y59..104 (h46), bow D=2.0pt, stroke ~1.5px
  Z-table cols:         ink y81..109 (h28), bow D=1.0pt, stroke ~1.5px
All parens BLACK. Build lands PNG ink at its own vline anchors, so the
digits' geometry does not move.
"""
import json, os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parens041")
os.makedirs(OUT, exist_ok=True)
DPI = 600
PAD = 0.5

# (name, S_pt, inkH_pt, D_pt, color)
CLASSES = [
    ("table", 1.5, 28.0, 1.0, "000000"),  # x1..x6 table column vectors y78..106
    ("wvec",  1.5, 46.0, 2.0, "000000"),  # Initial W = (4,-2,-2) y59..104
    ("ztab",  1.5, 26.0, 1.0, "000000"),  # Z1 table column vectors y82..108
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
