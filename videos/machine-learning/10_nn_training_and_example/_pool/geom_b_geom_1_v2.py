#!/usr/bin/env python3
"""Lane G (b_geom_1) — FINAL v2 geometry measurement (gateway-free, PIL only).

Canonical coordinate system = the SLIDE PAGE, 960x540.

The original frames are VIDEO CAPTURES, not clean renders: a white margin pads a
gray slide page, the source deck drew its own red border rect inside the page,
it drew its own yellow badge, and a mouse cursor / black letterbox appear in the
video. The render is the whole 13.33x7.5in slide (pdftoppm -r 150 -> 2001x1125,
BOX-resampled to 960x540) with the HOUSE chrome (0.15in red frame, house badge).

So each image is reduced to its own SLIDE PAGE and measured there:
  original: gray page detected as the non-white area -> mapped to 0..960/0..540
  render:   the whole frame IS the slide page -> identity mapping

This cancels every chrome difference (page position in the capture, frame inset,
badge geometry) and leaves only real content geometry. Cross-check: under this
mapping the yellow badge lands at canonical x~910..950 in BOTH images, and the
render's house frame lands at canonical x~10..950 while the original's own red
border lands at canonical x~2..937 - matching, not matching, exactly as expected
(chrome is masked in both).

Ink = local median-filter luminance difference (size 7, threshold 26): text
strokes AND drawn box borders are captured; large filled panels are not
wholesale ink.
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

REGIONS = {
    "001": [("title", 40, 130), ("subtitle", 210, 270), ("course_line", 270, 315),
            ("prepared_by", 330, 370), ("name_email", 365, 405),
            ("instructors_label", 400, 440), ("instructors_block", 440, 545)],
    "004": [("title", 20, 130), ("top_row", 130, 220), ("derivation", 220, 390),
            ("bottom_row", 400, 545)],
    "005": [("title", 30, 80), ("box1", 80, 185), ("box2", 185, 345),
            ("box3", 345, 535)],
    "006": [("title_block", 170, 250), ("subtitle", 250, 300),
            ("footer_note", 300, 360)],
    "007": [("title", 20, 90), ("diagram", 90, 370), ("bottom_strip", 395, 545)],
}
TITLE_REGIONS = {"title", "title_block"}


def load(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(np.int16)
    r = np.asarray(Image.open(f"{TMP}/frame_{n}.png").convert("RGB")).astype(np.int16)
    return o, r


def page_rect(a):
    """Original: the gray slide page = the non-white area ABOVE the black bar."""
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
    """Resample the ink mask so `rect` fills 0..960/0..540."""
    bx0, by0, bx1, by1 = rect
    out = np.zeros((540, 960), dtype=np.uint8)
    sy = (np.arange(0, 540) * ((by1 - by0) / 540.0) + by0).astype(int).clip(0, m.shape[0] - 1)
    sx = (np.arange(0, 960) * ((bx1 - bx0) / 960.0) + bx0).astype(int).clip(0, m.shape[1] - 1)
    out[:] = m[sy][:, sx]
    return out.astype(bool)


def bands(m, minpx=40, gap=3):
    rows = np.nonzero(m.sum(axis=1) > 0)[0]
    if rows.size == 0:
        return []
    out = []
    start = prev = rows[0]
    for y in rows[1:]:
        if y - prev > gap:
            out.append((start, prev + 1))
            start = y
        prev = y
    out.append((start, prev + 1))
    res = []
    for y0, y1 in out:
        sub = m[y0:y1]
        ys, xs = np.nonzero(sub)
        if xs.size >= minpx:
            res.append((int(y0), int(y1), int(xs.min()), int(xs.max()) + 1, int(xs.size)))
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
    print("LANE G b_geom_1 - FINAL v2 (canonical = slide page, 960x540)")
    print("TOLERANCE = %.1f px (~4px at 150dpi)" % TOL)
    for n in only:
        o, r = load(n)
        opg = page_rect(o)
        obr = red_rect(o)
        ob = badge_box(o)
        cur = CURSOR.get(n)
        om = to_canonical(chrome_out(structure(o), obr, ob, 517, cur), opg)
        rm = to_canonical(chrome_out(structure(r), red_rect(r), HOUSE_BADGE, None),
                          (0, 0, 959, 539))
        print("\n===== slide_%s" % n)
        print("  orig page=%s red=%s badge=%s cursor=%s" % (opg, obr, ob, cur))
        print("  ORIG bands:", bands(om))
        print("  REND bands:", bands(rm))
        print("  %-19s | %-45s | %-45s | %4s %4s %4s %4s %s" %
              ("region", "render box", "original box", "dL", "dR", "dT", "dB", "verdict"))
        for name, y0, y1 in REGIONS[n]:
            rb, obk = ink_box(rm, y0, y1), ink_box(om, y0, y1)
            if rb is None or obk is None:
                print("  %-19s | %-45s | %-45s | %4s %4s %4s %4s %s" %
                      (name, fmt(rb), fmt(obk), "-", "-", "-", "-",
                       "EXCEEDS-TOLERANCE (ink present in only one: rend=%s orig=%s)"
                       % (rb is not None, obk is not None)))
                continue
            dl, dr = obk["x0"] - rb["x0"], obk["x1"] - rb["x1"]
            dt, db = obk["y0"] - rb["y0"], obk["y1"] - rb["y1"]
            if name in TITLE_REGIONS:
                dx = max(abs(dl), abs(dr))
                v = ("PASS (x); dY chrome (house title box y=0.28in)"
                     if dx <= TOL else
                     "EXCEEDS-TOLERANCE (x); dY chrome (house title box y=0.28in)")
            else:
                dx, dy = max(abs(dl), abs(dr)), max(abs(dt), abs(db))
                v = "PASS" if dx <= TOL and dy <= TOL else "EXCEEDS-TOLERANCE"
            print("  %-19s | %-45s | %-45s | %4d %4d %4d %4d %s" %
                  (name, fmt(rb), fmt(obk), dl, dr, dt, db, v))


def os_environ_regionless():
    return False


if __name__ == "__main__":
    main()
