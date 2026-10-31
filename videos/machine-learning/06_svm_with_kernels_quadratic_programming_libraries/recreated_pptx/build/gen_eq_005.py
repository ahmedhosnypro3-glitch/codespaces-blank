#!/usr/bin/env python3
"""Generate 2D equation PNGs for slide 005 (Three Variables Example)."""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_005"
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

A = r"\left[\overset{a_{11}\;a_{12}\;a_{13}}{a_{21}\;a_{22}\;a_{23}}{a_{31}\;a_{32}\;a_{33}}\right]"
XV = r"\left(x_1\;x_2\;x_3\right)"
XC = r"\left[\overset{x_1}{x_2}{x_3}\right]"

compose("e1", [
    ("l", BLACK, XV + A + XC),
    ("eq", RED, r"\;=\;"),
    ("r", BLACK, r"\left[\overset{a_{11}x_1+a_{21}x_2+a_{31}x_3}{a_{12}x_1+a_{22}x_2+a_{32}x_3}{a_{13}x_1+a_{23}x_2+a_{33}x_3}\right]"),
])
compose("e2", [
    ("l", BLACK, r"=(a_{11}x_1+a_{21}x_2+a_{31}x_3)x_1+(a_{12}x_1+a_{22}x_2+a_{32}x_3)x_2+(a_{13}x_1+a_{23}x_2+a_{33}x_3)x_3"),
])
compose("e3", [
    ("l", BLACK, r"=\;a_{11}x_1^{2}+a_{21}x_1x_2+a_{31}x_1x_3+a_{12}x_1x_2+a_{22}x_2^{2}+a_{32}x_2x_3+a_{13}x_1x_3+a_{23}x_2x_3+a_{33}x_3^{2}"),
])
compose("e4", [
    ("l", BLACK, r"a_{11}x_1^{2}+a_{22}x_2^{2}+a_{33}x_3^{2}+(a_{21}+a_{12})x_1x_2+(a_{31}+a_{13})x_1x_3+(a_{32}+a_{23})x_2x_3"),
    ("arr", RED, r"\;\Rightarrow\;"),
    ("q", GREEN, r"\text{Quadratic form}"),
])
defs = [
    ("d1", [("t", BLACK, r"a_{11}"), ("a", RED, r"\;\Rightarrow\;"), ("e", RED, r"\text{Coefficient of }x_1^{2}")]),
    ("d2", [("t", BLACK, r"a_{22}"), ("a", RED, r"\;\Rightarrow\;"), ("e", RED, r"\text{Coefficient of }x_2^{2}")]),
    ("d3", [("t", BLACK, r"a_{33}"), ("a", RED, r"\;\Rightarrow\;"), ("e", RED, r"\text{Coefficient of }x_3^{2}")]),
    ("d4", [("t", BLACK, r"a_{21}+a_{12}"), ("a", RED, r"\;\Rightarrow\;"), ("e", RED, r"a_{12}=a_{21}=\frac{1}{2}\text{ coefficient of }x_1x_2")]),
    ("d5", [("t", BLACK, r"a_{31}+a_{13}"), ("a", RED, r"\;\Rightarrow\;"), ("e", RED, r"a_{13}=a_{31}=\frac{1}{2}\text{ coefficient of }x_1x_3")]),
    ("d6", [("t", BLACK, r"a_{32}+a_{23}"), ("a", RED, r"\;\Rightarrow\;"), ("e", RED, r"a_{32}=a_{23}=\frac{1}{2}\text{ coefficient of }x_2x_3")]),
]
for name, segs in defs:
    compose(name, segs)
# bottom diagram: left matrix with headers
compose("mat", [("m", BLACK, A)])
compose("hdr", [("h", BLACK, r"x_1\;\;\;x_2\;\;\;x_3")])
boxes = [
    ("b1", r"\text{coef of }x_1^{2}"), ("b2", r"0.5\,\text{coef of }x_1x_3"),
    ("b3", r"0.5\,\text{coef of }x_1x_2"), ("b4", r"0.5\,\text{coef of }x_1x_2"),
    ("b5", r"\text{coef of }x_2^{2}"), ("b6", r"0.5\,\text{coef of }x_2x_3"),
    ("b7", r"0.5\,\text{coef of }x_1x_3"), ("b8", r"0.5\,\text{coef of }x_2x_3"),
    ("b9", r"\text{coef of }x_3^{2}"),
]
for name, latex in boxes:
    compose(name, [("b", BLACK, latex)])
