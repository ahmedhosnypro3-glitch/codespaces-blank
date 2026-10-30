#!/usr/bin/env python3
"""Adjudicate_9e — isolate each label glyph in BOTH images and print character
templates from the build's own serif so every chip can be identified by shape.

Original: right label sits at approximately x730..756, y141..153 (the chord/dot
blob ends at x727). Render: build draws "(7, 7)" left-aligned at x724.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

o = np.asarray(Image.open(V + "/unique_slides/slide_032.jpg").convert("L")).astype(float)
rim = Image.open(V + "/recreated_pptx/qa/slide032/render_9.png").convert("L")
S = rim.size[1] / 540.0


def patch(a, x0, y0):
    print(f"  x{x0}..{x0 + a.shape[1]} y{y0}..{y0 + a.shape[0]}")
    for ry in range(a.shape[0]):
        print(f"  {int(y0) + ry:>3} " + "".join(
            "#" if v < 120 else ("+" if v < 175 else ("." if v < 225 else " ")) for v in a[ry, :]))


def clusters(sub, x0, y0, S_, gap=2, minpx=2):
    """column clusters of ink (lum<225) with their bboxes and pixel counts"""
    m = sub < 225
    cols = m.sum(axis=0)
    nz = np.nonzero(cols)[0]
    if len(nz) == 0:
        return []
    runs, start = [], nz[0]
    for a, b in zip(nz, nz[1:]):
        if b - a > gap:
            runs.append((start, a)); start = b
    runs.append((start, nz[-1]))
    out = []
    for a, b in runs:
        seg = m[:, a:b + 1]
        rs = np.nonzero(seg.sum(axis=1))[0]
        n = int(seg.sum())
        if n >= minpx and (b - a) >= 0:
            out.append((x0 + a / S_, x0 + b / S_, y0 + rs[0] / S_, y0 + rs[-1] / S_, n))
    return out


print("=" * 76)
print("ORIG label region — ink clusters (frame x731..762, y138..156)")
ox0, oy0, ox1, oy1 = 731, 138, 762, 156
osub = o[oy0:oy1, ox0:ox1]
for c in clusters(osub, ox0, oy0, 1.0):
    print(f"  cluster x{c[0]:.0f}..{c[1]:.0f} y{c[2]:.0f}..{c[3]:.0f}  px={c[4]}")
print()
print("ORIG full label, one glyph-group at a time:")
patch(o[oy0:oy1, ox0:ox1], ox0, oy0)

print()
print("=" * 76)
print("REND label region — ink clusters at native res, reported in frame px")
rx0, ry0, rx1, ry1 = 731, 138, 762, 156
rsub = np.asarray(rim.crop((int(rx0 * S), int(ry0 * S), int(rx1 * S), int(ry1 * S)))).astype(float)
for c in clusters(rsub, rx0, ry0, S):
    print(f"  cluster x{c[0]:.1f}..{c[1]:.1f} y{c[2]:.1f}..{c[3]:.1f}  px={c[4]} (native)")
print()
patch(rsub, rx0, ry0)

print()
print("=" * 76)
print("FONT TEMPLATES the build's serif family (Liberation Serif)")
print("=" * 76)
for ch in "0123456789()?, ":
    for sz in (8, 9, 10, 11):
        f = ImageFont.truetype(FONT, sz)
        bb = f.getbbox(ch)
        im = Image.new("L", (bb[2] - bb[0] + 2, bb[3] - bb[1] + 2), 255)
        d = ImageDraw.Draw(im)
        d.text((1 - bb[0], 1 - bb[1]), ch, font=f, fill=0)
        a = np.asarray(im).astype(float)
        if ch == " ":
            continue
        print(f"  --- {ch!r} size {sz} ---")
        for ry in range(a.shape[0]):
            print("      " + "".join("#" if v < 120 else ("+" if v < 175 else ("." if v < 225 else " "))
                                     for v in a[ry, :]))
