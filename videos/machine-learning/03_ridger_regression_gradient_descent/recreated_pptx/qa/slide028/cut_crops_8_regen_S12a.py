#!/usr/bin/env python3
"""Slide 028 — Procedure B crop pairs (attempt 8 family), regenerated S12a.

The original cut script for this pair family was transient (its run is banked as
crop_8_cut.out.txt) and did not survive; this file re-implements the SAME
Procedure B (judge_protocol_03.md) at the SAME frame boxes recorded in
crop_8_cut.out.txt so the banked crop_8_*_judge.txt transcripts reference
existing bytes again.

Frame px = 1pt (960x540). Render is 150dpi (2001x1125).
Render crop is taken NATIVE (no resample); the original crop is LANCZOS-upscaled
to the render crop's exact size so both images share one effective scale.
Renders are regenerated from the CURRENT deliverable bytes (see README.txt).
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORIG = os.path.join(DECK, "unique_slides", "slide_028.jpg")
RENDER = os.path.join(HERE, "render_8.png")

REGIONS = {
    "left_curve": (152, 208, 400, 466),
    "right_curve": (498, 205, 792, 466),
}


def main():
    r = Image.open(RENDER).convert("RGB")
    o = Image.open(ORIG).convert("RGB")
    sx = r.size[0] / 960.0
    sy = r.size[1] / 540.0
    print(f"orig {o.size}  render {r.size}  per-axis scale x={sx:.6f} y={sy:.6f}")
    for name, (x0, y0, x1, y1) in REGIONS.items():
        rb = (round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy))
        rc = r.crop(rb)
        oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
        fr = os.path.join(HERE, f"crop_8_{name}_render.png")
        fo = os.path.join(HERE, f"crop_8_{name}_orig.png")
        rc.save(fr)
        oc.save(fo)
        print(f"{name:12s} frame=({x0},{y0},{x1},{y1}) out={rc.size} "
              f"eff_scale=({rc.size[0] / (x1 - x0):.4f},{rc.size[1] / (y1 - y0):.4f}) "
              f"renderpx={os.path.getsize(fr)} origpx={os.path.getsize(fo)}")


if __name__ == "__main__":
    main()
