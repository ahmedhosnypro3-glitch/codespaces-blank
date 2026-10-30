#!/usr/bin/env python3
"""scope_r4 adjudication measurements — slide 011 (judge_attempt_2 MAJOR findings).

PIL/numpy measurement of BOTH the recreation render and the original frame.
A judge finding survives only if pixels confirm it.
"""
import numpy as np
from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
R = np.asarray(Image.open(f"{VID}/qa/slide011/rejudge/render-1.png").convert("RGB")).astype(int)
O = np.asarray(Image.open(f"{VID}/unique_slides/slide_011.jpg").convert("RGB")).astype(int)
DPI = 150


def box(a, x0, y0, x1, y1):
    return a[int(y0 * DPI):int(y1 * DPI), int(x0 * DPI):int(x1 * DPI)]


def rep(name, m):
    n = int(m.sum())
    if n == 0:
        print(f"{name}: 0 px")
        return None
    ys, xs = np.nonzero(m)
    print(f"{name}: {n} px  bbox_px=({xs.min()},{ys.min()})-({xs.max()},{ys.max()}) "
          f"in=({xs.min()/DPI:.2f},{ys.min()/DPI:.2f})-({xs.max()/DPI:.2f},{ys.max()/DPI:.2f})")
    return (xs.min(), ys.min(), xs.max(), ys.max())


def near(a, rgb, tol):
    return (np.abs(a - np.array(rgb)).max(axis=2) <= tol)


print("=== M1  yellow 'Output' overlay vs title glyphs (RENDER) ===")
title = box(R, 0.0, 0.20, 13.33, 0.95)
yellow = near(title, (255, 215, 0), 70)
red = near(title, (192, 0, 0), 80)
yb = rep("render title-band yellow", yellow)
rb = rep("render title-band red(C00000)", red)
if yb and rb:
    yx0, yy0, yx1, yy1 = yb
    rx0, ry0, rx1, ry1 = rb
    overlap_x = min(yx1, rx1) - max(yx0, rx0)
    overlap_y = min(yy1, ry1) - max(yy0, ry0)
    print(f"  yellow-vs-red bbox intersection: {overlap_x}x{overlap_y} px "
          f"({'COLLISION' if overlap_x > 0 and overlap_y > 0 else 'no overlap'})")
    inside = int(red[yy0:yy1 + 1, yx0:yx1 + 1].sum())
    print(f"  red title pixels INSIDE yellow bbox: {inside}")
    dil = yellow.copy()
    for _ in range(3):
        dil |= np.roll(dil, 1, 0) | np.roll(dil, -1, 0) | np.roll(dil, 1, 1) | np.roll(dil, -1, 1)
    near_red = int((red & dil).sum())
    print(f"  red title pixels within 3px of yellow: {near_red} "
          f"({'yellow sits ON the red glyphs' if near_red > 50 else 'yellow clear of red glyphs'})")

print("\n=== M1b same band, ORIGINAL frame (scaled to 150dpi coords) ===")
Ot = np.asarray(Image.open(f"{VID}/unique_slides/slide_011.jpg").convert("RGB")
                .resize((int(13.33 * DPI), int(7.5 * DPI)), Image.LANCZOS)).astype(int)
title_o = box(Ot, 0.0, 0.20, 13.33, 0.95)
yellow_o = near(title_o, (255, 215, 0), 70)
red_o = near(title_o, (192, 0, 0), 80)
ybo = rep("original title-band yellow", yellow_o)
rbo = rep("original title-band red(C00000)", red_o)
if ybo and rbo:
    ys, xs = np.nonzero(yellow_o)
    rs, rx = np.nonzero(red_o)
    print(f"  original: yellow inside red title span? "
          f"{'YES (highlight behind text)' if ((xs >= rx.min()) & (xs <= rx.max())).sum() > 0.5 * len(xs) else 'NO'}")
