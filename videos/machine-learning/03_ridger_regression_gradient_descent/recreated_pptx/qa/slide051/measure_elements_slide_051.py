#!/usr/bin/env python3
"""Whole-slide element inventory: original frame vs render, frame px.

Segments ink (luminance < 200) into x-clusters separated by gaps >= GAP px,
per horizontal band, and prints them side by side so missing / extra elements
are obvious.  Used to check the rebuild against the original before judging.
"""
import json
import sys
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
REND = sys.argv[1] if len(sys.argv) > 1 else DECK + "/recreated_pptx/qa/slide051/render_2.png"
OUT = DECK + "/recreated_pptx/qa/slide051/measure_elements_slide_051.json"
BANDS = [
    ("top_card", 58, 126, 72, 716),
    ("centre_block", 56, 112, 250, 450),
    ("z_area", 58, 120, 588, 670),
    ("aug", 140, 250, 75, 235),
    ("redbox", 268, 312, 70, 245),
    ("dec1", 144, 194, 280, 850),
    ("dec2", 210, 260, 280, 850),
    ("dec3", 276, 326, 280, 850),
    ("bottom", 330, 540, 40, 920),
]
GAP = 5
LUM = 200


def elements(path, is_render, y0, y1, x0, x1):
    img = Image.open(path).convert("L")
    W, H = img.size
    px = img.load()
    sx, sy = (W / 960.0, H / 540.0) if is_render else (1, 1)
    cols = {}
    for fx in range(x0, x1):
        ink = 0
        top = bot = None
        for fy in range(y0, y1):
            X = min(W - 1, int(round(fx * sx)))
            Y = min(H - 1, int(round(fy * sy)))
            if px[X, Y] < LUM:
                ink += 1
                if top is None:
                    top = fy
                bot = fy
        if ink:
            cols[fx] = (ink, top, bot)
    out = []
    cur = None
    for fx in sorted(cols):
        if cur is None or fx - cur["x1"] > GAP:
            if cur:
                out.append(cur)
            cur = {"x0": fx, "x1": fx, "ink": 0, "top": cols[fx][1], "bot": cols[fx][2]}
        c = cols[fx]
        cur["x1"] = fx
        cur["ink"] += c[0]
        cur["top"] = min(cur["top"], c[1])
        cur["bot"] = max(cur["bot"], c[2])
    if cur:
        out.append(cur)
    return out


def main():
    res = {}
    for name, y0, y1, x0, x1 in BANDS:
        o = elements(ORIG, False, y0, y1, x0, x1)
        r = elements(REND, True, y0, y1, x0, x1)
        res[name] = {"orig": o, "rend": r}
        print("=" * 100)
        print("BAND %s  y%d..%d x%d..%d   (orig %d elements / render %d elements)"
              % (name, y0, y1, x0, x1, len(o), len(r)))
        for j in range(max(len(o), len(r))):
            a = ("x%3d..%3d y%3d..%3d ink%5d" % (o[j]["x0"], o[j]["x1"], o[j]["top"], o[j]["bot"], o[j]["ink"])) if j < len(o) else ""
            b = ("x%3d..%3d y%3d..%3d ink%5d" % (r[j]["x0"], r[j]["x1"], r[j]["top"], r[j]["bot"], r[j]["ink"])) if j < len(r) else ""
            print("   %-36s | %s" % (a, b))
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
