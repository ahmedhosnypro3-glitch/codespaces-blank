#!/usr/bin/env python3
"""Cut the zoomed crop-pair certificates for slide 024 (Procedure B of
shared_patterns/judge_protocol_03.md).

Dense regions of this slide (measured in the frame, 960x540, 1px = 1pt):
  title     — the densest ink on the slide: 45pt bold red "Gradient Descent (GD)"
              including the two spanning parentheses (glyph-level + delimiter
              geometry detail lives below full-slide judge resolution)
  subtitles — the two-line small-text cluster ("and" 34pt + "How to apply to
              minimize Loss function" 30pt), line separation + centering detail
  icon      — the tiny bottom-center pen glyph (a 16x17 frame-px element;
              needs extra zoom to be legible at all)

Laws honoured:
  * crop-vs-crop ONLY (never the full frame as IMG2);
  * MATCHED effective scale per axis: effective = output_px / frame_px must be
    EQUAL on both sides. The render's native scale is 1125/540 = 2.08333 px per
    frame px; the original crop is LANCZOS-upscaled to exactly that. The icon
    region is far below the ~400px legibility floor (self-check law #6), so BOTH
    sides are additionally upscaled x3 (equal factor, so the pair stays matched
    at 6.25 px per frame px) — a matched pair never fabricates drift.
  * ~8px padding on every region.
Prints the manifest (also written as crop_manifest.json) so the judge dispatch
and the slide-space mapping of every crop (crop-relative coords -> slide coords:
  x_slide = x0 + x_crop / effective) are recorded.
"""
import json

import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{VID}/recreated_pptx/qa/slide024"
RENDER = f"{QA}/render_1.png"
ORIG = f"{VID}/unique_slides/slide_024.jpg"

BASE_SCALE = 1125 / 540.0          # 2.08333 render px per frame px
PAD = 8

REGIONS = [
    # name, slide-space bbox (x0, y0, x1, y1) frame px, extra equal zoom factor,
    # one-line region description for --capture
    ("title", (233, 216, 728, 272), 1,
     "the title band: bold red 45pt 'Gradient Descent (GD)' incl. its two parentheses"),
    ("subtitles", (193, 290, 767, 385), 1,
     "the two-line subtitle stack: 'and' (34pt) and 'How to apply to minimize Loss function' (30pt)"),
    ("icon", (454, 499, 488, 528), 3,
     "the tiny bottom-center dark pen glyph (~16x17 frame px)"),
]

ren = Image.open(RENDER).convert("RGB")
ori = Image.open(ORIG).convert("RGB")
RW, RH = ren.size
OW, OH = ori.size
assert (OW, OH) == (960, 540), f"original {OW}x{OH}, expected 960x540"

manifest = {"base_scale_render_px_per_frame_px": BASE_SCALE, "regions": []}
print(f"render {RW}x{RH} (scale {BASE_SCALE:.5f} px/frame-px) | original {OW}x{OH}")

for name, (x0, y0, x1, y1), zoom, desc in REGIONS:
    # slide-space crop box (inclusive, clipped to the frame) — the SAME box on both sides
    bx0, by0 = max(0, x0 - PAD), max(0, y0 - PAD)
    bx1, by1 = min(959, x1 + PAD), min(539, y1 + PAD)
    F_W, F_H = bx1 + 1 - bx0, by1 + 1 - by0        # frame px covered

    eff = BASE_SCALE * zoom                         # desired effective px/frame-px
    # Target output size: BOTH images are resized to EXACTLY this size, so the
    # effective scale is identical by construction (no independent-rounding drift).
    ow, oh = int(round(F_W * eff)), int(round(F_H * eff))

    # render: float box in render px (sub-pixel exact) -> LANCZOS resize to (ow,oh)
    rbox = (bx0 * BASE_SCALE, by0 * BASE_SCALE, (bx1 + 1) * BASE_SCALE, (by1 + 1) * BASE_SCALE)
    r_big = ren.resize((ow, oh), Image.LANCZOS, box=rbox)
    # original: native integer crop (exact) -> LANCZOS resize to the SAME size
    oc = ori.crop((bx0, by0, bx1 + 1, by1 + 1))
    o_big = oc.resize((ow, oh), Image.LANCZOS)

    eff_actual = ow / F_W                           # identical for both images by construction
    rp = f"{QA}/crop_1_{name}_render.png"
    op = f"{QA}/crop_1_{name}_orig.png"
    r_big.save(rp)
    o_big.save(op)
    print(f"\n[{name}] slide-space region x{bx0}..{bx1} y{by0}..{by1} "
          f"({F_W}x{F_H} frame px), desc: {desc}")
    print(f"   render crop -> {r_big.size} ; original crop {oc.size} -> {o_big.size}")
    print(f"   effective scale BOTH sides: {eff_actual:.5f} px/frame-px (target {eff:.5f}, zoom {zoom})")
    # assert the vertical effective scale matches too
    eff_v = o_big.height / F_H
    if abs(eff_actual - ow / F_W) > 1e-9 or abs(eff_v - eff_actual) > 0.02:
        raise SystemExit(f"MISMATCHED SCALE for {name}: h {eff_v:.5f} vs w {eff_actual:.5f}")
    manifest["regions"].append({
        "name": name, "region": [bx0, by0, bx1, by1],
        "render_crop": rp, "orig_crop": op,
        "effective_px_per_frame_px": round(eff_actual, 5),
        "zoom_factor": zoom,
        "crop_to_slide": {"formula": "x_slide = x0 + x_crop / effective",
                          "x0": bx0, "y0": by0},
        "description": desc,
    })
    print(f"   -> banked {rp.split('/')[-1]} + {op.split('/')[-1]}  (matched scale OK)")

with open(f"{QA}/crop_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(f"\nmanifest banked: {QA}/crop_manifest.json ({len(manifest['regions'])} regions)")
