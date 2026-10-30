#!/usr/bin/env python3
"""Slide 019 — full-resolution darkness maps of the label bands (original vs render).

Gridlines/curves are thin single rows; text glyphs are dense. 4-level luminance
ramp keeps both readable without a vision call.
"""
import numpy as np
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_019.jpg"
RENDER = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_019_rendered-1.png"


def lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


RAMP = {0: " ", 1: ".", 2: "+", 3: "#"}  # 0 bright .. 3 dark


def ramp(a):
    l = lum(a)
    t = np.zeros(l.shape, dtype=int)
    t[l < 170] = 3
    t[(l >= 170) & (l < 195)] = 2
    t[(l >= 195) & (l < 212)] = 1
    return t, RAMP


def show(arr, x0, y0, x1, y1, sx=1, sy=1, title=""):
    H, W = arr.shape[:2]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    sub = rampsub(arr[y0:y1, x0:x1])
    print(f"\n  -- {title}  box x={x0}..{x1} y={y0}..{y1} (step x{sx} y{sy}) --")
    print("       " + "".join(str(((x0 + i * sx) // 10) % 10) if (x0 + i * sx) % 10 == 0 else " "
                             for i in range(0, sub.shape[1], sx)))
    for r, yy in enumerate(range(0, sub.shape[0], sy)):
        print(f"  {y0 + yy * sy:5d} " + "".join(RAMP[sub[yy, c]] for c in range(0, sub.shape[1], sx)))


def rampsub(sub):
    return ramp(sub)[0]


def main():
    o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
    s = 2001 / 960
    ri = Image.open(RENDER).convert("RGB").resize((2001, 1125), Image.LANCZOS)
    r = np.asarray(ri).astype(int)
    fr = lambda v: int(round(v * s))

    print("========== ORIGINAL ==========")
    show(o, 106, 60, 260, 118, 2, 2, "ORIG sigmoid panel: y-label + legend band")
    show(o, 106, 60, 260, 118, 1, 1, "ORIG sigmoid legend left half (full res)")
    show(o, 500, 60, 640, 118, 2, 2, "ORIG tanh panel: y-label band")
    show(o, 500, 298, 700, 334, 1, 2, "ORIG arctan panel: title band")
    show(o, 106, 298, 260, 360, 2, 2, "ORIG tan panel: y-label band")

    print("\n========== RENDER (frame coords) ==========")
    show(r, fr(106), fr(60), fr(260), fr(118), 2, 2, "RENDER sigmoid panel: y-label + legend band")
    show(r, fr(500), fr(60), fr(640), fr(118), 2, 2, "RENDER tanh panel: y-label band")
    show(r, fr(500), fr(298), fr(700), fr(334), 1, 2, "RENDER arctan panel: title band")
    show(r, fr(106), fr(298), fr(260), fr(360), 2, 2, "RENDER tan panel: y-label band")


if __name__ == "__main__":
    main()
