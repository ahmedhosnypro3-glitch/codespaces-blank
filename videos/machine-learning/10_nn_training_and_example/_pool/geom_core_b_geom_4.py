#!/usr/bin/env python3
"""Lane G (b_geom_4): element-level ink measurement, original vs render.

Both sides are reduced to the 960x540 SOURCE-FRAME grid:
  - original JPEG  : 960x540 directly (slide pixels x38..921, y43..539)
  - render PNG     : 2001x1125 @150dpi; frame_px = render_px * 960/2001 (x),
                     * 540/1125 (y). Build scripts declare geometry in this same
                     960x540 source grid (PX = 13.33/960), so the grids match.

Elements are isolated on each side by COLOUR CLASS independently, so the
comparison is element-vs-element and never biased by a shared search window.

House chrome is excluded from BOTH sides:
  - render: red frame (0.15in inset), yellow badge, title box band
  - original: its own outer border ring, own yellow badge, white letterbox
"""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SCOPE = "b_geom_4"
TOL = 2.0   # source-frame px (== ~4.17 px at 150dpi)

O_BOX = (38, 43, 922, 539)
O_RING = [(38, 43, 41, 539), (919, 43, 922, 539), (38, 43, 922, 46), (38, 536, 922, 539)]
O_BADGE = (866, 46, 922, 98)
R_IN, R_OUT = 26, 1975
R_OUT_Y = 1099
R_BADGE = (1872, 45, 1947, 120)
R_TITLE = (90, 42, 1910, 130)


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def ink(a, bg, thr=45):
    return np.abs(a - bg).sum(axis=2) > thr


def cls(a, kind):
    """colour-class mask."""
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    if kind == "ink":
        return None
    if kind == "red":
        return (r > 100) & (r > g + 25) & (r > b + 25)
    if kind == "blue":
        return (b > 80) & (b > r + 20) & (b > g + 15)
    if kind == "green":
        return (g > 100) & (g > r + 20) & (g > b + 20)
    if kind == "yellow":
        return (r > 200) & (g > 180) & (b < 190)
    if kind == "dark":
        return a.mean(axis=2) < 110
    if kind == "nonbg":
        return None
    raise ValueError(kind)


def base_masks(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
    om = ink(o, fast_bg(o, O_BOX))
    om[: O_BOX[1], :] = om[O_BOX[3]:, :] = False
    om[:, : O_BOX[0]] = om[:, O_BOX[2]:] = False
    for x0, y0, x1, y1 in O_RING + [O_BADGE]:
        om[y0:y1, x0:x1] = False
    rm = ink(r, fast_bg(r, (30, 30, r.shape[1] - 30, r.shape[0] - 30)))
    rm[:R_IN, :] = rm[R_OUT_Y:, :] = False
    rm[:, :R_IN] = rm[:, R_OUT:] = False
    rm[R_BADGE[1]:R_BADGE[3], R_BADGE[0]:R_BADGE[2]] = False
    rm[R_TITLE[1]:R_TITLE[3], R_TITLE[0]:R_TITLE[2]] = False
    return o, om, r, rm, r.shape[1], r.shape[0]


def bbox(m):
    rr = np.where(m.any(axis=1))[0]
    cc = np.where(m.any(axis=0))[0]
    if len(rr) == 0:
        return None
    return int(cc[0]), int(rr[0]), int(cc[-1]), int(rr[-1])


def measure_region(n, kind, y0, y1, x0=None, x1=None):
    """Measure an element inside a y (and optional x) window on each side."""
    o, om, r, rm, RW, RH = base_masks(n)
    fx, fy = 960.0 / RW, 540.0 / RH
    rows = []
    for tag, img, m, is_orig in (("ORIG", o, om, True), ("REND", r, rm, False)):
        m2 = m.copy()
        cm = m2 if kind == "ink" else (cls(img, kind) & m2)
        if is_orig:
            ry0, ry1 = int(round(y0)), int(round(y1))
            rx0 = int(round(x0)) if x0 is not None else 0
            rx1 = int(round(x1)) if x1 is not None else m.shape[1]
        else:
            ry0, ry1 = int(round(y0 / fy)), int(round(y1 / fy))
            rx0 = int(round(x0 / fx)) if x0 is not None else 0
            rx1 = int(round(x1 / fx)) if x1 is not None else m.shape[1]
        sub = cm[ry0:ry1, rx0:rx1]
        lab, cnt = ndimage.label(sub)
        if cnt == 0:
            rows.append(None)
            continue
        sizes = ndimage.sum(sub, lab, range(1, cnt + 1))
        best = int(np.argmax(sizes)) + 1
        b = bbox(lab == best)
        if is_orig:
            rows.append((b[0] + rx0, b[1] + ry0, b[2] + rx0, b[3] + ry0))
        else:
            rows.append((round((b[0] + rx0) * fx, 1), round((b[1] + ry0) * fy, 1),
                         round((b[2] + rx0) * fx, 1), round((b[3] + ry0) * fy, 1)))
    return rows
