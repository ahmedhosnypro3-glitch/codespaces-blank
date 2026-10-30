#!/usr/bin/env python3
"""PIL adjudication of att34 topbox MAJOR: are the orig topbox band delimiters
straight bars or curved parens? Measures: (1) tall-vertical-stroke census per
column over the topbox, (2) per-row centroid x of each stroke (curvature test),
(3) same for the render. Slide space: orig 960x540, render 2001x1125 (~2.084x)."""
from PIL import Image
import sys

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg"
REND = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/render_34.png"

S = 2001 / 960.0

def load(p):
    return Image.open(p).convert("RGB")

def max_run_and_rows(px, w, h, x, y0, y1, thresh):
    """longest consecutive dark run in column x between y0..y1 and its extent"""
    best = 0; bs = be = 0; run = 0; start = 0
    for y in range(y0, y1):
        r, g, b = px[x, y]
        dark = (r + g + b) / 3 < thresh
        if dark:
            if run == 0: start = y
            run += 1
            if run > best: best, bs, be = run, start, y
        else:
            run = 0
    return best, bs, be

def stroke_census(im, x0, x1, y0, y1, thresh, scale=1.0):
    """for each column, max consecutive dark run; report columns with run>=40"""
    px = im.load()
    w, h = im.size
    out = []
    for x in range(x0, x1):
        best, bs, be = max_run_and_rows(px, w, h, x, y0, y1, thresh)
        if best >= 40:
            out.append((x, best, bs, be))
    # group adjacent columns
    groups = []
    for c in out:
        if groups and c[0] - groups[-1][-1][0] <= 2:
            groups[-1].append(c)
        else:
            groups.append([c])
    res = []
    for g in groups:
        xs = [c[0] for c in g]
        # use the column with the longest run as the stroke core
        core = max(g, key=lambda c: c[1])
        res.append({
            "x_slide": round(sum(xs) / len(xs) / scale, 1),
            "x_range": (round(min(xs) / scale, 1), round(max(xs) / scale, 1)),
            "run": core[1], "y0": core[2], "y1": core[3],
        })
    return res

def centroid_profile(im, x, y0, y1, thresh, halfw=3):
    """per-row ink centroid x in window x-halfw..x+halfw, sampled every 12 rows"""
    px = im.load()
    prof = []
    for y in range(y0, y1, 12):
        num = 0.0; den = 0
        for xx in range(x - halfw, x + halfw + 1):
            r, g, b = px[xx, y]
            d = 255 - (r + g + b) / 3
            if d > (255 - thresh):
                num += xx * d; den += d
        prof.append((y, round(num / den, 1) if den else None))
    return prof

print("=" * 78)
print("ORIG frame topbox: tall-stroke census (threshold 200, run>=40 rows)")
im = load(ORIG)
for g in stroke_census(im, 260, 620, 108, 302, 200):
    print(f"  x_slide={g['x_slide']:6} xr={g['x_range']} run={g['run']} y={g['y0']}..{g['y1']}")

print()
print("RENDER topbox: tall-stroke census (same, scale %.4f)" % S)
imr = load(REND)
for g in stroke_census(imr, int(260 * S), int(620 * S), int(108 * S), int(302 * S), 200, S):
    print(f"  x_slide={g['x_slide']:6} xr={g['x_range']} run={g['run']} y={g['y0'] / S:.0f}..{g['y1'] / S:.0f}")

print()
print("CURVATURE PROFILES (orig): per-row centroid x around each stroke core")
im = load(ORIG)
for xc, tag in [(296.5, "yellowL?"), (331.5, "yellowR"), (373.5, "cyanL?"), (414.5, "cyanR"), (517.5, "pinkL?"), (556.5, "pinkR"), (451, "midcolL"), (468, "midcolR")]:
    xi = int(xc)
    # find the actual stroke core near xi (max run in +/-4 window)
    best = None
    for x in range(xi - 4, xi + 5):
        b, bs, be = max_run_and_rows(im.load(), im.size[0], im.size[1], x, 140, 300, 200)
        if best is None or b > best[0]: best = (b, x, bs, be)
    if best[0] < 25:
        print(f"  {tag:9} x~{xc}: NO stroke >=25 rows (max run {best[0]})")
        continue
    prof = centroid_profile(im, best[1], max(108, best[2] - 6), min(302, best[3] + 6), 200)
    s = " ".join(f"{y}:{c}" for y, c in prof)
    print(f"  {tag:9} x~{xc} core_x={best[1]} run={best[0]} y={best[2]}..{best[3]}")
    print(f"      {s}")
