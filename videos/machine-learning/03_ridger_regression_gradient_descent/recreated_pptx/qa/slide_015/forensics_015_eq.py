#!/usr/bin/env python3
r"""Banked forensics for slide 015 equation bands (deck 03, 2026-10-23).

Measures from unique_slides/slide_015.jpg (960x540, 1px=1pt=1/72in):
row bands of dark/coloured ink, per-band column extents, colour classification
(black / red C00000 / blue / green / other) and horizontal underline-bar runs,
so each equation line can be rendered as its own mathtext PNG and placed at its
measured ink bbox (fleet pattern: render_eq.py -> 600dpi PNG -> addImage).

Usage: python3 forensics_015_eq.py [--bands a,b c,d ...]
"""
import sys
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg"

# ink = anything clearly darker/more saturated than the panel (E9E9E7=233, 233, 231)
LUM_THR = 190
# panel stroke columns excluded from band profiling
EXCL_COLS = [(50, 66), (892, 910)]


def load():
    im = Image.open(ORIG).convert("RGB")
    return np.asarray(im).astype(int)


def ink_mask(rgb):
    lum = rgb.mean(axis=2)
    return lum < LUM_THR


def clean_cols(m):
    for a, b in EXCL_COLS:
        m[:, a:b] = False
    return m


def bands(m, min_rows=2):
    rows = np.where(m.sum(axis=1) > 0)[0]
    out, start, prev = [], None, None
    for r in rows:
        if start is None:
            start = prev = r
            continue
        if r - prev > 1:
            if prev - start + 1 >= min_rows:
                out.append((int(start), int(prev)))
            start = r
        prev = r
    if start is not None and prev - start + 1 >= min_rows:
        out.append((int(start), int(prev)))
    return out


def classify(rgb, m):
    """Return (counts per class, per-class column groups) for a mask region."""
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    red = (r > 110) & (r - g > 45) & (r - b > 45)
    blue = (b > 90) & (b - r > 40)
    green = (g > 90) & (g - r > 40) & (g - b > 25)
    other = m & ~red & ~blue & ~green
    return {"red": red, "blue": blue, "green": green, "other": other}


def colgroups(m):
    cols = np.where(m.sum(axis=0) > 0)[0]
    groups, prev = [], None
    for c in cols:
        if prev is None or c - prev > 2:
            groups.append([int(c), int(c)])
        else:
            groups[-1][1] = int(c)
        prev = c
    return groups


def underline_runs(m, min_len=6):
    """Long horizontal runs (>=min_len px) = underline bars / fraction bars."""
    runs = []
    for y in range(m.shape[0]):
        row = m[y]
        cols = np.where(row)[0]
        if len(cols) == 0:
            continue
        s = p = cols[0]
        for c in cols[1:]:
            if c - p > 1:
                if p - s + 1 >= min_len:
                    runs.append((int(y), int(s), int(p)))
                s = c
            p = c
        if p - s + 1 >= min_len:
            runs.append((int(y), int(s), int(p)))
    # merge overlapping run sets on the same row
    out = []
    for y, s, e in runs:
        if out and out[-1][0] == y and s <= out[-1][2] + 2:
            out[-1][2] = max(out[-1][2], e)
        else:
            out.append([y, s, e])
    return [tuple(r) for r in out]


def report(y0, y1, tag):
    rgb = load()
    m = clean_cols(ink_mask(rgb))
    sub = m[y0:y1 + 1]
    cols = np.where(sub.sum(axis=0) > 0)[0]
    print(f"\n=== {tag}  rows {y0}..{y1}")
    if len(cols) == 0:
        print("   NO INK")
        return
    print(f"   ink x {cols.min()}..{cols.max()}  (w {cols.max()-cols.min()+1})")
    cls = classify(rgb[y0:y1 + 1], sub)
    for name, cm in cls.items():
        cnt = int((cm & sub).sum())
        if cnt == 0:
            continue
        cc = np.where((cm & sub).sum(axis=0) > 0)[0]
        print(f"   {name:6s} {cnt:6d}px  x {cc.min()}..{cc.max()}  groups={colgroups(cm & sub)}")
    print(f"   underline/long-bar runs: {underline_runs(sub)}")
    # per-row density to expose stacked-fraction structure
    dens = sub.sum(axis=1)
    print("   row density:", " ".join(f"{y0+i}:{int(d)}" for i, d in enumerate(dens) if d > 0))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--bands":
        for spec in args[1:]:
            a, b = spec.split(",")
            report(int(a), int(b), f"band {a}..{b}")
    else:
        # default: full-slide band scan
        rgb = load()
        m = clean_cols(ink_mask(rgb))
        for y0, y1 in bands(m):
            xcols = np.where(m[y0:y1 + 1].sum(axis=0) > 0)[0]
            print(f"rows {y0:3d}..{y1:3d}  x {xcols.min():3d}..{xcols.max():3d}  "
                  f"inkpx {int(m[y0:y1+1].sum())}")
