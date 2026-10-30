#!/usr/bin/env python3
"""PIL adjudication helper for a leg-1 (Template A) finding on slide 021.

Every judge finding must be measured against BOTH images before any build change
(PIL-first adjudication law; judging.md). This script takes a finding's claimed
crop-relative or frame coordinates and re-measures the actual ink in both the
original frame and the current render, so a claim can be refuted with numbers.

Usage:
  python3 adjudicate_leg1_10.py          # run the standing checks
  python3 adjudicate_leg1_10.py <finding-json>
"""
import json
import sys

import numpy as np
from PIL import Image

ROOT = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{ROOT}/unique_slides/slide_021.jpg"
REND = f"{ROOT}/recreated_pptx/qa/slide021/render_10.png"
SC = 2001 / 960.0

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)


def box(a, x0, y0, x1, y1, inv):
    """Dark-ink count + bbox in frame px. Threshold is white-relative so the same
    rule applies to both the JPEG original and the digital render."""
    if inv:
        X0, Y0 = int(round(x0 * SC)), int(round(y0 * SC))
        X1, Y1 = int(round(x1 * SC)), int(round(y1 * SC))
        sub = a[Y0:Y1, X0:X1]
        ox, oy, sc = X0, Y0, 1.0 / SC
    else:
        sub = a[int(y0):int(y1), int(x0):int(x1)]
        ox, oy, sc = x0, y0, 1.0
    bg = np.median(sub.reshape(-1, 3), axis=0).mean()
    d = sub.mean(axis=2) < bg - 75
    ys, xs = np.nonzero(d)
    if len(xs) == 0:
        return {"ink": 0, "bbox": None}
    return {
        "ink": int(d.sum()),
        "bbox": (
            round((ox + xs.min()) * sc, 1), round((ox + xs.max()) * sc, 1),
            round((oy + ys.min()) * sc, 1), round((oy + ys.max()) * sc, 1),
        ),
    }


def colour(a, x0, y0, x1, y1, inv, pred, label):
    """Count + bbox (crop-relative AND frame px) of pixels matching pred."""
    if inv:
        X0, Y0 = int(round(x0 * SC)), int(round(y0 * SC))
        X1, Y1 = int(round(x1 * SC)), int(round(y1 * SC))
        sub = a[Y0:Y1, X0:X1]
    else:
        sub = a[int(y0):int(y1), int(x0):int(x1)]
    m = pred(sub)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return {"n": 0}
    from collections import Counter
    c = Counter(map(tuple, sub.reshape(-1, 3)))
    if inv:
        X0, Y0 = int(round(x0 * SC)), int(round(y0 * SC))
        fbx = (X0 + xs.min()) / SC, (X0 + xs.max()) / SC, (Y0 + ys.min()) / SC, (Y0 + ys.max()) / SC
    else:
        fbx = (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())
    return {"n": int(m.sum()),
            "bbox_croprel": (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())),
            "bbox_frame": tuple(round(v, 1) for v in fbx),
            "dominant": [(k, v) for k, v in c.most_common(3)]}


def standing_checks():
    print("### standing adjudication checks — slide 021 (render_10 vs original) ###\n")
    COLS, ROWS = [90, 158, 226, 294], [341, 359, 376, 395]
    print("1) MIDDLE TABLE — highlight bands (claim candidate: colour/extent)")
    for idx, (ci, ri) in enumerate([(0, 0), (1, 1), (2, 2)]):
        x0, y0, x1, y1 = COLS[ci] + 3, ROWS[ri] + 3, COLS[ci + 1] - 3, ROWS[ri + 1] - 2
        oc = colour(o, x0, y0, x1, y1, False,
                    lambda s: (s[:, :, 0] > 200) & (s[:, :, 1] > 200) & (np.abs(s[:, :, 2].astype(int) - 150) < 60),
                    "orig")
        rc = colour(r, x0, y0, x1, y1, True,
                    lambda s: (s[:, :, 0] > 200) & (s[:, :, 1] > 200) & (np.abs(s[:, :, 2].astype(int) - 150) < 60),
                    "rend")
        print(f"   cell{idx}: ORIG {oc['n']}px frame{oc.get('bbox_frame')} | REND {rc['n']}px frame{rc.get('bbox_frame')}")
        print(f"           dominant render colours: {rc.get('dominant')}")

    print("\n2) TABLE GRIDLINES (claim candidate: row pitch / vertical alignment)")
    for nm, (x0, x1, y0, y1) in [("P1", (97, 303, 170, 232)), ("P2", (89, 295, 336, 400)),
                                 ("P3", (421, 626, 454, 514))]:
        ro = box(o, x0, y0, x1, y1, False)
        rr = box(r, x0, y0, x1, y1, True)
        print(f"   {nm} table ink: ORIG {ro} | REND {rr}")

    print("\n3) EQUATION INK BOXES (claim candidate: missing/wrong equation)")
    for nm, (x0, y0, x1, y1) in [("xtx", (97, 133, 141, 157)), ("det0", (341, 187, 435, 212)),
                                 ("d5685", (338, 354, 464, 379)), ("regmat", (89, 300, 206, 326)),
                                 ("lambda3", (245, 304, 289, 321)), ("invexpr", (155, 466, 289, 492))]:
        ao = box(o, x0, y0, x1, y1, False)
        ar = box(r, x0, y0, x1, y1, True)
        print(f"   {nm:8s} ORIG {ao} | REND {ar}")

    print("\n4) FRAME CONTAINMENT — ink outside each block's blue strokes")
    for nm, (bx0, by0, bx1, by1) in [("P1", (76, 129, 886, 257)), ("P2", (76, 288, 889, 418)),
                                     ("P3", (76, 437, 889, 530))]:
        # all ink inside the block band, left of the left stroke and right of the right stroke
        INSET = 5
        HOUSE_L, HOUSE_R = 64, 896  # inside the house C00000 strokes (x58.5 / x901)
        lo = o[by0 + 4:by1 - 4, HOUSE_L:bx0 - INSET]
        ro = o[by0 + 4:by1 - 4, bx1 + 1 + INSET:HOUSE_R]
        lr = r[int(round((by0 + 4) * SC)):int(round((by1 - 4) * SC)), int(round(HOUSE_L * SC)):int(round((bx0 - INSET) * SC))]
        rr = r[int(round((by0 + 4) * SC)):int(round((by1 - 4) * SC)), int(round((bx1 + 1 + INSET) * SC)):int(round(HOUSE_R * SC))]
        print(f"   {nm}: ORIG ink L={int((lo.mean(axis=2) < 140).sum())} R={int((ro.mean(axis=2) < 140).sum())}"
              f" | REND ink L={int((lr.mean(axis=2) < 140).sum())} R={int((rr.mean(axis=2) < 140).sum())}")

    print("\n5) NOTHING ABOVE THE TITLE (house strokes excluded)")
    band_o = o[46:76, 62:897]
    band_r = r[int(round(46 * SC)):int(round(76 * SC)), int(round(62 * SC)):int(round(897 * SC))]
    # red only (title is red)
    ro = (band_o[:, :, 0] > 120) & (band_o[:, :, 1] < 95) & (band_o[:, :, 2] < 95)
    rr = (band_r[:, :, 0] > 120) & (band_r[:, :, 1] < 95) & (band_r[:, :, 2] < 95)
    print(f"   red px y46..76 x62..897 (the C00000 L/R strokes only; title starts y77):"
          f" ORIG {int(ro.sum())} | REND {int(rr.sum())} — both should be the strokes, nothing more")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            print(json.dumps(json.load(f), indent=2))
    else:
        standing_checks()
