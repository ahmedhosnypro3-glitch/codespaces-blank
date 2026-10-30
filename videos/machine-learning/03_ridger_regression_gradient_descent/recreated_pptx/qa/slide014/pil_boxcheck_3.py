#!/usr/bin/env python3
"""Targeted check of the two vector boxes' borders on both images, plus the
exact pixel colours at the render's x~896 and x~900.5 to test the prior lane's
"right box border sits ON the right stroke" claim.
Frame space 960x540; render /2.084375.
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(DECK, "unique_slides", "slide_014.jpg")
S = 2001.0 / 960.0


def hscan_dark(path, sc, fy, x_lo, x_hi, thr=430):
    im = Image.open(path).convert("RGB")
    px = im.load()
    W, H = im.size
    y = min(H - 1, int(fy * sc))
    hits = []
    for x in range(int(x_lo * sc), min(W, int(x_hi * sc))):
        c = px[x, y]
        if sum(c) < thr:
            hits.append((round(x / sc, 2), c))
    return hits


def cluster(hits, gap=2.0):
    out = []
    for h in hits:
        if out and h[0] - out[-1][-1][0] <= gap:
            out[-1].append(h)
        else:
            out.append([h])
    return [(round(min(a[0] for a in c), 2), round(max(a[0] for a in c), 2), c[len(c) // 2][1]) for c in out]


def main():
    print("===== VERTICAL DARK STRUCTURE at frame y = 112, 150, 228 =====")
    for fy in (112, 150, 228):
        print("\n--- frame y=%d ---" % fy)
        for name, path, sc in (("ORIG", SRC, 1.0), ("RENDER", os.path.join(HERE, "render_3.png"), S)):
            hits = hscan_dark(path, sc, fy, 40, 930)
            cl = cluster(hits)
            print("  %-7s %d dark runs: %s" % (name, len(cl), cl))

    print("\n===== WHAT IS AT THE RENDER'S RIGHT EDGE (y=150, all x 885..905 frame) =====")
    im = Image.open(os.path.join(HERE, "render_3.png")).convert("RGB")
    px = im.load()
    y = int(150 * S)
    prev = None
    for xf in [885, 888, 890, 892, 894, 895, 896, 898, 900, 901, 902, 903, 905]:
        x = int(xf * S)
        print("  frame_x=%-5d px_x=%-5d rgb=%s" % (xf, x, px[x, y]))

    print("\n===== SAME FOR THE ORIGINAL (y=150, x 800..905) =====")
    im2 = Image.open(SRC).convert("RGB")
    px2 = im2.load()
    for xf in [800, 805, 808, 810, 812, 815, 820, 860, 880, 900, 901, 902]:
        print("  frame_x=%-5d rgb=%s" % (xf, px2[int(xf), 150]))

    print("\n===== BOX TOP/BOTTOM BORDERS: horizontal dark runs =====")
    for fy in (104, 106, 234, 236):
        print("\n--- frame y=%d ---" % fy)
        for name, path, sc in (("ORIG", SRC, 1.0), ("RENDER", os.path.join(HERE, "render_3.png"), S)):
            hits = hscan_dark(path, sc, fy, 40, 930)
            cl = cluster(hits, gap=3.0)
            # only report long runs (borders)
            long = [c for c in cl if c[1] - c[0] > 20]
            print("  %-7s long runs: %s" % (name, long))


if __name__ == "__main__":
    main()
