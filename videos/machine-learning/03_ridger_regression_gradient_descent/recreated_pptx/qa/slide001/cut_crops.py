#!/usr/bin/env python3
"""Cut zoomed crop-pairs for slide 001 attempt 1 (Procedure B, judge_protocol_03.md).

Regions (frame-px slide-space, ~8px padding around measured ink):
  title       3-line red title block        ink x278..668 y127..274
  preparedby  subtitle + Prepared By block   ink x348..627 y313..417
  instructors 2-entry instructors block      ink x84..376 y422..529
  logo        institutional logo (tiny text) ink x592..889 y459..531

Matched effective scale: render crop is native 150dpi (S = H_render/540 = 2.0833
render-px per frame-px); the original crop is LANCZOS-upscaled to the SAME
output pixel size as the render crop, so output_px/frame_px is identical for
both images. Forensics (ink px, ink span) are measured on BOTH crops and banked
for judge-rebuttal law.
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{VID}/recreated_pptx/qa/slide001"
R = Image.open(f"{QA}/render_1.png").convert("RGB")
O = Image.open(f"{VID}/unique_slides/slide_001.jpg").convert("RGB")
S = R.height / 540.0
print(f"render {R.width}x{R.height} scale {S:.4f}; original {O.width}x{O.height}")

REGIONS = [
    ("title",       (270, 119, 676, 282),  "three-line red title block (large bold red text)"),
    ("preparedby",  (340, 305, 635, 425),  "subtitle + Prepared By attribution block (small blue text)"),
    ("instructors", (76, 414, 384, 537),   "Instructors header + two name/email entries (left-aligned small text)"),
    ("logo",        (584, 444, 897, 537),  "institutional Zewail City logo (teal panel + tiny Arabic/English text)"),
]

for name, (x0f, y0f, x1f, y1f), desc in REGIONS:
    rb = (round(x0f * S), round(y0f * S), round(x1f * S), round(y1f * S))
    rc = R.crop(rb)
    oc = O.crop((x0f, y0f, x1f, y1f)).resize(rc.size, Image.LANCZOS)
    rc.save(f"{QA}/crop_1_{name}_render.png")
    oc.save(f"{QA}/crop_1_{name}_orig.png")
    line = f"crop_1_{name}: frame box x{x0f}..{x1f} y{y0f}..{y1f} -> output {rc.width}x{rc.height}px"
    for tag, im in (("render", rc), ("orig", oc)):
        a = np.asarray(im.convert("L"))
        ink = a < 180
        ys, xs = np.where(ink)
        if len(xs):
            fx0 = x0f + xs.min() / (rc.width / (x1f - x0f))
            fx1 = x0f + xs.max() / (rc.width / (x1f - x0f))
            fy0 = y0f + ys.min() / (rc.height / (y1f - y0f))
            fy1 = y0f + ys.max() / (rc.height / (y1f - y0f))
            line += f" | {tag}: ink={int(ink.sum())} span_frame_x {fx0:.1f}..{fx1:.1f} y {fy0:.1f}..{fy1:.1f}"
        else:
            line += f" | {tag}: NO INK"
    print(line)
print("\nWROTE", *[f"{QA}/crop_1_{n}_{t}.png" for n, _, _ in REGIONS for t in ("render", "orig")], sep="\n  ")
