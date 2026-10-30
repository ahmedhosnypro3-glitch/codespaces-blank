#!/usr/bin/env python3
"""Detect filled/stroked circles (nodes) and their colors in a slide region.

Finds connected blobs of saturated ink and circles, reports center/radius + color.
Usage: python3 a18_circles.py <slide#> <x0> <y0> <x1> <y1>
"""
import sys
from PIL import Image
import numpy as np
from scipy import ndimage

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"


def color_name(px):
    r, g, b = px
    if r > 200 and g > 190 and b < 175: return "YELLOW"
    if b > 130 and b - r > 45 and b - g > 25: return "BLUE"
    if g > 100 and g - r > 30 and g - b > 30: return "GREEN"
    if r > 180 and r - g > 60 and r - b > 60: return "RED"
    if r > 190 and 70 < g < 180 and b < 120: return "ORANGE"
    if r > 120 and b > 140 and g < 115: return "PURPLE"
    return "INK"


def main():
    n = int(sys.argv[1])
    x0, y0, x1, y1 = [int(v) for v in sys.argv[2:6]]
    im = Image.open(f"{BASE}/slide_{n:03d}.jpg").convert("RGB").crop((x0, y0, x1, y1))
    a = np.asarray(im).astype(int)
    h, w = a.shape[:2]
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

    # 1. Strongly colored circles (yellow/blue/green fills)
    for name, m in (("YELLOW", (r > 190) & (g > 175) & (b < 170)),
                    ("BLUE", (b > 130) & (b - r > 45) & (b - g > 25)),
                    ("GREEN", (g > 95) & (g - r > 30) & (g - b > 30)),
                    ("RED", (r > 140) & (r - g > 55) & (r - b > 55))):
        m = m & (a.mean(axis=2) < 250)
        lab, cnt = ndimage.label(m, np.ones((3, 3)))
        if cnt == 0:
            continue
        sizes = ndimage.sum(m, lab, range(1, cnt + 1))
        objs = ndimage.find_objects(lab)
        # merge nearby blobs into circle rows by proximity
        blobs = [(i + 1, int(sizes[i])) for i in range(cnt) if sizes[i] > 25]
        for idx, sz in sorted(blobs, key=lambda t: -t[1])[:14]:
            sl = objs[idx - 1]
            bh = sl[0].stop - sl[0].start
            bw = sl[1].stop - sl[1].start
            if bh < 5 or bw < 5:
                continue
            fill = m[sl[0].start:sl[0].stop, sl[1].start:sl[1].stop]
            fill_ratio = fill.mean()
            cx = x0 + (sl[1].start + sl[1].stop) / 2
            cy = y0 + (sl[0].start + sl[0].stop) / 2
            if 0.55 < fill_ratio < 0.95 and abs(bh - bw) <= max(4, 0.3 * bh):
                print(f"  {name} circle? bbox x {x0+sl[1].start}..{x0+sl[1].stop} "
                      f"y {y0+sl[0].start}..{y0+sl[0].stop} c=({cx:.0f},{cy:.0f}) "
                      f"r={bh/2:.0f} size={sz} fill={fill_ratio:.2f}")
            else:
                print(f"  {name} blob   bbox x {x0+sl[1].start}..{x0+sl[1].stop} "
                      f"y {y0+sl[0].start}..{y0+sl[0].stop} size={sz} fill={fill_ratio:.2f}")

    # 2. Detect gray/black stroked circles via circular Hough-ish: find ring
    #    pixel count using distance transform on dark ink
    ink = (a.mean(axis=2) < 190)
    lab, cnt = ndimage.label(ink, np.ones((3, 3)))
    sizes = ndimage.sum(ink, lab, range(1, cnt + 1))
    objs = ndimage.find_objects(lab)
    print("-- dark-ink blobs (possible node outlines):")
    for i in range(cnt):
        if sizes[i] < 20:
            continue
        sl = objs[i]
        bh = sl[0].stop - sl[0].start
        bw = sl[1].stop - sl[1].start
        if bh < 6 or bw < 6:
            continue
        sub = ink[sl[0].start:sl[0].stop, sl[1].start:sl[1].stop]
        fill = sub.mean()
        cx = x0 + (sl[1].start + sl[1].stop) / 2
        cy = y0 + (sl[0].start + sl[0].stop) / 2
        if 0.45 < fill < 0.9 and abs(bh - bw) <= max(4, 0.3 * bh):
            print(f"   ring? bbox x {x0+sl[1].start}..{x0+sl[1].stop} "
                  f"y {y0+sl[0].start}..{y0+sl[0].stop} c=({cx:.0f},{cy:.0f}) "
                  f"d={bh} size={int(sizes[i])} fill={fill:.2f}")


main()
