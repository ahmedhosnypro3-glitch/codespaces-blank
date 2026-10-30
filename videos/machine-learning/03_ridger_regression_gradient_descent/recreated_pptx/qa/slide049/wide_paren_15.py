#!/usr/bin/env python3
"""Slide 049 — wide region dumps: calc row 1 full, W-col wide, initial-W band scan."""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(BASE + "/unique_slides/slide_049.jpg").convert("L"), dtype=np.float32)
rend_img = Image.open(BASE + "/recreated_pptx/qa/slide049/render_13.png").convert("L")
S = rend_img.size[1] / orig.shape[0]

def art(a):
    out = []
    for row in a:
        out.append("".join("#" if v < 110 else ("+" if v < 170 else " ") for v in row).rstrip())
    return "\n".join(out)

def dump(x0, y0, x1, y1, name, arr, scale=1):
    print(f"\n===== {name} ({x0},{y0})-({x1},{y1}) =====")
    print(art(arr[y0:y1 + 1, x0:x1 + 1]))

# 1) orig calc row 1 full width (digits + high-bracket + = + result)
dump(274, 138, 540, 200, "ORIG calc row1 full", orig)
# 2) render calc row1 full width, downsampled to frame scale
r = np.array(rend_img.crop((int(274 * S), int(138 * S), int(541 * S), int(201 * S))), dtype=np.float32)
h, w = r.shape
r_small = r[: (h // 2) * 2, : (w // 2) * 2].reshape(h // 2, 2, w // 2, 2).mean(axis=(1, 3))
print("\n===== RENDER calc row1 full (downsampled) =====")
print(art(r_small))
# 3) orig W= section wide
dump(690, 138, 775, 200, "ORIG W= row1 wide", orig)
# 4) render W= section wide
r2 = np.array(rend_img.crop((int(690 * S), int(138 * S), int(776 * S), int(201 * S))), dtype=np.float32)
h2, w2 = r2.shape
r2_small = r2[: (h2 // 2) * 2, : (w2 // 2) * 2].reshape(h2 // 2, 2, w2 // 2, 2).mean(axis=(1, 3))
print("\n===== RENDER W= row1 wide (downsampled) =====")
print(art(r2_small))
# 5) initial-W band: row runs at y55-57 and y72-73, x250..540 (find the band + underline)
for y in (55, 56, 57, 60, 72, 73):
    row = orig[y, 250:540]
    runs, cur = [], None
    for i, v in enumerate(row):
        on = v < 170
        if on and cur is None:
            cur = i
        elif not on and cur is not None:
            runs.append((cur + 250, i - 1 + 250)); cur = None
    if cur is not None:
        runs.append((cur + 250, 289 + 250))
    print(f"y={y} ink runs (x<170): {runs}")
# 6) orig initial-W region wide x315..440 y44..100
dump(315, 44, 440, 100, "ORIG initial-W wide", orig)
r3 = np.array(rend_img.crop((int(315 * S), int(44 * S), int(441 * S), int(101 * S))), dtype=np.float32)
h3, w3 = r3.shape
r3_small = r3[: (h3 // 2) * 2, : (w3 // 2) * 2].reshape(h3 // 2, 2, w3 // 2, 2).mean(axis=(1, 3))
print("\n===== RENDER initial-W wide (downsampled) =====")
print(art(r3_small))
