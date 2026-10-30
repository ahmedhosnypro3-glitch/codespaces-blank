#!/usr/bin/env python3
"""Per-bracket vertical extent comparison: original frame vs 150dpi render.

Original ink is thin/faint handwriting -> ink threshold 205 with a 3-row run
rejection (phantom ink < 3 px is not a stroke).  Render ink is solid -> same
threshold, same rule, so both images are measured identically.

Outputs frame-px numbers plus the raw per-column row runs.
"""
import json
import sys
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
REND = sys.argv[1] if len(sys.argv) > 1 else DECK + "/recreated_pptx/qa/slide051/render_2.png"
OUT = DECK + "/recreated_pptx/qa/slide051/measure_bracket_extents_051.json"
THR = 205
MIN_RUN = 3


def runs_at_col(img, fx, y0, y1, is_render):
    g = img.convert("L")
    px = g.load()
    W, H = g.width, g.height
    if is_render:
        sx, sy = W / 960.0, H / 540.0
    else:
        sx = sy = 1.0
    hits = []
    for fy in range(y0, y1):
        X = min(W - 1, int(round(fx * sx)))
        Y = min(H - 1, int(round(fy * sy)))
        if px[X, Y] < THR:
            hits.append(fy)
    # group into runs, drop runs shorter than MIN_RUN
    out = []
    for y in hits:
        if out and y == out[-1][1] + 1:
            out[-1][1] = y
        else:
            out.append([y, y])
    return [(a, b) for a, b in out if b - a + 1 >= MIN_RUN], len(hits)


def band_extent(img, fx, y0, y1, is_render):
    rs, raw = runs_at_col(img, fx, y0, y1, is_render)
    if not rs:
        return None, raw
    top = min(a for a, _ in rs)
    bot = max(b for _, b in rs)
    return (top, bot), raw


def measure(img, cols, y0, y1, is_render):
    d = {}
    for fx in cols:
        ext, raw = band_extent(img, fx, y0, y1, is_render)
        d[fx] = {"extent": ext, "raw_ink_rows": raw}
    return d


def main():
    o = Image.open(ORIG)
    r = Image.open(REND)
    groups = {
        # group: (list of bracket stroke x positions (frame px), band y0, y1)
        "sample": ([90, 102, 111, 124, 134, 147, 156, 170, 179, 192, 202, 214], 60, 120),
        "centre_w": ([331, 352], 50, 115),
        "z": ([598, 612, 621, 634, 643, 656], 65, 120),
        "aug": ([94, 107, 115, 128, 137, 151, 160, 173, 182, 195, 205, 218], 165, 235),
        "dec1": ([384, 403], 138, 200),
        "dec2": ([384, 403], 204, 266),
        "dec3": ([384, 403], 270, 332),
    }
    res = {}
    print("%-9s %-5s %-24s %-24s %s" % ("group", "x", "ORIG extent (top..bot,len)",
                                        "REND extent (top..bot,len)", "dtop dbot"))
    for g, (cols, y0, y1) in groups.items():
        om = measure(o, cols, y0, y1, False)
        rm = measure(r, cols, y0, y1, True)
        res[g] = {"orig": om, "rend": rm}
        for fx in cols:
            oe = om[fx]["extent"]
            re_ = rm[fx]["extent"]
            if oe and re_:
                dtop = re_[0] - oe[0]
                dbot = re_[1] - oe[1]
                print("%-9s %-5d %-24s %-24s %+d %+d" %
                      (g, fx, "%d..%d (%d)" % (oe[0], oe[1], oe[1] - oe[0] + 1),
                       "%d..%d (%d)" % (re_[0], re_[1], re_[1] - re_[0] + 1), dtop, dbot))
            else:
                print("%-9s %-5d %-24s %-24s  (missing)" %
                      (g, fx, str(oe), str(re_)))
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
