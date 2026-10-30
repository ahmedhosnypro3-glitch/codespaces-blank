#!/usr/bin/env python3
"""Procedure B crop pairs for slide 022 — RESUME re-cut (2026-10-20, worker w4).

Re-cuts ALL zoomed crop regions from the CURRENT render (fresh re-render of the
current deliverable pptx, pixel-identical to the banked render_1.png —
md5 1a4b00687a154164f26cc785b260dd3f), so every crop's IMG1 provably comes from
the current render. Regions in slide-space frame px (~8px padding around
measured ink):

  title: x 170..750, y 220..380  (two-line title block — the slide's densest
         content region; contains L1 ink 189..726/235..274 and L2 ink
         274..652/325..364 plus the washed cursor sliver on the orig side)
  badge: x 840..897, y 46..102  (badge cluster 857..894/58..88 + purple ring;
         clear of the right stroke x901)
  line1: x 180..735, y 228..282 (TIGHT zoom on line 1 '[3] Inverse of High
         Dimension' — glyph-level detail incl. the '[3]' bracket delimiters)
  line2: x 265..665, y 318..372 (TIGHT zoom on line 2 '(non-singular) Matrix' —
         glyph-level detail incl. the parenthesised delimiter)

Render crops: frame px * (H_render/540). Original crops LANCZOS-upscaled to the
render crop's EXACT output size => matched effective scale per axis by
construction (judge_protocol_03.md Procedure B law).
"""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = "/home/ahmed/Projects/ai_llm_slides/scratch/verify_022/current_render.png"
ORIG = f"{BASE}/unique_slides/slide_022.jpg"

render = Image.open(RENDER)
orig = Image.open(ORIG)
S = render.height / 540.0
print(f"render size {render.size}, scale {S:.4f}")

regions = {
    "title": (170, 220, 750, 380),
    "badge": (840, 46, 897, 102),
    "line1": (180, 228, 735, 282),
    "line2": (265, 318, 665, 372),
}

for name, (x0, y0, x1, y1) in regions.items():
    rx0, ry0 = round(x0 * S), round(y0 * S)
    rx1, ry1 = round(x1 * S), round(y1 * S)
    rc = render.crop((rx0, ry0, rx1, ry1))
    oc = orig.crop((x0, y0, x1, y1)).resize((rc.width, rc.height), Image.LANCZOS)
    rp = f"{BASE}/recreated_pptx/qa/slide022/crop_1_{name}_render.png"
    op = f"{BASE}/recreated_pptx/qa/slide022/crop_1_{name}_orig.png"
    rc.save(rp); oc.save(op)
    ew = rc.width / (x1 - x0); eh = rc.height / (y1 - y0)
    ow = oc.width / (x1 - x0); oh = oc.height / (y1 - y0)
    print(f"{name}: render crop {rc.size} (eff {ew:.4f}x{eh:.4f} px/framepx), "
          f"orig crop {oc.size} (eff {ow:.4f}x{oh:.4f}) -> {rp}")
    assert (rc.width, rc.height) == (oc.width, oc.height)
    assert abs(ew - ow) < 1e-9 and abs(eh - oh) < 1e-9
print("OK matched effective scale for all regions")
