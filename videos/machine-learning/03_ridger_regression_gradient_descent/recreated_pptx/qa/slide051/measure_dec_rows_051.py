#!/usr/bin/env python3
"""Measure the three DEC decision rows of slide 051 by colour category, original vs render.

Colour classes (measured on the frame):
  blue   ~ (15,0,135)   green ~ (101,153,105)   red ~ (159,2,13)  black ink <150
Output is frame px.  Phantom ink (runs < 3 px) is dropped.
"""
import json
import sys
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
REND = sys.argv[1] if len(sys.argv) > 1 else DECK + "/recreated_pptx/qa/slide051/render_2.png"
OUT = DECK + "/recreated_pptx/qa/slide051/measure_dec_rows_051.json"
DEC = [(141, 197), (207, 263), (273, 329)]          # card tops, frame px
BANDS = [("label", 276, 340), ("value", 392, 470), ("cond", 470, 600),
         ("class", 600, 760), ("right", 760, 870)]


def classify(px):
    r, g, b = px
    if r < 150 and g < 150 and b < 150:
        return "black"
    if b > r + 40 and b > g + 40:
        return "blue"
    if g > r + 10 and g > b + 10 and g < 245:
        return "green"
    if r > g + 40 and r > b + 40 and r > 110:
        return "red"
    return None


def scan(path, is_render):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    px = img.load()
    if is_render:
        sx, sy = W / 960.0, H / 540.0
    else:
        sx = sy = 1.0
    out = {}
    for ri, (y0, y1) in enumerate(DEC):
        row = {}
        for name, bx0, bx1 in BANDS:
            cats = {}
            for fx in range(bx0, bx1):
                for fy in range(y0, y1):
                    X = min(W - 1, int(round(fx * sx)))
                    Y = min(H - 1, int(round(fy * sy)))
                    c = classify(px[X, Y])
                    if not c:
                        continue
                    e = cats.setdefault(c, [fx, fy, fx, fy, 0])
                    e[0] = min(e[0], fx)
                    e[1] = min(e[1], fy)
                    e[2] = max(e[2], fx)
                    e[3] = max(e[3], fy)
                    e[4] += 1
            row[name] = {k: v for k, v in cats.items()}
        out["dec%d" % (ri + 1)] = row
    return out


def fmt(e):
    return "x%d..%d y%d..%d n=%d" % (e[0], e[2], e[1], e[3], e[4])


def main():
    o = scan(ORIG, False)
    r = scan(REND, True)
    print("=== DEC rows: colour-classified ink bbox (frame px) ===")
    for k in o:
        print("\n### %s" % k)
        for name, _, _ in BANDS:
            oo = o[k][name]
            rr = r[k][name]
            for cat in ("black", "blue", "red", "green"):
                a = oo.get(cat)
                b = rr.get(cat)
                if a or b:
                    print("  %-7s %-6s ORIG %-34s REND %s" %
                          (name, cat, fmt(a) if a else "-",
                           fmt(b) if b else "-"))
    with open(OUT, "w") as f:
        json.dump({"orig": o, "rend": r}, f, indent=1)
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
