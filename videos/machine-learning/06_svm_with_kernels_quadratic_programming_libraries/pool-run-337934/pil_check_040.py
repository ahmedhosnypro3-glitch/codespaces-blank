#!/usr/bin/env python3
"""Closed-loop PIL check: recreation render vs original frame for slide 040."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
orig = Image.open(f"{NS}/qa/rejudge2/orig_png/slide_040.png").convert("RGB")
ren = Image.open(f"{NS}/recreated_pptx/renders/slide_040_recreated-1.png").convert("RGB")
print("orig", orig.size, "render", ren.size)

ow, oh = orig.size
rw, rh = ren.size

def ink_mask(im, thresh=200):
    a = np.asarray(im).astype(int)
    # ink = pixels notably darker than background
    return (a.sum(axis=2) < thresh * 3)

om = ink_mask(orig)
rm = ink_mask(ren)
print(f"ink coverage orig={om.mean()*100:.2f}% render={rm.mean()*100:.2f}%")

# scale normalized coords to render size
def region(mask, x0, y0, x1, y1, w, h):
    X0, Y0, X1, Y1 = int(x0*w), int(y0*h), int(x1*w), int(y1*h)
    return mask[Y0:Y1, X0:X1].mean()*100

# spec regions of interest (normalized)
regions = {
    "title":      (0.28, 0.10, 0.72, 0.20),
    "labels_top": (0.15, 0.21, 0.83, 0.25),
    "plots_top":  (0.11, 0.26, 0.86, 0.52),
    "labels_bot": (0.15, 0.57, 0.83, 0.61),
    "plots_bot":  (0.11, 0.62, 0.86, 0.88),
    "arrow":      (0.56, 0.56, 0.58, 0.58),
    "badge":      (0.88, 0.08, 0.96, 0.18),
}
for name, r in regions.items():
    print(f"{name:10s} orig_ink={region(om, *r, ow, oh):6.2f}%  render_ink={region(rm, *r, rw, rh):6.2f}%")

# colored-point presence in each plot panel (render): count strongly colored pixels
def color_frac(im, x0, y0, x1, y1):
    a = np.asarray(im)[int(y0*rh):int(y1*rh), int(x0*rw):int(x1*rw)].astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(axis=2); mn = a.min(axis=2)
    sat = (mx - mn) > 80
    return sat.mean() * 100

panels = {
    "Aggregation": (0.11, 0.26, 0.31, 0.52), "Compound": (0.39, 0.26, 0.58, 0.52),
    "Spiral": (0.67, 0.26, 0.86, 0.52), "Pathbased": (0.11, 0.62, 0.31, 0.88),
    "Flame": (0.39, 0.62, 0.58, 0.88), "Jain": (0.67, 0.62, 0.86, 0.88),
}
for name, r in panels.items():
    print(f"panel {name:12s} render_color_frac={color_frac(ren, *r):.2f}%  orig_color_frac={color_frac(orig, *r):.2f}%")
