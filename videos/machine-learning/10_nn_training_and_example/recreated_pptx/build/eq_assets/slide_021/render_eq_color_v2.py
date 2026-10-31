#!/usr/bin/env python3
"""Color-coded 2D equation PNGs for slide_021 (b11 rebuild).

Fix of render_eq_color.py v1: that script passed raw mathtext to TextPath and
fig.text WITHOUT '$...$' wrapping, so matplotlib rendered the source string as
literal text (measured in qa/slide021/rejudge/v3/render-1.png). This composer
renders every segment through the canonical scripts/render_eq.py mathtext
renderer, then stitches segments left-to-right on a common baseline.
"""
import importlib.util
import json
import os
import tempfile

from PIL import Image

SPEC = "/home/codespace/ai_llm_slides/scripts/render_eq.py"
_s = importlib.util.spec_from_file_location("render_eq", SPEC)
render_eq = importlib.util.module_from_spec(_s)
_s.loader.exec_module(render_eq)

OUT = os.path.dirname(os.path.abspath(__file__))
DPI = 600
FS = 18


def compose(segments, name):
    metas = []
    srcs = []
    for latex, color in segments:
        fd, tmp = tempfile.mkstemp(suffix=".png")
        os.close(fd)
        try:
            m = render_eq.render(latex, tmp, float(FS), color)
            metas.append(m)
            srcs.append(render_eq.np.asarray(Image.open(tmp).convert("RGBA")))
        finally:
            os.unlink(tmp)
    widths = [m["w_px"] for m in metas]
    asc = [int(round(m["baseline_frac"] * m["h_px"])) for m in metas]
    desc = [m["h_px"] - a for a in asc]
    base = max(asc)
    h = base + max(desc)
    w = sum(widths)
    canvas = render_eq.np.zeros((h, w, 4), dtype=render_eq.np.uint8)
    x = 0
    for arr, a, wd in zip(srcs, asc, widths):
        canvas[base - a:base - a + arr.shape[0], x:x + wd] = arr
        x += wd
    png = os.path.join(OUT, name + ".png")
    Image.fromarray(canvas).save(png)
    side = {"path": name + ".png", "w_px": int(w), "h_px": int(h),
            "w_in": round(w / DPI, 5), "h_in": round(h / DPI, 5),
            "baseline_px": int(base), "baseline_frac": round(base / h, 5),
            "dpi": DPI, "fontsize_pt": FS, "color": "#000000",
            "segments": [c for _, c in segments]}
    with open(os.path.join(OUT, name + ".json"), "w") as f:
        json.dump(side, f, indent=1)
    print(name, side["w_px"], "x", side["h_px"], "baseline_frac", side["baseline_frac"])


K, B, G, R = "#0F0F0F", "#0000CC", "#007A00", "#CC0000"
OJ = r"O_j(1-O_j)"
BR = r"[\,\sum_k(\delta_k w_{kj})\,]"
compose([(r"\Delta_{ji} = \eta\ ", K), (r"O_i\ ", B), (OJ + r"\ ", G), (BR, R)], "eq1d")
compose([(r"\Delta_{ji} = \eta\ ", K), (r"O_i\ ", B), (r"\delta_j", K)], "eq2d")
compose([(r"\mathrm{Where:}\ ", K), (r"\delta_j =\ ", R),
         (OJ + r"\ ", G), (BR, R)], "eq3d")
