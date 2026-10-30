#!/usr/bin/env python3
"""Procedure B crop pairs for slide 034 — matched effective scale (attempt 25).

Regions identical to the banked make_crops_6.py; only the render
(render_26, the red-border rebuild) and the crop_25_* names are new.
"""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = f"{BASE}/recreated_pptx/qa/slide034/render_26.png"
ORIG = f"{BASE}/unique_slides/slide_034.jpg"
QA = f"{BASE}/recreated_pptx/qa/slide034"

REGIONS = {
    "table": (74, 313, 887, 525),
    "plot": (599, 50, 853, 321),
}


def make(name, x0, y0, x1, y1):
    ren = Image.open(RENDER).convert("RGB")
    org = Image.open(ORIG).convert("RGB")
    Hr = ren.height
    sc = Hr / 540.0
    rc = ren.crop((int(round(x0 * sc)), int(round(y0 * sc)),
                   int(round(x1 * sc)), int(round(y1 * sc))))
    oc = org.crop((x0, y0, x1, y1))
    oc_up = oc.resize((int(round(oc.width * sc)), int(round(oc.height * sc))),
                      Image.LANCZOS)
    rc.save(f"{QA}/crop_25_{name}_render.png")
    oc_up.save(f"{QA}/crop_25_{name}_orig.png")
    print(f"crop {name}: bbox ({x0},{y0})-({x1},{y1}) frame {x1-x0}x{y1-y0}; "
          f"render {rc.size} orig_up {oc_up.size} mismatch "
          f"({abs(rc.width-oc_up.width)*100/oc.width:.2f}%, {abs(rc.height-oc_up.height)*100/oc.height:.2f}%)")


for n, r in REGIONS.items():
    make(n, *r)
