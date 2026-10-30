#!/usr/bin/env python3
"""Precise trajectory adjudication — slide 028.

Builds ASCII maps of curve/dot ink in each panel for original vs render, using
tight color masks that exclude the house chrome and the badge's purple ring.
"""
import numpy as np
from collections import Counter
from PIL import Image

ORIG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'
QA = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028/render_3.png'

o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
r = np.asarray(Image.open(QA).convert('RGB')).astype(int)
S = r.shape[0] / 540.0

def blue_tight(a):
    rr, gg, bb = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (np.abs(rr - 46) < 45) & (np.abs(gg - 117) < 45) & (np.abs(bb - 182) < 45)

def red_tight(a):
    rr, gg, bb = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (rr > 150) & (gg < 110) & (bb < 110)

def ascii_map(mask, x0, x1, y0, y1, cols=76, rows=32, sx=1.0):
    """Coarse occupancy map of a slide-space region."""
    h, w = mask.shape
    out = []
    for ry in range(rows):
        row = []
        ysl = slice(int((y0 + (y1 - y0) * ry / rows) * sx), int((y0 + (y1 - y0) * (ry + 1) / rows) * sx))
        for rx in range(cols):
            xsl = slice(int((x0 + (x1 - x0) * rx / cols) * sx), int((x0 + (x1 - x0) * (rx + 1) / cols) * sx))
            row.append('#' if mask[ysl, xsl].any() else '.')
        out.append(''.join(row))
    return out

print("=" * 78)
print("LEFT PANEL  x90..474  y180..470   (blue curve + dots)")
print("=" * 78)
bo = blue_tight(o); bo[:, :90] = False; bo[:, 474:] = False
br = blue_tight(r)
br[:, :int(90 * S)] = False; br[:, int(474 * S):] = False
print("\nORIG (960x540):")
for ln in ascii_map(bo, 90, 474, 180, 470):
    print("  " + ln)
print("\nREND (150dpi):")
for ln in ascii_map(br, 90, 474, 180, 470, sx=S):
    print("  " + ln)

print()
print("=" * 78)
print("RIGHT PANEL  x478..858  y180..470   (blue curve + dots)")
print("=" * 78)
bo = blue_tight(o); bo[:, :478] = False; bo[:, 858:] = False
br = blue_tight(r); br[:, :int(478 * S)] = False; br[:, int(858 * S):] = False
print("\nORIG:")
for ln in ascii_map(bo, 478, 858, 180, 470):
    print("  " + ln)
print("\nREND:")
for ln in ascii_map(br, 478, 858, 180, 470, sx=S):
    print("  " + ln)

# ---- red ink: arrowheads + title only ----
print()
print("=" * 78)
print("RED INK (title, arrowheads, house strokes)")
print("=" * 78)
ro = red_tight(o); rr_ = red_tight(r)
# exclude house vertical strokes x<95 / x>886 and bottom y>533
for nm, m, sc in [('ORIG', ro, 1.0), ('REND', rr_, S)]:
    mm = m.copy()
    mm[:, :int(95 * sc)] = False
    mm[:, int(886 * sc):] = False
    mm[int(533 * sc):, :] = False
    ys, xs = np.where(mm)
    if not len(ys):
        print(f"{nm}: no red ink outside chrome"); continue
    print(f"{nm}: red px={len(ys)} bbox x{xs.min()/sc:.0f}-{xs.max()/sc:.0f} y{ys.min()/sc:.0f}-{ys.max()/sc:.0f}")
    rowsum = mm.sum(axis=1)
    print("   rows with >=4 red px:", [(round(y / sc), rowsum[y]) for y in np.where(rowsum >= 4)[0]])
    colsum = mm.sum(axis=0)
    print("   cols with >=4 red px:", [(round(x / sc), colsum[x]) for x in np.where(colsum >= 4)[0]])
