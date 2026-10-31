#!/usr/bin/env python3
"""Slide 012: four-line lower-objective PNGs (judge MAJOR: separate term lines)."""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_012"
BLUE = "0000CC"

def compose(name, latex, fs=12):
    arr, _b = render_segment(latex, "#" + BLUE, fs)
    h, w = arr.shape[0], arr.shape[1]
    canvas = np.zeros((h + 2 * PAD_PX, w + 2 * PAD_PX, 4), dtype=np.uint8)
    canvas[PAD_PX:PAD_PX + h, PAD_PX:PAD_PX + w] = arr
    out = f"{OUT}/{name}.png"
    Image.fromarray(canvas).save(out)
    meta = {"path": out, "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
            "w_in": round(canvas.shape[1] / DPI, 5), "h_in": round(canvas.shape[0] / DPI, 5)}
    with open(out + ".json", "w") as fh:
        json.dump(meta, fh)
    print(name, meta["w_in"], "x", meta["h_in"])

a = lambda i: rf"\alpha_{{{i}}}"
compose("q1", r"[+2" + a(1) + r"^{2}+4" + a(1) + a(2) + r"-11" + a(1) + a(3)
        + r"-12" + a(1) + a(4) + r"+4" + a(1) + a(4) + r"\text{[?]}")
compose("q2", r"+8" + a(2) + r"^{2}-22" + a(2) + a(3) + r"-24" + a(2) + a(4))
compose("q3", r"-11" + a(3) + a(1) + r"-22" + a(3) + a(2) + r"+65" + a(3) + r"^{2}+72" + a(3) + a(4))
compose("q4", r"-12" + a(4) + a(1) + r"-24" + a(4) + a(2) + r"+72" + a(4) + a(3) + r"+80" + a(4)
        + r"^{2}]-[" + a(1) + r"+" + a(2) + r"+" + a(3) + r"+" + a(4) + r"]")
