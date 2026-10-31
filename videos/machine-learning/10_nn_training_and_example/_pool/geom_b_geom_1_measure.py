#!/usr/bin/env python3
"""Lane G (b_geom_1) — final region-window geometry measurement.

Both images are reduced to the canonical 960x540 slide box:
  - original: its own red-border rect (x57..902, y42..517) mapped to 0..960/0..540
  - render:   the 960x540 BOX-resampled frame (already the whole slide)

Structure mask = local median-filter luminance difference, so drawn box borders
and text strokes are both captured and large filled panels are not wholesale ink.

Chrome (each image's own border line, badge, black bottom strip) is masked.
Region y-windows come from the certified layout regions + the measured original
structure. Tolerance: 2.0 canonical px (~4px at 150dpi).

NOTE on the title block: the house rule fixes the title box at y=0.28in
(canonical y~20), so a title-block VERTICAL delta against the original is
house-chrome-driven, not a defect. Title-block HORIZONTAL extent is reported as
content geometry (font size / alignment).
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_1"
TOL = 2.0
PAD = 5

# slide -> [(region, y0, y1)]
REGIONS = {
    "001": [("title", 0, 148), ("body_upper", 148, 340), ("body_lower", 340, 450), ("footer", 450, 540)],
    "004": [("title", 0, 105), ("top_row", 105, 265), ("derivation", 265, 430), ("bottom_row", 430, 540)],
    "005": [("title", 0, 60), ("box1", 60, 158), ("box2", 158, 362), ("box3", 362, 540)],
    "006": [("title", 0, 92), ("subtitle", 92, 170), ("footer", 170, 540)],
    "007": [("title", 0, 72), ("diagram", 72, 452), ("bottom_strip", 452, 540)],
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


def badge_box(a, rect):
    h, w = a.shape[:2]
    bx0, by0, bx1, by1 = rect
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    yel = (r > 185) & (g > 170) & (b > 110) & (b < 220)
    win = np.zeros_like(yel)
    win[by0:by1, bx0:bx1] = True
    win[:, :int(0.78 * w)] = False
    win[int(0.22 * h):, :] = False
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


def structure(a, rect, badge_b, strip_y, k=7, thr=26):
    lum = a.astype(np.float32).mean(axis=2)
    med = ndimage.median_filter(lum, size=k)
    m = np.abs(lum - med) > thr
    x0, y0, x1, y1 = rect
    m[max(0, y0 - 4):y0 + 6, :] = False
    m[max(0, y1 - 5):y1 + 5, :] = False
    m[:, max(0, x0 - 4):x0 + 6] = False
    m[:, max(0, x1 - 5):x1 + 5] = False
    m[strip_y:, :] = False
    if badge_b:
        px0, py0, px1, py1 = badge_b
        m[max(0, py0 - PAD):py1 + PAD, max(0, px0 - PAD):px1 + PAD] = False
    lab, cnt = ndimage.label(m, structure=np.ones((3, 3)))
    if cnt:
        keep = np.zeros_like(m)
        for i in range(1, cnt + 1):
            ys, xs = np.nonzero(lab == i)
            if ys.size >= 8:
                keep[ys, xs] = True
        m = keep
    return m


def canonical(m, rect):
    """Resample the structure mask into 960x540 canonical coords."""
    bx0, by0, bx1, by1 = rect
    out = np.zeros((540, 960), dtype=np.uint8)
    sy = (np.arange(0, 540) * ((by1 - by0) / 540.0) + by0).astype(int).clip(0, m.shape[0] - 1)
    sx = (np.arange(0, 960) * ((bx1 - bx0) / 960.0) + bx0).astype(int).clip(0, m.shape[1] - 1)
    out[:] = m[sy][:, sx]
    return out.astype(bool)


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
    print("LANE G b_geom_1 — canonical 960x540 slide-box geometry")
    print("TOLERANCE = %.1f canonical px (~4px at 150dpi)" % TOL)
    for n in only:
        o, r = load(n)
        obr, rbr = red_rect(o), red_rect(r)
        ob, rbb = badge_box(o, obr), badge_box(r, rbr)
        om = canonical(structure(o, obr, ob, 517), obr)
        rm = canonical(structure(r, rbr, rbb, 529), rbr)
        print("\n===== slide_%s" % n)
        print("  orig rect=%s badge=%s | rend rect=%s badge=%s" % (obr, ob, rbr, rbb))
        print("  %-11s | %-46s | %-46s | %5s %5s %5s %5s %s" %
              ("region", "render box", "original box", "dL", "dR", "dT", "dB", "verdict"))
        for name, y0, y1 in REGIONS[n]:
            rb, obk = ink_box(rm, y0, y1), ink_box(om, y0, y1)
            if rb is None or obk is None:
                print("  %-11s | %-46s | %-46s | %5s %5s %5s %5s %s" %
                      (name, fmt(rb), fmt(obk), "-", "-", "-", "-",
                       "EXCEEDS-TOLERANCE (ink present in only one: rend=%s orig=%s)" %
                       (rb is not None, obk is not None)))
                continue
            dl, dr = obk["x0"] - rb["x0"], obk["x1"] - rb["x1"]
            dt, db = obk["y0"] - rb["y0"], obk["y1"] - rb["y1"]
            if name in TITLE_REGIONS:
                # title box y is house chrome; judge the title block on its
                # horizontal extent only, and report the vertical delta.
                dx = max(abs(dl), abs(dr))
                v = "PASS (x)" if dx <= TOL else "EXCEEDS-TOLERANCE (x)"
                note = " | dY omitted: house title box y=0.28in (chrome)"
            else:
                dx, dy = max(abs(dl), abs(dr)), max(abs(dt), abs(db))
                v = "PASS" if dx <= TOL and dy <= TOL else "EXCEEDS-TOLERANCE"
                note = ""
            print("  %-11s | %-46s | %-46s | %5d %5d %5d %5d %s%s" %
                  (name, fmt(rb), fmt(obk), dl, dr, dt, db, v, note))


if __name__ == "__main__":
    main()
