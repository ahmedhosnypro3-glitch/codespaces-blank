#!/usr/bin/env python3
"""Focused checks: (1) right vector box border extents on both images,
(2) lower blue region vertical extent + gutter, (3) panel stroke positions.
Frame space 960x540; render /2.084375.
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(DECK, "unique_slides", "slide_014.jpg")
S = 2001.0 / 960.0


def load(path):
    im = Image.open(path).convert("RGB")
    return im, im.load(), im.size


def isdark(c, thr=430):
    return sum(c) < thr


def rightbox(path, sc):
    im, px, (W, H) = load(path)
    y0, y1 = int(100 * sc), int(240 * sc)
    # vertical dark lines present over most of the box band
    vlines = []
    for x in range(0, W):
        col = [px[x, y] for y in range(y0, y1, max(1, int(sc)))]
        d = sum(1 for c in col if isdark(c))
        if d >= len(col) * 0.75:
            vlines.append(x)
    # cluster them
    clusters = []
    for x in vlines:
        if clusters and x - clusters[-1][-1] <= max(1, int(1.6 * sc)):
            clusters[-1].append(x)
        else:
            clusters.append([x])
    # horizontal dark lines spanning a wide span
    hlines = []
    for y in range(y0, y1):
        row = [px[x, y] for x in range(0, W, 2)]
        d = sum(1 for c in row if isdark(c))
        if d >= 40:
            hlines.append(y)
    hcl = []
    for y in hlines:
        if hcl and y - hcl[-1][-1] <= 2:
            hcl[-1].append(y)
        else:
            hcl.append([y])
    return {
        "vline_clusters": [(round(min(c) / sc, 1), round(max(c) / sc, 1)) for c in clusters],
        "hline_clusters": [(round(min(c) / sc, 1), round(max(c) / sc, 1)) for c in hcl],
    }


def lowerblue(path, sc):
    im, px, (W, H) = load(path)
    ys = []
    xs_left = []
    xs_right = []
    for y in range(int(455 * sc), min(H, int(540 * sc))):
        row = [px[x, y] for x in range(0, W)]
        blue = [x for x in range(0, W) if row[x][2] > row[x][0] + 8 and row[x][2] > row[x][1] and row[x][0] < 240]
        if len(blue) > 40:
            ys.append(round(y / sc, 2))
            xs_left.append(round(min(blue) / sc, 2))
            xs_right.append(round(max(blue) / sc, 2))
    if not ys:
        return None
    # detect gutters: rows where the blue span is split
    gut = []
    for i, y in enumerate(range(int(455 * sc), int(540 * sc))):
        row = [px[x, y] for x in range(0, W)]
        blue = [x for x in range(0, W) if row[x][2] > row[x][0] + 8 and row[x][2] > row[x][1] and row[x][0] < 240]
        if len(blue) > 40:
            s = set(blue)
            gaps = []
            st = min(blue)
            prev = min(blue)
            for x in sorted(blue):
                if x - prev > 3:
                    if (x - prev) / sc > 8:
                        gaps.append((round(prev / sc, 1), round(x / sc, 1)))
                prev = x
            if gaps:
                gut.append((round(y / sc, 1), gaps))
    return {
        "y_from": min(ys),
        "y_to": max(ys),
        "x_left_min": min(xs_left),
        "x_left_max": max(xs_left),
        "x_right_min": min(xs_right),
        "x_right_max": max(xs_right),
        "gutters": gut[:40],
    }


def strokes(path, sc):
    im, px, (W, H) = load(path)
    out = {}
    # left vertical red stroke: scan x 40..70 at y=300 for reddish px
    best = None
    for x in range(int(40 * sc), int(75 * sc)):
        col = [px[x, y] for y in range(int(50 * sc), int(530 * sc), max(1, int(sc)))]
        red = [c for c in col if c[0] > 130 and c[1] < 90 and c[2] < 90]
        if len(red) >= len(col) * 0.5:
            best = (round(x / sc, 2), len(red), len(col))
    out["left_stroke_x"] = best
    best = None
    for x in range(int(885 * sc), int(920 * sc)):
        col = [px[x, y] for y in range(int(50 * sc), int(530 * sc), max(1, int(sc)))]
        red = [c for c in col if c[0] > 130 and c[1] < 90 and c[2] < 90]
        if len(red) >= len(col) * 0.5:
            best = (round(x / sc, 2), len(red), len(col))
    out["right_stroke_x"] = best
    return out


def main():
    print("===== RIGHT VECTOR BOX (y100..240) =====")
    for name, path, sc in (("ORIG", SRC, 1.0), ("RENDER", os.path.join(HERE, "render_3.png"), S)):
        r = rightbox(path, sc)
        print("  %s vlines=%s" % (name, r["vline_clusters"]))
        print("  %s hlines=%s" % (name, r["hline_clusters"]))
    print("\n===== STROKES =====")
    for name, path, sc in (("ORIG", SRC, 1.0), ("RENDER", os.path.join(HERE, "render_3.png"), S)):
        print("  %-7s %s" % (name, strokes(path, sc)))
    print("\n===== LOWER BLUE REGION =====")
    for name, path, sc in (("ORIG", SRC, 1.0), ("RENDER", os.path.join(HERE, "render_3.png"), S)):
        print("  %s %s" % (name, lowerblue(path, sc)))


if __name__ == "__main__":
    main()
