#!/usr/bin/env python3
"""Cut slide-025 crop pairs at MATCHED effective scale (Procedure B, judge_protocol_03.md).

render_1.png is 2001x1125 (150dpi) -> scale = 1125/540 = 2.08333 render-px per frame-px.
Both sides are cropped at the same slide-space region and the ORIGINAL crop is
LANCZOS-upscaled by 2.08333 so output_px/frame_px is EQUAL per axis.

Regions (frame px, ~8px padding) follow the FINAL measured geometry:
  TL plot x60..460 y116..290 | TR plot x480..898 y116..316
  BL plot x60..460 y296..527 | BR plot x480..898 y346..530
  label boxes LB1 (270..406,137..179) LB2 (475..612,184..226)
               LB3 (474..612,351..392) LB4 (382..519,448..490)
"""
from PIL import Image

R = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_025"
O = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"

render = Image.open(R + "/render_1.png").convert("RGB")
orig = Image.open(O).convert("RGB")
S = render.size[1] / 540.0
print("render", render.size, "scale = %.5f render-px/frame-px" % S)

REGIONS = {
    "lbl_upper": (255, 130, 625, 235),   # LB1 + LB2 blue label boxes
    "lbl_lower": (375, 345, 528, 495),   # LB3 + LB4 blue label boxes
    "tl":        (58, 114, 462, 292),    # concave dome + 2 red max lines + ticks
    "tr":       (478, 114, 900, 318),    # convex bowl + 2 red min lines + ticks
    "bl":        (58, 294, 462, 529),    # non-convex + red line + 4 annotations
    "br":       (478, 344, 900, 532),    # gradient-descent path + arrows
    "title":    (255, 58, 600, 92),      # red title
}

for name, (x0, y0, x1, y1) in REGIONS.items():
    rc = render.crop((int(round(x0 * S)), int(round(y0 * S)),
                      int(round((x1 + 1) * S)), int(round((y1 + 1) * S))))
    oc = orig.crop((x0, y0, x1 + 1, y1 + 1))
    ow, oh = oc.size
    ou = oc.resize((int(round(ow * S)), int(round(oh * S))), Image.LANCZOS)
    rc.save("%s/crop_1_%s_render.png" % (R, name))
    ou.save("%s/crop_1_%s_orig.png" % (R, name))
    ok = (abs(ou.size[0] / ow - rc.size[0] / (x1 - x0 + 1)) < 0.01
          and abs(ou.size[1] / oh - rc.size[1] / (y1 - y0 + 1)) < 0.01)
    print("%-10s frame %dx%d -> render %dx%d | orig %dx%d -> up %dx%d  matched=%s"
          % (name, x1 - x0 + 1, y1 - y0 + 1, rc.size[0], rc.size[1], ow, oh,
             ou.size[0], ou.size[1], ok))
print("done")
