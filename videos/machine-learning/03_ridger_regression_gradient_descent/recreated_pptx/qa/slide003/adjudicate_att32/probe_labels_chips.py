#!/usr/bin/env python3
"""Probe 3: dimension-label colors, y-vector chips-vs-text, ones-column.
crop_33_matrix pair: slide-space region (74,320)-(538,520)."""
import numpy as np
from PIL import Image

Q = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"
X0, Y0, X1, Y1 = 74, 320, 538, 520

r = np.asarray(Image.open(Q + "/crop_33_matrix_render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(Q + "/crop_33_matrix_orig.png").convert("RGB")).astype(int)
H, W = o.shape[:2]
sx, sy = (X1 - X0) / W, (Y1 - Y0) / H
print(f"crop sizes: orig {o.shape[1]}x{o.shape[0]}  render {r.shape[1]}x{r.shape[0]}  slide-px/crop-px {sx:.4f}/{sy:.4f}")

def box_stats(img, bx0, by0, bx1, by1, tag):
    cx0, cy0 = int((bx0 - X0) / sx), int((by0 - Y0) / sy)
    cx1, cy1 = int((bx1 - X0) / sx), int((by1 - Y0) / sy)
    sub = img[cy0:cy1, cx0:cx1]
    rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    mx = sub.max(axis=2); mn = sub.min(axis=2)
    sat = (mx - mn) > 45
    dark = mx < 110
    ink = sat | dark
    n = int(ink.sum())
    out = [f"  {tag}: ink={n} sat={int(sat.sum())} dark={int(dark.sum())}"]
    if n:
        px = sub[ink]
        # quantize to 32-steps
        q = (px // 32) * 32 + 16
        vals, cnts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
        order = np.argsort(-cnts)
        for k in order[:4]:
            c = vals[k]
            out.append(f"    cluster rgb~({c[0]},{c[1]},{c[2]}) n={cnts[k]}")
    return "\n".join(out)

print("=== dimension labels (slide-space boxes) ===")
for name, bx0, by0, bx1, by1 in [
    ("L1 'N x 1'  ", 120, 452, 204, 480),
    ("L2 'N x d+1'", 394, 462, 516, 492),
    ("L3 'd+1 x 1'", 446, 480, 534, 508),
]:
    print(box_stats(o, bx0, by0, bx1, by1, f"ORIG {name}"))
    print(box_stats(r, bx0, by0, bx1, by1, f"REND {name}"))

print("=== y-vector column x100..150 y352..492: chips (sat) vs dark text, per row band ===")
bands = [("y1 band", 362, 394), ("y2 band", 395, 425), ("... band", 426, 454), ("yn band", 455, 482)]
for tag, by0, by1 in bands:
    for img, lab in ((o, "ORIG"), (r, "REND")):
        sub_box = img[int((by0 - Y0) / sy):int((by1 - Y0) / sy), int((100 - X0) / sx):int((150 - X0) / sx)]
        mx = sub_box.max(axis=2); mn = sub_box.min(axis=2)
        sat = (mx - mn) > 45; dark = mx < 110
        line = f"  {lab} {tag}: sat={int(sat.sum())} dark={int(dark.sum())}"
        if sat.sum():
            px = sub_box[sat]
            q = (px // 32) * 32 + 16
            vals, cnts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
            k = np.argsort(-cnts)[:2]
            line += " sat-clusters: " + ", ".join(f"({vals[i][0]},{vals[i][1]},{vals[i][2]})x{cnts[i]}" for i in k)
        print(line)

print("=== ones column x200..228 y356..490: dark glyph px per band ===")
for tag, by0, by1 in bands:
    for img, lab in ((o, "ORIG"), (r, "REND")):
        sub_box = img[int((by0 - Y0) / sy):int((by1 - Y0) / sy), int((200 - X0) / sx):int((228 - X0) / sx)]
        dark = (sub_box.max(axis=2) < 110)
        print(f"  {lab} {tag}: dark={int(dark.sum())}")
