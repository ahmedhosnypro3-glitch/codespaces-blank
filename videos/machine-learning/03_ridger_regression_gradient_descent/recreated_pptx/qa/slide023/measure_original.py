#!/usr/bin/env python3
"""PIL measurement of slide_023.jpg original frame (960x540, 1px=1pt).
Measures: colored highlight boxes (green/blue/yellow), text bands inside,
red-ink spans, title bbox, colors. Outputs JSON to stdout."""
import numpy as np
from PIL import Image
import json, sys

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

out = {}

def find_regions(mask, name):
    """Find connected row-bands and column extents of a mask."""
    rows = np.where(mask.any(axis=1))[0]
    if len(rows) == 0:
        out[name] = None
        return
    # split into contiguous row bands
    bands = []
    start = rows[0]; prev = rows[0]
    for r in rows[1:]:
        if r != prev + 1:
            bands.append((start, prev)); start = r
        prev = r
    bands.append((start, prev))
    res = []
    for (r0, r1) in bands:
        cols = np.where(mask[r0:r1+1].any(axis=0))[0]
        res.append({'y0': int(r0), 'y1': int(r1), 'x0': int(cols[0]), 'x1': int(cols[-1])})
    out[name] = res

# ---- highlight boxes by fill color (large uniform areas) ----
# light green E2EFDA ~ (226,239,218); light blue DDEBF7 ~ (221,235,247); light yellow FFF2CC ~ (255,242,204)
green = (np.abs(R-226)<12) & (np.abs(G-239)<12) & (np.abs(B-218)<12)
blue  = (np.abs(R-221)<12) & (np.abs(G-235)<12) & (np.abs(B-247)<12)
yellow= (np.abs(R-255)<10) & (np.abs(G-242)<12) & (np.abs(B-204)<12)
gray_panel = (np.abs(R-233)<8) & (np.abs(G-233)<8) & (np.abs(B-230)<8)

for m, n in [(green,'green_box'), (blue,'blue_box'), (yellow,'yellow_box'), (gray_panel,'gray_panel')]:
    # keep only large regions: count pixels per row band
    find_regions(m, n)

# ---- fill exact colors: sample interior of each box ----
def sample(name, mask):
    if out.get(name):
        b = out[name][0]
        cy = (b['y0']+b['y1'])//2; cx = (b['x0']+b['x1'])//2
        # take a small patch away from text: scan for the most common color in the region
        reg = a[b['y0']:b['y1']+1, b['x0']:b['x1']+1]
        regm = mask[b['y0']:b['y1']+1, b['x0']:b['x1']+1]
        px = reg[regm]
        out[name+'_mean_color'] = [int(v) for v in px.mean(axis=0)]

for m, n in [(green,'green_box'), (blue,'blue_box'), (yellow,'yellow_box')]:
    sample(n, m)

# ---- dark ink (text) bands ----
dark = (R<120)&(G<120)&(B<120)
find_regions(dark, 'dark_ink_bands')

# ---- red ink ----
red = (R>120)&(R<230)&(G<110)&(B<110)
find_regions(red, 'red_ink_bands')

# ---- title: red text top area ----
title_zone = red.copy(); title_zone[100:,:] = False
find_regions(title_zone, 'title_red')

# ---- stroke lines (C00000 family, dark maroon) ----
maroon = (R>90)&(R<180)&(G<90)&(B<90)
find_regions(maroon, 'maroon')

print(json.dumps(out, indent=1))
