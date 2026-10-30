#!/usr/bin/env python3
"""Probe 40: red axis ARROWHEAD geometry. Reports the red-ink bbox and per-row
runs at the top of each y-axis and at the right end of each x-axis, plus the
navy chart-panel border bbox and the exact blue fitted-line endpoints.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
RED = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
NAVY = (b > 90) & ((b - r) > 40) & ((b - g) > 30)

def runs_of(vals, gap=2):
    vals = sorted(int(v) for v in vals)
    if not vals: return []
    out, s, p = [], vals[0], vals[0]
    for v in vals[1:]:
        if v <= p + gap: p = v; continue
        out.append((s, p)); s = p = v
    out.append((s, p)); return out

print("=== NAVY chart-panel border bboxes ===")
for nm, x0, x1 in (("LEFT", 90, 470), ("RIGHT", 482, 875)):
    m = NAVY[100:480, x0:x1+1]
    ys, xs = np.nonzero(m)
    print(f"  {nm}: x{x0+xs.min()}..{x0+xs.max()} y{100+ys.min()}..{100+ys.max()} n={int(m.sum())}")
    rh = m.sum(axis=1); ch = m.sum(axis=0)
    print(f"    rows>150: {runs_of(np.where(rh>150)[0]+100)}")
    print(f"    cols>150: {runs_of(np.where(ch>150)[0]+x0)}")

print("\n=== RED axis arrowheads ===")
for nm, x0, x1, yaxis_cols in (("LEFT", 95, 464, (125, 127)), ("RIGHT", 487, 870, (539, 541))):
    print(f"  -- {nm}")
    # y-axis: per-row runs for rows 138..175 (top region)
    for yy in range(138, 165):
        rr = runs_of(np.nonzero(RED[yy, x0:x1+1])[0] + x0)
        if rr: print(f"     y{yy}: " + "  ".join(f"x{p}..{q}" for p, q in rr))
    print(f"     ... x-axis right end, per-col y-runs x{x1-40}..{x1}")
    for xx in range(x1-40, x1+1):
        rr = runs_of(np.nonzero(RED[425:445, xx])[0] + 425, gap=1)
        if rr: print(f"     x{xx}: " + "  ".join(f"y{p}..{q}" for p, q in rr))

print("\n=== BLUE fitted-line exact endpoints ===")
BLU = (b > 120) & ((b - r) > 40) & ((b - g) > 30)
for nm, x0, x1 in (("LEFT", 95, 464), ("RIGHT", 487, 870)):
    m = BLU[195:415, x0:x1+1]   # exclude annotation box band
    ys, xs = np.nonzero(m)
    print(f"  {nm}: x{x0+xs.min()}..{x0+xs.max()} y{195+ys.min()}..{195+ys.max()} n={int(m.sum())}")
    for xx in (x0+xs.min(), (x0+xs.min()+x0+xs.max())//2, x0+xs.max()):
        rr = runs_of(np.nonzero(BLU[195:415, xx])[0] + 195, gap=1)
        if rr: print(f"    x{xx}: " + "  ".join(f"y{p}..{q}" for p, q in rr))
