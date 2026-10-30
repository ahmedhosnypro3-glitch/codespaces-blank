#!/usr/bin/env python3
"""Connected-component inventory of one DEC decision row, original vs render.

Ink = luminance < 200.  The card border is excluded by scanning strictly inside
the card rectangle.  Components smaller than MIN_INK are rejected as phantom.
Each component reports its bbox, ink count and colour class (black/blue/green/red).

usage: measure_dec_cc_051.py [render.png]
"""
import json
import sys
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
REND = sys.argv[1] if len(sys.argv) > 1 else DECK + "/recreated_pptx/qa/slide051/render_2.png"
OUT = DECK + "/recreated_pptx/qa/slide051/measure_dec_cc_051.json"
ROWS = [(141, 197), (207, 263), (273, 329)]
X0, X1 = 279, 850
LUM = 200
MIN_INK = 3


def classify(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    if b > r + 40 and b > g + 40:
        return "blue"
    if g > r + 25 and g > b + 25:
        return "green"
    if r > g + 50 and r > b + 50:
        return "red"
    if mx - mn < 40:
        return "black"
    return "other"


def mask_for(path, is_render, y0, y1):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    px = img.load()
    sx, sy = (W / 960.0, H / 540.0) if is_render else (1, 1)
    mask = {}
    for fy in range(y0 + 3, y1 - 2):
        Y = min(H - 1, int(round(fy * sy)))
        for fx in range(X0, X1):
            X = min(W - 1, int(round(fx * sx)))
            r, g, b = px[X, Y]
            if 0.299 * r + 0.587 * g + 0.114 * b < LUM:
                mask[(fx, fy)] = (r, g, b)
    return mask


def components(mask):
    seen = set()
    comps = []
    for start in mask:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        cells = []
        while stack:
            p = stack.pop()
            cells.append(p)
            x, y = p
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    q = (x + dx, y + dy)
                    if q in mask and q not in seen:
                        seen.add(q)
                        stack.append(q)
        xs = [c[0] for c in cells]
        ys = [c[1] for c in cells]
        cols = {}
        for c in cells:
            r, g, b = mask[c]
            k = classify(r, g, b)
            cols[k] = cols.get(k, 0) + 1
        dom = max(cols, key=cols.get)
        comps.append({
            "x0": min(xs), "x1": max(xs), "top": min(ys), "bot": max(ys),
            "ink": len(cells), "cls": dom, "mix": cols,
            "mean": tuple(sum(mask[c][i] for c in cells) // len(cells) for i in range(3)),
        })
    comps.sort(key=lambda c: (c["top"], c["x0"]))
    return [c for c in comps if c["ink"] >= MIN_INK]


def ascii_art(path, is_render, y0, y1, x0, x1):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    px = img.load()
    sx, sy = (W / 960.0, H / 540.0) if is_render else (1, 1)
    lines = []
    for fy in range(y0, y1):
        row = []
        for fx in range(x0, x1):
            X = min(W - 1, int(round(fx * sx)))
            Y = min(H - 1, int(round(fy * sy)))
            r, g, b = px[X, Y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            if lum >= 200:
                row.append(" ")
            else:
                row.append(classify(r, g, b)[0])
        lines.append("%3d %s" % (fy, "".join(row)))
    return lines


def main():
    res = {}
    for i, (y0, y1) in enumerate(ROWS):
        o = components(mask_for(ORIG, False, y0, y1))
        r = components(mask_for(REND, True, y0, y1))
        res["dec%d" % (i + 1)] = {"orig": o, "rend": r}
        print("=" * 100)
        print("DEC row %d  (frame px, card y%d..%d)" % (i + 1, y0, y1))
        print("  %-56s | %s" % ("ORIGINAL components", "RENDER components"))
        for j in range(max(len(o), len(r))):
            def fmt(c):
                if not c:
                    return ""
                return "x%3d..%3d y%3d..%3d ink%4d %-5s mix%s" % (
                    c["x0"], c["x1"], c["top"], c["bot"], c["ink"], c["cls"], c["mix"])
            print("  %-56s | %s" % (fmt(o[j] if j < len(o) else None),
                                    fmt(r[j] if j < len(r) else None)))
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print("\nwrote", OUT)

    print("\n\n########## ORIGINAL ASCII ART, DEC row 1 (x276..620) ##########")
    for l in ascii_art(ORIG, False, 141, 175, 276, 620):
        print(l)


if __name__ == "__main__":
    main()
