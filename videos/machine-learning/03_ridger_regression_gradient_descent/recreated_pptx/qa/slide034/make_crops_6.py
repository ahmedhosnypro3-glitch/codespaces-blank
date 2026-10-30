#!/usr/bin/env python3
"""Procedure B crop pairs for slide 034 — matched effective scale (attempt 6).

Protocol: crop BOTH images at the same slide-space region; upscale the ORIGINAL crop
by H_render/540 (LANCZOS) so output_px/frame_px is equal for both images.

Regions are the MEASURED bboxes from unique_slides/slide_034.jpg:
  table: rows 313..525, cols 74..887 (main table; measured rows 321..517, cols 82..879)
  plot : rows 50..321, cols 599..853 (function plot; measured axes box cols 607..845, rows 58..313)
"""
import sys

from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = f"{BASE}/recreated_pptx/qa/slide034/render_6.png"
ORIG = f"{BASE}/unique_slides/slide_034.jpg"
QA = f"{BASE}/recreated_pptx/qa/slide034"

REGIONS = {
    # densest region: the 8-row x 19-column numeric table (data fidelity)
    "table": (74, 313, 887, 525),
    # second dense region: the function plot (curve + markers + annotations)
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
    rc.save(f"{QA}/crop_6_{name}_render.png")
    oc_up.save(f"{QA}/crop_6_{name}_orig.png")
    print(f"crop {name}: slide bbox ({x0},{y0})-({x1},{y1}) = {x1-x0}x{y1-y0} frame px")
    print(f"  render crop {rc.size} @ {sc:.3f}x  = {rc.width/(x1-x0):.3f} px/frame-px")
    print(f"  orig   crop {oc_up.size} @ {sc:.3f}x  = {oc_up.width/(x1-x0):.3f} px/frame-px")
    print(f"  effective-scale match: {abs(rc.width/(x1-x0) - oc_up.width/(x1-x0)) < 0.02}")


if __name__ == "__main__":
    for n in (sys.argv[1:] or list(REGIONS)):
        mk = REGIONS[n]
        make(n, *mk)
