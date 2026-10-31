#!/usr/bin/env python3
"""Generate 2D equation PNGs for slide 030 (RBF Kernel derivation)."""
import json, os, sys
import numpy as np
from PIL import Image

BUILD = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
         "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build")
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

OUT = BUILD + "/eq_030"
os.makedirs(OUT, exist_ok=True)
RED, BLACK = "C00000", "000000"
FS = 19

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

# E1: kernel identity; first term sits on peach box
compose("e1a", [("t", BLACK, r"e^{-\frac{1}{2}(a-b)^{2}}")], fs=22)
compose("e1b", [("t", BLACK,
    r"=e^{-\frac{1}{2}(a^{2}+b^{2}-2ab)}=e^{-\frac{a^{2}}{2}}e^{-\frac{b^{2}}{2}}e^{ab}=")])

# E2: phi(a)^T row vector
compose("e2", [("t", BLACK,
    r"e^{-\frac{a^{2}}{2}}\left(1,\;\frac{a}{\sqrt{1!}},\;\frac{a^{2}}{\sqrt{2!}},"
    r"\;\frac{a^{3}}{\sqrt{3!}},\;\frac{a^{4}}{\sqrt{4!}},\;....,\;....,\;\infty\right)")])

# phi(b) column vector: render each row, stack with a fixed pitch, bracket drawn as lines
entries = [r"1", r"\frac{b}{\sqrt{1!}}", r"\frac{b^{2}}{\sqrt{2!}}",
           r"\frac{b^{3}}{\sqrt{3!}}", r"\frac{b^{4}}{\sqrt{4!}}", r"....", r"....\;\infty"]
FS_C = 15
rows = [render_segment(e, "#" + BLACK, FS_C) for e in entries]
PITCH = max(a.shape[0] for a, _ in rows) + 24
total_h = PITCH * len(rows) + 2 * PAD_PX
inner_w = max(a.shape[1] for a, _ in rows)
lw = 8
col_w = inner_w + 2 * PAD_PX + 2 * lw + 12
canvas = np.zeros((total_h, col_w, 4), dtype=np.uint8)
x = PAD_PX
canvas[PAD_PX:total_h - PAD_PX, x:x + lw] = 255
x += lw + 6
for i, (arr, b) in enumerate(rows):
    y = PAD_PX + i * PITCH + (PITCH - arr.shape[0]) // 2
    canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
x += inner_w + 6
canvas[PAD_PX:total_h - PAD_PX, x:x + lw] = 255
out = f"{OUT}/colb.png"
Image.fromarray(canvas).save(out)
meta = {"path": out, "w_px": int(col_w), "h_px": int(total_h),
        "w_in": round(col_w / DPI, 5), "h_in": round(total_h / DPI, 5)}
with open(out + ".json", "w") as fh:
    json.dump(meta, fh)
print("colb", meta["w_in"], "x", meta["h_in"])
compose("eb2", [("t", BLACK, r"e^{-\frac{b^{2}}{2}}")], fs=18)

# labels
compose("phia", [("t", RED, r"\phi(a)^{T}")], fs=18)
compose("phib", [("t", RED, r"\phi(b)")], fs=18)

# right panel
compose("rbf", [("t", BLACK, r"e^{-\gamma(a-b)^{2}}")], fs=22)
