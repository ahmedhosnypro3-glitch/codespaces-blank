#!/usr/bin/env python3
# Round 3: connected-component glyph extraction for ambiguous regions.
import numpy as np
from PIL import Image
from collections import deque

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide049"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)
H, W = orig.shape[:2]
rh, rw = rend.shape[:2]
sx, sy = rw / W, rh / H


def lum(a):
    return (a[:, :, 0] * 299 + a[:, :, 1] * 587 + a[:, :, 2] * 114) // 1000


olum = lum(orig)
rlum = lum(rend)
x0s = np.minimum((np.arange(W) * sx).astype(int), rw - 1)
y0s = np.minimum((np.arange(H) * sy).astype(int), rh - 1)
rmin_rows = np.minimum.reduceat(rlum, y0s, axis=0)
rmin = np.minimum.reduceat(rmin_rows, x0s, axis=1)
r_ink = rmin < 150
o_ink = olum < 205


def cc_label(ink, x0, x1, y0, y1, bridge=2):
    """8-conn components with horizontal dilation `bridge` to merge glyph parts."""
    h, w = y1 - y0, x1 - x0
    sub = ink[y0:y1, x0:x1]
    # dilate horizontally by bridge to glue glyph strokes
    d = sub.copy()
    for k in range(1, bridge + 1):
        d[:, k:] |= sub[:, :-k]
        d[:, :-k] |= sub[:, k:]
    lab = np.zeros((h, w), int)
    nxt = 0
    comps = []
    for i in range(h):
        for j in range(w):
            if d[i, j] and lab[i, j] == 0:
                nxt += 1
                q = deque([(i, j)])
                lab[i, j] = nxt
                pix = []
                while q:
                    a, b = q.popleft()
                    pix.append((a, b))
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < h and 0 <= nb < w and d[na, nb] and lab[na, nb] == 0:
                                lab[na, nb] = nxt
                                q.append((na, nb))
                ys = [p[0] for p in pix]
                xs = [p[1] for p in pix]
                comps.append((min(xs), max(xs), min(ys), max(ys), pix))
    comps.sort(key=lambda c: c[0])
    return comps


def show(ink, x0, x1, y0, y1, label, bridge=2, minw=1):
    comps = cc_label(ink, x0, x1, y0, y1, bridge)
    print(f"\n=== {label} ({len(comps)} comps) ===")
    for (cx0, cx1, cy0, cy1, pix) in comps:
        w = cx1 - cx0 + 1
        h = cy1 - cy0 + 1
        if w < minw:
            continue
        print(f"-- comp x{x0+cx0}..{x0+cx1} y{y0+cy0}..{y0+cy1} (w{w} h{h})")
        if w <= 60 and h <= 60:
            grid = ["  "]
            for yy in range(cy0, cy1 + 1):
                row = "".join("#" if (yy, xx) in {(a, b) for a, b in pix} else "." for xx in range(cx0, cx1 + 1))
                grid.append(row)
            print("\n".join(grid))


# row-1 expression band, excluding the box borders: y142..195, x276..772
show(o_ink, 276, 772, 142, 196, "ORIG row1 glyphs", bridge=1)
show(r_ink, 276, 772, 142, 196, "RENDER row1 glyphs", bridge=1)
