#!/usr/bin/env python3
"""Region-A top-table paren measurement, all 6 pairs, orig frame vs current render.

Founder defect: font-paren txt() calls render bold deep-bow black parens vs the
original's thin light small-bow strokes. This banks per-pair bow / tip / span /
stroke-gray numbers to set the replacement Bezier class constants.

Frame coords: orig 960x540 (1px=1pt). render_13 2001x1125 -> scale 2.0844x/2.0833y.
"""
import numpy as np
from PIL import Image

NS = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{NS}/unique_slides/slide_049.jpg"
REND = f"{NS}/recreated_pptx/qa/slide049/render_13.png"

colL = [90, 111, 133, 156, 179, 201]
colR = [102, 125, 147, 170, 193, 215]

Y0, Y1 = 70, 115          # row scan band (frame coords)
THR = 215                 # ink threshold on luminance

def lum(a):
    return a[..., :3].mean(axis=-1)

def measure(img, scale_x, scale_y, side, cx, i):
    """leftmost (side='lp') or rightmost (side='rp') ink x per row, window around cx."""
    sx0 = int((cx - 7) * scale_x); sx1 = int((cx + 7) * scale_x)
    rows = []
    for yf in range(Y0, Y1):
        yr = int(round(yf * scale_y))
        band = lum(img[yr, sx0:sx1])
        ink = np.nonzero(band < THR)[0]
        if len(ink) == 0:
            continue
        x = sx0 + (ink.min() if side == "lp" else ink.max())
        rows.append((yf, x / scale_x, band.min() if side == "lp" else band.max()))
    if not rows:
        return None
    xs = np.array([r[1] for r in rows])
    if side == "lp":
        bow_x, tip_x = xs.min(), xs.max()
    else:
        bow_x, tip_x = xs.max(), xs.min()
    bow_rows = [r[0] for r in rows if abs(r[1] - bow_x) <= 0.6]
    top_row, bot_row = rows[0][0], rows[-1][0]
    # stroke darkness at the bow: min/mean luminance of ink pixels at bow band
    bx0 = int(bow_x * scale_x) - 1; bx1 = int(bow_x * scale_x) + 2
    mids = [int(round((yf) * scale_y)) for yf in bow_rows]
    vals = []
    for yr in mids:
        seg = lum(img[yr, bx0:bx1 + 1])
        vals.extend(seg[seg < THR].tolist())
    return dict(pair=i, tip_x=round(tip_x, 1), bow_x=round(bow_x, 1),
                bow=round(abs(tip_x - bow_x), 1), top=top_row, bot=bot_row,
                h=bot_row - top_row + 1, n_bow_rows=len(bow_rows),
                gray_min=round(min(vals), 1) if vals else None,
                gray_mean=round(sum(vals) / len(vals), 1) if vals else None)

for tag, path, sx, sy in (("ORIG", ORIG, 1.0, 1.0),
                          ("RENDER_13", REND, 2001 / 960, 1125 / 540)):
    img = np.array(Image.open(path).convert("RGB"))
    print(f"== {tag}  ({path.split('/')[-1]})")
    for i in range(6):
        lp = measure(img, sx, sy, "lp", colL[i], i)
        rp = measure(img, sx, sy, "rp", colR[i], i)
        for side, m in (("lp", lp), ("rp", rp)):
            if m is None:
                print(f"  {side}{i+1}: NO INK")
            else:
                print(f"  {side}{i+1}: tip_x={m['tip_x']:6} bow_x={m['bow_x']:6} "
                      f"bow={m['bow']:4} rows {m['top']}..{m['bot']} h={m['h']:2} "
                      f"bow_rows={m['n_bow_rows']:2} gray min={m['gray_min']} mean={m['gray_mean']}")
