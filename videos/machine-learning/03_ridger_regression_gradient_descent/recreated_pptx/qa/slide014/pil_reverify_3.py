#!/usr/bin/env python3
"""Independent re-measurement of the slide_014 mid-region band defects.
Frame space 960x540 (1px = 1pt). Render native 2001x1125 / 2.084375.

Per row: classify every px, take the DOMINANT kind, record that kind's x extent
(contiguous extent of px matching the dominant kind). Then group consecutive
rows with the same dominant kind into bands.
"""
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(DECK, "unique_slides", "slide_014.jpg")

S = 2001.0 / 960.0
OUT = os.path.join(HERE, "pil_reverify_attempt3.json")


def classify(rgb):
    r, g, b = rgb
    # panel gray E9E9E7 ~ (233,233,231)
    if abs(r - 233) < 10 and abs(g - 233) < 10 and abs(b - 231) < 10:
        return "panel"
    # peach (248,222,193) / (248,220,193): r>>b
    if r > 225 and g > 195 and b > 160 and r - b > 25:
        return "peach"
    # yellow (245,252,218) / (249,253,218): b > r, g > r, bright
    if b > r + 12 and g > r + 12 and r > 200:
        return "yellow"
    # blue
    if b > r + 30 and b > g + 30:
        return "blue"
    # pink FFEBEE (255,235,238): r > g,b slightly
    if r > 245 and g > 225 and b > 225 and r - b > 10 and r - g > 8:
        return "pink"
    # white canvas
    if r > 245 and g > 245 and b > 245:
        return "white"
    return "other"


def scan(path, scale):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    y0, y1 = 335, 460
    x0, x1 = 40, 920
    y0p, y1p = int(y0 * scale), min(H, int(y1 * scale))
    x0p, x1p = int(x0 * scale), min(W, int(x1 * scale))
    rows = []
    for y in range(y0p, y1p):
        counts = {}
        xof = {}
        for x in range(x0p, x1p):
            c = px[x, y]
            k = classify(c)
            counts[k] = counts.get(k, 0) + 1
            if k not in xof:
                xof[k] = [x, x]
            else:
                xof[k][1] = x
        # dominant non-"other" kind
        cand = {k: v for k, v in counts.items() if k not in ("other",)}
        if not cand:
            continue
        dom = max(cand, key=lambda k: cand[k])
        rows.append(
            {
                "y": round(y / scale, 2),
                "dom": dom,
                "x_min": round(xof[dom][0] / scale, 2),
                "x_max": round(xof[dom][1] / scale, 2),
                "n_dom": cand[dom],
                "counts": counts,
                "sample": px[(xof[dom][0] + xof[dom][1]) // 2, y],
            }
        )
    return rows


def group(rows):
    bands = []
    cur = []
    for r in rows:
        if cur and (
            r["dom"] != cur[-1]["dom"] or abs(r["y"] - cur[-1]["y"]) > 3
        ):
            bands.append(cur)
            cur = []
        cur.append(r)
    if cur:
        bands.append(cur)
    out = []
    for b in bands:
        out.append(
            {
                "dom": b[0]["dom"],
                "y_from": round(b[0]["y"], 2),
                "y_to": round(b[-1]["y"], 2),
                "x_from": min(r["x_min"] for r in b),
                "x_to": max(r["x_max"] for r in b),
                "n_rows": len(b),
                "sample_fill": b[len(b) // 2]["sample"],
            }
        )
    return out


def main():
    res = {"scale": S, "original_frame": group(scan(SRC, 1.0)), "render_3": group(scan(os.path.join(HERE, "render_3.png"), S))}
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print("wrote", OUT)
    for key in ("original_frame", "render_3"):
        print("\n=== %s ===" % key)
        for i, b in enumerate(res[key]):
            print(
                "  %-6s y %7.2f..%7.2f  x %7.2f..%7.2f  rows=%3d  fill=%s"
                % (b["dom"], b["y_from"], b["y_to"], b["x_from"], b["x_to"], b["n_rows"], b["sample_fill"])
            )


if __name__ == "__main__":
    main()
