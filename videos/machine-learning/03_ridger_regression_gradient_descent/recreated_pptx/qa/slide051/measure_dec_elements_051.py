#!/usr/bin/env python3
"""Segment every ink element inside each DEC decision row, original vs render.

Ink = luminance < 200 (frame px).  Elements are separated by x-gaps >= GAP px.
Reports each element's x-range, y-range, mean colour tag and ink pixel count,
so the original's element inventory can be compared with the render's.
"""
import json
import sys
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
REND = sys.argv[1] if len(sys.argv) > 1 else DECK + "/recreated_pptx/qa/slide051/render_2.png"
OUT = DECK + "/recreated_pptx/qa/slide051/measure_dec_elements_051.json"
ROWS = [(141, 197), (207, 263), (273, 329)]
X0, X1 = 276, 860
GAP = 4
LUM = 200


def elements(path, is_render, y0, y1):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    px = img.load()
    sx, sy = (W / 960.0, H / 540.0) if is_render else (1, 1)
    cols = {}
    for fx in range(X0, X1):
        ink = 0
        top = bot = None
        rs = gs = bs = n = 0
        for fy in range(y0, y1):
            X = min(W - 1, int(round(fx * sx)))
            Y = min(H - 1, int(round(fy * sy)))
            r, g, b = px[X, Y]
            if 0.299 * r + 0.587 * g + 0.114 * b < LUM:
                ink += 1
                rs += r; gs += g; bs += b; n += 1
                if top is None:
                    top = fy
                bot = fy
        if ink:
            cols[fx] = (ink, top, bot, (rs // n, gs // n, bs // n))
    out = []
    cur = None
    for fx in sorted(cols):
        if cur is None or fx - cur["x1"] > GAP:
            if cur:
                out.append(cur)
            cur = {"x0": fx, "x1": fx, "ink": 0, "top": cols[fx][1], "bot": cols[fx][2],
                   "r": 0, "g": 0, "b": 0, "n": 0}
        c = cols[fx]
        cur["x1"] = fx
        cur["ink"] += c[0]
        cur["top"] = min(cur["top"], c[1])
        cur["bot"] = max(cur["bot"], c[2])
        cur["r"] += c[3][0] * c[0]; cur["g"] += c[3][1] * c[0]; cur["b"] += c[3][2] * c[0]
        cur["n"] += c[0]
    if cur:
        out.append(cur)
    for e in out:
        e["rgb"] = (e["r"] // e["n"], e["g"] // e["n"], e["b"] // e["n"])
        del e["r"], e["g"], e["b"], e["n"]
    return out


def main():
    res = {}
    for i, (y0, y1) in enumerate(ROWS):
        o = elements(ORIG, False, y0, y1)
        r = elements(REND, True, y0, y1)
        res["dec%d" % (i + 1)] = {"orig": o, "rend": r}
        print("=" * 96)
        print("DEC row %d  (frame px, card y%d..%d)" % (i + 1, y0, y1))
        print("  %-32s | %s" % ("ORIGINAL elements", "RENDER elements"))
        for j in range(max(len(o), len(r))):
            a = ("x%3d..%3d y%3d..%3d ink%4d rgb%s" %
                 (o[j]["x0"], o[j]["x1"], o[j]["top"], o[j]["bot"], o[j]["ink"], o[j]["rgb"])
                 ) if j < len(o) else ""
            b = ("x%3d..%3d y%3d..%3d ink%4d rgb%s" %
                 (r[j]["x0"], r[j]["x1"], r[j]["top"], r[j]["bot"], r[j]["ink"], r[j]["rgb"])
                 ) if j < len(r) else ""
            print("  %-46s | %s" % (a, b))
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
