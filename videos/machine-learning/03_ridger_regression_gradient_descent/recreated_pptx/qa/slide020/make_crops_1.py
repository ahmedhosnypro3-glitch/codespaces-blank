#!/usr/bin/env python3
"""Procedure B crop pairs for slide 020 (attempt 1 render).
Regions in slide-space frame px (~8px padding around measured ink):
  title: x 148..770, y 220..356  (title ink 159..758 / 230..344 incl underline)
  badge: x 838..896, y 46..102   (badge cluster 855..895 / 54..94; stays inside
                                  the gray panel, clear of the right stroke x901)
Render crops: frame px * (H_render/540); original crops LANCZOS-upscaled to the
render crop's EXACT output size => matched effective scale per axis by construction.
"""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = f"{BASE}/recreated_pptx/qa/slide020/render_1.png"
ORIG = f"{BASE}/unique_slides/slide_020.jpg"

render = Image.open(RENDER)
orig = Image.open(ORIG)
S = render.height / 540.0
print(f"render size {render.size}, scale {S:.4f}")

regions = {
    "title": (148, 220, 770, 356),
    "badge": (838, 46, 896, 102),
}

for name, (x0, y0, x1, y1) in regions.items():
    rx0, ry0 = round(x0 * S), round(y0 * S)
    rx1, ry1 = round(x1 * S), round(y1 * S)
    rc = render.crop((rx0, ry0, rx1, ry1))
    oc = orig.crop((x0, y0, x1, y1)).resize((rc.width, rc.height), Image.LANCZOS)
    rp = f"{BASE}/recreated_pptx/qa/slide020/crop_1_{name}_render.png"
    op = f"{BASE}/recreated_pptx/qa/slide020/crop_1_{name}_orig.png"
    rc.save(rp); oc.save(op)
    ew = rc.width / (x1 - x0); eh = rc.height / (y1 - y0)
    ow = oc.width / (x1 - x0); oh = oc.height / (y1 - y0)
    print(f"{name}: render crop {rc.size} (eff {ew:.4f}x{eh:.4f} px/framepx), "
          f"orig crop {oc.size} (eff {ow:.4f}x{oh:.4f}) -> {rp}")
    assert (rc.width, rc.height) == (oc.width, oc.height)
    # effective scales equal per axis by construction; assert anyway
    assert abs(ew - ow) < 1e-9 and abs(eh - oh) < 1e-9
print("OK matched effective scale")
