#!/usr/bin/env python3
"""Full-slide band detector for slide_014: find LONG horizontal runs (>=150px)
of near-uniform colour on each row, classify them, and report band extents.

Frame space 960x540 (1px = 1pt); render native 2001x1125 / 2.084375.
"""
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(DECK, "unique_slides", "slide_014.jpg")
S = 2001.0 / 960.0
MIN_RUN = 150  # frame-px; a band is >=150 px wide

PAL = {
    "peach": (248, 222, 193),
    "yellow": (245, 252, 218),
    "render_yellow": (255, 249, 196),
    "render_pink": (255, 235, 238),
    "panel": (233, 233, 231),
    "blue": (95, 90, 170),
    "render_blue": (120, 165, 235),
    "white": (255, 255, 255),
}

TOL = {
    "peach": 14,
    "yellow": 14,
    "render_yellow": 8,
    "render_pink": 6,
    "panel": 6,
    "blue": 60,
    "render_blue": 45,
    "white": 5,
}


def bands(path, scale, y_lo, y_hi):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    rows = []
    for y in range(int(y_lo * scale), min(H, int(y_hi * scale))):
        # contiguous runs of near-uniform colour
        runs = []
        x = 0
        while x < W:
            c = px[x, y]
            x2 = x
            while x2 + 1 < W and (
                abs(px[x2 + 1, y][0] - c[0]) <= 6
                and abs(px[x2 + 1, y][1] - c[1]) <= 6
                and abs(px[x2 + 1, y][2] - c[2]) <= 6
            ):
                x2 += 1
            if (x2 - x + 1) / scale >= MIN_RUN:
                runs.append((round(x / scale, 1), round(x2 / scale, 1), c))
            x = x2 + 1
        rows.append({"y": round(y / scale, 2), "runs": runs})
    # group consecutive rows whose matching-run x-extents are stable
    return rows


def merge(rows, kind, tol):
    """Group rows that contain a long run matching palette[kind] within tol."""
    t = PAL[kind]
    segs = []
    cur = []
    for r in rows:
        match = None
        for (a, b, c) in r["runs"]:
            if all(abs(c[i] - t[i]) <= tol for i in range(3)):
                match = (a, b, c)
                break
        if match:
            cur.append((r["y"], match[0], match[1], match[2]))
        else:
            if cur:
                segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    out = []
    for s in segs:
        # split on x-jump > 30 frame-px (a different block)
        sub = [s[0]]
        for prev, nxt in zip(s, s[1:]):
            if abs(nxt[1] - prev[1]) > 30 or abs(nxt[2] - prev[2]) > 30:
                if sub:
                    out.append(sub)
                sub = []
            sub.append(nxt)
        if sub:
            out.append(sub)
    res = []
    for sub in out:
        res.append(
            {
                "kind": kind,
                "y_from": round(sub[0][0], 2),
                "y_to": round(sub[-1][0], 2),
                "x_from": round(min(r[1] for r in sub), 2),
                "x_to": round(max(r[2] for r in sub), 2),
                "n_rows": len(sub),
                "fill": sub[len(sub) // 2][3],
            }
        )
    return res


def main():
    result = {}
    for label, path, sc in (
        ("original", SRC, 1.0),
        ("render", os.path.join(HERE, "render_3.png"), S),
    ):
        rows = bands(path, sc, 40, 540)
        segs = []
        for kind in ("peach", "yellow", "render_yellow", "render_pink", "blue", "render_blue", "panel"):
            segs.extend(merge(rows, kind, TOL[kind]))
        segs.sort(key=lambda s: (s["y_from"], s["x_from"]))
        result[label] = segs
        print("\n===== %s =====" % label)
        for s in segs:
            print(
                "  %-12s y %7.2f..%7.2f  x %7.2f..%7.2f  rows=%3d  fill=%s"
                % (s["kind"], s["y_from"], s["y_to"], s["x_from"], s["x_to"], s["n_rows"], s["fill"])
            )
    with open(os.path.join(HERE, "pil_bands_full_attempt3.json"), "w") as f:
        json.dump({"scale": S, "result": result}, f, indent=1, default=str)
    print("\nwrote pil_bands_full_attempt3.json")


if __name__ == "__main__":
    main()
