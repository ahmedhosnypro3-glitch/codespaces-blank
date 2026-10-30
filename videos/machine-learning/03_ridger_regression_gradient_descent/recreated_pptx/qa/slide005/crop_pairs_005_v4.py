#!/usr/bin/env python3
"""Cut the Procedure B crop pairs for slide 005 from render_6.png.

Protocol law (shared_patterns/judge_protocol_03.md §Procedure B):
  - crop BOTH images at the SAME slide-space bbox (frame px, ~8px padding);
  - scale = H_render/540 = 1125/540 = 2.0833 render-px per frame-px;
  - LANCZOS-upscale the original crop by that factor and force the two crops to
    identical pixel dimensions (an 8% mismatch fabricates drift MAJORs).
Regions are the ORIGINAL's dense ink (qa/slide005/ink_bands_slide005.json):
  eqstack  (88,360)-(886,510): the two derivative equations, the
          "(X^TX)W -> X^TY ->" arrow chain, the green-boxed W = (X^TX)^-1X^TY
          and the lower-right Remember box.
  losseqs  (68,100)-(886,240): the three Loss expansions plus the upper-right
          Remember box.
"""
from PIL import Image

SCALE = 1125 / 540.0
Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/"
RENDER = Q + "render_6.png"
ORIG = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
        "unique_slides/slide_005.jpg")

REGIONS = {
    "eqstack": (88, 360, 886, 510),
    "losseqs": (68, 100, 886, 240),
}


def main():
    r = Image.open(RENDER)
    o = Image.open(ORIG)
    for name, (x0, y0, x1, y1) in REGIONS.items():
        rc = r.crop((int(x0 * SCALE), int(y0 * SCALE), int(x1 * SCALE), int(y1 * SCALE)))
        oc = o.crop((x0, y0, x1, y1))
        w, h = oc.size
        oc2 = oc.resize((int(round(w * SCALE)), int(round(h * SCALE))), Image.LANCZOS)
        if oc2.size != rc.size:               # guard against rounding drift
            oc2 = oc2.resize(rc.size, Image.LANCZOS)
        rc.save(Q + "crop_4_%s_render.png" % name)
        oc2.save(Q + "crop_4_%s_orig.png" % name)
        print("%-8s region %-22s render %s orig %s matched=%s"
              % (name, (x0, y0, x1, y1), rc.size, oc2.size, rc.size == oc2.size))


if __name__ == "__main__":
    main()
