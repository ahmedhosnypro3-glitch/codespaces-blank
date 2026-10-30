#!/usr/bin/env python3
"""Full-slide independent re-measurement of every item in the slide_014 defect
table. Frame space 960x540 (1px = 1pt); render native 2001x1125 / 2.084375.

Verifies, on BOTH images:
  A. ridge/objective band x-extents and fills
  B. right vector box border x-extent
  C. mid-region band stack (the 3 BLOCKERs)
  D. lower blue region continuity + extents
"""
import json
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(DECK, "unique_slides", "slide_014.jpg")
S = 2001.0 / 960.0


def px_of(path):
    im = Image.open(path).convert("RGB")
    return im, im.load()


def hscan(path, scale, band_lo, band_hi, isnear):
    """For each y in the band, the x-extent of px matching isnear."""
    im, px = px_of(path)
    H, W = im.size[1], im.size[0]
    out = []
    for y in range(int(band_lo * scale), min(H, int(band_hi * scale))):
        xs = []
        for x in range(0, W):
            if isnear(px[x, y]):
                xs.append(x)
        if xs:
            # contiguous run containing the median
            xs.sort()
            mid = xs[len(xs) // 2]
            lo = hi = mid
            s = set(xs)
            while lo - 1 in s:
                lo -= 1
            while hi + 1 in s:
                hi += 1
            out.append((round(y / scale, 2), round(lo / scale, 2), round(hi / scale, 2), len(xs)))
    return out


def summarise(rows, label):
    if not rows:
        print("  %-22s EMPTY" % label)
        return None
    xs_min = min(r[1] for r in rows)
    xs_max = max(r[2] for r in rows)
    ys = [r[0] for r in rows]
    print(
        "  %-22s y %7.2f..%7.2f  x %7.2f..%7.2f  nrows=%d"
        % (label, min(ys), max(ys), xs_min, xs_max, len(rows))
    )
    return {"y_from": min(ys), "y_to": max(ys), "x_from": xs_min, "x_to": xs_max, "nrows": len(rows)}


def near(c, t, tol):
    return all(abs(c[i] - t[i]) <= tol for i in range(3))


def main():
    res = {}

    print("=== A. RIDGE band (yellow-ish, y245..285) ===")
    for name, path, sc in (
        ("orig", SRC, 1.0),
        ("render", os.path.join(HERE, "render_3.png"), S),
    ):
        yellow = lambda c: c[1] > c[0] and c[2] > c[0] and c[0] > 195
        r = hscan(path, sc, 245, 285, yellow)
        res["ridge_%s" % name] = summarise(r, "ridge-%s" % name)

    print("=== A2. OBJECTIVE band (yellow-ish, y303..340) ===")
    for name, path, sc in (
        ("orig", SRC, 1.0),
        ("render", os.path.join(HERE, "render_3.png"), S),
    ):
        yellow = lambda c: c[1] > c[0] and c[2] > c[0] and c[0] > 195
        r = hscan(path, sc, 303, 340, yellow)
        res["objective_%s" % name] = summarise(r, "objective-%s" % name)

    print("=== B. RIGHT VECTOR BOX top edge (y ~104..236) ===")
    for name, path, sc in (
        ("orig", SRC, 1.0),
        ("render", os.path.join(HERE, "render_3.png"), S),
    ):
        # a box border is a thin dark vertical line; find the rightmost dark column
        im, px = px_of(path)
        W, H = im.size
        y0p, y1p = int(104 * sc), min(H, int(236 * sc))
        best = None
        for x in range(W - 1, int(480 * sc), -1):
            col = [
                px[x, y]
                for y in range(y0p, y1p, max(1, int(sc)))
            ]
            dark = sum(1 for c in col if sum(c) < 450)
            if dark >= len(col) * 0.6:
                best = (x, round(x / sc, 2), dark, len(col))
                break
        print("  %-22s rightmost dark vertical at px=%s frame_x=%s dark=%d/%d" % (name, best[0], best[1], best[2], best[3]) if best else "  %-22s none" % name)
        res["rightbox_%s" % name] = best

    print("=== C. MID REGION band stack (y335..460) peach+yellow ===")
    for name, path, sc in (
        ("orig", SRC, 1.0),
        ("render", os.path.join(HERE, "render_3.png"), S),
    ):
        peach = lambda c: c[0] > 225 and c[1] > 195 and c[2] > 160 and c[0] - c[2] > 25
        r = hscan(path, sc, 335, 460, peach)
        res["mid_peach_%s" % name] = summarise(r, "mid-peach-%s" % name)
        yellow = lambda c: c[1] > c[0] and c[2] > c[0] and c[0] > 195
        r = hscan(path, sc, 335, 460, yellow)
        res["mid_yellow_%s" % name] = summarise(r, "mid-yellow-%s" % name)
        pink = lambda c: near(c, (255, 235, 238), 10)
        r = hscan(path, sc, 335, 460, pink)
        res["mid_pink_%s" % name] = summarise(r, "mid-pink-%s" % name)

    print("=== D. LOWER BLUE REGION (y462..532) ===")
    for name, path, sc in (
        ("orig", SRC, 1.0),
        ("render", os.path.join(HERE, "render_3.png"), S),
    ):
        blue = lambda c: c[2] > c[0] + 8 and c[2] > c[1] and c[0] < 235
        r = hscan(path, sc, 462, 532, blue)
        res["lower_blue_%s" % name] = summarise(r, "lower-blue-%s" % name)

    with open(os.path.join(HERE, "pil_fulltable_attempt3.json"), "w") as f:
        json.dump({k: v for k, v in res.items()}, f, indent=1, default=str)
    print("\nwrote pil_fulltable_attempt3.json")


if __name__ == "__main__":
    main()
