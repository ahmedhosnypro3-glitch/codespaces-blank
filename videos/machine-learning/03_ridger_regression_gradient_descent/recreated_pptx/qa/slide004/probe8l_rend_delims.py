#!/usr/bin/env python3
"""Probe 8l: REND delimiter strokes at FRAME coordinates (scale render coords by S=W/960)."""
from PIL import Image
import numpy as np

REND = np.asarray(Image.open("recreated_pptx/qa/slide004/render_8.png").convert("RGB")).astype(int)
S = REND.shape[1] / 960.0

def runs_in_row(row_mask, x0):
    out, in_run = [], False
    for i, v in enumerate(row_mask):
        if v and not in_run:
            start = i; in_run = True
        elif not v and in_run:
            out.append((x0 + start, x0 + i - 1)); in_run = False
    if in_run:
        out.append((x0 + start, x0 + len(row_mask) - 1))
    return out

for label, fx0, fx1 in [("REND left box", 140, 215), ("REND right box", 465, 555)]:
    rx0, rx1 = int(fx0 * S), int(fx1 * S)
    ry0, ry1 = int(95 * S), int(220 * S)
    print(f"===== {label} frame x{fx0}..{fx1} y95..220 (raw x{rx0}..{rx1}) =====")
    reg = REND[ry0:ry1, rx0:rx1]
    ink = reg.min(axis=2) < 215
    colsum = ink.sum(axis=0)
    # report columns with ink, grouped, in FRAME coords
    cols = [fx0 + i / S for i in range(len(colsum)) if colsum[i] >= 20]
    print(f"columns (frame) with >=20 ink raw-rows: {[round(c,1) for c in cols]}")
    for fy in range(95, 220, 4):
        ry = int(fy * S) - ry0
        if ry < 0 or ry >= reg.shape[0]:
            continue
        rr = runs_in_row(ink[ry], fx0)
        if not rr:
            continue
        parts = []
        for (a, b) in rr:
            ra, rb = int(a * S) - rx0, int(b * S + S) - rx0
            seg = REND[ry0 + ry, max(0, ra):rb + 1]
            m = seg.mean(axis=0).astype(int)
            parts.append(f"x{a}..{b} rgb({m[0]},{m[1]},{m[2]})")
        print(f"  y{fy:3d}: " + "  |  ".join(parts))
    print()
