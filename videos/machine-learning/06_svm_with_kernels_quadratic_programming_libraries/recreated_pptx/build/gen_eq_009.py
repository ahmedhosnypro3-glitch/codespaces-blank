#!/usr/bin/env python3
"""Generate 2D equation PNGs for slide 009 (Example QP)."""
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
FS = 18

def compose(name, segs, gap=6, fs=FS):
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

compose("m1", [("t", BLACK, r"\text{Minimize }0.5x^{2}+3x+4y")])
compose("m2", [
    ("a", BLACK, r"\text{Minimize }0.5x^{2}+"),
    ("g", GREEN, r"0y^{2}+"),
    ("r", RED, r"0xy"),
    ("b", BLACK, r"+3x+4y"),
])
compose("m3", [
    ("a", BLACK, r"\text{Minimize }\frac{1}{2}[x^{2}+"),
    ("g", GREEN, r"0y^{2}+"),
    ("r", RED, r"0xy"),
    ("b", BLACK, r"]+3x+4y"),
])
compose("boxed", [("t", RED, r"[x^{T}Px]+q^{T}x")])
compose("P", [("e", BLACK, r"P="), ("m", BLACK, r"\left[\overset{1\;\;0}{0\;\;0}\right]")], fs=16)
compose("q", [("e", BLACK, r"q="), ("m", BLACK, r"\left[\overset{3}{4}\right]")], fs=16)
compose("gh", [("g", RED, r"G"), ("x", BLACK, r"x"), ("le", RED, r"\leq"), ("h", RED, r"h")], fs=16)
compose("G", [("e", BLACK, r"G="), ("m", BLACK, r"\left[\overset{-1\;\;0}{0\;-1}{-1\;-3}{2\;\;5}{3\;\;4}\right]")], fs=15)
compose("h", [("e", BLACK, r"h="), ("m", BLACK, r"\left[\overset{0}{0}{-15}{100}{80}\right]")], fs=15)
compose("c1", [("t", BLACK, r"x+3y=15\;\Rightarrow\;\geq15")])
compose("c2", [("t", BLACK, r"2x+5y=25\;\Rightarrow\;\leq100")])
compose("c3", [("t", BLACK, r"3x+4y=20\;\Rightarrow\;\leq80")])
compose("c4", [("t", BLACK, r"x\geq0")])
compose("c5", [("t", BLACK, r"y\geq0")])
compose("t1", [("t", BLACK, r"x\geq0")])
compose("t2", [("t", BLACK, r"y\geq0")])
compose("t3", [("t", BLACK, r"-x-3y\leq-15")])
compose("t4", [("t", BLACK, r"2x+5y\leq100")])
compose("t5", [("t", BLACK, r"3x+4y\leq80")])
compose("t6", [("t", BLACK, r"-x\leq0")])
compose("t7", [("t", BLACK, r"-y\leq0")])
compose("minv", [("t", BLUE, r"0.5x^{2}+3x+4y=20")])
