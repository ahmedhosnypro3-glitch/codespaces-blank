#!/usr/bin/env python3
"""Probe v3: claim-3 label-swap test. In the original BL panel, extract the two
bottom annotation labels (slide-space y~448-472, x83-376), split into left/right
clusters, and cross-NCC against the render's labels. Build k14 places Global
Minima at x156 (left) and Local Minima at x313 (right); the fresh judge claims
the ORIGINAL has them the other way around."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
r = Image.open(f"{RJ}/slide025/render.png").convert("RGB").resize((960, 540), Image.LANCZOS)
o = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
R = np.asarray(r).astype(int); O = np.asarray(o).astype(int)
rdark = R.sum(axis=2) < 330
odark = O.sum(axis=2) < 330

def label_clusters(dark, y0, y1, x0, x1, minpx=6):
    sub = dark[y0:y1, x0:x1]
    cols = sub.sum(axis=0)
    clusters, start = [], None
    for i, v in enumerate(cols):
        if v >= 1 and start is None: start = i
        elif v < 1 and start is not None:
            if i - start >= minpx: clusters.append((x0 + start, x0 + i))
            start = None
    if start is not None: clusters.append((x0 + start, x0 + len(cols)))
    return clusters, sub

print("== label row bands in BL panel (x83-376):")
for nm, dark in (("render", rdark), ("orig", odark)):
    sub = dark[400:527, 83:376]
    rows = sub.sum(axis=1)
    bands, start = [], None
    for i, v in enumerate(rows):
        if v > 4 and start is None: start = i
        elif v <= 4 and start is not None:
            if i - start >= 3: bands.append((400 + start, 400 + i))
            start = None
    print(f"  {nm}: {bands}")

# focus on the lowest two text bands (the two bottom labels)
def bottom_labels(dark):
    sub = dark[400:527, 83:376]
    rows = sub.sum(axis=1)
    bands, start = [], None
    for i, v in enumerate(rows):
        if v > 4 and start is None: start = i
        elif v <= 4 and start is not None:
            if i - start >= 3: bands.append((400 + start, 400 + i))
            start = None
    return bands[-2:] if len(bands) >= 2 else bands

def ncc(a, b):
    H = max(a.shape[0], b.shape[0]); W = max(a.shape[1], b.shape[1])
    A = np.zeros((H, W)); B = np.zeros((H, W))
    A[:a.shape[0], :a.shape[1]] = a; B[:b.shape[0], :b.shape[1]] = b
    A = A - A.mean(); B = B - B.mean()
    d = np.sqrt((A * A).sum()) * np.sqrt((B * B).sum())
    return float((A * B).sum() / d) if d else 0.0

rb = bottom_labels(rdark); ob = bottom_labels(odark)
print("render bottom bands:", rb, " orig bottom bands:", ob)

def band_img(dark, y0, y1):
    return dark[y0:y1, 83:376]

if len(rb) == 2 and len(ob) == 2:
    # split each band into left/right half by x mid of panel
    for bi in range(2):
        ry0, ry1 = rb[bi]; oy0, oy1 = ob[bi]
        Rb = band_img(rdark, ry0, ry1); Ob = band_img(odark, oy0, oy1)
        # render left label vs orig left label / orig right label
        rl = Rb[:, :147]; rr = Rb[:, 147:]
        ol = Ob[:, :147]; orr = Ob[:, 147:]
        print(f"band{bi}: NCC(render-left, orig-left)={ncc(rl, ol):.3f}  NCC(render-left, orig-right)={ncc(rl, orr):.3f}  "
              f"NCC(render-right, orig-right)={ncc(rr, orr):.3f}  NCC(render-right, orig-left)={ncc(rr, ol):.3f}")
        # ink widths of each label in each image
        for nm, img in (("render", Rb), ("orig", Ob)):
            l = img[:, :147]; rr2 = img[:, 147:]
            lx = np.where(l.sum(axis=0) > 0)[0]; rx = np.where(rr2.sum(axis=0) > 0)[0]
            lw = (lx.max() - lx.min() + 1) if len(lx) else 0
            rw = (rx.max() - rx.min() + 1) if len(rx) else 0
            li = int(l.sum()); ri = int(rr2.sum())
            print(f"   {nm} band{bi}: left label x-width={lw} ink={li} | right label x-width={rw} ink={ri}")
