#!/usr/bin/env python3
"""Procedure B — cut the zoomed crop-pairs for slide 011 (attempt K).

Law (judge_protocol_03.md, Procedure B):
  1. regions picked from the ORIGINAL frame (960x540, 1px=1pt), ~8px padding;
  2. BOTH images cropped at the SAME slide-space region;
  3. effective scale MATCHED per axis — the original crop is LANCZOS-upscaled to
     the render crop's exact pixel size (never pass the full frame; never pair
     crops of different effective scale);
  4. a small extra uniform zoom (same factor for BOTH crops, sizes kept equal)
     is applied to regions whose native output would be under ~300px wide, so
     the judge can read the detail; the scale stays matched by construction;
  5. banked as qa/slide011/crop_K_<name>_render.png + crop_K_<name>_orig.png
     (+ crop_K_regions.json with the frame-px boxes and final scales).

Dense regions on this slide (from the full-frame ink census banked in the build
script header and selfcheck output):
  title      rows 230..264 x 111..817 — 8 words, the densest ink on the slide
  underline  rows 258..261 x 595..698 — the just-fixed 'outlier' underline bar
  subtitle   rows 301..329 x 242..683 — the blue italic parenthetical line
  badge      rows ~55..93 x ~855..897 — small-text cluster ('11' in a 35px disc)
"""
import json
import sys

from PIL import Image

VID = "machine-learning/03_ridger_regression_gradient_descent"
QA = f"videos/{VID}/recreated_pptx/qa/slide011"
K = sys.argv[1] if len(sys.argv) > 1 else "1"

RENDER = f"{QA}/render_{K}.png"
ORIG = f"videos/{VID}/unique_slides/slide_011.jpg"

S = Image.open(RENDER).size[1] / 540.0  # H_render/540 = render px per frame px
print(f"render scale S = {S:.5f} render-px / frame-px")

REGIONS = {
    # name: (frame-px bbox x0,y0,x1,y1, min-output-width-px)
    "title":     (103, 220, 826, 272, 300),
    "underline": (578, 244, 718, 276, 300),
    "subtitle":  (233, 292, 693, 338, 300),
    "badge":     (846, 43, 907, 103, 300),
}

r = Image.open(RENDER).convert("RGB")
o = Image.open(ORIG).convert("RGB")
meta = {"render_scale": S, "attempt": K, "regions": {}}

for name, (x0, y0, x1, y1, minw) in REGIONS.items():
    box_r = (round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S))
    rc = r.crop(box_r)
    oc = o.crop((x0, y0, x1, y1))
    # matched effective scale: original upscaled to the render crop's exact size
    oc_m = oc.resize(rc.size, Image.LANCZOS)
    eff_scale = rc.size[0] / (x1 - x0)
    # uniform extra zoom for small regions (applied to BOTH -> scale stays matched)
    zoom = 1
    if rc.size[0] < minw:
        zoom = round(minw / rc.size[0] + 0.5)
        if zoom < 2:
            zoom = 2
        nw, nh = rc.size[0] * zoom, rc.size[1] * zoom
        rc = rc.resize((nw, nh), Image.LANCZOS)
        oc_m = oc_m.resize((nw, nh), Image.LANCZOS)
    assert rc.size == oc_m.size, (rc.size, oc_m.size)
    rc.save(f"{QA}/crop_{K}_{name}_render.png")
    oc_m.save(f"{QA}/crop_{K}_{name}_orig.png")
    meta["regions"][name] = {
        "frame_bbox": [x0, y0, x1, y1],
        "render_px_box": list(box_r),
        "frame_size_px": [x1 - x0, y1 - y0],
        "output_size_px": list(rc.size),
        "uniform_zoom": zoom,
        "effective_scale_px_per_frame_px": round(rc.size[0] / (x1 - x0), 5),
        "match_check": "equal (original LANCZOS-upscaled to render crop size)",
    }
    print(f"  {name:10s} frame {x1-x0}x{y1-y0}px -> output {rc.size[0]}x{rc.size[1]} "
          f"(zoom x{zoom}, effective scale {rc.size[0]/(x1-x0):.3f} px/frame-px, MATCHED)")

json.dump(meta, open(f"{QA}/crop_{K}_regions.json", "w"), indent=2)
print(f"banked crop_{K}_regions.json")
