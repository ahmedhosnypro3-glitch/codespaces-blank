#!/usr/bin/env python3
"""Independent PIL verification of the current slide 016 deliverable render.

Checks, in 960x540 frame space (1px = 1pt):
  1. all three original black underline segments are present;
  2. no black underline crosses the inner content-frame border;
  3. every measured body-text band is inked in the render.

Usage: python3 verify_attempt6_current.py [render.png]
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

QA = Path(__file__).resolve().parent
DECK = QA.parents[2]
ORIG = DECK / "unique_slides" / "slide_016.jpg"
RENDER = Path(sys.argv[1]) if len(sys.argv) > 1 else QA / "render_6.png"

EXPECTED_UNDERLINES = [
    (500.0, 446.0, 640.0),
    (500.0, 710.0, 806.0),
    (525.0, 110.0, 162.0),
]
BODY_BANDS = [
    (104, 117), (129, 146), (179, 197), (230, 248), (256, 273),
    (281, 298), (332, 350), (357, 374), (408, 426), (434, 447),
    (484, 502), (510, 527),
]


def neutral_dark(a):
    """Neutral dark ink: excludes the purple inner border and red house strokes."""
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    return (mx < 140) & ((mx - mn) <= 20)


def horizontal_strokes(a, scale, x0=80, x1=830, y0=470, y1=540, min_width=12):
    """Long neutral horizontal runs, reported in frame px."""
    seg = a[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    mask = neutral_dark(seg)
    found = []
    for row in range(mask.shape[0]):
        run, start = None, None
        for col, hit in enumerate(mask[row]):
            if hit and start is None:
                start = col
            elif not hit and start is not None:
                if (col - start) / scale >= min_width:
                    found.append((row / scale + y0, start / scale + x0,
                                  (col - 1) / scale + x0))
                start = None
        if start is not None and (len(mask[row]) - start) / scale >= min_width:
            found.append((row / scale + y0, start / scale + x0,
                          (len(mask[row]) - 1) / scale + x0))
    merged = []
    for y, sx0, sx1 in found:
        if merged and abs(merged[-1][0] - y) <= 1.6 and abs(merged[-1][2] - sx0) < 6:
            m = merged[-1]
            merged[-1] = ((m[0] + y) / 2, min(m[1], sx0), max(m[2], sx1))
        else:
            merged.append((y, sx0, sx1))
    return merged


def ink_count(a, scale, x0, y0, x1, y1):
    seg = a[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    return int((seg.mean(axis=2) < 170).sum())


orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
render = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
scale = render.shape[0] / orig.shape[0]
print(f"original {orig.shape[1]}x{orig.shape[0]}  render {render.shape[1]}x{render.shape[0]}  scale={scale:.4f}")
print(f"render file: {RENDER}")

failures = []
for tag, a, s in (("original", orig, 1.0), ("render", render, scale)):
    print(f"\n{tag}: neutral horizontal strokes >=12 frame px in x80..830 y470..540")
    strokes = horizontal_strokes(a, s)
    if not strokes:
        print("  (none)")
    for y, x0, x1 in strokes:
        print(f"  y={y:6.1f} x={x0:6.1f}..{x1:6.1f} width={x1-x0:6.1f}")
        if tag == "render" and x1 > 832:
            failures.append(f"render stroke y={y:.1f} x={x0:.1f}..{x1:.1f} crosses inner border x~830")

render_strokes = horizontal_strokes(render, scale)
print("\nunderline matching")
for ey, ex0, ex1 in EXPECTED_UNDERLINES:
    matches = [s for s in render_strokes if abs(s[0] - ey) <= 2.0]
    best = None
    for s in matches:
        overlap = min(s[2], ex1) - max(s[1], ex0)
        if overlap > 0 and (best is None or overlap > best[0]):
            best = (overlap, s)
    if best is None:
        failures.append(f"missing underline near y={ey} x={ex0}..{ex1}")
        print(f"  MISSING y={ey} x={ex0}..{ex1}")
    else:
        overlap, s = best
        print(f"  FOUND   y={ey} x={ex0}..{ex1} -> y={s[0]:.1f} x={s[1]:.1f}..{s[2]:.1f} overlap={overlap:.1f}")
        if overlap < 0.8 * (ex1 - ex0):
            failures.append(f"underline y={ey} overlaps only {overlap:.1f}/{ex1-ex0:.1f} px")

print("\nbody-text band ink (x88..828)")
for y0, y1 in BODY_BANDS:
    oi = ink_count(orig, 1.0, 88, y0, 828, y1)
    ri = ink_count(render, scale, 88, y0, 828, y1)
    status = "OK" if ri >= 500 else "FAIL"
    print(f"  y={y0:3d}..{y1:3d}: original={oi:5d} render={ri:5d} {status}")
    if ri < 500:
        failures.append(f"body band y={y0}..{y1} has only {ri} ink px")

print("\nRESULT")
if failures:
    for f in failures:
        print("  FAIL:", f)
    raise SystemExit(1)
print("  PASS: 3/3 underlines present and contained; 12/12 body bands inked")
