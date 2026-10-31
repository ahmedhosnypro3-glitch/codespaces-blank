#!/usr/bin/env python3
"""Slide 009 rb4: G (5x2) and h (5x1) matrices as true multi-row renders.

Nested \\overset and \\substack collapse to a single ink band in this
matplotlib build, so rows are rendered individually and stacked with PIL;
brackets are rendered at a font size matched to the body height.
Usage: python3 gen_eq_009_rb4.py
"""
import json
import os
import sys

import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_009"
BLACK = "#000000"

G_ROWS = [r"-1\;\;0", r"0\;-1", r"-1\;-3", r"2\;\;5", r"3\;\;4"]
H_ROWS = [r"0", r"0", r"-15", r"100", r"80"]


def bracket(target_h_px, glyph):
    fs = 10.0
    while True:
        arr, _ = render_segment(glyph, BLACK, fs)
        if arr.shape[0] >= target_h_px or fs > 400:
            break
        fs *= 1.15
    im = Image.fromarray(arr)
    im = im.resize((max(24, int(arr.shape[1] * 0.3)), target_h_px), Image.LANCZOS)
    return np.asarray(im)


def matrix(name, label, rows, fs=13.0, max_h_in=1.3):
    rendered = [render_segment(r, BLACK, fs) for r in rows]
    lab, lab_b = render_segment(label, BLACK, fs)
    body_w = max(a.shape[1] for a, _ in rendered)
    gap = int(fs * DPI / 72 * 0.55)
    body_h = sum(a.shape[0] for a, _ in rendered) + gap * (len(rendered) - 1)
    h_in = (body_h + 2 * PAD_PX) / DPI
    if h_in > max_h_in:
        fs *= max_h_in / h_in * 0.98
        return matrix(name, label, rows, fs, max_h_in)
    lb = bracket(body_h, r"\lbrack")
    rb = bracket(body_h, r"\rbrack")
    total_w = lab.shape[1] + PAD_PX + lb.shape[1] + PAD_PX + body_w + PAD_PX + rb.shape[1] + 2 * PAD_PX
    total_h = body_h + 2 * PAD_PX
    canvas = np.zeros((total_h, total_w, 4), dtype=np.uint8)
    x = PAD_PX
    y = (total_h - lab.shape[0]) // 2 + lab.shape[0] - lab_b
    canvas[y:y + lab.shape[0], x:x + lab.shape[1]] = lab
    x += lab.shape[1] + PAD_PX
    canvas[PAD_PX:PAD_PX + body_h, x:x + lb.shape[1]] = lb
    x += lb.shape[1] + PAD_PX
    y = PAD_PX
    for arr, _ in rendered:
        canvas[y:y + arr.shape[0], x:x + body_w] = arr[:, :body_w] if arr.shape[1] >= body_w else np.pad(arr, ((0, 0), (0, body_w - arr.shape[1]), (0, 0)))
        y += arr.shape[0] + gap
    x += body_w + PAD_PX
    canvas[PAD_PX:PAD_PX + body_h, x:x + rb.shape[1]] = rb
    out = f"{OUT}/{name}.png"
    Image.fromarray(canvas).save(out)
    meta = {"path": out, "w_px": int(total_w), "h_px": int(total_h),
            "w_in": round(total_w / DPI, 5), "h_in": round(total_h / DPI, 5),
            "dpi": DPI, "fontsize_pt": fs,
            "rows": [f"{BLACK}:{label}", *rows]}
    with open(out + ".json", "w") as fh:
        json.dump(meta, fh, indent=2)
    print(name, meta["w_in"], "x", meta["h_in"], "fs", round(fs, 2))


matrix("G_rb4", r"G=", G_ROWS)
matrix("h_rb4", r"h=", H_ROWS)
