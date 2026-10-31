#!/usr/bin/env python3
"""Wave-3 rebuild: extra equation PNGs for slide 009 not present in eq_009/.

Adds: ge15 (x+3y>=15, left constraint list), arrow (=> between lists),
G_rb3/h_rb3 (G/h matrices at fs=11 so they fit the spec region beside the
vertical divider). Existing m1-m3/boxed/P/q/gh/c1-c5/t1-t7/minv already match
the reanalysis2 spec and are reused as-is.

Usage: python3 gen_eq_009_rb3.py
"""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_009"
os.makedirs(OUT, exist_ok=True)
BLUE, RED, GREEN, BLACK = "0000CC", "CC0000", "008000", "000000"


def compose(name, segs, gap=6, fs=18):
    out = f"{OUT}/{name}.png"
    rendered = [render_segment(latex, "#" + color, fs) for _, color, latex in segs]
    max_b = max(b for _, b in rendered)
    heights = [a.shape[0] for a, _ in rendered]
    total_h = max_b + max(h - b for (_, b), h in zip(rendered, heights)) + 2 * PAD_PX
    total_w = sum(a.shape[1] for a, _ in rendered) + gap * (len(rendered) - 1) + 2 * PAD_PX
    canvas = np.zeros((total_h, total_w, 4), dtype=np.uint8)
    x = PAD_PX
    for (arr, b), _ in zip(rendered, segs):
        y = max_b - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1] + gap
    Image.fromarray(canvas).save(out)
    meta = {"path": out, "w_px": int(total_w), "h_px": int(total_h),
            "w_in": round(total_w / DPI, 5), "h_in": round(total_h / DPI, 5)}
    with open(out + ".json", "w") as fh:
        json.dump(meta, fh)
    print(name, meta["w_in"], "x", meta["h_in"])


compose("ge15", [("t", BLACK, r"x+3y\geq15")])
compose("arrow", [("t", BLACK, r"\Rightarrow")], gap=0)
compose("G_rb3", [("e", BLACK, r"G="),
                  ("m", BLACK, r"\left[\overset{-1\;\;0}{0\;-1}{-1\;-3}{2\;\;5}{3\;\;4}\right]")],
        fs=10)
compose("h_rb3", [("e", BLACK, r"h="),
                  ("m", BLACK, r"\left[\overset{0}{0}{-15}{100}{80}\right]")],
        fs=10)
