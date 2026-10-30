#!/usr/bin/env python3
"""ATTEMPT-8 MEASUREMENT PART 3 — LO subscript calibration only.

slide003 build used SAME-SIZE runs (11pt/15pt) with subscript:true for the
vector entries. If the certified render_33 shows the subscript digit clearly
smaller than the main glyph, LibreOffice auto-shrinks baseline runs and the
same pattern reproduces 004's measured main-h~10px / sub-h~7-9px ratio.
"""
from PIL import Image
import numpy as np

BASE = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
r33 = np.asarray(Image.open(f"{BASE}/recreated_pptx/qa/slide003/render_33.png").convert("RGB")).astype(int)
o33 = np.asarray(Image.open(f"{BASE}/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
SX, SY = 2001 / 960, 1125 / 540


def bands(m, gap=2, run=1):
    idx = np.where(m)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v - p > gap:
            if p - s + 1 >= run:
                out.append((int(s), int(p)))
            s = v
        p = v
    if p - s + 1 >= run:
        out.append((int(s), int(p)))
    return out


def probe(tag, img, fx0, fx1, fy0, fy1, sx, sy):
    reg = img[int(fy0 * sy):int(fy1 * sy), int(fx0 * sx):int(fx1 * sx)]
    dk = (reg[..., 0] + reg[..., 1] + reg[..., 2]) < 430
    print(f"-- {tag} frame x{fx0}..{fx1} y{fy0}..{fy1}")
    for s, e in bands(dk.any(axis=1), gap=4):
        seg = dk[s:e + 1]
        parts = []
        for c0, c1 in bands(seg.any(axis=0), gap=2):
            sub = seg[:, c0:c1 + 1]
            rr = np.where(sub.any(axis=1))[0]
            parts.append(f"x{fx0 + int(round(c0 / sx))}..{fx0 + int(round(c1 / sx))} "
                         f"h{(rr.max() - rr.min() + 1) / sy:.1f}")
        print(f"   row y{fy0 + s / sy:.0f}..{fy0 + e / sy:.0f}: " + "  ".join(parts))


# 003 y-vector entries: 'y' 15pt + subscript digit 15pt, rows y368/397/427/456, x109..143
probe("RENDER33 yvec rows1-2", r33, 111, 141, 366, 424, SX, SY)
probe("ORIG003  yvec rows1-2", o33, 111, 141, 366, 424, 1.0, 1.0)
# 003 matrix entries: 'x' 11pt + subscript, first column x~198..230 y368..425
probe("RENDER33 matrix col1", r33, 198, 232, 366, 425, SX, SY)
probe("ORIG003  matrix col1", o33, 198, 232, 366, 425, 1.0, 1.0)
