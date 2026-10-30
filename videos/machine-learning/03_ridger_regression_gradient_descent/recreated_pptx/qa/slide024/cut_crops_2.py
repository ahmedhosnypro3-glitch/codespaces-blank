#!/usr/bin/env python3
"""Cut the zoomed crop-pair certificates for slide 024 ATTEMPT 2 (Procedure B
of shared_patterns/judge_protocol_03.md), this time from render_2.png — the
render proven by pixel identity (md5 fcb312e2f4636e352248e4bb055ce4f9 == fresh
rebuild) to serve the CURRENT deliverable pptx.

Procedure-B laws honoured (same as cut_crops_1.py):
  * crop-vs-crop ONLY (never the full frame as IMG2);
  * MATCHED effective scale per axis: both images are resized to EXACTLY the
    same output size from a float-exact box mapping (identical by construction);
  * ~8px padding on every region; icon gets an equal x3 zoom on BOTH sides.
Prints the manifest (also written as crop_manifest_2.json).
"""
import json

import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
VID = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{VID}/recreated_pptx/qa/slide024"
RENDER = f"{QA}/render_2.png"
ORIG = f"{VID}/unique_slides/slide_024.jpg"

BASE_SCALE = 1125 / 540.0          # 2.08333 render px per frame px
PAD = 8
K = "2"

REGIONS = [
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
assert (RW, RH) == (2001, 1125), f"render {RW}x{RH}, expected 2001x1125"

manifest = {"base_scale_render_px_per_frame_px": BASE_SCALE,
            "source_render": "render_2.png (md5 fcb312e2f4636e352248e4bb055ce4f9, "
                             "proven by rebuild to serve the current pptx)",
            "regions": []}
print(f"render {RW}x{RH} (scale {BASE_SCALE:.5f} px/frame-px) | original {OW}x{OH}")

for name, (x0, y0, x1, y1), zoom, desc in REGIONS:
    bx0, by0 = max(0, x0 - PAD), max(0, y0 - PAD)
    bx1, by1 = min(959, x1 + PAD), min(539, y1 + PAD)
    F_W, F_H = bx1 + 1 - bx0, by1 + 1 - by0

    eff = BASE_SCALE * zoom
    ow, oh = int(round(F_W * eff)), int(round(F_H * eff))

    rbox = (bx0 * BASE_SCALE, by0 * BASE_SCALE, (bx1 + 1) * BASE_SCALE, (by1 + 1) * BASE_SCALE)
    r_big = ren.resize((ow, oh), Image.LANCZOS, box=rbox)
    oc = ori.crop((bx0, by0, bx1 + 1, by1 + 1))
    o_big = oc.resize((ow, oh), Image.LANCZOS)

    eff_actual = ow / F_W
    rp = f"{QA}/crop_{K}_{name}_render.png"
    op = f"{QA}/crop_{K}_{name}_orig.png"
    r_big.save(rp)
    o_big.save(op)

    # BOTH sides must carry ink (a black/empty crop is not evidence)
    ra = np.asarray(r_big.convert("L"), dtype=int)
    oa = np.asarray(o_big.convert("L"), dtype=int)
    r_ink = int((ra < 200).sum()); o_ink = int((oa < 200).sum())
    if r_ink < 20 or o_ink < 20:
        raise SystemExit(f"{name}: crop has no ink (render {r_ink}, orig {o_ink})")

    eff_v = o_big.height / F_H
    if abs(eff_actual - ow / F_W) > 1e-9 or abs(eff_v - eff_actual) > 0.02:
        raise SystemExit(f"MISMATCHED SCALE for {name}: h {eff_v:.5f} vs w {eff_actual:.5f}")

    print(f"\n[{name}] slide-space region x{bx0}..{bx1} y{by0}..{by1} "
          f"({F_W}x{F_H} frame px), desc: {desc}")
    print(f"   render crop -> {r_big.size} ; original crop {oc.size} -> {o_big.size}")
    print(f"   effective scale BOTH sides: {eff_actual:.5f} px/frame-px (target {eff:.5f}, zoom {zoom})")
    print(f"   ink pixels (lum<200): render {r_ink}, orig {o_ink} — both carry ink")
    print(f"   -> banked crop_{K}_{name}_render.png + crop_{K}_{name}_orig.png (matched scale OK)")
    manifest["regions"].append({
        "name": name, "region": [bx0, by0, bx1, by1],
        "render_crop": rp, "orig_crop": op,
        "effective_px_per_frame_px": round(eff_actual, 5),
        "zoom_factor": zoom,
        "crop_to_slide": {"formula": "x_slide = x0 + x_crop / effective",
                          "x0": bx0, "y0": by0},
        "description": desc,
    })

with open(f"{QA}/crop_manifest_2.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(f"\nmanifest banked: {QA}/crop_manifest_2.json ({len(manifest['regions'])} regions)")
