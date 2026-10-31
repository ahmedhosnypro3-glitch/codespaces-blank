#!/usr/bin/env python3
"""Lane G (b_geom_1) — FINAL v3 region measurement (gateway-free, PIL only).

Canonical system = each image's own SLIDE PAGE mapped to 960x540:
  original: the gray slide page (non-white area above the black letterbox)
  render:   the whole frame (the slide is the page)

Each image's own chrome is masked before measuring:
  original: own red border rect, own yellow badge, black letterbox, mouse cursor
  render:   house red frame rect, house badge FIXED at 12.48/0.30/0.5 in

Regions are windowed SEPARATELY per image, because the house template places
the title block at y=0.28in while the source decks place theirs elsewhere
(slide 006's title is mid-slide in the original) - that vertical difference is
chrome-driven, not a content defect, so it must not be forced through a shared
window.

Ink = local median-filter luminance difference (size 7, threshold 26): captures
text strokes AND drawn box borders; large filled panels are not wholesale ink.
TOL = 2.0 canonical px (~4px at 150dpi).
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_1"
TOL = 2.0
HOUSE_BADGE = (896, 18, 939, 61)
CURSOR = {"001": (795, 150, 830, 180)}

# slide -> [(region, orig_y0, orig_y1, rend_y0, rend_y1, is_title_region)]
REGIONS = {
    "001": [("title", 55, 125, 25, 70, 1),
            ("subtitle", 180, 245, 68, 112, 0),
            ("course_line", 270, 315, 135, 170, 0),
            ("prepared_by", 330, 368, 180, 215, 0),
            ("name_email", 360, 415, 215, 268, 0),
            ("instructors_label", 405, 440, 368, 398, 0),
            ("instructors_block", 435, 540, 420, 518, 0)],
    "004": [("title", 10, 72, 20, 62, 1),
            ("top_row", 72, 255, 62, 305, 0),
            ("derivation", 250, 420, 318, 375, 0),
            ("bottom_row", 415, 540, 375, 452, 0)],
    "005": [("title_header", 10, 78, 10, 70, 1),
            ("box1_chain_rule", 78, 176, 70, 205, 0),
            ("box2_weights", 176, 355, 205, 356, 0),
            ("box3_substitution", 355, 540, 356, 540, 0)],
    "006": [("title", 185, 240, 22, 68, 1),
            ("subtitle", 260, 315, 66, 108, 0),
            ("formula_block", 318, 360, 115, 150, 0)],
    "007": [("title", 8, 44, 22, 52, 1),
            ("subtitle", 42, 102, 52, 84, 0),
            ("diagram", 100, 402, 150, 452, 0),
            ("bottom_formula_strip", 400, 540, 452, 540, 0)],
}


def load(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(np.int16)
    r = np.asarray(Image.open(f"{TMP}/frame_{n}.png").convert("RGB")).astype(np.int16)
    return o, r


def page_rect(a):
    """Original: the gray slide page = the non-white area above the black bar."""
    h, w = a.shape[:2]
    dark = (a.max(axis=2) < 40)
    drow = np.nonzero(dark.sum(axis=1) > 0.50 * w)[0]
    limit = int(drow.min()) if drow.size else h
    sub = a[:limit]
    nw = ~((sub[..., 0] > 238) & (sub[..., 1] > 238) & (sub[..., 2] > 238))
    colfrac = nw.sum(axis=0) / sub.shape[0]
    rowfrac = nw.sum(axis=1) / w
    cols = np.nonzero(colfrac > 0.30)[0]
    rows = np.nonzero(rowfrac > 0.30)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())


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


def chrome_out(m, rect, badge, strip_y, cursor=None):
    x0, y0, x1, y1 = rect
    m[max(0, y0 - 3):y0 + 5, :] = False
    m[max(0, y1 - 4):y1 + 4, :] = False
    m[:, max(0, x0 - 3):x0 + 5] = False
    m[:, max(0, x1 - 4):x1 + 4] = False
    if strip_y is not None:
        m[strip_y:, :] = False
    if badge:
        px0, py0, px1, py1 = badge
        m[max(0, py0 - 5):py1 + 5, max(0, px0 - 5):px1 + 5] = False
    if cursor:
        cx0, cy0, cx1, cy1 = cursor
        m[max(0, cy0 - 3):cy1 + 3, max(0, cx0 - 3):cx1 + 3] = False
    return m


def to_canonical(m, rect):
    bx0, by0, bx1, by1 = rect
    out = np.zeros((540, 960), dtype=np.uint8)
    sy = (np.arange(0, 540) * ((by1 - by0) / 540.0) + by0).astype(int).clip(0, m.shape[0] - 1)
    sx = (np.arange(0, 960) * ((bx1 - bx0) / 960.0) + bx0).astype(int).clip(0, m.shape[1] - 1)
    out[:] = m[sy][:, sx]
    return out.astype(bool)


def long_lines(m, frac=0.35, minrun=60):
    """Rows/cols with a long continuous ink run: drawn box borders."""
    res = []
    for y in range(m.shape[0]):
        xs = np.nonzero(m[y])[0]
        if xs.size < minrun:
            continue
        gaps = np.nonzero(np.diff(xs) > 3)[0]
        runs = np.split(xs, gaps + 1)
        for r in runs:
            if r.size >= minrun:
                res.append((y, int(r[0]), int(r[-1]) + 1, int(r.size)))
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
    print("LANE G b_geom_1 - FINAL v3 (per-image windows, page-canonical)")
    print("TOLERANCE = %.1f px (~4px at 150dpi)" % TOL)
    for n in only:
        o, r = load(n)
        opg, obr, ob = page_rect(o), red_rect(o), badge_box(o)
        cur = CURSOR.get(n)
        om = to_canonical(chrome_out(structure(o), obr, ob, 517, cur), opg)
        rm = to_canonical(chrome_out(structure(r), red_rect(r), HOUSE_BADGE, None),
                          (0, 0, 959, 539))
        print("\n===== slide_%s  orig page=%s red=%s badge=%s cursor=%s" % (n, opg, obr, ob, cur))
        print("  ORIG long ink runs (y,x0,x1,len):", long_lines(om))
        print("  REND long ink runs (y,x0,x1,len):", long_lines(rm))
        print("  %-22s | %-45s | %-45s | %4s %4s %4s %4s %s" %
              ("region", "render box", "original box", "dL", "dR", "dT", "dB", "verdict"))
        for name, oy0, oy1, ry0, ry1, is_title in REGIONS[n]:
            rb, obk = ink_box(rm, ry0, ry1), ink_box(om, oy0, oy1)
            if rb is None or obk is None:
                print("  %-22s | %-45s | %-45s | %4s %4s %4s %4s %s" %
                      (name, fmt(rb), fmt(obk), "-", "-", "-", "-",
                       "EXCEEDS-TOLERANCE (ink present in only one: rend=%s orig=%s)"
                       % (rb is not None, obk is not None)))
                continue
            dl, dr = obk["x0"] - rb["x0"], obk["x1"] - rb["x1"]
            dt, db = obk["y0"] - rb["y0"], obk["y1"] - rb["y1"]
            if is_title:
                dx = max(abs(dl), abs(dr))
                v = ("PASS (x); dY chrome (house title box y=0.28in)"
                     if dx <= TOL else
                     "EXCEEDS-TOLERANCE (x); dY chrome (house title box y=0.28in)")
            else:
                dx, dy = max(abs(dl), abs(dr)), max(abs(dt), abs(db))
                v = "PASS" if dx <= TOL and dy <= TOL else "EXCEEDS-TOLERANCE"
            print("  %-22s | %-45s | %-45s | %4d %4d %4d %4d %s" %
                  (name, fmt(rb), fmt(obk), dl, dr, dt, db, v))


if __name__ == "__main__":
    main()
