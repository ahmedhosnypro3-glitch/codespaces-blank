#!/usr/bin/env python3
"""Slide 045: render-vs-frame geometry comparison for the calc panel (adjudication prep).

Compares measured ink extents in render_1.png against the frame's measured x-groups,
so any FAIL from the judge can be adjudicated against banked numbers.
"""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045"
r = np.asarray(Image.open(QA + "/render_1.png").convert("RGB")).astype(int)
f = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
S = r.shape[0] / 540.0
lum = r.mean(axis=2)
flum = f.mean(axis=2)


def rp(x, y):
    return int(round(x * S)), int(round(y * S))


def groups(prof, x0, minrun=2):
    out, cur = [], None
    for i, v in enumerate(prof):
        if v > 0 and cur is None:
            cur = [x0 + i, x0 + i]
        elif v > 0:
            cur[1] = x0 + i
        else:
            if cur and cur[1] - cur[0] + 1 >= minrun:
                out.append((cur[0], cur[1]))
            cur = None
    if cur and cur[1] - cur[0] + 1 >= minrun:
        out.append((cur[0], cur[1]))
    return out


ROWS = [
    ("row1", 158, 180, 140, 197),
    ("row2", 224, 244, 207, 263),
    ("row3", 290, 309, 272, 329),
    ("row4", 359, 379, 338, 395),
    ("row5", 421, 440, 404, 461),
    ("row6", 487, 507, 470, 528),
]

for name, t0, t1, b0, b1 in ROWS:
    # render text-line x groups (frame coords)
    rx0, ry0 = rp(280, t0)
    rx1, ry1 = rp(860, t1)
    seg = lum[ry0:ry1 + 1, rx0:rx1 + 1]
    prof = (seg < 190).sum(axis=0)
    gr = groups(prof, 280)
    # frame text-line x groups
    fseg = flum[t0:t1 + 1, 280:861]
    fprof = (fseg < 200).sum(axis=0)
    gf = groups(fprof, 280)
    print("%s text line y%d..%d" % (name, t0, t1))
    print("   render x-groups: %s" % " ".join("%d-%d" % g for g in gr))
    print("   frame  x-groups: %s" % " ".join("%d-%d" % g for g in gf))

print()
print("=== overflow check: ink outside calc panel x274..853, y139..528 ===")
rx0, ry0 = rp(274, 139)
rx1, ry1 = rp(853, 528)
inner = lum[ry0:ry1 + 1, rx0:rx1 + 1]
print("   inner region render px %dx%d, darkest=%d" % (inner.shape[1], inner.shape[0], inner.min()))
# check the strip just outside the right edge for text ink (would indicate overflow)
rx2, ry2 = rp(858, 139)
strip = lum[ry0:ry1 + 1, rx2:rx2 + 40]
print("   ink px right of panel (x858..): %d (threshold <200)" % int((strip < 200).sum()))
rx3, ry3 = rp(266, 139)
strip2 = lum[ry0:ry1 + 1, rx3:rx3 + 15]
print("   ink px left of panel (x266..274): %d" % int((strip2 < 200).sum()))

print()
print("=== bracket vertical thickness (render) ===")
for label, x in [("d-vec left x379.5", 379.5), ("d-vec right x403.5", 403.5), ("W-vec left x729.5", 729.5), ("W-vec right x753.5", 753.5)]:
    cx, y0 = rp(x, 148)
    _, y1 = rp(x, 189)
    col = lum[y0:y1 + 1, cx - 3:cx + 4]
    dark = (col < 190)
    cols_with_ink = [cx - 3 + i for i in range(col.shape[1]) if dark[:, i].sum() > (y1 - y0) * 0.8]
    print("   %-22s vertical stroke cols=%s  span px=%d" % (label, cols_with_ink, int(dark.sum())))
