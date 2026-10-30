#!/usr/bin/env python3
"""ATTEMPT-8 MEASUREMENT PART 4 — sub-baseline offsets + italic slant checks."""
from PIL import Image
import numpy as np

BASE = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
A = np.asarray(Image.open(f"{BASE}/unique_slides/slide_004.jpg").convert("RGB")).astype(int)


def dkmask(a, t=470):
    return (a[..., 0] + a[..., 1] + a[..., 2]) < t


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


def blobs(x0, x1, y0, y1, tag, t=470):
    reg = A[y0:y1, x0:x1]
    m = dkmask(reg, t)
    print(f"-- {tag} x{x0}..{x1} y{y0}..{y1}")
    for s, e in bands(m.any(axis=1), gap=2):
        seg = m[s:e + 1]
        cb = bands(seg.any(axis=0), gap=2)
        for c0, c1 in cb:
            sub = seg[:, c0:c1 + 1]
            rr = np.where(sub.any(axis=1))[0]
            col = tuple(int(v) for v in np.median(reg[s:e + 1, c0:c1 + 1][sub], axis=0)) if sub.any() else None
            print(f"   x{x0+c0}..{x0+c1} y{y0+s+rr.min()}..{y0+s+rr.max()} h{rr.max()-rr.min()+1} {col}")


def slant(x0, x1, y0, y1, tag, t=470):
    reg = A[y0:y1, x0:x1]
    m = dkmask(reg, t)
    ys, xs = np.where(m)
    if len(xs) == 0:
        print(f"-- {tag}: EMPTY")
        return
    top = xs[ys < ys.min() + (ys.max() - ys.min()) / 3].mean()
    bot = xs[ys > ys.max() - (ys.max() - ys.min()) / 3].mean()
    print(f"-- {tag}: top {top:.1f} bottom {bot:.1f} slant {top - bot:+.1f}px ({'italic' if top - bot > 0.8 else 'upright?'})")


# 1. per-blob rows for where-line fragments (t looser to catch full glyphs)
blobs(560, 630, 283, 306, "L1 'X' + sub Nxd+1", 500)
blobs(570, 625, 311, 338, "L2 'Y' + sub Nx1", 500)
blobs(560, 600, 343, 366, "L3 'W'", 500)
blobs(770, 800, 283, 306, "O1 arrow", 500)
blobs(770, 800, 311, 338, "O2 arrow", 500)
blobs(770, 800, 343, 366, "O3 arrow", 500)

# 2. italic slant: h of Where (stem), M of Model, Y lead-ins
slant(521, 531, 285, 304, "'h' of Where")
slant(617, 631, 345, 360, "'M' of Model")
slant(119, 131, 145, 158, "box1 lead-in 'Y'")
slant(465, 475, 145, 164, "box2 lead-in 'Yh'")
# reference italic on this slide: Objective 'Y' (build italic, judge-passed)
slant(148, 162, 260, 285, "Objective 'Y' (ref italic)")
