#!/usr/bin/env python3
"""Slide 041: extract every parenthesized column group and its digit glyphs.

The panel's math is rendered as a chain of small parenthesised 2-row column
vectors (points), so each paren pair is one point (x above, y below).
Dumps each pair's interior glyphs as ASCII art plus the box geometry, so the
values can be transcribed verbatim.
"""
import numpy as np
from PIL import Image

IM = Image.open("/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/"
               "machine-learning/03_ridger_regression_gradient_descent/"
               "unique_slides/slide_041.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]
FILL = np.array([255, 247, 224])
INK = np.abs(A - FILL[None, None, :]).sum(axis=2) > 90

# tall vertical strokes = parentheses (span both digit rows, thin, curved)
LEFT_Y0, LEFT_Y1 = 76, 108
RIGHT_Y0, RIGHT_Y1 = 60, 112


def parens(y0, y1, x0, x1):
    out = []
    for x in range(x0, x1 + 1):
        col = INK[y0:y1 + 1, x]
        if col.sum() < 15:
            continue
        ys = np.where(col)[0] + y0
        runs, s = [], ys[0]
        for i in range(1, len(ys)):
            if ys[i] != ys[i - 1] + 1:
                runs.append((s, ys[i - 1])); s = ys[i]
        runs.append((s, ys[-1]))
        # a paren spans ~the full band or has far-apart tip runs
        span = ys.max() - ys.min() + 1
        if span >= 26 and len(runs) <= 3 and col.sum() >= 15:
            out.append((x, ys.min(), ys.max(), span, runs))
    # group adjacent columns of the same paren
    groups = []
    for p in out:
        if groups and p[0] - groups[-1][-1][0] <= 1:
            groups[-1].append(p)
        else:
            groups.append([p])
    return [(g[0][0], g[-1][0], min(q[1] for q in g), max(q[2] for q in g)) for g in groups]


def glyph_rows(y0, y1, x0, x1):
    """split interior into digit rows by the horizontal ink profile"""
    m = INK[y0:y1 + 1, x0:x1 + 1]
    prof = m.sum(axis=1)
    bands, s = [], None
    for i, v in enumerate(prof):
        if v and s is None:
            s = i
        elif not v and s is not None:
            bands.append((s + y0, i - 1 + y0)); s = None
    if s is not None:
        bands.append((s + y0, y1))
    return [b for b in bands if b[1] - b[0] >= 5]


def dump(y0, y1, x0, x1, tag):
    print("   %-12s x%d..%d y%d..%d" % (tag, x0, x1, y0, y1))
    step = 1
    for y in range(y0, y1 + 1):
        print("     y%4d %s" % (y, "".join("#" if INK[y, x] else "." for x in range(x0, x1 + 1))))


def run(zone, y0, y1, x0, x1, label):
    print("\n############ %s ############" % label)
    ps = parens(y0, y1, x0, x1)
    print("paren groups (x0,x1,ytop,ybot):", ps)
    # pair them up: consecutive pairs
    for i in range(0, len(ps) - 1, 2):
        L, Rt = ps[i], ps[i + 1]
        ix0, ix1 = L[1] + 1, Rt[0] - 1
        rows = glyph_rows(y0, y1, ix0, ix1)
        print("\n== point #%d: parens x%d..%d / x%d..%d  (top y%d bot y%d), interior x%d..%d"
              % (i // 2 + 1, L[0], L[1], Rt[0], Rt[1], L[2], L[3], ix0, ix1))
        print("   digit bands:", rows)
        for (a0, a1) in rows:
            dump(a0, a1, ix0, ix1, "digit")


run("left", LEFT_Y0, LEFT_Y1, 85, 220, "LEFT TABLE POINTS")
run("right", RIGHT_Y0, RIGHT_Y1, 594, 660, "RIGHT ZONE POINTS")

print("\n############ LEFT TABLE HEADERS + CLASS LABELS ############")
print("header x-groups (y63..74):")
for x0, x1 in [(91, 101), (114, 123), (135, 146), (158, 168), (181, 191), (204, 214)]:
    print("  x%d..%d" % (x0, x1))
print("label x-groups (y110..126) with dominant colour:")
for x0, x1 in [(90, 102), (113, 124), (134, 146), (157, 169), (180, 192), (203, 214)]:
    seg = A[110:127, x0:x1 + 1]
    m = INK[110:127, x0:x1 + 1]
    px = seg[m]
    if len(px):
        red = int(((px[:, 0] > 150) & (px[:, 1] < 110) & (px[:, 2] < 110)).sum())
        blue = int(((px[:, 2] > 140) & (px[:, 2] - px[:, 0] > 50) & (px[:, 2] - px[:, 1] > 40)).sum())
        navy = int(((px[:, 2] - px[:, 0] > 40) & (px[:, 2] - px[:, 1] > 40) & (px.max(axis=1) < 200)).sum())
        dark = int((px.max(axis=1) - px.min(axis=1) < 70).sum())
        print("  x%d..%d  red=%d blue=%d navy=%d dark=%d  sample=%s"
              % (x0, x1, red, blue, navy, dark, px[len(px) // 2].tolist()))
