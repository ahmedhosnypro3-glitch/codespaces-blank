#!/usr/bin/env python3
"""scope_r4: original-frame color evidence for slide 011 fixes."""
import numpy as np
from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
DPI = 150
O = np.asarray(Image.open(f"{VID}/unique_slides/slide_011.jpg").convert("RGB")
               .resize((2001, 1125), Image.LANCZOS)).astype(int)
R = np.asarray(Image.open(f"{VID}/qa/slide011/rejudge/render-1.png").convert("RGB")).astype(int)


def near(a, rgb, tol):
    return np.abs(a - np.array(rgb)).max(axis=2) <= tol


print("### original: red pixel x-clusters in the bottom strip (blue-bordered box) ###")
strip = O[int(6.4 * DPI):int(7.2 * DPI), int(0.3 * DPI):int(13.0 * DPI)]
red = near(strip, (192, 0, 0), 60)
ys, xs = np.nonzero(red)
print(f"red px in strip: {len(xs)}")
if len(xs):
    # cluster by contiguous x runs
    order = np.argsort(xs)
    xs_s = xs[order]
    breaks = np.nonzero(np.diff(xs_s) > 12)[0]
    clusters = np.split(xs_s, breaks + 1)
    for c in clusters:
        print(f"  x-cluster {(0.3 + c.min()/DPI):.2f}-{(0.3 + c.max()/DPI):.2f}in  n={len(c)}")
print("\n### original: median color of the yellow title highlight ###")
t = O[int(0.40 * DPI):int(0.95 * DPI), int(7.28 * DPI):int(8.41 * DPI)]
yel = near(t, (255, 215, 0), 90)
px = t[yel]
print(f"n={len(px)}  median RGB={np.median(px, axis=0).astype(int)}")
print(f"render yellow 'Output' glyph median RGB="
      f"{np.median(R[int(0.22*DPI):int(0.51*DPI), int(5.57*DPI):int(6.63*DPI)].reshape(-1,3)[near(R[int(0.22*DPI):int(0.51*DPI), int(5.57*DPI):int(6.63*DPI)], (255,215,0), 70)], axis=0).astype(int)}")

print("\n### original: dark-line ink in the diagram fan zones (x 4.3-5.45, y 2.6-5.8) ###")
for x0, x1 in ((2.75, 3.75), (4.30, 5.45), (6.35, 7.15), (8.05, 8.95)):
    b = O[int(2.6 * DPI):int(5.8 * DPI), int(x0 * DPI):int(x1 * DPI)]
    dark = (b.mean(axis=2) < 150)
    ys2, xs2 = np.nonzero(dark)
    print(f"  band x{x0}-{x1}: dark px={dark.sum()}  "
          f"x-span {(x0 + xs2.min()/DPI):.2f}-{(x0 + xs2.max()/DPI):.2f}in  "
          f"y-span {(2.6 + ys2.min()/DPI):.2f}-{(2.6 + ys2.max()/DPI):.2f}in" if dark.sum()
          else f"  band x{x0}-{x1}: none")
