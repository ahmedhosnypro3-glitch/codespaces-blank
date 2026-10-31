#!/usr/bin/env python3
"""Round-4 math assets for slide_021: bracketed array columns (legible stacks)."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_math as rm

matplotlib.rcParams["mathtext.fontset"] = "stix"

OUT = os.path.join(HERE, "eq_021")
os.makedirs(OUT, exist_ok=True)

HDR = "#333333:[||#CC0000:a^{T}||#0000CC:b||#333333:]^{2}"
AB = [
    "#CC0000:a_{1}||#333333:\\ \\vert\\ ||#0000CC:b_{1}",
    "#CC0000:a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{2}",
]
NORMAL = [
    "#CC0000:a_{1}\\ a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{1}",
    "#CC0000:\\phantom{a_{1}\\ a_{2}}||#333333:\\ \\vert\\ ||#0000CC:b_{2}",
]
# mathtext has no \\begin{array}; render stacked columns as per-row brackets
PINK = [
    "#CC0000:\\left[a_{1}^{2}\\right]||#333333:\\ ,\\ ||#0000CC:\\left[b_{1}^{2}\\right]",
    "#CC0000:\\left[a_{2}^{2}\\right]||#333333:\\ ,\\ ||#0000CC:\\left[b_{2}^{2}\\right]",
    "#CC0000:\\left[\\sqrt{2}\\,a_{1}a_{2}\\right]||#333333:\\ ,\\ ||#0000CC:\\left[\\sqrt{2}\\,b_{1}b_{2}\\right]",
]
KERNEL = [
    "#CC0000:a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}||#333333:\\ \\vert\\ ||#0000CC:\\left[b_{1}^{2}\\right]",
    "#CC0000:\\phantom{a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}}||#333333:\\ \\vert\\ ||#0000CC:\\left[b_{2}^{2}\\right]",
    "#CC0000:\\phantom{a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}}||#333333:\\ \\vert\\ ||#0000CC:\\left[\\sqrt{2}\\,b_{1}b_{2}\\right]",
]

ASSETS = [
    ("r4_header", 30, 1.04, 0.41, [HDR]),
    ("r4_chip", 28, 0.98, 0.54, [HDR]),
    ("r4_ab", 24, 1.12, 0.79, AB),
    ("r4_normal", 22, 1.17, 0.84, NORMAL),
    ("r4_calc_ab", 18, 1.19, 0.23, [
        "#1A1A1A:\\mathrm{Calculate}\\ \\ ||#CC0000:a^{T}\\ ||#0000CC:b",
    ]),
    ("r4_calc_uv", 18, 1.07, 0.23, [
        "#1A1A1A:\\mathrm{Calculate}\\ \\ ||#CC0000:u^{T}\\ ||#0000CC:v",
    ]),
    ("r4_mapping", 20, 1.38, 0.27, [
        "#CC0000:a\\ ,\\ b\\ \\Rightarrow\\ u\\ ,\\ v",
    ]),
    ("r4_pink", 22, 1.76, 2.00, PINK),
    ("r4_kernel", 22, 2.74, 1.95, KERNEL),
]


def main():
    for name, size, maxw, maxh, rows in ASSETS:
        canvases, sizes = [], []
        for r in rows:
            c, pt = rm.fit_row(r, size, maxw, maxh)
            canvases.append(c)
            sizes.append(pt)
        w = max(c.shape[1] for c in canvases)
        h = sum(c.shape[0] for c in canvases) + 10 * (len(canvases) - 1)
        canvas = np.zeros((h, w, 4), dtype=np.uint8)
        y = 0
        for c in canvases:
            x = (w - c.shape[1]) // 2
            canvas[y:y + c.shape[0], x:x + c.shape[1]] = c
            y += c.shape[0] + 10
        png = os.path.join(OUT, name + ".png")
        Image.fromarray(canvas).save(png)
        info = {"path": png, "w_px": int(w), "h_px": int(h),
                "w_in": round(w / 600, 5), "h_in": round(h / 600, 5), "dpi": 600,
                "fontsize_pt": sizes, "rows": rows}
        with open(os.path.join(OUT, name + ".json"), "w") as fh:
            json.dump(info, fh, indent=2)
        print(name, info["w_in"], "x", info["h_in"], "in",
              [round(float(p), 1) for p in sizes])


if __name__ == "__main__":
    main()
