#!/usr/bin/env python3
"""Right-side equations: 6 rows. For each, report glyph clusters with colour."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
satred = (rf - gf > 45) & (rf - bf > 45) & (rf > 110)
satblue = (bf - rf > 40) & (bf - gf > 25) & (bf > 110)
ink = (LUM < 178) | satred | satblue

X0, X1 = 272, 856


def runs(mask, gap):
    idx = np.where(mask)[0]
    if not len(idx):
        return []
    out = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i - p <= gap + 1: p = i
        else: out.append((s, p)); s = i; p = i
    out.append((s, p)); return out


def cls(px):
    R, G, B = px
    if B > 110 and B - R > 40 and B - G > 25: return "B"
    if R > 110 and R - G > 45 and R - B > 45: return "R"
    if R < 150 and G < 150 and B < 150: return "k"
    return "?"


def line(y0, y1, label):
    print(f"\n### {label} y{y0}..{y1}")
    band = ink[y0:y1 + 1, X0:X1 + 1]
    cc = band.sum(axis=0)
    cl = []
    for a, b in runs(cc > 0, 1):
        blk = band[:, a:b + 1]
        rgb = IM[y0:y1 + 1, X0:X1 + 1][:, a:b + 1][blk]
        cl.append((X0 + a, X0 + b, Counter(cls(p) for p in rgb).most_common(1)[0][0]))
    print("  " + " ".join(f"[{a}-{b}{c}]" for a, b, c in cl))


line(398, 462, "ROW 5  d(x5)")
line(455, 530, "ROW 6  d(x6)")
