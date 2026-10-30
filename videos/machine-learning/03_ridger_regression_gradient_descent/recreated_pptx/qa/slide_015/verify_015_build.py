#!/usr/bin/env python3
r"""Build-verification for slide 015, attempt 3 (render_3.png vs the original).

PIL-first adjudication harness: 960x540 original (1 frame px == 1 pt == 1/200 in
at 150dpi) against the 2001x1125 render.  Measures, for every element:
  - ink census (dark-pixel counts and bbox) inside windows that exclude borders
  - alignment: origin vs render ink bbox in slide px, and the w/h ratios
  - fills/borders sampled from BOTH images at the element's core pixels
Nothing here fixes anything; it is the evidence layer for adjudicating any judge
finding and for proving the build is current.

Usage: verify_015_build.py [render_path]
"""
import sys

import numpy as np
from PIL import Image

D = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

# (label, y0, y1, x0, x1) window INTERIOR to the element (excludes its border)
WINDOWS = [
    ("title", 66, 86, 122, 850),
    ("redsentence", 294, 318, 210, 706),
    ("Remember", 277, 292, 788, 860),
    ("eq1_l1", 104, 152, 95, 795),
    ("eq1_l2", 163, 211, 95, 765),
    ("eq1_l3", 217, 264, 95, 656),
    ("redbox_eq", 278, 302, 78, 208),
    ("peach_eq", 295, 328, 788, 892),
    ("deriv_l1", 350, 403, 76, 655),
    ("deriv_l2", 416, 468, 76, 500),
    ("normal", 482, 510, 226, 545),
    ("solution", 477, 511, 552, 882),
]

# (label, want_hex, [(y, x), ...]) sampled OUTSIDE the element's ink
FILLS = [
    ("creamA", "FBFDE5", [(110, 700), (250, 700), (110, 120)]),
    ("creamB", "FBFDE5", [(350, 400), (500, 400), (350, 120)]),
    ("pink",   "F7D0D3", [(300, 300), (285, 600), (330, 600)]),
    ("peach",  "F7DCBE", [(278, 830), (300, 880), (325, 830)]),
    ("green",  "CFFFE3", [(490, 700), (505, 700), (490, 600)]),
    ("title_red", "C00000", [(76, 300), (76, 380)]),
    ("title_blue", "00008B", [(76, 600), (76, 640)]),
]


def hexdiff(h, rgb):
    return sum(abs(int(h[2 * i:2 * i + 2], 16) - rgb[i]) for i in range(3))


def main():
    rend = sys.argv[1] if len(sys.argv) > 1 else f"{D}/recreated_pptx/qa/slide_015/render_3.png"
    o = np.asarray(Image.open(f"{D}/unique_slides/slide_015.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(rend).convert("RGB")).astype(int)
    F = r.shape[1] / 960.0
    oL = o.mean(axis=2)
    rL = r.mean(axis=2)
    print(f"original {oL.shape} render {r.shape} scale F={F:.4f} (render px per frame px)")
    print(f"deck target 1px=1pt, 150dpi => expected 2001/960={2001/960:.4f}\n")
    print(f"NOTE: ink counts are compared at equal EFFECTIVE AREA: the render covers"
          f" F^2={F * F:.2f} px per frame px, so the render's raw count is scaled"
          f" down by F^2 before comparison.\n")

    print("== INK CENSUS + ALIGNMENT (luma<150) ==")
    bad = 0
    for label, y0, y1, x0, x1 in WINDOWS:
        om = oL[y0:y1 + 1, x0:x1 + 1] < 150
        rm = rL[int(y0 * F):int(y1 * F), int(x0 * F):int(x1 * F)] < 150
        oc, rc = int(om.sum()), int(rm.sum())
        rc_n = rc / (F * F)  # equal-area comparison
        flag = ""
        if oc == 0 or rc == 0:
            flag = "  <-- INK MISSING"
            bad += 1
        elif min(oc, rc_n) / max(oc, rc_n) < 0.7:
            flag = "  <-- CENSUS MISMATCH"
            bad += 1
        oy, ox = np.where(om)
        ry, rx = np.where(rm)
        if len(oy):
            ob = (x0 + ox.min(), x0 + ox.max(), y0 + oy.min(), y0 + oy.max())
        else:
            ob = (-1, -1, -1, -1)
        if len(ry):
            rb = (x0 + rx.min() / F, x0 + rx.max() / F,
                  y0 + ry.min() / F, y0 + ry.max() / F)
            dx = rb[0] - ob[0]
            dy = rb[2] - ob[2]
        else:
            rb, dx, dy = (-1, -1, -1, -1), 0, 0
        print(f"{label:13s} ink orig={oc:6d} rend={rc_n:6.0f} (raw {rc:6d}) ratio={oc / max(rc_n, 1):.2f}{flag}")
        print(f"{'':13s}   orig bbox x{ob[0]}..{ob[1]} y{ob[2]}..{ob[3]} | "
              f"rend bbox x{rb[0]:.0f}..{rb[1]:.0f} y{rb[2]:.0f}..{rb[3]:.0f} | delta dx={dx:+.0f} dy={dy:+.0f}")

    print("\n== FILL / INK COLOUR (sampled in both images) ==")
    for label, want, pts in FILLS:
        for y, x in pts:
            rgb = tuple(o[min(max(y, 0), 539), min(max(x, 0), 959)])
            rr = tuple(r[int(y * F), int(x * F)])
            eo = hexdiff(want, rgb)
            er = hexdiff(want, rr)
            print(f"{label:11s} ({x},{y}) want #{want} orig #{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X} "
                  f"err={eo:3d} | rend #{rr[0]:02X}{rr[1]:02X}{rr[2]:02X} err={er:3d}"
                  + ("  <-- OUT" if max(eo, er) > 40 else ""))

    print("\n== HOUSE PANEL / STROKE PRESENCE ==")
    px = lambda v: int(round(v * F))
    panel_o = oL[45:540, 54:904]
    panel_r = rL[94:, 112:1884]
    print(f"panel lum orig mean={panel_o.mean():.1f} rend mean={panel_r.mean():.1f}")
    for name, cols in (("left stroke", px(58.5)), ("right stroke", px(901))):
        col_o = int((oL[46:539, cols - 1:cols + 2] < 160).sum())
        col_r = int((rL[96:, cols - 1:cols + 2] < 160).sum())
        print(f"{name}: orig red px={col_o} rend red px={col_r}")
    row = int(round(538.5 * F))
    bot_o = int((oL[535:540, 58:903] < 160).sum())
    bot_r = int((rL[row - 3:row + 4, px(58):px(903)] < 160).sum())
    print(f"bottom stroke: orig red px={bot_o} rend red px={bot_r}")
    top_o = int((oL[0:30, 0:960] < 160).sum())
    top_r = int((rL[0:62, :] < 160).sum())
    print(f"top band red px (must be 0): orig={top_o} rend={top_r}")

    print(f"\nRESULT: {bad} elements with a census/missing flag")


if __name__ == "__main__":
    main()
