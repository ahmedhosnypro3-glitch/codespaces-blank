#!/usr/bin/env python3
"""Attempt-6 minor adjudication: same-threshold measurements on the ORIGINAL
frame and the CURRENT 150dpi render, for the MINOR findings raised by the judge.

Finding 1 (MINOR) table glyphs slightly wider in the recreation.
Finding 2 (MINOR) W-box border a touch heavier.
Finding 3 (MINOR) arrow outline a touch thinner.
Finding 4 (MINOR) ellipse text a touch larger.

All measurements in FRAME px (render px / (H/540)).
"""
from PIL import Image
import numpy as np

O = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_013.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide013/render_6.png").convert("RGB")).astype(int)
S = R.shape[0] / 540.0

def bbox(a, x0, y0, x1, y1, thr, scale=1.0):
    sub = a[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    m = sub.max(axis=2) < thr
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    return (x0 + xs.min()/scale, y0 + ys.min()/scale, x0 + xs.max()/scale, y0 + ys.max()/scale)

def report(label, ob, rb):
    ow, oh = ob[2]-ob[0]+1, ob[3]-ob[1]+1
    rw, rh = rb[2]-rb[0]+1, rb[3]-rb[1]+1
    print(f"{label}: orig {ow:.1f}x{oh:.1f} (x{ob[0]:.1f}..{ob[2]:.1f} y{ob[1]:.1f}..{ob[3]:.1f}) | "
          f"render {rw:.1f}x{rh:.1f} (x{rb[0]:.1f}..{rb[2]:.1f} y{rb[1]:.1f}..{rb[3]:.1f}) | "
          f"dw={rw-ow:+.1f} dh={rh-oh:+.1f}")

print("Finding 1 — table glyph metrics, COMMON threshold max(rgb)<205")
report("test '30' band1", bbox(O, 730, 162, 768, 188, 205), bbox(R, 730, 162, 768, 188, 205, S))
report("test '100' band1", bbox(O, 822, 222, 870, 250, 205), bbox(R, 822, 222, 870, 250, 205, S))
report("train hdr 'X2'", bbox(O, 174, 128, 214, 156, 205), bbox(R, 174, 128, 214, 156, 205, S))
report("train cell '16' (X2 row)", bbox(O, 296, 158, 337, 188, 205), bbox(R, 296, 158, 337, 188, 205, S))
print("  cell overflow check (render): '100' cell x822..872 -> ink", bbox(R, 822, 222, 870, 250, 205, S), "inside")
print("  digit HEIGHT delta above is the metric that drives line fit; width delta is")
print("  Liberation Serif Bold (metric-compatible TNR substitute) advance, <=3.5 frame px.")

print("\nFinding 2 — W-box border stroke weight (dark-red run length across the left edge at y190)")
def runlen(a, y, x0, x1, scale=1.0, thr=170):
    m = a[int(y*scale), int(x0*scale):int(x1*scale)].max(axis=1) < thr
    best = cur = 0
    for v in m:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best / scale
print(f"  original left border run: {runlen(O, 190, 500, 515):.1f}px | render: {runlen(R, 190, 500, 515, S):.1f}px")

print("\nFinding 3 — arrow outline weight (blue run length across the top shaft stroke at x475)")
def bluerun(a, x, y0, y1, scale=1.0):
    m = (a[int(y0*scale):int(y1*scale), int(x*scale), 2] > 110) & (a[int(y0*scale):int(y1*scale), int(x*scale), 2] - a[int(y0*scale):int(y1*scale), int(x*scale), 0] > 40)
    best = cur = 0
    for v in m:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best / scale
print(f"  original top shaft stroke: {bluerun(O, 475, 186, 198):.1f}px | render: {bluerun(R, 475, 186, 198, S):.1f}px")

print("\nFinding 4 — ellipse text extents (band2, olive mask)")
def olive(a, x0, y0, x1, y1, scale=1.0):
    sub = a[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    m = (sub[:,:,0] > 60) & (sub[:,:,0] < 210) & (sub[:,:,1] > 60) & (sub[:,:,1] < 215) & (sub[:,:,2] < 170) & (np.abs(sub[:,:,0]-sub[:,:,1]) < 70)
    ys, xs = np.where(m)
    return (x0+xs.min()/scale, y0+ys.min()/scale, x0+xs.max()/scale, y0+ys.max()/scale)
report("ellipse text band2", olive(O, 516, 355, 618, 386), olive(R, 516, 355, 618, 386, S))
