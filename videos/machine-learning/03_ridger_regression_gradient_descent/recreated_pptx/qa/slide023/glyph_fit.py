#!/usr/bin/env python3
"""Glyph-level font identification for the title of slide_023.
Segment original ink into per-glyph column runs (using per-column ink counts and
gap>1), record each glyph's x-range and top/bottom row, then compare against
PIL-rendered Arial Bold / Liberation Sans Bold at several sizes."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
d = np.abs(a - np.array([233, 233, 231])).sum(axis=2)
ink = d > 60
sub = ink[74:110, 200:680]
colcount = sub.sum(axis=0)
present = colcount > 0
xs = np.where(present)[0]


def segment(xs, gap=1):
    runs = []
    s = xs[0]; p = xs[0]
    for x in xs[1:]:
        if x > p + gap:
            runs.append((s, p)); s = x
        p = x
    runs.append((s, p))
    return runs


gr = segment(xs, 1)
print("ORIGINAL glyph runs (x_offset+200, width, top, bottom, h):")
out = []
for (s, e) in gr:
    seg = sub[:, s:e + 1]
    ys = np.where(seg.any(axis=1))[0]
    out.append((s + 200, e - s + 1, ys[0] + 74, ys[-1] + 74, ys[-1] - ys[0] + 1))
for o in out:
    print("   x%4d w%2d y%3d..%3d h%2d" % o)
print("total glyphs:", len(out))
print("first glyph x:", out[0][0], " last glyph right:", out[-1][0] + out[-1][1] - 1)
print("span:", out[-1][0] + out[-1][1] - 1 - out[0][0] + 1)

print()
for path, name in [('/usr/share/fonts/TTF/Arialbd.TTF', 'Arialbd'),
                   ('/usr/share/fonts/liberation/LiberationSans-Bold.ttf', 'LibSansBd')]:
    for size in [26, 27, 28, 29, 30, 31, 32]:
        f = ImageFont.truetype(path, size=size * 8)
        dd = ImageDraw.Draw(Image.new('L', (10, 10)))
        W = int(dd.textlength('Inverse of High Dimension Matrix', font=f)) + 40
        img = Image.new('L', (W, size * 4), 0)
        d2 = ImageDraw.Draw(img)
        d2.text((10, 10), 'Inverse of High Dimension Matrix', font=f, fill=255)
        m = np.array(img) > 128
        cc = m.any(axis=0)
        xx = np.where(cc)[0]
        rr = segment(xx, 1)
        adv = dd.textlength('Inverse of High Dimension Matrix', font=f) / 8.0
        print(f"{name} {size}pt adv={adv:.1f} nglyphs={len(rr)} "
              f"firstx={rr[0][0]-10} lastx={rr[-1][1]-10} span={rr[-1][1]-rr[0][0]+1-10}")
