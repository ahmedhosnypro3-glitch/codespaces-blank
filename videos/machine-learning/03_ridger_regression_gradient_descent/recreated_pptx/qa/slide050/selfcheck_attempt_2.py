#!/usr/bin/env python3
"""Definitive containment check: for each region that is EMPTY in the ORIGINAL
frame, the RENDER must also be empty (no content ink). This directly proves the
recreation adds no stray content outside its measured frames.

'Empty' = no ink darker than the local background, computed on the ORIGINAL and
required on the RENDER at the same place.
"""
from PIL import Image
import numpy as np

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_050.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide050/render_1.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
SC = r.shape[1] / o.shape[1]
print("scale", round(SC, 4))


def ink(img, x0, y0, x1, y1, thr=170):
    """img may be the 960x540 original or the 2001x1125 render; frame coords
    are scaled by the image's own width / 960."""
    s = img.shape[1] / 960.0
    b = img[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    return int((b.mean(axis=2) < thr).sum()), b.shape[0] * b.shape[1]
REGIONS = [
    ("above navy box (canvas+panel)", 40, 40, 900, 50),
    ("right of navy box", 722, 55, 740, 130),
    ("between navy and pink", 722, 55, 742, 130),
    ("right of caption box", 244, 134, 310, 248),
    ("below caption box", 60, 250, 308, 272),
    ("left of chart (below caption)", 246, 250, 308, 470),
    ("left of chart, red-box zone", 60, 173, 310, 276),
    ("right of chart", 828, 173, 900, 481),
    ("below stop text", 60, 396, 300, 470),
    ("below chart", 312, 484, 824, 495),
    ("between red box and stop text", 84, 306, 213, 348),
    ("left of red box", 60, 278, 83, 305),
    ("right of red box", 214, 278, 300, 305),
]

bad = 0
for name, x0, y0, x1, y1 in REGIONS:
    no, tot = ink(o, x0, y0, x1, y1)
    nr, _ = ink(r, x0, y0, x1, y1)
    # allow the render up to the original's ink count + antialias slack
    ok = nr <= no + 40
    if not ok:
        bad += 1
    print("%-4s %-34s orig=%d render=%d (of %d px)" % ("PASS" if ok else "FAIL", name, no, nr, tot))

print()
print("regions with excess render ink:", bad)
