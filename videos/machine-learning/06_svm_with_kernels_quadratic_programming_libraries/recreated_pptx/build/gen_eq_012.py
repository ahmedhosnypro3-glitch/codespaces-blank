#!/usr/bin/env python3
"""Generate 2D equation PNGs for slide 012 (QP objective in alpha)."""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_012"
os.makedirs(OUT, exist_ok=True)
BLUE, RED, GREEN, BLACK = "0000CC", "CC0000", "008000", "000000"

def compose(name, segs, gap=6, fs=17):
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

a = lambda i: rf"\alpha_{{{i}}}"
compose("obj1", [("t", BLUE,
    r"[+1" + a(1) + r"^{2}+2" + a(1) + a(2) + r"-5.5" + a(1) + a(3) + r"-6" + a(1) + a(4)
    + r"+2" + a(2) + a(4) + r"+4" + a(2) + r"^{2}-11" + a(2) + a(3) + r"-12" + a(2) + a(4))])
compose("obj2", [("t", BLUE,
    r"-5.5" + a(3) + a(1) + r"-11" + a(3) + a(2) + r"+32.5" + a(3) + r"^{2}+36" + a(3) + a(4)
    + r"-6" + a(4) + a(1) + r"-12" + a(4) + a(2) + r"+36" + a(4) + a(3) + r"+40" + a(4) + r"^{2}]"
    r"-[" + a(1) + r"+" + a(2) + r"+" + a(3) + r"+" + a(4) + r"]")])
compose("c1", [("t", RED, r"\sum\alpha_i y_i=0")], fs=13)
compose("c2", [("t", RED, a(1) + r"+" + a(2) + r"-" + a(3) + r"-" + a(4) + r"=0")], fs=13)
compose("c3", [("t", RED, r"\alpha_i\leq C")], fs=13)
compose("c4", [("t", RED, a(1) + r"\leq1,\;" + a(2) + r"\leq1,\;" + a(3) + r"\leq1,\;" + a(4) + r"\leq1")], fs=13)
compose("c5", [("t", RED, r"\alpha_i\geq 0")], fs=13)
compose("c6", [("t", RED, a(1) + r">0,\;" + a(2) + r">0,\;" + a(3) + r">0,\;" + a(4) + r">0")], fs=13)
compose("compact", [
    ("h", GREEN, r"\frac{1}{2}"),
    ("b", BLUE, r"[X^{T}PX]+"),
    ("q", RED, r"q^{T}"),
    ("x", BLUE, r"X"),
], fs=15)
compose("half", [("t", GREEN, r"\frac{1}{2}")], fs=20)
compose("lobj1", [("t", BLUE,
    r"[+2" + a(1) + r"^{2}+4" + a(1) + a(2) + r"-11" + a(1) + a(3) + r"-12" + a(1) + a(4)
    + r"+4" + a(2) + a(4) + r"+8" + a(2) + r"^{2}-22" + a(2) + a(3) + r"-24" + a(2) + a(4))])
compose("lobj2", [("t", BLUE,
    r"-11" + a(3) + a(1) + r"-22" + a(3) + a(2) + r"+65" + a(3) + r"^{2}+72" + a(3) + a(4)
    + r"-12" + a(4) + a(1) + r"-24" + a(4) + a(2) + r"+72" + a(4) + a(3) + r"+80" + a(4) + r"^{2}]"
    r"-[" + a(1) + r"+" + a(2) + r"+" + a(3) + r"+" + a(4) + r"]")])
P = r"\left(\overset{2\;\;4\;-11\;-12}{4\;\;8\;-22\;-24}{-11\;-22\;65\;72}{-12\;-24\;72\;80}\right)"
compose("P", [("e", BLACK, r"P="), ("m", BLUE, P)], fs=14)
compose("q", [("e", RED, r"q^{T}="), ("m", BLUE, r"[-1\;-1\;-1\;-1]")], fs=14)
