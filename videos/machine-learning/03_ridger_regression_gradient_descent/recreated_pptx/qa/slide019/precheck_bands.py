#!/usr/bin/env python3
"""PIL pre-adjudication: per-row ink profile in the render vs the original,
per content column. Used to find wrapping / spacing deviations BEFORE the judge.
"""
import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
Q = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019"
ORIG = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"

R = np.asarray(Image.open(Q + "/render_3.png").convert("RGB")).astype(int)
O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
SC = R.shape[0] / 540.0


def ink(row):
    rr, gg, bb = row[:, 0], row[:, 1], row[:, 2]
    gray = (abs(rr - 233) < 16) & (abs(gg - 233) < 16) & (abs(bb - 231) < 18)
    near_white = (rr > 235) & (gg > 235) & (bb > 235)
    return ~(gray | near_white)


def row_ink(img, y, x0, x1, scale=1.0):
    yy = int((y + 0.5) * scale)
    xa, xb = int(x0 * scale), int(x1 * scale)
    return int(ink(img[yy, xa:xb]).sum())


def band(rows, thr=3, gap=4):
    """Group rows into contiguous text bands."""
    out = []
    cur = None
    for y, n in rows:
        if n > thr:
            if cur is None:
                cur = [y, y]
            elif y - cur[1] <= gap:
                cur[1] = y
            else:
                out.append(tuple(cur))
                cur = [y, y]
        elif cur is not None and y - cur[1] > gap:
            out.append(tuple(cur))
            cur = None
    if cur is not None:
        out.append(tuple(cur))
    return out


REGIONS = [
    ("NO REG  x124..380", 124, 380, 200, 380),
    ("RIDGE3  x384..640", 384, 640, 300, 390),
    ("RIDGE10 x644..900", 644, 900, 400, 480),
    ("OUTLIER x57..124", 57, 124, 165, 530),
]

for name, x0, x1, y0, y1 in REGIONS:
    print("=" * 70)
    print(name, f"y{y0}..{y1}")
    ro = [(y, row_ink(O, y, x0, x1)) for y in range(y0, y1)]
    rr = [(y, row_ink(R, y, x0, x1, SC)) for y in range(y0, y1)]
    bo, br = band(ro), band(rr)
    print("  ORIG bands   :", bo)
    print("  RENDER bands :", br)
    print("  band counts  : orig", len(bo), "render", len(br))
