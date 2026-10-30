#!/usr/bin/env python3
"""Paren-curve-direction census for the S23 sweep (deck 03).

Finds tall thin ink components (parenthesis-like strokes) in a slide image
(render 2001x1125 or original 960x540) and measures each stroke's belly
direction: mid-row weighted ink centroid vs top/bottom-tip weighted centroid.

  delta = belly_x - tips_x
  delta < -T  -> "("   (belly left, opening right)
  delta > +T  -> ")"   (belly right, opening left)
  |delta| <= T -> straight / ambiguous (brackets, digits, ties)

Usage:
  scan_dir_render.py IMG [--thresh N] [--min-h N] [--max-frac F] [--json OUT]
"""
import argparse
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage


def load_ink(path, thresh):
    im = Image.open(path).convert("L")
    a = np.asarray(im, dtype=np.float64)
    ink = np.clip(thresh - a, 0, None)  # weight = how far below threshold
    return ink


def stroke_census(ink, min_h, max_frac):
    mask = ink > 0
    lab, n = ndimage.label(mask, structure=np.ones((3, 3), dtype=int))
    out = []
    H, W = mask.shape
    for sl in ndimage.find_objects(lab):
        if sl is None:
            continue
        y0, y1 = sl[0].start, sl[0].stop
        x0, x1 = sl[1].start, sl[1].stop
        h, w = y1 - y0, x1 - x0
        if h < min_h:
            continue
        if h < 3 or w < 2:
            continue
        if w > max_frac * h:
            continue  # wide blob: letters like C/G/O, circles, boxes
        sub = ink[sl]
        ys, xs = np.nonzero(sub)
        if len(ys) == 0:
            continue
        wts = sub[ys, xs]
        rel_y = ys / h  # 0 top .. 1 bottom
        tips = (rel_y <= 0.18) | (rel_y >= 0.82)
        mid = (rel_y >= 0.35) & (rel_y <= 0.65)
        if tips.sum() < 4 or mid.sum() < 4:
            continue
        tips_x = float((xs[tips] * wts[tips]).sum() / wts[tips].sum())
        belly_x = float((xs[mid] * wts[mid]).sum() / wts[mid].sum())
        # secondary: extreme-x rows — leftmost ink column's row-centroid vs
        # the glyph's row span (a "(" reaches its leftmost at mid-height)
        leftmost_col = xs.min()
        lm_rows = ys[xs == leftmost_col]
        rightmost_col = xs.max()
        rm_rows = ys[xs == rightmost_col]
        lm_frac = float(lm_rows.mean()) / h
        rm_frac = float(rm_rows.mean()) / h
        delta = belly_x - tips_x
        if abs(delta) <= 1.2:
            verdict = "STRAIGHT"
        elif delta < 0:
            verdict = "("
        else:
            verdict = ")"
        out.append({
            "bbox": [x0, y0, x1, y1], "w": int(w), "h": int(h),
            "belly_x": round(belly_x, 2), "tips_x": round(tips_x, 2),
            "delta": round(delta, 2), "verdict": verdict,
            "leftmost_at_ymid_frac": round(lm_frac, 2),
            "rightmost_at_ymid_frac": round(rm_frac, 2),
        })
    out.sort(key=lambda d: (d["bbox"][1], d["bbox"][0]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--thresh", type=int, default=160)
    ap.add_argument("--min-h", type=int, default=18)
    ap.add_argument("--max-frac", type=float, default=0.55)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    ink = load_ink(args.image, args.thresh)
    strokes = stroke_census(ink, args.min_h, args.max_frac)

    print(f"# {args.image} thresh={args.thresh} min_h={args.min_h} "
          f"max_frac={args.max_frac} -> {len(strokes)} tall thin strokes")
    hdr = (f"{'bbox(x0,y0,x1,y1)':>24} {'w':>4} {'h':>4} {'belly':>7} "
           f"{'tips':>7} {'delta':>6} {'verdict':>9} {'lmF':>5} {'rmF':>5}")
    print(hdr)
    for s in strokes:
        b = s["bbox"]
        print(f"({b[0]:>5},{b[1]:>5},{b[2]:>5},{b[3]:>5}) {s['w']:>4} {s['h']:>4} "
              f"{s['belly_x']:>7.2f} {s['tips_x']:>7.2f} {s['delta']:>6.2f} "
              f"{s['verdict']:>9} {s['leftmost_at_ymid_frac']:>5.2f} "
              f"{s['rightmost_at_ymid_frac']:>5.2f}")
    if args.json:
        with open(args.json, "w") as f:
            json.dump(strokes, f, indent=1)
        print(f"# banked {args.json}")


if __name__ == "__main__":
    main()
