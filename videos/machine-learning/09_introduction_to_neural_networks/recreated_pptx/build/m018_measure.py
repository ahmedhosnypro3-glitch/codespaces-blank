#!/usr/bin/env python3
"""Numeric region measurement for slide 018 (original frame vs render)."""
import sys
import numpy as np
from PIL import Image


def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(int)


def masks(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return {
        "red": (R > 140) & (R - G > 50) & (R - B > 50),
        "yellow": (R > 235) & (G > 225) & (B > 200) & (B < 250),
        "blue": (B > 120) & (B - R > 45) & (B - G > 25),
        "green": (G > 90) & (G - R > 25) & (G - B > 25),
        "black": (R < 70) & (G < 70) & (B < 70),
        "graybg": (abs(R - 232) < 10) & (abs(G - 232) < 10) & (abs(B - 232) < 10),
    }


def long_runs(mask, axis):
    """Find maximal runs of True along an axis; return (start,end) in the other axis."""
    out = []
    n = mask.shape[0] if axis == 0 else mask.shape[1]
    for i in range(n):
        line = mask[i, :] if axis == 0 else mask[:, i]
        if not line.any():
            continue
        idx = np.where(line)[0]
        # split into contiguous groups
        grp = []
        s = idx[0]
        p = idx[0]
        for v in idx[1:]:
            if v != p + 1:
                grp.append((s, p))
                s = v
            p = v
        grp.append((s, p))
        for g in grp:
            if g[1] - g[0] >= 20:
                out.append((i, g[0], g[1]))
    return out


def bbox(m):
    ys, xs = np.where(m)
    if len(ys) == 0:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def report(path):
    a = load(path)
    H, W, _ = a.shape
    M = masks(a)
    print(f"=== {path}  {W}x{H} ===")

    # frame: long horizontal red runs
    hred = [r for r in long_runs(M["red"], axis=0) if r[2] - r[1] > 0.6 * W]
    vred = [r for r in long_runs(M["red"], axis=1) if r[2] - r[1] > 0.6 * H]
    print("red horizontal runs (y, x0, x1):", hred[:6])
    print("red vertical runs   (x, y0, y1):", vred[:6])

    # black strip
    bb = bbox(M["black"])
    print("black bbox:", bb)
    rows = np.where(M["black"].sum(axis=1) > 0.7 * W)[0]
    print("black full-width rows:", (int(rows.min()), int(rows.max())) if len(rows) else None)

    # yellow filled cards: rows where yellow count is large
    ycount = M["yellow"].sum(axis=1)
    for y in range(H):
        pass
    bands = []
    ys = np.where(ycount > 40)[0]
    if len(ys):
        s = ys[0]
        p = ys[0]
        for v in ys[1:]:
            if v != p + 1:
                bands.append((s, p))
                s = v
            p = v
        bands.append((s, p))
    for b in bands:
        sub = M["yellow"][b[0]:b[1] + 1]
        xs = np.where(sub.any(axis=0))[0]
        # split x into groups
        grp = []
        st = xs[0]
        pr = xs[0]
        for v in xs[1:]:
            if v != pr + 1:
                grp.append((st, pr))
                st = v
            pr = v
        grp.append((st, pr))
        print(f"yellow band y={b} xgroups={grp}")

    # blue frame lines (chart pane borders)
    hblue = [r for r in long_runs(M["blue"], axis=0) if r[2] - r[1] > 120]
    vblue = [r for r in long_runs(M["blue"], axis=1) if r[2] - r[1] > 100]
    print("blue horizontal runs:", hblue[:14])
    print("blue vertical runs  :", vblue[:14])

    # green / red curve colors
    print("green bbox:", bbox(M["green"]))
    print("red bbox :", bbox(M["red"]))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        report(p)
