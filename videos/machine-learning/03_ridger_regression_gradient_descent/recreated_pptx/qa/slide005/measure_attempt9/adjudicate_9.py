#!/usr/bin/env python3
"""PIL adjudication helpers for slide 005 attempt-9 verdicts (both legs).

Banked go-tos, measured on BOTH images before any build change:
  * accept `<3 ink px per column/row` = JPEG noise (the 45px phantom band), never draw it
  * reuse the prior band measurements from ink_bands_slide005.json / eq_fit_slide005.json
Every FAIL/MINOR a judge raises is re-measured here against BOTH images first.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

Q = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
       "03_ridger_regression_gradient_descent")
ORIG = os.path.join(VID, "unique_slides/slide_005.jpg")
REND = os.path.join(Q, "render_9.png")
SX, SY = 2001 / 960.0, 1125 / 540.0
TOL = 8.0
MININK = 3  # <3 ink px per column/row => noise

REG = {
    "eq1": (90, 552, 105, 154), "eq2": (90, 637, 168, 218), "eq3": (90, 530, 225, 275),
    "eq4": (90, 600, 371, 421), "eq5": (90, 640, 456, 506),
    "pinkfrac": (77, 170, 293, 338), "rem1": (675, 874, 210, 240),
    "rem2": (650, 876, 392, 424), "green": (692, 876, 466, 496),
    "title": (160, 812, 66, 92), "rememberU": (678, 764, 136, 152),
    "rememberL": (654, 734, 374, 392), "getbest": (185, 504, 302, 328),
}


def load():
    o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
    r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
    return o, r


def ink(arr, x0, x1, y0, y1, sx, sy, thr=200):
    X0, X1, Y0, Y1 = int(x0 * sx), int(x1 * sx), int(y0 * sy), int(y1 * sy)
    sub = arr[Y0:Y1 + 1, X0:X1 + 1].mean(axis=2) < thr
    if not sub.any():
        return None
    ys, xs = np.nonzero(sub)
    return ((X0 + xs.min()) / sx, (Y0 + ys.min()) / sy,
            (X0 + xs.max()) / sx, (Y0 + ys.max()) / sy)


def band_deltas(o=None, r=None):
    if o is None or r is None:
        o, r = load()
    out, worst = {}, 0.0
    for k, w in REG.items():
        ob, rb = ink(o, *w, 1, 1), ink(r, *w, SX, SY)
        if ob is None or rb is None:
            out[k] = None
            continue
        d = tuple(rb[i] - ob[i] for i in range(4))
        w_ = max(abs(v) for v in d)
        out[k] = (d, w_)
        worst = max(worst, w_)
    return out, worst


def noise_reject_columns(arr, x0, x1, y0, y1, sx, sy, minink=MININK):
    """Real glyph groups: ink columns with >=minink ink rows, merged across <3px gaps.
    Columns/rows with <minink px are rejected as JPEG noise."""
    X0, X1, Y0, Y1 = int(x0 * sx), int(x1 * sx), int(y0 * sy), int(y1 * sy)
    sub = arr[Y0:Y1 + 1, X0:X1 + 1].mean(axis=2) < 200
    cs = sub.sum(axis=0)
    g = 3.0
    out, s = [], None
    for i, v in enumerate(cs):
        if v >= minink and s is None:
            s = i
        elif v < minink and s is not None:
            nxt = i
            while nxt < len(cs) and cs[nxt] < minink:
                nxt += 1
            if nxt - i >= g or nxt >= len(cs):
                out.append(((X0 + s) / sx, (X0 + i - 1) / sx))
                s = None
    if s is not None:
        out.append(((X0 + s) / sx, (X0 + len(cs) - 1) / sx))
    return [x for x in out if x[1] - x[0] >= 2.5]


def frame_containment(r=None):
    if r is None:
        _, r = load()
    dark = r.mean(axis=2) < 200
    zones = {
        "left_of_stroke(x<58)": dark[:, :int(58 * SX)],
        "right_of_stroke(x>902)": dark[:, int(902 * SX):],
        "above_panel(y<44)": dark[:int(44 * SY), :],
        "below_bottom(y>539.5)": dark[int(539.5 * SY):, :],
    }
    return {k: int(v.sum()) for k, v in zones.items()}


def banked_bands():
    p = os.path.join(Q, "ink_bands_slide005.json")
    return json.load(open(p)) if os.path.exists(p) else None


if __name__ == "__main__":
    o, r = load()
    bands, worst = band_deltas(o, r)
    print("== INK-BAND DELTAS render_9 vs original (frame px) ==")
    for k, v in bands.items():
        if v is None:
            print(f"  {k:10s} SKIP (empty region)")
            continue
        d, w_ = v
        print(f"  {k:10s} dx0={d[0]:+.2f} dy0={d[1]:+.2f} dx1={d[2]:+.2f} dy1={d[3]:+.2f} "
              f"worst={w_:.2f} {'<=TOL' if w_ <= TOL else '>*TOL'}")
    print(f"  WORST = {worst:.2f} frame px (TOL {TOL})")
    print("== HOUSE-FRAME CONTAINMENT ==")
    for k, v in frame_containment(r).items():
        print(f"  {k:24s} {v} px {'OK' if v == 0 else 'OVERFLOW'}")
    print("== eq5 NOISE-REJECTED GROUPS (the 45px phantom refutation) ==")
    print("  ORIG:", noise_reject_columns(o, 90, 686, 456, 508, 1, 1))
    print("  REND:", noise_reject_columns(r, 90, 686, 456, 508, SX, SY))
