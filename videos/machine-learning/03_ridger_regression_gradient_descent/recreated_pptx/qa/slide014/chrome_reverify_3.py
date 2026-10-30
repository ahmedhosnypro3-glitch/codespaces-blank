#!/usr/bin/env python3
"""Independent house-chrome re-verification for slide_014 render_3.png.
Deck law: panel E9E9E7 x54..903 y45..540; red C00000 1pt strokes LEFT x58.5,
RIGHT x901, BOTTOM y538.5; NO top stroke; badge circle ~d35 centered (876,73).
Frame space 960x540; render 2001x1125 (x2.084375).
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(DECK, "unique_slides", "slide_014.jpg")
S = 2001.0 / 960.0


def isred(c):
    return c[0] > 130 and c[1] < 90 and c[2] < 90


def vstroke(path, sc, x_lo, x_hi, y_lo=40, y_hi=540):
    im = Image.open(path).convert("RGB")
    px = im.load()
    W, H = im.size
    best = []
    for x in range(int(x_lo * sc), min(W, int(x_hi * sc))):
        col = [px[x, y] for y in range(int(y_lo * sc), min(H, int(y_hi * sc)), 2)]
        n = sum(1 for c in col if isred(c))
        if n >= len(col) * 0.9:
            best.append(round(x / sc, 2))
    return best


def hstroke(path, sc, y_lo, y_hi, x_lo=40, x_hi=930):
    im = Image.open(path).convert("RGB")
    px = im.load()
    W, H = im.size
    best = []
    for y in range(int(y_lo * sc), min(H, int(y_hi * sc))):
        row = [px[x, y] for x in range(int(x_lo * sc), min(W, int(x_hi * sc)), 2)]
        n = sum(1 for c in row if isred(c))
        if n >= len(row) * 0.8:
            best.append(round(y / sc, 2))
    return best


def top_red(path, sc):
    """Red pixels in the top band y0..45 (a top stroke would be a BUILD DEFECT)."""
    im = Image.open(path).convert("RGB")
    px = im.load()
    W, H = im.size
    n = 0
    for y in range(0, min(H, int(45 * sc))):
        for x in range(0, W, 2):
            if isred(px[x, y]):
                n += 1
    return n


def panel_extent(path, sc):
    im = Image.open(path).convert("RGB")
    px = im.load()
    W, H = im.size
    y = int(300 * sc)
    runs = []
    x = 0
    while x < W:
        c = px[x, y]
        x2 = x
        while x2 + 1 < W and all(abs(px[x2 + 1, y][i] - c[i]) <= 4 for i in range(3)):
            x2 += 1
        if (x2 - x + 1) / sc > 200:
            runs.append((round(x / sc, 1), round(x2 / sc, 1), c))
        x = x2 + 1
    return runs


def badge(path, sc):
    """Find the yellow badge near frame (876,73)."""
    im = Image.open(path).convert("RGB")
    px = im.load()
    W, H = im.size
    # search a window
    x0, x1 = int(830 * sc), min(W, int(930 * sc))
    y0, y1 = int(30 * sc), min(H, int(120 * sc))
    hits = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if c[0] > 240 and c[1] > 240 and c[2] < 190 and c[2] > 110:
                hits.append((x, y))
    if not hits:
        return None
    xs = [h[0] for h in hits]
    ys = [h[1] for h in hits]
    return {
        "cx_frame": round((min(xs) + max(xs)) / 2 / sc, 1),
        "cy_frame": round((min(ys) + max(ys)) / 2 / sc, 1),
        "d_frame": round((max(xs) - min(xs) + 1) / sc, 1),
        "n": len(hits),
    }


def main():
    for name, path, sc in (("ORIG", SRC, 1.0), ("RENDER", os.path.join(HERE, "render_3.png"), S)):
        print("===== %s =====" % name)
        print("  vstroke x40..75 : %s" % vstroke(path, sc, 40, 75))
        print("  vstroke x885..925: %s" % vstroke(path, sc, 885, 925))
        print("  hstroke y525..540: %s" % hstroke(path, sc, 525, 540))
        print("  hstroke y0..45   : %s   <-- must be EMPTY (no top stroke)" % hstroke(path, sc, 0, 45))
        print("  TOP BAND RED PX : %d  <-- must be 0" % top_red(path, sc))
        print("  panel runs y300 : %s" % panel_extent(path, sc))
        print("  badge           : %s" % badge(path, sc))


if __name__ == "__main__":
    main()
