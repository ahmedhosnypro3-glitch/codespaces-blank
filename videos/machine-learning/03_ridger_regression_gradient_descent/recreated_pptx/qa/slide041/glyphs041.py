#!/usr/bin/env python3
"""Slide 041: precise per-cell glyph extraction from the original frame.

Ink = deviation from the pale-yellow panel fill. Column groups are taken from
the banked measurements (measurements.json / measurements8.json); each glyph in
each band is dumped as ASCII art with its dominant colour class, so the panel
text can be read verbatim without a vision call.
"""
import numpy as np
from PIL import Image
from collections import deque

IM = Image.open("/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/"
               "machine-learning/03_ridger_regression_gradient_descent/"
               "unique_slides/slide_041.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]
FILL = np.array([255, 247, 224])
D = np.abs(A - FILL[None, None, :]).sum(axis=2)
INK = D > 90


def colour(y0, y1, x0, x1):
    seg = A[y0:y1 + 1, x0:x1 + 1]
    m = INK[y0:y1 + 1, x0:x1 + 1]
    px = seg[m]
    if not len(px):
        return "none"
    red = ((px[:, 0] - px[:, 1] > 60) & (px[:, 0] - px[:, 2] > 60)).sum()
    blue = ((px[:, 2] - px[:, 0] > 60) & (px[:, 2] - px[:, 1] > 30)).sum()
    green = ((px[:, 1] - px[:, 0] > 40) & (px[:, 1] - px[:, 2] > 40)).sum()
    dark = ((px.max(axis=1) - px.min(axis=1) < 60) & (px.mean(axis=1) < 150)).sum()
    navy = ((px[:, 2] - px[:, 0] > 40) & (px[:, 2] - px[:, 1] > 40)
            & (px.max(axis=1) < 190)).sum()
    n = len(px)
    lab = {"r": int(red), "b": int(blue), "g": int(green),
           "d": int(dark), "n": int(navy)}
    best = max((k for k in "rbgd"), key=lambda k: lab[k])
    return "%s (r%d b%d g%d d%d n%d)" % (best, red, blue, green, dark, navy)


def groups(y0, y1, x0, x1, gap=2):
    row = INK[y0:y1 + 1, x0:x1 + 1].any(axis=0)
    out, s = [], None
    for i, v in enumerate(row):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s + x0, i - 1 + x0)); s = None
    if s is not None:
        out.append((s + x0, len(row) - 1 + x0))
    # merge closer than gap
    merged = []
    for g in out:
        if merged and g[0] - merged[-1][1] - 1 <= gap:
            merged[-1] = (merged[-1][0], g[1])
        else:
            merged.append(g)
    return merged


def dump(y0, y1, x0, x1, title):
    print("\n--- %s  x%d..%d y%d..%d ---" % (title, x0, x1, y0, y1))
    print("      " + "".join(str(x % 10) for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        print("y%4d %s" % (y, "".join("#" if INK[y, x] else "." for x in range(x0, x1 + 1))))
    print("     col:", colour(y0, y1, x0, x1))


BANDS = [
    ("header", 63, 74),
    ("subs", 75, 78),
    ("row1", 79, 90),
    ("row2", 95, 106),
    ("labels", 110, 126),
]

print("################ LEFT TABLE (x69..220) ################")
for name, y0, y1 in BANDS:
    gs = groups(y0, y1, 69, 222)
    print("\n=== %s band y%d..%d groups: %s" % (name, y0, y1, gs))
    for i, (a0, a1) in enumerate(gs):
        if (y1 - y0 + 1) >= 3:
            dump(y0, y1, a0, a1, "%s.%d" % (name, i + 1))

print("\n################ MID ZONE (x225..400) ################")
for name, y0, y1 in [("midall", 57, 126)]:
    gs = groups(y0, y1, 225, 400, gap=4)
    print("groups:", gs)
    for i, (a0, a1) in enumerate(gs):
        dump(y0, y1, a0, a1, "%s.%d" % (name, i + 1))

print("\n################ RIGHT ZONE (x430..720) ################")
for name, y0, y1 in [("rall", 57, 126)]:
    gs = groups(y0, y1, 430, 720, gap=4)
    print("groups:", gs)
    for i, (a0, a1) in enumerate(gs):
        dump(y0, y1, a0, a1, "%s.%d" % (name, i + 1))
