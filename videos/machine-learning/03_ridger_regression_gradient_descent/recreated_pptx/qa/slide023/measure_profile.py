#!/usr/bin/env python3
"""Detailed profile measurement of slide_023.jpg — per-row counts of each color
class + band extraction + targeted crop maps."""
import numpy as np
from PIL import Image
import json

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# color classes (tolerant of JPEG shift, using hue-ish logic)
# green fill E2EFDA=(226,239,218): G>R>B, G-R>8, G-B>12, bright
green_fill = (G > R + 6) & (G > B + 10) & (G > 200) & (R > 180)
# blue fill DDEBF7=(221,235,247): B>G>R, B-R>10, bright
blue_fill = (B > G + 6) & (G > R + 6) & (B > 200) & (R > 180)
# yellow fill FFF2CC=(255,242,204): R>G>B, R-B>30, bright
yellow_fill = (R > G + 6) & (G > B + 20) & (R > 220) & (B > 160)
# red ink C00000-family: R>>G,B
red_ink = (R > 120) & (R - G > 90) & (R - B > 90)
# dark ink
dark_ink = (R < 110) & (G < 110) & (B < 110)
# gray panel E9E9E7: near-equal, ~231
gray = (np.abs(R - G) < 8) & (np.abs(G - B) < 10) & (R > 200) & (R < 250)

def bands(mask, min_gap=2):
    rows = np.where(mask.sum(axis=1) > 3)[0]
    if len(rows) == 0:
        return []
    out = []
    start = prev = rows[0]
    for r in rows[1:]:
        if r > prev + min_gap:
            out.append((start, prev)); start = r
        prev = r
    out.append((start, prev))
    return out

report = {}
for name, m in [('green_fill', green_fill), ('blue_fill', blue_fill),
                ('yellow_fill', yellow_fill), ('red_ink', red_ink),
                ('dark_ink', dark_ink), ('gray', gray)]:
    bs = bands(m)
    report[name] = []
    for (y0, y1) in bs:
        seg = m[y0:y1+1]
        cols = np.where(seg.any(axis=0))[0]
        report[name].append({'y0': int(y0), 'y1': int(y1),
                             'x0': int(cols[0]), 'x1': int(cols[-1]),
                             'px': int(seg.sum())})

print(json.dumps(report, indent=1))
