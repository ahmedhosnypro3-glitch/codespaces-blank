#!/usr/bin/env python3
"""Self-check attempt 1: render_1.png (150dpi, 2001x1125) vs original targets.
Frame->render scale: 1125/540 = 2.0833. 1 frame px = 2.0833 render px.
Targets (frame px): L1 ink x 159..758 y 230..264; L2 ink x 183..744 y 310..344
(underline core rows 338..340). Tolerance: <=6 render px (~3 frame px).
"""
import sys
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide020/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_020.jpg"

S = 1125 / 540.0

def measure(path, label, is_render):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
    # exclude chrome strokes + badge: panel interior only
    m = red.copy()
    if is_render:
        m[:, : int(62 * S)] = False
        m[:, int(898 * S):] = False
        m[int(533 * S):, :] = False
        m[: int(52 * S), :] = False
    else:
        m[:, :62] = False; m[:, 898:] = False; m[533:, :] = False; m[:52, :] = False
    ys, xs = np.where(m)
    H = im.shape[0]
    print(f"== {label} (H={H}) ==")
    if not len(ys):
        print("  NO RED INK FOUND"); return None
    # split into line bands by row gaps
    rows = np.where(m.sum(axis=1) > 0)[0]
    bands = []
    start = rows[0]; prev = rows[0]
    for y in rows[1:]:
        if y > prev + 6:
            bands.append((start, prev)); start = y
        prev = y
    bands.append((start, prev))
    out = {}
    for (y0, y1) in bands:
        band = m[y0:y1 + 1]
        cols = np.where(band.any(axis=0))[0]
        print(f"  red band y {y0}..{y1} (h={y1-y0+1}) x {cols.min()}..{cols.max()} (w={cols.max()-cols.min()+1}) px={int(band.sum())}")
        out.setdefault("bands", []).append((y0, y1, cols.min(), cols.max()))
    return out

orig = measure(ORIG, "ORIGINAL frame (frame px)", False)
rend = measure(RENDER, "RENDER_1 (render px)", True)

if rend and len(rend["bands"]) >= 1:
    print()
    print("== deltas (render_px -> frame_px, target vs actual) ==")
    ob = orig["bands"]
    rb = rend["bands"]
    # map: original bands = [L1, L2(+underline merged)]; render same order
    names = ["L1", "L2"]
    for i, name in enumerate(names):
        if i >= len(rb) or i >= len(ob):
            print(f"  {name}: MISSING BAND (orig bands={len(ob)}, render bands={len(rb)})")
            continue
        oy0, oy1, ox0, ox1 = ob[i]
        ry0, ry1, rx0, rx1 = rb[i]
        # render->frame
        fy0, fy1, fx0, fx1 = ry0 / S, ry1 / S, rx0 / S, rx1 / S
        print(f"  {name}: y_top {fy0:.1f} (target {oy0}) d={fy0-oy0:+.1f} | y_bot {fy1:.1f} (target {oy1}) d={fy1-oy1:+.1f}"
              f" | x_left {fx0:.1f} (target {ox0}) d={fx0-ox0:+.1f} | x_right {fx1:.1f} (target {ox1}) d={fx1-ox1:+.1f}"
              f" | w {fx1-fx0+1:.1f} (target {ox1-ox0+1})")

    # underline band: rows 338..341*S in render, count solid core + extent
    im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
    print()
    print("== underline check (render rows around 339*S=706..709) ==")
    for fy in range(334, 346):
        y0 = int(fy * S); y1 = int((fy + 1) * S)
        band = red[y0:y1]
        cols = np.where(band.any(axis=0))[0]
        if len(cols):
            print(f"  frame-y {fy}: render rows {y0}..{y1-1} ink x {cols.min()/S:.1f}..{cols.max()/S:.1f} ({int(band.sum())} px)")
        else:
            print(f"  frame-y {fy}: (no red)")

    # frame containment: ink must stay inside panel x 54..903, y 45..540 (frame px)
    print()
    print("== containment: content ink outside chrome bounds? ==")
    ok = True
    for (y0, y1, x0, x1) in rb:
        fx0, fx1, fy0, fy1 = x0 / S, x1 / S, y0 / S, y1 / S
        if fx0 < 64 or fx1 > 894 or fy0 < 52 or fy1 > 533:
            print(f"  band y{fy0:.0f}..{fy1:.0f} x{fx0:.0f}..{fx1:.0f} CROSSES panel bounds"); ok = False
    print("  containment OK" if ok else "  containment FAIL")

    # line/box wrap check: no ink below L2 band beyond underline zone
    l2 = rb[-1]
    below = red[int((l2[1] + 8)): int(530 * S), int(64 * S): int(894 * S)]
    print(f"  ink below L2 band (+8px gap) up to y=530f: {int(below.sum())} px (expect 0)")
sys.exit(0)
