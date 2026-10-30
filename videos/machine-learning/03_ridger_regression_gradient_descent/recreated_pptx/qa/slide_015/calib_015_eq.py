#!/usr/bin/env python3
r"""Banked equation calibration for slide 015 (deck 03, 2026-10-23).

Renders every equation of slide 015 in PROFESSIONAL 2D mathtext form
(stacked \frac, \partial fractions, \underline{W}) via scripts/render_eq.py
and reports the ink geometry in FRAME px (600dpi PNG -> px/8.3333) so each
image can be placed at its measured frame ink bbox and its font size chosen to
match the frame's measured ink extents.

Also probes the darkest-pixel colour of each border/ink region of the original.

Usage: python3 calib_015_eq.py
"""
import json
import os
import subprocess

import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
TMP = os.path.join(ROOT, "scratch/tmp")
ORIG = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg")
render_eq = os.path.join(ROOT, "scripts/render_eq.py")

# measured frame ink extents (forensics_015_eq.py / boxes_015.py, 2026-10-23),
# target x/y = the frame px where the image's ink must land
EQ = {
    # tag: (mathtext, measured ink x0..x1, y0..y1)
    "eq1_l1": (r"J(W) = \frac{1}{2}(Y-\hat{Y})^{T}(Y-\hat{Y}) + \frac{1}{2}\lambda W^{T}W"
               r" = \frac{1}{2}(Y-XW)^{T}(Y-XW) + \frac{1}{2}\lambda W^{T}W",
               (97, 792), (108, 151)),
    "eq1_l2": (r"J(W) = \frac{1}{2}[Y^{T}Y + (XW)^{T}(XW) - Y^{T}(XW) - (XW)^{T}Y]"
               r" + \frac{1}{2}\lambda W^{T}W",
               (97, 761), (167, 209)),
    "eq1_l3": (r"J(W) = \frac{1}{2}[Y^{T}Y + (XW)^{T}(XW) - 2(XW)^{T}Y] + \frac{1}{2}\lambda W^{T}W",
               (97, 653), (220, 263)),
    "redbox_eq": (r"\frac{\partial J(W)}{\partial W} = 0",
                  (100, 268), (288, 309)),
    "peach_eq": (r"\frac{\partial W^{T}W}{\partial W} = 2W",
                 (800, 884), (296, 330)),
    "deriv_l1": (r"\frac{\partial J(W)}{\partial W} = 0 = \frac{1}{2}[(XW)^{T}(X) + (X)^{T}(XW) - 2(X)^{T}Y] + \lambda W",
                 (78, 654), (351, 402)),
    "deriv_l2": (r"\frac{\partial J(W)}{\partial W} = 0 = \frac{1}{2}[2X^{T}XW - 2X^{T}Y] + \lambda I W",
                 (78, 500), (417, 467)),
    "normal_eq": (r"(X^{T}X + \lambda I)W = X^{T}Y",
                  (229, 520), (484, 509)),
    "solution": (r"\underline{W} = (X^{T}X + \lambda I)^{-1}X^{T}Y",
                 (560, 880), (478, 508)),
}

# per-symbol colours: (default, phantom-this-part -> colour)
COLORS = {
    "eq1_l1": ("000000", [(r"J(W)", "0000A5"), (r"\frac{1}{2}\lambda W^{T}W", "1E7B1E")]),
    "eq1_l2": ("000000", [(r"J(W)", "0000A5"), (r"\frac{1}{2}\lambda W^{T}W", "1E7B1E")]),
    "eq1_l3": ("000000", [(r"J(W)", "0000A5"), (r"\frac{1}{2}\lambda W^{T}W", "1E7B1E")]),
    "redbox_eq": ("000000", []),
    "peach_eq": ("000000", []),
    "deriv_l1": ("000000", [(r"\lambda W", "1E7B1E")]),
    "deriv_l2": ("000000", [(r"\lambda I W", "1E7B1E")]),
    "normal_eq": ("000000", [(r"\lambda I", "1E7B1E")]),
    "solution": ("000000", []),
}
PXPT = 600 / 72  # PNG px per frame pt (1 frame px = 1 pt)


def render(tex, out, fs, color):
    p = subprocess.run(["python3", render_eq, tex, out, str(fs), color],
                       capture_output=True, text=True, cwd=ROOT)
    if p.returncode != 0:
        raise SystemExit(f"render failed {tex!r}: {p.stderr[-400:]}")
    return json.loads(p.stdout)


def frame_px(info):
    return info["w_px"] / PXPT, info["h_px"] / PXPT


def mincolor(x0, y0, x1, y1, tag):
    rgb = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
    f = rgb[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    l = f.sum(axis=1)
    k = np.argsort(l)[:12]
    c = f[k].mean(axis=0)
    print(f"  {tag:24s} darkest=({c[0]:.0f},{c[1]:.0f},{c[2]:.0f}) #%02X%02X%02X"
          % tuple(int(round(v)) for v in c))


def main():
    os.makedirs(TMP, exist_ok=True)
    rgb = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
    print("=== darkest-ink colour probe (original frame)")
    mincolor(129, 68, 826, 84, "title RED words")
    mincolor(289, 68, 383, 84, "title BLUE words")
    mincolor(74, 277, 74, 331, "redbox left border")
    mincolor(709, 277, 709, 331, "redbox right border")
    mincolor(74, 276, 708, 276, "redbox top border")
    mincolor(787, 277, 787, 331, "peach border left")
    mincolor(548, 476, 548, 514, "greenbox border left")
    mincolor(548, 473, 883, 473, "greenbox border top")
    mincolor(100, 290, 650, 300, "redbox fill mode-see probe")
    mincolor(97, 108, 149, 151, "eq1 'J(W)' head")
    mincolor(200, 110, 330, 150, "eq1 body black")
    mincolor(350, 110, 430, 150, "eq1 green lambda tail")
    mincolor(560, 478, 880, 508, "greenbox solution ink")
    mincolor(229, 484, 520, 509, "normal_eq ink")

    print("\n=== equation ink geometry (frame px) at candidate font sizes")
    for tag, (tex, (x0, x1), (y0, y1)) in EQ.items():
        mw, mh = x1 - x0 + 1, y1 - y0 + 1
        print(f"\n{tag}  measured {mw}x{mh}px")
        for fs in (16, 18, 20, 22, 24):
            info = render(tex, f"{TMP}/cal_{tag}_{fs}.png", fs, "000000")
            w, h = frame_px(info)
            print(f"   fs={fs:2d}: {w:6.1f} x {h:5.1f}   (dw={w-mw:+6.1f} dh={h-mh:+5.1f})")


if __name__ == "__main__":
    main()
