#!/usr/bin/env python3
"""Closed-loop ground-truth measurement: original frame vs fresh render.

All output is normalized to slide inches (13.333 x 7.5) so the two images
compare directly regardless of raster resolution.
"""
import sys
import numpy as np
from PIL import Image

SW, SH = 13.333, 7.5


def load(path):
    im = Image.open(path).convert("RGB")
    a = np.array(im).astype(int)
    return a, im.size[0], im.size[1]


def inches(box, W, H):
    x0, y0, x1, y1 = box
    return (x0 / W * SW, y0 / H * SH, x1 / W * SW, y1 / H * SH)


def red_mask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & ((r - g) > 55) & ((r - b) > 55)


def runs_from_profile(prof, thresh):
    """Return contiguous index runs where profile >= thresh."""
    out = []
    start = None
    for i, v in enumerate(prof):
        if v >= thresh and start is None:
            start = i
        elif v < thresh and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(prof) - 1))
    return out


def analyze(path, label):
    a, W, H = load(path)
    print(f"\n{'='*66}\n{label}: {path}\n  raster {W}x{H}  bg mean RGB "
          f"{[round(float(v),1) for v in a.mean(axis=(0,1))]}")
    R = red_mask(a)

    # --- house frame (outermost long red runs) ---
    hprof = R.sum(axis=1)
    vprof = R.sum(axis=0)
    hruns = [r for r in runs_from_profile(hprof, W * 0.60)]
    vruns = [r for r in runs_from_profile(vprof, H * 0.60)]
    print(f"  house frame h-rows(px): {hruns[:3]}  v-cols(px): {vruns[:3]}")
    for r in hruns[:2]:
        print(f"    h-row {r} -> y {r[0]/H*SH:.3f}..{r[1]/H*SH:.3f} in")
    for c in vruns[:2]:
        print(f"    v-col {c} -> x {c[0]/W*SW:.3f}..{c[1]/W*SW:.3f} in")

    # --- truth table grid: red lines inside top-left quadrant ---
    q = R[:int(H * 0.62), :int(W * 0.42)]
    qh = q.sum(axis=1)
    qv = q.sum(axis=0)
    hlines = runs_from_profile(qh, q.shape[1] * 0.30)
    vlines = runs_from_profile(qv, q.shape[0] * 0.25)
    print(f"  TABLE h-lines(px): {hlines}  -> in y "
          f"{[round(r[0]/H*SH,3) for r in hlines]}")
    print(f"  TABLE v-lines(px): {vlines}  -> in x "
          f"{[round(c[0]/W*SW,3) for c in vlines]}")
    if hlines:
        y0, y1 = hlines[0][0], hlines[-1][1]
        print(f"    table bbox in x {vlines[0][0]/W*SW:.3f}..{vlines[-1][1]/W*SW:.3f} "
              f"y {y0/H*SH:.3f}..{y1/H*SH:.3f}")
        if len(hlines) >= 2:
            rows = [(hlines[i][0] + hlines[i][1]) / 2 for i in range(len(hlines))]
            print(f"    row centers in: {[round(y/H*SH,3) for y in rows]}")

    # --- plot white area (top-right) ---
    white = (a[:, :, 0] > 232) & (a[:, :, 1] > 232) & (a[:, :, 2] > 232)
    half = int(W * 0.45)
    sub = white[:int(H * 0.70), half:]
    cols = sub.sum(axis=0)
    cand = [c for c in runs_from_profile(cols, sub.shape[0] * 0.35)]
    cand2 = [c for c in runs_from_profile(cols, sub.shape[0] * 0.20)]
    use = cand if cand else cand2
    if use:
        x0 = use[0][0] + half
        x1 = use[-1][1] + half
        rowsel = white[:, x0:x1]
        rprof = rowsel.sum(axis=1)
        rr = [r for r in runs_from_profile(rprof, (x1 - x0) * 0.35)] or \
             [r for r in runs_from_profile(rprof, (x1 - x0) * 0.20)]
        y0, y1 = rr[0][0], rr[-1][1]
        print(f"  PLOT white bbox in x {x0/W*SW:.3f}..{x1/W*SW:.3f} "
              f"y {y0/H*SH:.3f}..{y1/H*SH:.3f}")

    # --- markers + decision line inside plot area ---
    r_, g_, b_ = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    green = (g_ > 170) & (r_ < 140) & (b_ < 140)
    cyan = (g_ > 190) & (b_ > 190) & (r_ < 150)
    blue = (b_ > 150) & (r_ < 150) & (g_ < 150)
    for nm, m in (("GREEN", green), ("CYAN", cyan), ("BLUE", blue)):
        sub = m[:int(H * 0.72), half:]
        ys, xs = np.nonzero(sub)
        if len(xs) == 0:
            print(f"  {nm}: none in top-right")
            continue
        print(f"  {nm}: n={len(xs)} bbox in x {(xs.min()+half)/W*SW:.3f}..{(xs.max()+half)/W*SW:.3f} "
              f"y {ys.min()/H*SH:.3f}..{ys.max()/H*SH:.3f}")
        if nm != "BLUE" and len(xs) > 20:
            # cluster markers
            pts = np.stack([xs + half, ys], axis=1)
            clusters = []
            used = np.zeros(len(pts), bool)
            for i in range(len(pts)):
                if used[i]:
                    continue
                d = np.hypot(pts[:, 0] - pts[i, 0], pts[:, 1] - pts[i, 1])
                sel = (d < 0.02 * W) & ~used
                used |= sel
                clusters.append(pts[sel].mean(axis=0))
            for c in clusters:
                print(f"    marker centroid in x {c[0]/W*SW:.3f} y {c[1]/H*SH:.3f} "
                      f"(n={int((np.hypot(pts[:,0]-c[0], pts[:,1]-c[1]) < 0.02*W).sum())})")

    # --- peach equation box ---
    peach = (r_ > 225) & (g_ > 195) & (g_ < 245) & (b_ > 150) & (b_ < 225)
    ys, xs = np.nonzero(peach)
    if len(xs) > 50:
        print(f"  PEACH box in x {xs.min()/W*SW:.3f}..{xs.max()/W*SW:.3f} "
              f"y {ys.min()/H*SH:.3f}..{ys.max()/H*SH:.3f}  (n={len(xs)})")
    else:
        print(f"  PEACH box: not found (n={len(xs)})")

    # --- perceptron region: dark ink in bottom-left ---
    bl = slice(int(H * 0.60), int(H * 0.98))
    lc = slice(int(W * 0.05), int(W * 0.52))
    reg = a[bl, lc]
    ink = (reg.max(axis=2) < 150)
    ys, xs = np.nonzero(ink)
    if len(xs):
        print(f"  NET ink bbox in x {(xs.min()+int(W*0.05))/W*SW:.3f}..{(xs.max()+int(W*0.05))/W*SW:.3f} "
              f"y {(ys.min()+int(H*0.60))/H*SH:.3f}..{(ys.max()+int(H*0.60))/H*SH:.3f}")


if __name__ == "__main__":
    analyze(sys.argv[1], "ORIGINAL")
    analyze(sys.argv[2], "RENDER")
