#!/usr/bin/env python3
"""Slide 012 round-3 assets: red objectives (2-line layout), fixed compact
equation, larger bound rows, p_matrix sidecar."""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_012"
RED, BLUE, GREEN = "CC0000", "0000CC", "008000"

def compose(name, segs, fs=17, gap=4):
    """segs: list of (color, latex); baseline-aligned multi-color line."""
    rendered = [render_segment(latex, "#" + color, fs) for color, latex in segs]
    max_b = max(b for _, b in rendered)
    heights = [a.shape[0] for a, _ in rendered]
    total_h = max_b + max(h - b for (_, b), h in zip(rendered, heights)) + 2 * PAD_PX
    total_w = sum(a.shape[1] for a, _ in rendered) + gap * (len(rendered) - 1) + 2 * PAD_PX
    canvas = np.zeros((total_h, total_w, 4), dtype=np.uint8)
    x = PAD_PX
    for (arr, b), _ in zip(rendered, segs):
        y = max_b - b + PAD_PX
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        x += arr.shape[1] + gap
    out = f"{OUT}/{name}.png"
    Image.fromarray(canvas).save(out)
    meta = {"path": out, "w_px": int(total_w), "h_px": int(total_h),
            "w_in": round(total_w / DPI, 5), "h_in": round(total_h / DPI, 5)}
    with open(f"{OUT}/{name}.json", "w") as fh:
        json.dump(meta, fh)
    print(name, meta["w_in"], "x", meta["h_in"])

a = lambda i: rf"\alpha_{{{i}}}"
# Red objective lines (judge: original renders objectives red), 2-line layout
compose("r1", [(RED, r"[+1" + a(1) + r"^{2}+2" + a(1) + a(2) + r"-5.5" + a(1) + a(3)
    + r"-6" + a(1) + a(4) + r"+2" + a(2) + a(4) + r"\text{[?]}+4" + a(2) + r"^{2}"
    + r"-11" + a(2) + a(3) + r"-12" + a(2) + a(4))], fs=17)
compose("r2", [(RED, r"-5.5" + a(3) + a(1) + r"-11" + a(3) + a(2) + r"+32.5" + a(3) + r"^{2}"
    + r"+36" + a(3) + a(4) + r"-6" + a(4) + a(1) + r"-12" + a(4) + a(2) + r"+36" + a(4)
    + a(3) + r"+40" + a(4) + r"^{2}]-[" + a(1) + r"+" + a(2) + r"+" + a(3) + r"+" + a(4) + r"]")], fs=17)
compose("r10", [(RED, r"[+2" + a(1) + r"^{2}+4" + a(1) + a(2) + r"-11" + a(1) + a(3)
    + r"-12" + a(1) + a(4) + r"+4" + a(1) + a(4) + r"\text{[?]}+8" + a(2) + r"^{2}"
    + r"-22" + a(2) + a(3) + r"-24" + a(2) + a(4))], fs=17)
compose("r11", [(RED, r"-11" + a(3) + a(1) + r"-22" + a(3) + a(2) + r"+65" + a(3) + r"^{2}"
    + r"+72" + a(3) + a(4) + r"-12" + a(4) + a(1) + r"-24" + a(4) + a(2) + r"+72" + a(4)
    + a(3) + r"+80" + a(4) + r"^{2}]-[" + a(1) + r"+" + a(2) + r"+" + a(3) + r"+" + a(4) + r"]")], fs=17)
# Fixed compact formula (baseline-aligned, fills the amber box)
compose("e9b", [(GREEN, r"\frac{1}{2}"), (BLUE, r"[X^{T}PX]+"), (RED, r"q^{T}"), (BLUE, r"X")], fs=20, gap=6)
# Larger, clearer bound/positivity rows
compose("e6b", [(RED, a(1) + r"\leq1,\;" + a(2) + r"\leq1,\;" + a(3) + r"\leq1,\;" + a(4) + r"\leq1")], fs=17)
compose("e8b", [(RED, a(1) + r">0,\;" + a(2) + r">0,\;" + a(3) + r">0,\;" + a(4) + r">0")], fs=17)
# Sidecar for the proper matplotlib-drawn matrix
im = Image.open(f"{OUT}/p_matrix.png")
meta = {"path": f"{OUT}/p_matrix.png", "w_px": im.size[0], "h_px": im.size[1],
        "w_in": round(im.size[0] / DPI, 5), "h_in": round(im.size[1] / DPI, 5)}
with open(f"{OUT}/p_matrix.json", "w") as fh:
    json.dump(meta, fh)
print("p_matrix", meta["w_in"], "x", meta["h_in"])
