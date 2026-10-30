#!/usr/bin/env python3
"""Cut matched-scale crop pairs for slide 013 attempt 6 (Procedure B).
Render crop: render_6.png at scale H_render/540 (2.083333 px per frame px).
Original crop: the SAME frame bbox from the 960x540 original, LANCZOS-upscaled
to the render crop's pixel size (equal effective scale on both axes).
"""
from PIL import Image
import os

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide013"
ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_013.jpg"
REND = os.path.join(QA, "render_6.png")

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
S = r.size[1] / 540.0  # 2.083333 per Procedure B
print(f"render {r.size}; scale = render_H/540 = {S:.6f}")

REGIONS = {
    "wbox1":  (498, 119, 631, 260),   # band-1 W box: vector, parens, ellipse text
    "wbox2":  (498, 257, 631, 398),   # band-2 W box: widest vector (0.67 / 0.64)
    "train1": (84, 118, 467, 257),    # band-1 training table: headers + all rows
    "test1":  (711, 88, 880, 260),    # band-1 test table + Test label + mint row
    "arrows1": (447, 178, 675, 218),  # band-1 arrow pair (hollow heads)
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = r.crop((int(round(x0*S)), int(round(y0*S)), int(round(x1*S)), int(round(y1*S))))
    oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rp = os.path.join(QA, f"crop_6_{name}_render.png")
    op = os.path.join(QA, f"crop_6_{name}_orig.png")
    rc.save(rp); oc.save(op)
    # scale audit: px per frame px, both axes, both images (must be equal)
    sx_r, sy_r = rc.size[0]/(x1-x0), rc.size[1]/(y1-y0)
    sx_o, sy_o = oc.size[0]/(x1-x0), oc.size[1]/(y1-y0)
    print(f"{name}: bbox=({x0},{y0},{x1},{y1}) size={rc.size} "
          f"scale render=({sx_r:.5f},{sy_r:.5f}) orig=({sx_o:.5f},{sy_o:.5f}) equal={abs(sx_r-sx_o)<1e-9 and abs(sy_r-sy_o)<1e-9}")
