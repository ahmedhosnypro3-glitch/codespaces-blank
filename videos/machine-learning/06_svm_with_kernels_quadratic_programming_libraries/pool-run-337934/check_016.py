#!/usr/bin/env python3
"""Closed-loop PIL check: render vs original for slide 016 (ink presence per spec region)."""
import os
from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
orig = Image.open(os.path.join(NS, "qa/rejudge2/orig_png/slide_016.png")).convert("RGB")
ren = Image.open(os.path.join(NS, "recreated_pptx/renders/slide_016_recreated-1.png")).convert("RGB")
print("orig", orig.size, "render", ren.size)
o = np.asarray(orig).astype(int)
r = np.asarray(ren).astype(int)

REGIONS = {
    "title_band":      [0.098, 0.065, 0.902, 0.145],
    "badge":           [0.905, 0.065, 0.985, 0.145],
    "mapping_box":     [0.060, 0.205, 0.275, 0.315],
    "right_text":      [0.690, 0.235, 0.905, 0.340],
    "boundary_label":  [0.740, 0.400, 0.900, 0.455],
    "v_axis":          [0.330, 0.185, 0.346, 0.780],
    "h_axis":          [0.025, 0.775, 0.885, 0.785],
    "boundary_line":   [0.300, 0.505, 0.885, 0.515],
    "cyan_pts":        [0.260, 0.190, 0.630, 0.510],
    "red_pts":         [0.380, 0.625, 0.590, 0.750],
    "x_circles":       [0.305, 0.760, 0.735, 0.790],
    "cursor":          [0.165, 0.450, 0.195, 0.495],
}

def ink_frac(img, reg, pred):
    h, w, _ = img.shape
    x0, y0, x1, y1 = int(reg[0]*w), int(reg[1]*h), int(reg[2]*w), int(reg[3]*h)
    sub = img[y0:y1, x0:x1]
    if sub.size == 0:
        return 0.0
    m = pred(sub.reshape(-1, 3)).mean()
    return float(m)

dark = lambda px: (px.sum(axis=1) < 420)
redish = lambda px: (px[:, 0] > 120) & (px[:, 0] - px[:, 1] > 50) & (px[:, 0] - px[:, 2] > 50)
blueish = lambda px: (px[:, 2] > 110) & (px[:, 2] - px[:, 0] > 40)
cyanish = lambda px: (px[:, 1] > 130) & (px[:, 2] > 150) & (px[:, 2] - px[:, 0] > 60)
anyink = lambda px: (px.sum(axis=1) < 600)

PREDS = {
    "title_band": anyink, "badge": anyink, "mapping_box": anyink, "right_text": anyink,
    "boundary_label": blueish, "v_axis": redish, "h_axis": redish,
    "boundary_line": blueish, "cyan_pts": cyanish, "red_pts": redish,
    "x_circles": anyink, "cursor": dark,
}
print(f"{'region':16s} {'orig':>7s} {'render':>7s}")
for name, reg in REGIONS.items():
    p = PREDS[name]
    print(f"{name:16s} {ink_frac(o, reg, p):7.3f} {ink_frac(r, reg, p):7.3f}")

# global ink-edge rough comparison
def edges(img):
    g = img.mean(axis=2)
    gx = np.abs(np.diff(g, axis=1)) > 40
    gy = np.abs(np.diff(g, axis=0)) > 40
    return gx.mean() + gy.mean()
print("edge density orig %.4f render %.4f" % (edges(o), edges(r)))
