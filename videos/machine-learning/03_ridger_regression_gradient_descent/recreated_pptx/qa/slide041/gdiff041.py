#!/usr/bin/env python3
"""Side-by-side ASCII comparison: original glyph cell vs rendered candidate glyph."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ORIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "unique_slides", "slide_041.jpg"))
im = Image.open(ORIG).convert("RGB")
A = np.asarray(im).astype(int)

FONTS = {
    "LS": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "LSB": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "LSI": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "DVS": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "DVSB": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
}


def ink_mask(x0, y0, x1, y1):
    a = A[y0:y1, x0:x1]
    d = np.abs(a - np.array([254, 255, 232])).sum(axis=2)
    return d > 90


def norm(m):
    ys, xs = np.nonzero(m)
    if not len(ys):
        return None
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def render(ch, fp, size):
    f = ImageFont.truetype(fp, size)
    img = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(img).text((size, size), ch, font=f, fill=255)
    a = np.asarray(img) > 90
    ys, xs = np.nonzero(a)
    if not len(ys):
        return None
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def pad(m, h, w):
    o = np.zeros((h, w), bool)
    o[:m.shape[0], :m.shape[1]] = m
    return o


def iou(a, b):
    h = max(a.shape[0], b.shape[0]); w = max(a.shape[1], b.shape[1])
    A_ = pad(a, h, w); B_ = pad(b, h, w)
    u = np.logical_or(A_, B_).sum()
    return np.logical_and(A_, B_).sum() / u if u else 0


def show(m):
    return "\n".join("".join("#" if v else "." for v in row) for row in m)


TARGETS = {
    "L4_r2": (159, 95, 168, 107),
    "R1_r2": (601, 95, 611, 109),
    "R1_r1": (601, 82, 611, 94),
    "L4_r1": (159, 79, 168, 91),
    "L6_r1": (204, 78, 213, 91),
    "L5_r1": (182, 78, 191, 91),
}

for name, (x0, y0, x1, y1) in TARGETS.items():
    t = norm(ink_mask(x0, y0, x1, y1))
    print("=" * 70)
    print(f"{name} target shape={t.shape}")
    print(show(t))
    scored = []
    for ch in "0123456789":
        for fn, fp in FONTS.items():
            if not os.path.exists(fp):
                continue
            for size in range(9, 18):
                tm = render(ch, fp, size)
                if tm is None:
                    continue
                # penalize aspect/size mismatch
                s = iou(t, tm)
                s -= 0.02 * abs(tm.shape[0] - t.shape[0]) + 0.02 * abs(tm.shape[1] - t.shape[1])
                scored.append((s, ch, fn, size, tm))
    scored.sort(key=lambda r: -r[0])
    for s, ch, fn, size, tm in scored[:3]:
        print(f"--- candidate {ch!r} {fn} size={size} iou_adj={s:.3f} shape={tm.shape}")
        print(show(tm))
