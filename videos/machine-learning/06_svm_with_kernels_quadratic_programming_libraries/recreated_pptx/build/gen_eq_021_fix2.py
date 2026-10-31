#!/usr/bin/env python3
"""Fix-2 assets for slide_021: big two-row panel images (pink + kernel)."""
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

ASSETS = [
    ("fix2_pink", 20, 1.72, 0.95, [
        "#CC0000:\\left[\\overset{a_{1}^{2}}{\\overset{a_{2}^{2}}{\\sqrt{2}\\,a_{1}a_{2}}}\\right]",
        "#333333:\\ ,\\ \\ ||#0000CC:\\left[\\overset{b_{1}^{2}}{\\overset{b_{2}^{2}}{\\sqrt{2}\\,b_{1}b_{2}}}\\right]",
    ]),
    ("fix2_kernel", 18, 2.70, 0.90, [
        "#CC0000:a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}||#333333:\\ \\vert\\ ",
        "#0000CC:\\left[\\overset{b_{1}^{2}}{\\overset{b_{2}^{2}}{\\sqrt{2}\\,b_{1}b_{2}}}\\right]",
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
              [round(float(p), 1) for p in sizes])


if __name__ == "__main__":
    main()
