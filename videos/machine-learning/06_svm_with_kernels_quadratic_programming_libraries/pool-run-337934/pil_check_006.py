#!/usr/bin/env python3
"""Refined PIL check: luminance ink + hue color masks, per-band, slide_006."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
o = np.asarray(Image.open(NS + "/qa/rejudge2/orig_png/slide_006.png").convert("RGB")).astype(int)
r = np.asarray(Image.open(NS + "/recreated_pptx/renders/slide_006_recreated-1.png").convert("RGB")
              .resize((960, 540), Image.LANCZOS)).astype(int)


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


def ink(a):
    return lum(a) < 190


def hue_mask(a, lo, hi, sat_min=60):
    mx = a.max(axis=2); mn = a.min(axis=2)
    sat = mx - mn
    h = np.zeros_like(mx)
    r_, g_, b_ = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = mx == r_
    h[m] = ((g_ - b_)[m] / np.maximum(sat[m], 1) * 60) % 360
    m = (mx == g_) & (mx != r_)
    h[m] = (b_ - r_)[m] / np.maximum(sat[m], 1) * 60 + 120
    m = (mx == b_) & (mx != g_) & (mx != r_)
    h[m] = (r_ - g_)[m] / np.maximum(sat[m], 1) * 60 + 240
    return (h >= lo) & (h < hi) & (sat > sat_min) & (mx < 250)


bands = {"title": (0.03, 0.15), "panel1": (0.16, 0.34), "panel2": (0.345, 0.575),
         "panel3": (0.585, 0.875), "bottom": (0.875, 1.0)}
for name, (y0, y1) in bands.items():
    sl = slice(int(y0 * 540), int(y1 * 540))
    print(f"{name:7s} ink orig={ink(o[sl]).mean():.4f} rend={ink(r[sl]).mean():.4f}")

for cname, lo, hi in [("red", 340, 360), ("red2", 0, 12), ("blue", 200, 260),
                      ("green", 80, 160), ("yellow", 45, 70)]:
    print(f"{cname:6s} orig={hue_mask(o, lo, hi).sum():6d} rend={hue_mask(r, lo, hi).sum():6d}")

# where does the dark footer start in orig?
rowlum = lum(o).mean(axis=1)
dark_rows = np.where(rowlum < 100)[0]
print("orig dark rows from y=", dark_rows.min() if len(dark_rows) else None,
      "to", dark_rows.max() if len(dark_rows) else None,
      "frac of 540:", (dark_rows.min() / 540 if len(dark_rows) else None))

# per-band column thirds with luminance ink
for name, (y0, y1) in [("panel1", (0.16, 0.34)), ("panel2", (0.345, 0.575)), ("panel3", (0.585, 0.875))]:
    sl = slice(int(y0 * 540), int(y1 * 540))
    for tag, a in [("orig", o), ("rend", r)]:
        prof = ink(a[sl]).mean(axis=0)
        print(f"{name} {tag} thirds: " + " ".join(f"{prof[i*320:(i+1)*320].mean():.3f}" for i in range(3)))
