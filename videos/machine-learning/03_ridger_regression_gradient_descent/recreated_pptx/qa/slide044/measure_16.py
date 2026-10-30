#!/usr/bin/env python3
"""Comprehensive geometry: for each region, list text lines with glyph clusters + colour.
Regions:
  A) top blue box  x68..719 y54..130  -> left table (x74..250) + centre text (x250..715)
  B) left-mid blue box x66..237 y136..257
  C) right equations x272..855 y136..330 and y329..534
  D) red Iteration-3 badge
"""
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
satyel = (rf > 200) & (gf > 200) & (bf < 185)
ink = (LUM < 205) | satred | satblue | satyel


def runs(cnt, thr, gap=0):
    out = []; i = 0; n = len(cnt)
    while i < n:
        if cnt[i] > thr:
            a = i; last = i; j = i + 1
            while j < n:
                if cnt[j] > thr: last = j; j += 1
                elif all(cnt[k] <= thr for k in range(j, min(j + gap + 1, n))): break
                else: j += 1
            out.append((a, last)); i = last + 1
        else: i += 1
    return out


def cls(px):
    R, G, B = px
    if R > 200 and G > 200 and B < 185: return "YEL"
    if B > 110 and B - R > 40 and B - G > 25: return "BLUE"
    if R > 110 and R - G > 45 and R - B > 45: return "RED"
    if R < 150 and G < 150 and B < 150: return "blk"
    return "?"


def scan(x0, x1, y0, y1, label, lthr=3, gmax=0):
    print(f"\n### {label}   x{x0}..{x1} y{y0}..{y1}")
    sub = ink[y0:y1 + 1, x0:x1 + 1]
    rc = sub.sum(axis=1)
    for ly0, ly1 in runs(rc, lthr, 0):
        band = ink[ly0:ly1 + 1, x0:x1 + 1]
        cc = band.sum(axis=0)
        cl = []
        for a, bb in runs(cc, 1, gmax):
            if bb - a < 2: continue
            blk = band[:, a:bb + 1]
            rgb = IM[ly0:ly1 + 1, x0:x1 + 1][:, a:bb + 1][blk]
            cl.append((x0 + a, x0 + bb,
                       Counter(cls(p) for p in rgb).most_common(1)[0][0]))
        if cl:
            print(f"  y{ly0 + y0}..{ly1 + y0} h{ly1 - ly0 + 1}: "
                  + " ".join(f"[{a}-{b} {c}]" for a, b, c in cl))


# ---- A) top blue box interior (exclude borders x68-70/x718-720, y54-56/y128-130)
scan(75, 715, 58, 126, "A1 TOP BOX LEFT-COL (table) ", gmax=3)
scan(250, 715, 58, 126, "A2 TOP BOX CENTRE-TEXT", gmax=3)

# ---- B) left-middle blue box interior
scan(75, 232, 140, 254, "B LEFT-MID BOX", gmax=3)

# ---- C) right equations, full height
scan(272, 855, 136, 534, "C RIGHT EQUATIONS", gmax=3)
