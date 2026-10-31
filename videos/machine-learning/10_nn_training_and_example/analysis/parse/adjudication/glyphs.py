#!/usr/bin/env python3
"""Glyph-vs-diagram discriminator for adjudication.

Inside a window, report dark-ink connected components with height
histograms. Text = many small components (h 6..24px) arranged in
horizontal lines; diagram = few large blobs. Numbers only.
Usage: glyphs.py <jpg> x0 y0 x1 y1 [label]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage


def main():
    path = sys.argv[1]
    x0, y0, x1, y1 = (int(float(v)) for v in sys.argv[2:6])
    label = sys.argv[6] if len(sys.argv) > 6 else "win"
    a = np.asarray(Image.open(path).convert("L")).astype(np.int16)
    w = a[y0:y1, x0:x1]
    dark = w < 110
    print("WIN %s x=%d..%d y=%d..%d (%dx%d) dark_px=%d frac=%.4f"
          % (label, x0, x1, y0, y1, x1 - x0, y1 - y0, dark.sum(), dark.mean()))
    lab, n = ndimage.label(dark, structure=np.ones((3, 3)))
    objs = ndimage.find_objects(lab)
    comps = []
    for i, sl in enumerate(objs):
        if sl is None:
            continue
        cy, cx = sl[0].start + y0, sl[1].start + x0
        h = sl[0].stop - sl[0].start
        wd = sl[1].stop - sl[1].start
        px = int((lab[sl] == i + 1).sum())
        comps.append((cx, cy, wd, h, px))
    comps.sort(key=lambda t: (t[1], t[0]))
    hs = [c[3] for c in comps]
    if hs:
        hist, edges = np.histogram(hs, bins=[0, 6, 10, 14, 18, 24, 40, 80, 1000])
        print("HEIGHT_HIST " + " ".join("%d-%d:%d" % (edges[i], edges[i + 1], hist[i]) for i in range(len(hist))))
    small = [c for c in comps if 6 <= c[3] <= 26 and c[2] <= 60 and c[4] >= 4]
    big = [c for c in comps if c[3] > 26 or c[2] > 60]
    print("COMP_TOTAL %d  SMALL_GLYPH_LIKE %d  LARGE %d" % (len(comps), len(small), len(big)))
    print("SMALL_LIST (x,y,w,h,px) first 120:")
    for c in small[:120]:
        print("  %d %d %d %d %d" % c)
    # horizontal line grouping of small comps (text lines)
    ys = sorted(c[1] for c in small)
    lines = []
    for y in ys:
        if lines and y - lines[-1][1] <= 6:
            lines[-1][1] = y
        else:
            lines.append([y, y])
    print("GLYPH_LINES n=%d %s" % (len(lines), lines[:40]))
    print("BIG_LIST first 30:")
    for c in big[:30]:
        print("  x=%d y=%d w=%d h=%d px=%d" % c)


if __name__ == "__main__":
    main()
