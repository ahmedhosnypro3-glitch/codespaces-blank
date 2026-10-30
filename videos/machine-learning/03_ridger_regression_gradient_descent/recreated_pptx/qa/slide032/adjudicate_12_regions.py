#!/usr/bin/env python3
"""Adjudicate slide 032 all five Procedure-B regions against BOTH images.

960x540 original (1px=1pt), 2001x1125 render (2.084375 render px per frame px).
Every claim measured here before any build change. Phantom trap enforced:
ink columns/rows with fewer than 3 ink px are rejected.
"""
import numpy as np
from PIL import Image

NS = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide032"
FRAME = NS + "/unique_slides/slide_032.jpg"
REND = QA + "/render_11.png"

o = np.array(Image.open(FRAME).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
SX = r.shape[1] / 960.0
SY = r.shape[0] / 540.0
print(f"orig {o.shape[1]}x{o.shape[0]}  render {r.shape[1]}x{r.shape[0]}  "
      f"scale x={SX:.6f} y={SY:.6f}")


def lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


LO = lum(o)
LR = lum(r)

# Regions banked verbatim from make_crops_10.py (frame px, x0,y0,x1,y1)
REGIONS = [
    ("title", (72, 58, 568, 98)),
    ("params", (68, 170, 216, 259)),
    ("graph", (565, 58, 818, 316)),
    ("callouts", (328, 176, 600, 362)),
    ("table", (290, 322, 608, 535)),
]

PAD = 6  # frame px search margin so ink extents are never clipped at the crop box


def ink_bbox(arr_lo, x0, y0, x1, y1, thr=248, min_ink=3):
    sub = arr_lo[y0:y1 + 1, x0:x1 + 1]
    m = sub < thr
    cols = np.nonzero(m.sum(axis=0) >= min_ink)[0]
    rows = np.nonzero(m.sum(axis=1) >= min_ink)[0]
    if not len(cols) or not len(rows):
        return None, None, None
    return (x0 + int(cols[0]), y0 + int(rows[0]),
            x0 + int(cols[-1]), y0 + int(rows[-1])), m.sum(), m


def med(a, box):
    x0, y0, x1, y1 = box
    return tuple(int(np.median(a[y0:y1 + 1, x0:x1 + 1, c])) for c in range(3))


def hexc(t):
    return "".join("%02X" % v for v in t)


out = []
for name, (x0, y0, x1, y1) in REGIONS:
    # original: exact frame bbox, no resize (1px=1pt)
    ob, on, _ = ink_bbox(LO, x0, y0, x1, y1)
    # render: the crop box is round(x*S) etc. -> map frame bbox to render px
    rx0, ry0 = round(x0 * SX), round(y0 * SY)
    rx1, ry1 = round(x1 * SX), round(y1 * SY)
    rb, rn, _ = ink_bbox(LR, rx0, ry0, rx1, ry1)

    print(f"\n=== {name} ===")
    print(f"  crop box frame ({x0},{y0},{x1},{y1})")
    print(f"  crop box render ({rx0},{ry0},{rx1},{ry1}) size "
          f"{rx1-rx0+1}x{ry1-ry0+1} effective scale "
          f"{(rx1-rx0+1)/(x1-x0+1):.4f}/{(ry1-ry0+1)/(y1-y0+1):.4f}")
    if ob is None or rb is None:
        print("  INK NOT FOUND (both images must have ink here)")
        continue
    print(f"  ink FRAME  x{ob[0]}..{ob[2]} y{ob[1]}..{ob[3]} "
          f"({ob[2]-ob[0]+1}x{ob[3]-ob[1]+1}) n={on}")
    print(f"  ink RENDER x{rb[0]}..{rb[2]} y{rb[1]}..{rb[3]} "
          f"({rb[2]-rb[0]+1}x{rb[3]-rb[1]+1}) n={rn}")
    # map render ink bbox back to frame px
    fx0 = (rb[0] - rx0) / (rx1 - rx0 + 1) * (x1 - x0 + 1) + x0
    fx1 = (rb[2] - rx0) / (rx1 - rx0 + 1) * (x1 - x0 + 1) + x0
    fy0 = (rb[1] - ry0) / (ry1 - ry0 + 1) * (y1 - y0 + 1) + y0
    fy1 = (rb[3] - ry0) / (ry1 - ry0 + 1) * (y1 - y0 + 1) + y0
    print(f"  render ink mapped to frame: x{fx0:.1f}..{fx1:.1f} y{fy0:.1f}..{fy1:.1f}")
    print(f"  DELTA size  dw={(fx1-fx0)-(ob[2]-ob[0]):+.1f}pt "
          f"dh={(fy1-fy0)-(ob[3]-ob[1]):+.1f}pt")
    print(f"  DELTA place dx={fx0-ob[0]:+.1f}pt dy={fy0-ob[1]:+.1f}pt")
    # background median inside the region (text-free corner) for fill colour check
    bg_o = med(o, (x0, y0, min(x0 + 6, x1), min(y0 + 6, y1)))
    bg_r = med(r, (rx0, ry0, min(rx0 + 12, rx1), min(ry0 + 12, ry1)))
    print(f"  corner fill FRAME {hexc(bg_o)}  RENDER {hexc(bg_r)}")
    out.append((name, ob, rb))

print("\n=== SUMMARY (frame-space render-ink bbox vs original-ink bbox) ===")
for name, ob, rb in out:
    print(f"  {name:9s} FRAME x{ob[0]}..{ob[2]} y{ob[1]}..{ob[3]}   "
          f"RENDER x{rb[0]}..{rb[2]} y{rb[1]}..{rb[3]}")
