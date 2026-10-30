#!/usr/bin/env python3
"""Slide 046 Procedure B — cut crop pairs at matched effective scale.

Frame px = 1pt. Render is 150dpi (2001x1125) => scale = H_render/540.
Render crop is taken NATIVE (no resample); the original crop is LANCZOS-upscaled
to the render crop's exact size so both images share one effective scale.
"""
import os
from PIL import Image

D = "videos/machine-learning/03_ridger_regression_gradient_descent"
Q = D + "/recreated_pptx/qa/slide046"
RENDER = Q + "/render_4.png"
ORIG = D + "/unique_slides/slide_046.jpg"

REGIONS = {
    "topmatrix": (60, 50, 725, 130),
    "zmatrix": (588, 55, 668, 112),
    "initial": (260, 54, 460, 112),
    "yellowbox": (732, 54, 836, 148),
    "augbox": (60, 136, 252, 258),
    "plot": (306, 167, 831, 488),
    "stopbox": (58, 325, 251, 421),
}


def main():
    r = Image.open(RENDER).convert("RGB")
    o = Image.open(ORIG).convert("RGB")
    s = r.size[1] / 540.0
    for name, (x0, y0, x1, y1) in REGIONS.items():
        rb = (round(x0 * s), round(y0 * s), round(x1 * s), round(y1 * s))
        rc = r.crop(rb)
        oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
        fr = f"{Q}/crop_4_{name}_render.png"
        fo = f"{Q}/crop_4_{name}_orig.png"
        rc.save(fr)
        oc.save(fo)
        print(f"{name:10s} frame=({x0},{y0},{x1},{y1}) out={rc.size} "
              f"eff_scale={rc.size[0] / (x1 - x0):.4f} renderpx={os.path.getsize(fr)} origpx={os.path.getsize(fo)}")


if __name__ == "__main__":
    main()
