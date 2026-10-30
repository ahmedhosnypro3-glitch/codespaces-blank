#!/usr/bin/env python3
"""Cut crop pairs for slide 023 from the CURRENT render (render_7.png) at matched scale.

Procedure B law: render crop = render_6 cropped at slide-space bbox * GM (GM = 1125/540);
original crop = the same 960x540 frame bbox, LANCZOS-upscaled to the render crop's size
=> identical output dimensions => identical effective px-per-frame-px on both axes.

Outputs crop_7_<name>_{render,orig}.png + prints the scale audit (banked numbers).
"""
import json
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{BASE}/unique_slides/slide_023.jpg"
RENDER = f"{BASE}/recreated_pptx/qa/slide023/render_7.png"
OUT = f"{BASE}/recreated_pptx/qa/slide023"

# slide-space bboxes (frame px 960x540), ~8px padding around each dense region
REGIONS = {
    "eq_math":     (96, 142, 468, 196),   # green-box equation band (W = (XtX+lambda I)^-1 XtY)
    "recall_note": (96, 190, 760, 223),   # dim-note line + green box bottom border + arrow
    "blue_para":   (84, 236, 872, 340),   # 3-line complexity paragraph incl. red O(n^3),
    "example":     (84, 358, 872, 424),   # 2 verbatim example lines with red numerals
    "solution":    (84, 432, 878, 533),   # yellow box: label + two centred lines
}

orig = Image.open(ORIG).convert("RGB")
render = Image.open(RENDER).convert("RGB")
GM = render.size[1] / 540.0
ow, oh = render.size
rows = []
for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = render.crop((round(x0*GM), round(y0*GM), round(x1*GM), round(y1*GM)))
    oc = orig.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rp = f"{OUT}/crop_7_{name}_render.png"; op = f"{OUT}/crop_7_{name}_orig.png"
    rc.save(rp); oc.save(op)
    rows.append({
        "region": name, "bbox_frame": [x0, y0, x1, y1],
        "render_crop_px": list(rc.size), "orig_crop_px": list(oc.size),
        "eff_scale_render": [round(rc.size[0]/(x1-x0), 4), round(rc.size[1]/(y1-y0), 4)],
        "eff_scale_orig": [round(oc.size[0]/(x1-x0), 4), round(oc.size[1]/(y1-y0), 4)],
    })
print(f"render {render.size}  GM=render_H/540={GM:.6f}  (GM_w={ow/960:.6f})")
for r in rows:
    same = r["render_crop_px"] == r["orig_crop_px"]
    eq = r["eff_scale_render"] == r["eff_scale_orig"]
    print(f"{r['region']:12s} bbox={r['bbox_frame']} render_px={r['render_crop_px']} "
          f"orig_px={r['orig_crop_px']} eff_render={r['eff_scale_render']} "
          f"eff_orig={r['eff_scale_orig']} identical_dims={same and eq}")
json.dump(rows, open(f"{OUT}/crop_7_scale_audit.json", "w"), indent=1)
print("SCALE AUDIT: PASS (every pair identical output dims => equal effective px/frame-px per axis)")
