#!/usr/bin/env python3
"""Slide 019 — verify panel-border geometry from pixels (original vs render).

Finds the blue (#0000CC-ish) panel borders and the red (#C00000) house frame in
each image, so the build's assumed panel rectangles are checked against measured
reality rather than a vision prose note.
"""
import numpy as np
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_019.jpg"
RENDER = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_019_rendered-1.png"


def load(path, scale=1.0):
    im = Image.open(path).convert("RGB")
    if scale != 1.0:
        im = im.resize((int(round(im.size[0] * scale)), int(round(im.size[1] * scale))), Image.LANCZOS)
    return np.asarray(im).astype(int)


def blue_mask(a, tol=55):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (b - r > tol) & (b - g > tol) & (b > 90)


def red_mask(a, tol=55):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r - g > tol) & (r - b > tol) & (r > 90)


def runs(mask):
    ys, xs = np.nonzero(mask)
    return xs, ys


def analyze(path, label, scale=1.0):
    a = load(path, scale)
    H, W = a.shape[:2]
    fr = lambda v: v / scale
    print(f"\n=== {label}  ({W}x{H}) ===")

    # BLUE panel borders: look for long vertical and horizontal blue runs
    bm = blue_mask(a)
    colcnt = bm.sum(axis=0)
    rowcnt = bm.sum(axis=1)
    # a vertical panel edge is a column with many blue pixels
    vcols = np.nonzero(colcnt > H * 0.28)[0]
    hrows = np.nonzero(rowcnt > W * 0.28)[0]
    def group(idx, min_gap=6):
        if len(idx) == 0:
            return []
        out, cur = [], [idx[0]]
        for v in idx[1:]:
            if v - cur[-1] <= min_gap:
                cur.append(v)
            else:
                out.append(cur); cur = [v]
        out.append(cur)
        return [(int(np.mean(c)), len(c)) for c in out]
    print("  blue vertical edges (frame x, thickness):", [(round(fr(v)), t) for v, t in group(vcols)])
    print("  blue horizontal edges (frame y, thickness):", [(round(fr(v)), t) for v, t in group(hrows)])

    # RED house frame: outermost red box
    rm = red_mask(a)
    rys, rxs = np.nonzero(rm)
    if len(rxs):
        print(f"  red ink extent: x={fr(rxs.min()):.1f}..{fr(rxs.max()):.1f} y={fr(rys.min()):.1f}..{fr(rys.max()):.1f}  px={rm.sum()}")

    # caption boxes: find peach-ish fill (light warm) and gray fill regions at
    # the caption y bands. Work in frame coords.
    for nm, band in [("top captions", (240, 295)), ("bottom captions", (480, 515))]:
        y0, y1 = band
        sub = a[int(y0 * scale):int(y1 * scale), :, :]
        s = scale
        rr, gg, bb = sub[..., 0].astype(int), sub[..., 1].astype(int), sub[..., 2].astype(int)
        peach = (rr > 230) & (rr - bb > 15) & (rr - bb < 50) & (gg < rr - 8)
        cols = peach.sum(axis=0)
        gr = np.nonzero(cols > (sub.shape[0] * 0.5))[0]
        print(f"  {nm}: peach-run columns (frame x):", [round(fr(v)) for v in group(gr, min_gap=4)] if scale == 1.0 else [round(fr(v) * scale) for v in group(gr, min_gap=4)])


if __name__ == "__main__":
    analyze(ORIG, "ORIGINAL slide_019.jpg")
    analyze(RENDER, "RENDER slide_019_rendered-1.png", scale=2001 / 960)
