#!/usr/bin/env python3
"""Slide 003 PIL adjudication, take 6 (single-step burst 2).

Settles the take-5 judge findings against BOTH the ORIGINAL frame and the
CURRENT render (render_5.png, built from build/slide_003.js @ 2026-10-24 00:56),
both in 960x540 frame-px space. Judge findings are hypotheses; the frame wins.

Usage: python3 adjudicate_6.py <region> [...]
  regions: br bl top brfull blfull title remember ingeneral arrow wvector topband
"""
import sys
import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
B = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{B}/unique_slides/slide_003.jpg"
RENDER = f"{B}/recreated_pptx/qa/slide003/render_5.png"
FRAME_H = 540.0

REGIONS = {
    # judge-disputed regions (frame px, with padding)
    "br":        (560, 310, 765, 530),   # bottom-right box (Where block)
    "bl":        (60, 310, 545, 530),    # bottom-left expanded equation
    "top":       (260, 95, 610, 315),    # top matrix box
    "topband":   (280, 110, 605, 305),   # inside top box (bands)
    "title":     (55, 55, 900, 105),     # title band (line count)
    "remember":  (640, 145, 885, 230),   # Remember box
    "ingeneral": (650, 260, 860, 300),   # In General box
    "arrow":     (520, 320, 585, 415),   # connector arrow
    "wvector":   (340, 330, 430, 500),   # w-vector + bracket region
    "matrixlab": (140, 470, 340, 500),   # dimension labels under matrix
}


def load(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    return im, im.shape[0] / FRAME_H


def cls(r, g, b):
    if r > 240 and g > 240 and b > 240:
        return " "
    if abs(r - 233) < 16 and abs(g - 233) < 16 and abs(b - 231) < 18:
        return "."
    if r < 100 and g < 100 and b < 100:
        return "#"
    if r > 145 and r - g > 45 and r - b > 45:
        return "R"
    if b > 145 and b - r > 30:
        return "B"
    if r > 235 and g > 235 and b < 215:
        return "Y"
    if g > 215 and b > 215 and r < 225:
        return "C"
    if r > 225 and 165 < g < 225 and 160 < b < 228:
        return "P"
    return "?"


def ascii_map(a, s, reg, sx=2, sy=2, label=""):
    x0, y0, x1, y1 = reg
    print(f"--- {label} frame x{x0}..{x1} y{y0}..{y1} (1 col={sx}px, 1 row={sy}px) ---")
    hdr = "".join(str((x0 + i * sx) // 100 % 10) for i in range((x1 - x0) // sx))
    print("      " + hdr)
    for y in range(y0, y1, sy):
        cols = []
        for x in range(x0, x1, sx):
            vals = {}
            for dy in range(sy):
                yy = y + dy
                if yy >= a.shape[0]:
                    continue
                for dx in range(sx):
                    xx = x + dx
                    if xx >= a.shape[1]:
                        continue
                    c = cls(*a[yy, xx])
                    vals[c] = vals.get(c, 0) + 1
            if not vals:
                cols.append(" ")
                continue
            best = max(vals, key=vals.get)
            if best in (" ", ".") and sum(v for k, v in vals.items()
                                         if k not in (" ", ".")) >= 2:
                ink = [k for k in vals if k not in (" ", ".")]
                best = max(ink, key=vals.get)
            cols.append(best)
        print(f"{y:5d} " + "".join(cols))


def row_ink(a, s, reg):
    """Non-background ink pixel count per row, frame px."""
    x0, y0, x1, y1 = reg
    sub = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    bg = (np.abs(sub[:, :, 0] - 233) < 16) & (np.abs(sub[:, :, 1] - 233) < 16) & \
         (np.abs(sub[:, :, 2] - 231) < 18)
    wht = (sub[:, :, 0] > 240) & (sub[:, :, 1] > 240) & (sub[:, :, 2] > 240)
    ink = ~(bg | wht)
    return ink.sum(axis=1)


def color_hist(a, s, reg):
    x0, y0, x1, y1 = reg
    sub = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    sub = sub.reshape(-1, 3)
    # exclude gray panel + white
    nonbg = ~((np.abs(sub[:, 0] - 233) < 16) & (np.abs(sub[:, 1] - 233) < 16) &
              (np.abs(sub[:, 2] - 231) < 18)) & ~((sub[:, 0] > 240) & (sub[:, 1] > 240) &
                                                  (sub[:, 2] > 240))
    red = ((sub[:, 0] > 145) & (sub[:, 0] - sub[:, 1] > 45) &
           (sub[:, 0] - sub[:, 2] > 45) & nonbg).sum()
    blue = ((sub[:, 2] > 145) & (sub[:, 2] - sub[:, 0] > 30) & nonbg).sum()
    dark = ((sub[:, 0] < 100) & (sub[:, 1] < 100) & (sub[:, 2] < 100) & nonbg).sum()
    return {"red": int(red), "blue": int(blue), "dark": int(dark),
            "nonbg": int(nonbg.sum())}


def main():
    ao, so = load(ORIG)
    for name in sys.argv[1:]:
        reg = REGIONS[name]
        print("=" * 78)
        print(f"REGION {name} {reg}")
        for which, a, s in (("ORIG", ao, so), ("RENDER", None, None)):
            if which == "RENDER":
                a, s = load(RENDER)
            x0, y0, x1, y1 = reg
            ri = row_ink(a, s, reg)
            rows_with_ink = [(y0 + i / s, int(v)) for i, v in enumerate(ri) if v > 6]
            # compress to bands
            bands = []
            for y, v in rows_with_ink:
                if bands and y - bands[-1][1] <= 3.5:
                    bands[-1][1] = y
                    bands[-1][2] += v
                else:
                    bands.append([y, y, v])
            print(f"  {which}: size {a.shape[1]}x{a.shape[0]} ink-row bands "
                  f"(y-range, inkpx): "
                  + ", ".join(f"{b[0]:.0f}-{b[1]:.0f}({b[2]})" for b in bands))
            h = color_hist(a, s, reg)
            print(f"  {which}: colors red={h['red']} blue={h['blue']} dark={h['dark']} "
                  f"nonbg={h['nonbg']}")
        ascii_map(ao, so, reg, label=f"ORIG:{name}")
        ar, sr = load(RENDER)
        ascii_map(ar, sr, reg, label=f"RENDER:{name}")
        print()


if __name__ == "__main__":
    main()
