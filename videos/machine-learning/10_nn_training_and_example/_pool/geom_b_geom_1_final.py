#!/usr/bin/env python3
"""Lane G (b_geom_1) — FINAL geometry measurement (gateway-free, PIL only).

Canonical coordinate system = the shared 960x540 slide frame.
recreated_pptx/build/slide_001.js:123 maps an original-frame crop with
`x = 588 / 960 * 13.33`, i.e. original frame px -> slide inches via px/960*13.33
and py/540*7.5. The render is the whole 13.33x7.5 slide BOX-resampled to
960x540, so render frame px use the SAME divisors. Original frame px and render
frame px are therefore compared directly in one shared coordinate system
(no border re-normalisation). Cross-check: the yellow badge is 35 px wide in
both the original frame and the render frame, and under this mapping the
original title band (raw x 284..655) brackets the render title (x 325..636)
far better than a page-normalised mapping does.

Ink = local median-filter luminance difference: captures text strokes AND drawn
box borders, without treating large filled panels as solid ink.

Chrome (masked, never reported as a finding):
  original: own red border rect, own yellow badge, black letterbox y>=517.
  render:   house red frame rect, house badge FIXED at 12.48/0.30/0.5 in
            -> x899..935, y21..57 (auto-detect fails on 007: the diagram's warm
            colours merge with the badge).
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_1"
TOL = 2.0          # ~4px at 150dpi
HOUSE_BADGE = (896, 18, 939, 61)

REGIONS = {
    "001": [("title", 20, 100), ("body_upper", 100, 250), ("body_lower", 250, 375),
            ("prepared_by", 375, 460), ("footer", 460, 540)],
    "004": [("title", 20, 100), ("top_row", 100, 240), ("derivation", 240, 370),
            ("bottom_row", 370, 540)],
    "005": [("title", 20, 70), ("box1", 70, 150), ("box2", 150, 300),
            ("box3", 300, 470), ("footer", 470, 540)],
    "006": [("title_block", 20, 120), ("subtitle", 120, 200), ("footer", 200, 540)],
    "007": [("title", 20, 80), ("diagram", 80, 400), ("bottom_strip", 400, 540)],
}
TITLE_REGIONS = {"title", "title_block"}


def load(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(np.int16)
    r = np.asarray(Image.open(f"{TMP}/frame_{n}.png").convert("RGB")).astype(np.int16)
    return o, r


def red_rect(a):
    h, w = a.shape[:2]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > 110) & (r - g > 35) & (r - b > 35)
    rows = np.nonzero(red.sum(axis=1) > 0.50 * w)[0]
    cols = np.nonzero(red.sum(axis=0) > 0.50 * h)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())


def badge_box(a):
    h, w = a.shape[:2]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    yel = (r > 185) & (g > 170) & (b > 110) & (b < 220)
    win = np.zeros_like(yel)
    win[:int(0.22 * h), int(0.78 * w):] = True
    yel &= win
    lab, n = ndimage.label(yel, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < 30:
            continue
        if xs.max() - xs.min() > 46 or ys.max() - ys.min() > 46:
            continue
        if best is None or len(ys) > best[0]:
            best = (len(ys), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    if best is None:
        return None
    return best[1], best[2], best[3], best[4]


def structure(a):
    lum = a.astype(np.float32).mean(axis=2)
    med = ndimage.median_filter(lum, size=7)
    m = np.abs(lum - med) > 26
    lab, cnt = ndimage.label(m, structure=np.ones((3, 3)))
    if cnt:
        keep = np.zeros_like(m)
        for i in range(1, cnt + 1):
            ys, xs = np.nonzero(lab == i)
            if ys.size >= 8:
                keep[ys, xs] = True
        m = keep
    return m


def apply_chrome(m, rect, badge, strip_y):
    x0, y0, x1, y1 = rect
    m[max(0, y0 - 4):y0 + 6, :] = False
    m[max(0, y1 - 5):y1 + 5, :] = False
    m[:, max(0, x0 - 4):x0 + 6] = False
    m[:, max(0, x1 - 5):x1 + 5] = False
    if strip_y is not None:
        m[strip_y:, :] = False
    if badge:
        px0, py0, px1, py1 = badge
        m[max(0, py0 - 5):py1 + 5, max(0, px0 - 5):px1 + 5] = False
    return m


def bands(m, minpx=40):
    rows = np.nonzero(m.sum(axis=1) > 0)[0]
    if rows.size == 0:
        return []
    out = []
    start = prev = rows[0]
    for y in rows[1:]:
        if y - prev > 3:
            out.append((start, prev + 1))
            start = y
        prev = y
    out.append((start, prev + 1))
    res = []
    for y0, y1 in out:
        sub = m[y0:y1]
        ys, xs = np.nonzero(sub)
        if xs.size >= minpx:
            res.append((y0, y1, int(xs.min()), int(xs.max()) + 1, int(xs.size)))
    return res


def ink_box(m, y0, y1):
    sub = m[y0:y1]
    ys, xs = np.nonzero(sub)
    if xs.size < 6:
        return None
    return {"x0": int(xs.min()), "x1": int(xs.max()) + 1,
            "y0": int(ys.min()) + y0, "y1": int(ys.max()) + 1 + y0, "px": int(xs.size)}


def fmt(b):
    if b is None:
        return "EMPTY"
    return "x %4d..%4d (w=%4d) y %4d..%4d (h=%3d) px=%d" % (
        b["x0"], b["x1"], b["x1"] - b["x0"], b["y0"], b["y1"], b["y1"] - b["y0"], b["px"])


def main():
    only = sys.argv[1:] or list(REGIONS)
    print("LANE G b_geom_1 - FINAL geometry (shared 960x540 frame coords)")
    print("TOLERANCE = %.1f px (~4px at 150dpi)" % TOL)
    for n in only:
        o, r = load(n)
        obr, rbr = red_rect(o), red_rect(r)
        ob = badge_box(o)
        om = apply_chrome(structure(o), obr, ob, 517)
        rm = apply_chrome(structure(r), rbr, HOUSE_BADGE, None)
        print("\n===== slide_%s" % n)
        print("  orig red=%s badge=%s | rend red=%s badge(FIXED house)=%s" % (obr, ob, rbr, HOUSE_BADGE))
        print("  ORIG bands (y0,y1,x0,x1,px):", bands(om))
        print("  REND bands (y0,y1,x0,x1,px):", bands(rm))
        print("  %-12s | %-45s | %-45s | %4s %4s %4s %4s %s" %
              ("region", "render box", "original box", "dL", "dR", "dT", "dB", "verdict"))
        for name, y0, y1 in REGIONS[n]:
            rb, obk = ink_box(rm, y0, y1), ink_box(om, y0, y1)
            if rb is None or obk is None:
                print("  %-12s | %-45s | %-45s | %4s %4s %4s %4s %s" %
                      (name, fmt(rb), fmt(obk), "-", "-", "-", "-",
                       "EXCEEDS-TOLERANCE (ink present in only one: rend=%s orig=%s)"
                       % (rb is not None, obk is not None)))
                continue
            dl, dr = obk["x0"] - rb["x0"], obk["x1"] - rb["x1"]
            dt, db = obk["y0"] - rb["y0"], obk["y1"] - rb["y1"]
            if name in TITLE_REGIONS:
                dx = max(abs(dl), abs(dr))
                v = ("PASS (x); dY house title box y=0.28in (chrome)"
                     if dx <= TOL else
                     "EXCEEDS-TOLERANCE (x); dY house title box y=0.28in (chrome)")
            else:
                dx, dy = max(abs(dl), abs(dr)), max(abs(dt), abs(db))
                v = "PASS" if dx <= TOL and dy <= TOL else "EXCEEDS-TOLERANCE"
            print("  %-12s | %-45s | %-45s | %4d %4d %4d %4d %s" %
                  (name, fmt(rb), fmt(obk), dl, dr, dt, db, v))


if __name__ == "__main__":
    main()
