#!/usr/bin/env python3
"""Fix-pass math assets for slide_021: stix fontset, larger glyphs, single-row kernel."""
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

ASSETS = [
    ("fix_header", 26, 1.05, 0.41, [HDR]),
    ("fix_chip", 24, 1.02, 0.54, [HDR]),
    ("fix_ab", 20, 1.10, 0.76, [
        "#CC0000:a_{1}||#333333:\\ \\vert\\ ||#0000CC:b_{1}",
        "#CC0000:a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{2}",
    ]),
    ("fix_normal", 18, 1.14, 0.81, [
        "#CC0000:a_{1}\\ a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{1}",
        "#CC0000:\\phantom{a_{1}\\ a_{2}}||#333333:\\ \\vert\\ ||#0000CC:b_{2}",
    ]),
    ("fix_calc_ab", 14, 1.19, 0.23, [
        "#1A1A1A:\\mathrm{Calculate}\\ \\ ||#CC0000:a^{T}\\ ||#0000CC:b",
    ]),
    ("fix_calc_uv", 14, 1.07, 0.23, [
        "#1A1A1A:\\mathrm{Calculate}\\ \\ ||#CC0000:u^{T}\\ ||#0000CC:v",
    ]),
    ("fix_mapping", 15, 1.40, 0.27, [
        "#CC0000:a\\ ,\\ b\\ \\Rightarrow\\ u\\ ,\\ v",
    ]),
    ("fix_pink", 14, 1.72, 1.95, [
        "#CC0000:\\left[\\overset{a_{1}^{2}}{\\overset{a_{2}^{2}}{\\sqrt{2}\\,a_{1}a_{2}}}\\right]"
        "||#333333:\\ ,\\ ||#0000CC:\\left[\\overset{b_{1}^{2}}{\\overset{b_{2}^{2}}{\\sqrt{2}\\,b_{1}b_{2}}}\\right]",
    ]),
    ("fix_kernel", 16, 2.70, 1.90, [
        "#CC0000:a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}"
        "||#333333:\\ \\vert\\ ||#0000CC:\\left[\\overset{b_{1}^{2}}{\\overset{b_{2}^{2}}{\\sqrt{2}\\,b_{1}b_{2}}}\\right]",
    ]),
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
              info["w_px"], "x", info["h_px"], "px",
              [round(p, 1) for p in sizes])


if __name__ == "__main__":
    main()
