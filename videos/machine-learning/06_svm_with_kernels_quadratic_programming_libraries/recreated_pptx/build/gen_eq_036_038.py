#!/usr/bin/env python3
"""Generate 2D color-coded equation PNGs for slides 036, 037, 038.

Each job is a list of [label, color, latex] segments. Segments render at the
same size, align on a shared baseline and concatenate horizontally. A sibling
<name>.segments.json records each labelled segment's pixel bbox so build scripts
can place highlight shapes exactly over the term they mark.

Usage: python3 gen_eq_036_038.py [name-substring ...]
"""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

BLUE, RED, BLACK = "0000CC", "CC0000", "000000"
FS = 20


def compose(out, segs, gap=0):
    rendered = [render_segment(latex, "#" + color, FS) for _, color, latex in segs]
    max_b = max(b for _, b in rendered)
    heights = [a.shape[0] for a, _ in rendered]
    total_h = max_b + max(h - b for (_, b), h in zip(rendered, heights)) + PAD_PX
    total_w = sum(a.shape[1] for a, _ in rendered) + gap * (len(rendered) - 1) + 2 * PAD_PX
    canvas = np.zeros((total_h, total_w, 4), dtype=np.uint8)
    boxes = {}
    x = PAD_PX
    for (arr, b), (label, _, _) in zip(rendered, segs):
        y = max_b - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        boxes[label] = {"x0": int(x), "x1": int(x + arr.shape[1]),
                        "y0": int(y), "y1": int(y + arr.shape[0])}
        x += arr.shape[1] + gap
    Image.fromarray(canvas).save(out)
    meta = {"path": out, "w_px": int(total_w), "h_px": int(total_h),
            "w_in": round(total_w / DPI, 5), "h_in": round(total_h / DPI, 5),
            "segments": boxes}
    with open(out + ".segments.json", "w") as fh:
        json.dump(meta, fh, indent=1)
    print(json.dumps({k: meta[k] for k in ("path", "w_px", "h_px", "w_in", "h_in")}))
    return meta


def lag(tail):
    return [
        ["lag", BLUE, r"\mathcal{L}_D(\alpha)"],
        ["eq", BLACK, "="],
        ["sum_a", RED, r"\sum_{i=1}^{N}\alpha_i"],
        ["minus", BLACK, "-"],
        ["half", BLACK, r"\frac{1}{2}"],
        ["sum_ij", RED, r"\sum_{j=1}^{N}\sum_{i=1}^{N}\alpha_i\alpha_j y_i y_j"],
        ["kern", BLACK, tail],
    ]


def b_form(opener, term, closer):
    return [
        ["b", BLUE, "b"],
        ["eq", BLACK, "="],
        ["minus", BLACK, "-"],
        ["half", BLACK, r"\frac{1}{2}"],
        ["max", RED, opener + r" \max_{i,y=-1}"],
        ["t1", BLACK, term],
        ["min", RED, r"+ \min_{i,y=+1}"],
        ["t2", BLACK, term],
        ["close", RED, closer],
    ]


W_FORM = [["W", BLUE, "W"], ["eq", BLACK, "="],
          ["sum", RED, r"\sum_{i=1}^{N}\alpha_i y_i X_i"]]

JOBS = {
    "eq_036/eq_lag_orig.png": lag(r"(X_i^T X_j)"),
    "eq_036/eq_lag_k.png": lag(r"(X_i^T X_j)^2"),
    "eq_036/eq_W.png": W_FORM,
    "eq_036/eq_b_orig.png": b_form(r"\{", r"(W^T X_i)", r"\}"),
    "eq_036/eq_b_k.png": b_form(r"\{", r"[W^T X_i]^2", r"\}"),
    "eq_036/eq_kernel_quad.png": [["k", RED, r"\mathbf{K}(\alpha,b)=\alpha^T b^2"]],
    "eq_037/eq_lag_orig.png": lag(r"(X_i^T X_j)"),
    "eq_037/eq_lag_k.png": lag(r"(X_i^T X_j + 1)^d"),
    "eq_037/eq_W.png": W_FORM,
    "eq_037/eq_b_orig.png": b_form(r"[", r"(W^T X_i)", r"]"),
    "eq_037/eq_b_k.png": b_form(r"[", r"[W^T X_i + 1]^d", r"]"),
    "eq_037/eq_kernel_poly.png": [["k", RED, r"\mathbf{K}(\alpha,b)=(\alpha^T b + 1)^d"]],
    "eq_038/eq_minimize.png": [
        ["min", BLACK, r"\mathrm{Minimize}\ \ \mathcal{L}_D(\alpha) = \frac{1}{2}"],
        ["body", BLACK, r"\sum_{j=1}^{N}\sum_{i=1}^{N}\alpha_i\alpha_j y_i y_j [X_i^T X_j + 1]^2"],
        ["lin", BLACK, r"-\sum_{i=1}^{N}\alpha_i"],
    ],
    "eq_038/eq_constraint_sum.png": [["sum", BLACK, r"\sum \alpha_i y_i = 0"]],
}

if __name__ == "__main__":
    only = sys.argv[1:] or None
    for name, segs in JOBS.items():
        if only and not any(o in name for o in only):
            continue
        out = os.path.join(BUILD, name)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        compose(out, segs)
