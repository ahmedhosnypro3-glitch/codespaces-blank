#!/usr/bin/env python3
"""Generate 2D equation PNGs for slide 004 (Quadratic Coefficients)."""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_004"
os.makedirs(OUT, exist_ok=True)
BLUE, RED, GREEN, BLACK = "0000CC", "CC0000", "008000", "000000"
FS = 20

def compose(name, segs, gap=6):
    out = f"{OUT}/{name}.png"
    rendered = [render_segment(latex, "#" + color, FS) for _, color, latex in segs]
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

# 2x2 matrix with brackets: rows via overset
A = r"\left[\overset{a_{11}\;a_{12}}{a_{21}\;a_{22}}\right]"
XV = r"\left(x_1\;x_2\right)"
XC = r"\left[\overset{x_1}{x_2}\right]"
ROW = r"\left(a_{11}x_1+a_{21}x_2\;\;a_{12}x_1+a_{22}x_2\right)"

compose("eq1", [
    ("l", BLACK, XV + A + XC),
    ("eq", BLACK, r"\;=\;"),
    ("r", BLACK, ROW + XC),
])
compose("eq2", [
    ("l", BLACK, r"=\;(a_{11}x_1+a_{21}x_2)x_1+(a_{12}x_1+a_{22}x_2)x_2"),
    ("m", BLACK, r"\;=\;"),
    ("r", BLACK, r"a_{11}x_1^{2}+a_{21}x_1x_2+a_{12}x_1x_2+a_{22}x_2^{2}"),
])
compose("eq3", [
    ("l", BLACK, r"=\;a_{11}x_1^{2}+(a_{21}+a_{12})x_1x_2+a_{22}x_2^{2}"),
    ("arr", BLUE, r"\;\Rightarrow\;"),
    ("q", GREEN, r"\text{Quadratic form}"),
])
compose("c1", [
    ("t", BLUE, r"a_{11}"),
    ("a", BLUE, r"\;\Rightarrow\;"),
    ("e", BLACK, r"\text{Coefficient of }x_1^{2}"),
])
compose("c2a", [
    ("t", BLUE, r"a_{21}+a_{12}"),
    ("a", BLUE, r"\;\Rightarrow\;"),
    ("e", BLACK, r"\text{Coefficient of }x_1x_2"),
])
compose("c2b", [
    ("o", RED, r"a_{12}=a_{21}=\frac{1}{2}"),
    ("e", BLACK, r"\;\text{Coefficient of }x_1x_2"),
])
compose("c3", [
    ("t", BLUE, r"a_{22}"),
    ("a", BLUE, r"\;\Rightarrow\;"),
    ("e", BLACK, r"\text{Coefficient of }x_2^{2}"),
])
compose("dmat", [
    ("h1", BLUE, r"x_1\;\;x_2"),
    ("m", BLUE, A),
])
compose("darrow", [("a", BLUE, r"\Rightarrow")])
compose("bx1", [("b", BLUE, r"\text{coef of }"), ("v", RED, r"x_1^{2}")])
compose("bx2", [("b", BLUE, r"0.5\,\text{coef of }"), ("v", RED, r"x_1x_2")])
compose("bx3", [("b", BLUE, r"0.5\,\text{coef of }"), ("v", RED, r"x_1x_2")])
compose("bx4", [("b", BLUE, r"\text{coef of }"), ("v", RED, r"x_2^{2}")])
compose("r1", [("r", RED, r"x_1")])
compose("r2", [("r", RED, r"x_2")])
