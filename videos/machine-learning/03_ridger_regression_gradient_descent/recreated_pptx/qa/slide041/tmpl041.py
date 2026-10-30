#!/usr/bin/env python3
"""Template-match small glyph cells on slide 041 against rendered serif digit templates."""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ORIG = os.path.join(os.path.dirname(__file__), "..", "..", "..", "unique_slides", "slide_041.jpg")
ORIG = os.path.abspath(ORIG)
im = Image.open(ORIG).convert("RGB")
A = np.asarray(im).astype(int)

FONTS = [
    ("LiberationSerif", "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"),
    ("LiberationSerif-Bold", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"),
    ("LiberationSerif-It", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"),
    ("DejaVuSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
    ("DejaVuSerif-It", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"),
    ("NimbusRoman", "/usr/share/fonts/truetype/urw-base35/NimbusRoman-Regular.otf"),
]


def ink_mask(x0, y0, x1, y1):
    """Binary mask of non-background ink inside bbox (bg = pale panel fill)."""
    a = A[y0:y1, x0:x1]
    # background is pale yellow ~ (254,255,232); anything much darker/different is ink
    d = np.abs(a - np.array([254, 255, 232])).sum(axis=2)
    m = d > 90
    return m


def norm_mask(m):
    ys, xs = np.nonzero(m)
    if len(ys) == 0:
        return None
    sub = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return sub


def render(ch, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    img = Image.new("L", (size * 3, size * 3), 0)
    d = ImageDraw.Draw(img)
    d.text((size, size), ch, font=f, fill=255)
    a = np.asarray(img) > 90
    ys, xs = np.nonzero(a)
    if len(ys) == 0:
        return None
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def score(target, tmpl):
    """Shape similarity invariant to small scale differences: resize tmpl to target size."""
    if target is None or tmpl is None:
        return -1.0
    t = Image.fromarray((target * 255).astype(np.uint8)).resize(
        (tmpl.shape[1], tmpl.shape[0]), Image.BILINEAR)
    t = np.asarray(t) > 110
    inter = np.logical_and(t, tmpl).sum()
    union = np.logical_or(t, tmpl).sum()
    return inter / union if union else -1.0


def iou2(target, tmpl):
    """Same-size IoU after aligning tmpl (same pixel size) - exact-font test."""
    if target is None or tmpl is None:
        return -1.0
    h = max(target.shape[0], tmpl.shape[0])
    w = max(target.shape[1], tmpl.shape[1])
    tp = np.zeros((h, w), bool)
    qp = np.zeros((h, w), bool)
    tp[:target.shape[0], :target.shape[1]] = target
    qp[:tmpl.shape[0], :tmpl.shape[1]] = tmpl
    inter = np.logical_and(tp, qp).sum()
    union = np.logical_or(tp, qp).sum()
    return inter / union if union else -1.0


CELLS = {
    # name: (x0,y0,x1,y1) inclusive-exclusive
    "L1_r1": (93, 79, 101, 91),
    "L1_r2": (93, 95, 101, 107),
    "L2_r1": (114, 78, 123, 91),
    "L2_r2": (114, 95, 123, 107),
    "L3_r1": (136, 79, 145, 91),
    "L3_r2": (136, 95, 145, 107),
    "L4_r1": (159, 79, 168, 91),
    "L4_r2": (159, 95, 168, 107),
    "L5_r1": (182, 78, 191, 91),
    "L5_r2": (182, 95, 191, 107),
    "L6_r1": (204, 78, 213, 91),
    "L6_r2": (204, 95, 213, 107),
    "R1_r1": (601, 82, 611, 94),
    "R1_r2": (601, 95, 611, 109),
    "R2_r1": (624, 82, 633, 94),
    "R2_r2": (624, 96, 633, 109),
    "R3_r1": (646, 82, 655, 94),
    "R3_r2": (646, 96, 655, 109),
    "MID_top": (333, 61, 351, 72),
    "MID_mid": (333, 77, 351, 88),
    "MID_bot": (333, 95, 351, 106),
}

CHARS = list("0123456789")

out = {}
for name, (x0, y0, x1, y1) in CELLS.items():
    m = ink_mask(x0, y0, x1, y1)
    t = norm_mask(m)
    res = []
    for ch in CHARS:
        best = -1
        bestmeta = None
        for fname, fp in FONTS:
            if not os.path.exists(fp):
                continue
            for size in range(9, 22):
                tm = render(ch, fp, size)
                s = score(t, tm)
                if s > best:
                    best = s
                    bestmeta = (fname, size)
        res.append((best, ch, bestmeta))
    res.sort(reverse=True)
    out[name] = res[:4]
    print(f"{name:10s} bbox=({x0},{y0},{x1},{y1}) ink={m.sum():3d} shape={None if t is None else t.shape}")
    for s, ch, meta in res[:4]:
        print(f"      {ch!r} score={s:.3f} {meta}")
print(json.dumps({k: [(round(s, 4), c) for s, c, _ in v] for k, v in out.items()}))
