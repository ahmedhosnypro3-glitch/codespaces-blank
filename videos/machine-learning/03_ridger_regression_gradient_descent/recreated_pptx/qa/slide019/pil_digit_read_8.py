#!/usr/bin/env python3
"""Objective digit read of the NO REG column's green predicted-y values.

Segments the green ink of each row group's y-line into numbers by x-gap, then
builds a digit template set from render_8 (labels taken from build/slide_019.js
columnData, never hand-read from pixels) and classifies render_6.
"""
from PIL import Image
import numpy as np

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019"
SCALE = 150 / 72.0

KNOWN = {
    "rowgroup1": ["60", "80", "100"],
    "rowgroup2": ["32.4", "42.3", "52.3"],
    "rowgroup3": ["24.4", "31.2", "38"],
}
# NO REG column frame x134..376, and the frame-y band of each group's green y-line
COL_X = (134, 376)
ROW_Y = {"rowgroup1": (243, 265), "rowgroup2": (348, 370), "rowgroup3": (458, 480)}
NUM_GAP = 10      # px (render space) that separates two numbers
GLYPH_GAP = 2     # px that separates glyphs inside one number


def green_mask(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (g > 60) & (g - r > 35) & (g - b > 35)


def clusters(mask, frame_box, gap):
    x0, x1, y0, y1 = frame_box
    sub = mask[y0:y1, x0:x1]
    cols = np.nonzero(sub.any(axis=0))[0]
    if len(cols) == 0:
        return []
    groups, start, prev = [], cols[0], cols[0]
    for c in cols[1:]:
        if c - prev > gap:
            groups.append((start, prev))
            start = c
        prev = c
    groups.append((start, prev))
    out = []
    for a, b in groups:
        bm = sub[:, a:b + 1]
        ys = np.nonzero(bm.any(axis=1))[0]
        if len(ys) == 0:
            continue
        bm = bm[ys.min():ys.max() + 1, :]
        if bm.sum() < 3:      # phantom-trap law
            continue
        out.append((x0 + int(a), bm))
    return out


def box(row):
    fx0, fx1 = COL_X
    fy0, fy1 = ROW_Y[row]
    return (int(fx0 * SCALE), int(fx1 * SCALE), int(fy0 * SCALE), int(fy1 * SCALE))


def numbers(mask, row):
    """Split the row's green y-line into individual numbers, each a glyph list."""
    num_groups = clusters(mask, box(row), NUM_GAP)
    result = []
    for ns, _ in num_groups:
        # each num_group covers a contiguous x span; re-segment inside it
        span = clusters(mask, (ns, ns + 200, box(row)[2], box(row)[3]), GLYPH_GAP)
        # keep only glyphs whose x-start falls inside this number's span
        nxt = min([g for g, _ in clusters(mask, box(row), 1)], default=None)
        result.append(span)
    return result


def all_numbers(mask, row):
    glyphs = clusters(mask, box(row), GLYPH_GAP)
    # group glyphs into numbers by x-gap > NUM_GAP
    nums, cur = [], []
    prev_end = None
    for gx, bm in glyphs:
        if prev_end is not None and gx - prev_end > NUM_GAP:
            nums.append(cur)
            cur = []
        cur.append((gx, bm))
        prev_end = gx + bm.shape[1]
    if cur:
        nums.append(cur)
    return nums


def normalise(bm, w=12, h=16):
    return np.asarray(Image.fromarray((bm * 255).astype(np.uint8))
                      .resize((w, h), Image.BILINEAR)).astype(float) / 255.0


def extract(path):
    mask = green_mask(path)
    out = {}
    for row in KNOWN:
        out[row] = all_numbers(mask, row)
    return out


def classify(bm, templates):
    v = normalise(bm)
    best, bestd = "?", 1e9
    for ch, exs in templates.items():
        for ex in exs:
            d = float(((v - ex) ** 2).sum())
            if d < bestd:
                best, bestd = ch, d
    return best, bestd


r8 = extract(f"{QA}/render_8.png")
templates = {}
for row, vals in KNOWN.items():
    for idx, val in enumerate(vals):
        nums = r8[row]
        if idx >= len(nums):
            print(f"!! missing number {row} v{idx+1}")
            continue
        chars = list(val)
        gl = nums[idx]
        if len(gl) != len(chars):
            print(f"!! align mismatch {row} v{idx+1}: '{val}' -> {len(gl)} glyphs")
            continue
        for (gx, bm), ch in zip(gl, chars):
            templates.setdefault(ch, []).append(normalise(bm))

print(f"template digits: {sorted(templates)}  exemplars={sum(len(v) for v in templates.values())}")
print()
for row in KNOWN:
    r6n = extract(f"{QA}/render_6.png")[row]
    r8n = r8[row]
    for idx, val in enumerate(KNOWN[row]):
        if idx >= len(r6n):
            print(f"RENDER_6 {row} v{idx+1}: MISSING")
            continue
        chars = [classify(bm, templates)[0] for _, bm in r6n[idx]]
        r8chars = [classify(bm, templates)[0] for _, bm in r8n[idx]] if idx < len(r8n) else []
        fx0 = r6n[idx][0][0] / SCALE
        print(f"{row} v{idx+1}: RENDER_6 read '{''.join(chars)}'  |  "
              f"RENDER_8 read '{''.join(r8chars)}'  |  build truth '{val}'  "
              f"frame x~{fx0:.0f}")
