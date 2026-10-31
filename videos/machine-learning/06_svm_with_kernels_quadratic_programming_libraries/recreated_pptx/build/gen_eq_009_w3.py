#!/usr/bin/env python3
"""Wave-3 rebuild assets for slide 009: every spec section-8 equation rendered
as its own matplotlib mathtext PNG (600 dpi, transparent, tight) into eq_009/.
Matrices are nested \\overset row stacks inside \\left[...\\right] (mathtext has
no matrix env; \\overset takes exactly 2 args, so rows nest). Multi-row blocks
share one font size scaled to fit the whole block. Usage: python3 gen_eq_009_w3.py
"""
import json
import os
import sys

import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from render_math import parse_row, measure_segment, render_row, DPI  # noqa: E402

OUT = os.path.join(BUILD, "eq_009")
os.makedirs(OUT, exist_ok=True)

BLACK, RED, GREEN, BLUE = "#000000", "#FF0000", "#008000", "#0000FF"
MIN = r"\mathrm{Minimize}\ "


def gen(name, size, maxw, maxh, rows, rowgap_px=16):
    parsed = [parse_row(r) for r in rows]
    meas = [[measure_segment(latex, color, size) for color, latex in segs]
            for segs in parsed]
    total_w = max(sum(w for w, _ in m) for m in meas)
    total_h = sum(max(h for _, h in m) for m in meas) \
        + (rowgap_px / 72.0) * (len(rows) - 1)
    scale = min(maxw / total_w, maxh / total_h)
    pt = max(6.0, size * scale * 0.995)
    canvases = [render_row(r, pt) for r in rows]
    w = max(c.shape[1] for c in canvases)
    h = sum(c.shape[0] for c in canvases) + rowgap_px * (len(canvases) - 1)
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    y = 0
    for c in canvases:
        canvas[y:y + c.shape[0], 0:c.shape[1]] = c
        y += c.shape[0] + rowgap_px
    out = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(out)
    meta = {"path": out, "w_px": int(w), "h_px": int(h),
            "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5),
            "dpi": DPI, "fontsize_pt": pt, "rows": rows}
    with open(out + ".json", "w") as fh:
        json.dump(meta, fh, indent=2)
    print(name, meta["w_in"], "x", meta["h_in"], "pt", round(pt, 1))


# Upper equation stack (spec sec. 3/8 regions in inches)
gen("m1", 20, 8.079, 0.315, [f"{BLACK}:{MIN}0.5x^{{2}}+3x+4y"], 0)
gen("m2", 18, 5.132, 0.308,
    [f"{BLACK}:{MIN}0.5x^{{2}}+||{GREEN}:0y^{{2}}||{BLACK}:+||{RED}:0xy||{BLACK}:+3x+4y"], 0)
gen("m3", 18, 4.934, 0.443,
    [f"{BLACK}:{MIN}\\frac{{1}}{{2}}\\left[x^{{2}}+0y^{{2}}+0xy\\right]+3x+4y"], 0)
gen("boxed", 18, 3.030, 0.400, [f"{RED}:\\left[x^{{T}}Px\\right]+q^{{T}}x"], 0)
# P and q matrices
gen("P", 14, 0.653, 0.480,
    [f"{BLACK}:P=\\left[\\overset{{1\\;\\;0}}{{0\\;\\;0}}\\right]"], 0)
gen("q", 14, 0.560, 0.480, [f"{BLACK}:q=\\left[\\overset{{3}}{{4}}\\right]"], 0)
# Standard-form header Gx<=h (G and h red per spec)
gen("gh", 16, 1.680, 0.368, [f"{RED}:G||{BLACK}:x||{BLACK}:\\leq||{RED}:h"], 0)
# G (5x2) and h (5x1) matrices as nested row stacks
gen("G", 13, 1.027, 1.530,
    [f"{BLACK}:G=\\left[\\overset{{-1\\;\\;0}}{{\\overset{{0\\;-1}}"
     f"{{\\overset{{-1\\;-3}}{{\\overset{{2\\;\\;5}}{{3\\;\\;4}}}}}}}}\\right]"], 0)
gen("h", 13, 0.900, 1.530,
    [f"{BLACK}:h=\\left[\\overset{{0}}{{\\overset{{0}}"
     f"{{\\overset{{-15}}{{\\overset{{100}}{{80}}}}}}}}\\right]"], 0)
# Arrow between constraint lists
gen("arrow", 16, 0.440, 0.270, [f"{BLACK}:\\Rightarrow"], 0)
# Left original constraints (5 rows, one shared font size)
gen("consL", 14, 1.227, 1.485,
    [f"{BLACK}:{t}" for t in
     [r"x\geq0", r"y\geq0", r"x+3y\geq15", r"2x+5y\leq100", r"3x+4y\leq80"]])
# Transformed constraints after the arrow (5 rows)
gen("consR", 13, 1.506, 1.290,
    [f"{BLACK}:{t}" for t in
     [r"-x\leq0", r"-y\leq0", r"-x-3y\leq-15", r"2x+5y\leq100", r"3x+4y\leq80"]])
# Right-box feasibility checks (5 rows)
gen("checks", 14, 4.690, 1.013,
    [f"{BLACK}:{t}" for t in
     [r"x+3y=15\ \Rightarrow\ \geq15", r"2x+5y=25\ \Rightarrow\ \leq100",
      r"3x+4y=20\ \Rightarrow\ \leq80", r"x\geq0", r"y\geq0"]], 10)
# Blue minimum-value line
gen("finalv", 14, 4.690, 0.270, [f"{BLUE}:0.5x^{{2}}+3x+4y=20"], 0)
