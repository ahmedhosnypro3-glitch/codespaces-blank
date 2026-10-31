"""Ink bounding-box helper for parse-lane adjudication.

Reports horizontal/vertical ink runs in a band so a parse <x_><y_> token can be
resolved to a pixel box without eyeballing.
"""
import sys
import json
from PIL import Image


def ink_map(path, x0, y0, x1, y1, thresh=46):
    im = Image.open(path).convert("L")
    W, H = im.size
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    crop = im.crop((x0, y0, x1, y1))
    w, h = crop.size
    px = crop.load()
    cols = []
    for x in range(w):
        n = 0
        for y in range(h):
            if px[x, y] < 255 - thresh:
                n += 1
        cols.append(n)
    rows = []
    for y in range(h):
        n = 0
        for x in range(w):
            if px[x, y] < 255 - thresh:
                n += 1
        rows.append(n)
    return {"box": [x0, y0, x1, y1], "cols": cols, "rows": rows}


def runs(vals, min_gap=3):
    out = []
    start = None
    gap = 0
    for i, v in enumerate(vals):
        if v > 0:
            if start is None:
                start = i
            gap = 0
        else:
            if start is not None:
                gap += 1
                if gap > min_gap:
                    out.append((start, i - gap))
                    start = None
    if start is not None:
        out.append((start, len(vals) - 1))
    return out


if __name__ == "__main__":
    path = sys.argv[1]
    x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
    th = int(sys.argv[6]) if len(sys.argv) > 6 else 46
    d = ink_map(path, x0, y0, x1, y1, th)
    print(json.dumps({
        "box": d["box"],
        "col_runs": runs(d["cols"]),
        "row_runs": runs(d["rows"]),
    }))
