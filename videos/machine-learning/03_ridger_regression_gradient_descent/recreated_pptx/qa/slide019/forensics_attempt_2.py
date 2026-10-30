#!/usr/bin/env python3
"""PIL forensics for slide 019 attempt 2.

Part 1: prove banked render_1.png is not a faithful render of
slide_019_recreated.pptx (same-PPTX determinism + fresh-render diff + chrome
check), so attempt 2 was re-rendered and banked as render_2.png.
Part 2: region-by-region ink-geometry comparison of render_2.png vs the
original frame, before spending any vision call.
"""
import subprocess
import sys

import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
Q = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019"
ORIG = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"

SCALE = 150 / 72.0  # render px per frame px


def to_frame(render):
    """Sample a 150dpi render down to 960x540 frame space."""
    ys = (np.arange(540) + 0.5) * SCALE
    xs = (np.arange(960) + 0.5) * SCALE
    return render[np.ix_(ys.astype(int), xs.astype(int))].astype(int)


def ink_mask(a):
    """Non-panel, non-canvas ink, tolerant of the original's JPEG noise."""
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
    near_white = (r > 235) & (g > 235) & (b > 235)
    return ~(gray | near_white)


def runs(flags, minlen=1):
    idx = np.where(flags)[0]
    out = []
    if not len(idx):
        return out
    s = prev = idx[0]
    for i in idx[1:]:
        if i != prev + 1:
            if prev - s + 1 >= minlen:
                out.append((int(s), int(prev)))
            s = i
        prev = i
    if prev - s + 1 >= minlen:
        out.append((int(s), int(prev)))
    return out


def col_extent(mask, y0, y1, x0, x1):
    """Contiguous ink column runs inside a region."""
    cols = mask[y0:y1, x0:x1].sum(axis=0) > 0
    return [(a + x0, b + x0) for a, b in runs(cols)]


def bbox(mask, y0, y1, x0, x1):
    sub = mask[y0:y1, x0:x1]
    if not sub.any():
        return None
    ys, xs = np.where(sub)
    return (int(ys.min() + y0), int(ys.max() + y0), int(xs.min() + x0), int(xs.max() + x0))


print("=" * 78)
print("PART 1 — render provenance")
print("=" * 78)
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
render = np.asarray(Image.open(Q + "/render_2.png").convert("RGB")).astype(int)
banked = np.asarray(Image.open(Q + "/render_1.png").convert("RGB")).astype(int)
d = np.abs(render - banked).sum(axis=2)
print(f"fresh render vs banked render_1.png: differing px = {int((d > 0).sum())} / {d.size}")
print(f"  diff bbox y {int(np.where(d > 0)[0].min())}..{int(np.where(d > 0)[0].max())} "
      f"x {int(np.where(d > 0)[1].min())}..{int(np.where(d > 0)[1].max())}")
print(f"chrome check render_2.png rc = "
      f"{subprocess.run([sys.executable, ROOT + '/videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/house_chrome_check.py', Q + '/render_2.png', '19'], capture_output=True).returncode}")
print(f"chrome check render_1.png rc = "
      f"{subprocess.run([sys.executable, ROOT + '/videos/machine-learning/03_ridger_regression_gradient_descent/shared_patterns/house_chrome_check.py', Q + '/render_1.png', '19'], capture_output=True).returncode}")

print()
print("=" * 78)
print("PART 2 — region geometry: render_2 vs original (frame px)")
print("=" * 78)
R = to_frame(render)
mo, mr = ink_mask(o), ink_mask(R)

REGIONS = [
    ("title-box",      60, 165,  66, 440),
    ("title-text",     68, 158,  70, 435),
    ("badge",          52,  95, 855, 905),
    ("test-ref-line",  76, 104, 430, 900),
    ("outlier-col",   165, 530,  57, 125),
    ("col-noreg",     165, 530, 122, 382),
    ("col-ridge3",    165, 530, 382, 642),
    ("col-ridge10",   165, 530, 642, 905),
    ("intercol-arrows", 300, 345, 375, 650),
]
for name, y0, y1, x0, x1 in REGIONS:
    bo, br = bbox(mo, y0, y1, x0, x1), bbox(mr, y0, y1, x0, x1)
    def fmt(b):
        return "none" if b is None else f"y{b[0]}-{b[1]} x{b[2]}-{b[3]}"
    print(f"{name:14s} orig[{fmt(bo)}]  render[{fmt(br)}]")

print()
print("row ink profile, main grid (ink px/row, x 63..898):")
print("   y   orig render")
for y in range(165, 535, 5):
    print(f"{y:4d} {int(mo[y, 63:898].sum()):5d} {int(mr[y, 63:898].sum()):5d}")
