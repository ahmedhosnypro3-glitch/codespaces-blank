#!/usr/bin/env python3
"""PIL pre-adjudication aid for rejudge_20261027 FAIL verdicts.

Usage: rejudge_adjudicate.py NNN [--full | --crop]

Prints the strongest pixel-difference regions between the recreation render and
the original frame, in SLIDE-SPACE px (960x540) coordinates, with ink counts —
the objective input for adjudicating a vision-model FAIL claim (the claim may
name a defect; this says where the bytes actually differ).
Never rewrites anything. Read-only.
"""
import sys
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"

SLIDE = sys.argv[1]
MODE = "--crop" if "--crop" in sys.argv else "--full"
OUT = f"{RJ}/slide{SLIDE}"

if MODE == "--full":
    rp = Image.open(f"{OUT}/render.png").convert("RGB")
    op = Image.open(f"{NS}/unique_slides/slide_{SLIDE}.jpg").convert("RGB")
else:
    rp = Image.open(f"{OUT}/crop_dense_render.png").convert("RGB")
    op = Image.open(f"{OUT}/crop_dense_orig.png").convert("RGB")

if rp.size != op.size:
    op = op.resize(rp.size, Image.LANCZOS)
r = np.asarray(rp).astype(int)
o = np.asarray(op).astype(int)
H, W = r.shape[:2]
sx, sy = W / 960.0, H / 540.0
print(f"slide {SLIDE} mode {MODE} render {W}x{H} scale=({sx:.3f},{sy:.3f})")

d = np.abs(r - o).sum(axis=2)
mask = d > 90
print(f"diff px total: {int(mask.sum())} ({100.0 * mask.sum() / (W * H):.3f}% of frame)")

# coarse 40x24 grid of diff density; report the densest cells
gy, gx = 24, 40
cell = np.zeros((gy, gx), int)
for i in range(gy):
    for j in range(gx):
        y0, y1 = int(i * H / gy), int((i + 1) * H / gy)
        x0, x1 = int(j * W / gx), int((j + 1) * W / gx)
        cell[i, j] = mask[y0:y1, x0:x1].sum()
flat = [(cell[i, j], i, j) for i in range(gy) for j in range(gx)]
flat.sort(reverse=True)
print("densest diff cells (slide-space px coords, diff px count):")
for c, i, j in flat[:12]:
    if c < 60:
        break
    x0p, y0p = int(j * 960 / gx), int(i * 540 / gy)
    x1p, y1p = int((j + 1) * 960 / gx), int((i + 1) * 540 / gy)
    print(f"  box x{x0p}-{x1p} y{y0p}-{y1p}: {c} diff px")

# ink-mass comparison per cell: where does one image have ink the other lacks?
def ink(a):
    return (a.sum(axis=2) < 600)

r_only = int((ink(r) & ~ink(o)).sum())
o_only = int((ink(o) & ~ink(r)).sum())
print(f"ink only in render: {r_only} px; ink only in original: {o_only} px")
if r_only + o_only > 0:
    print("  (render-heavy = extra/off-position ink; original-heavy = missing content)")
