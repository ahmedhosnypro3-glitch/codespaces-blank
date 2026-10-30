#!/usr/bin/env python3
"""Procedure B crop-pair preparation for slide 033 (zoom leg, attempt 4).

Cut ONE pair per dense region of the ORIGINAL frame (960x540, 1px = 1pt) and of the
150dpi render (render_5.png, 2001x1125), at EXACTLY matched effective scale.

Matched-scale method (per judge_protocol_03.md Procedure B step 3: output_px/frame_px
must be EQUAL for both images on BOTH axes) — same construction as slide038:
  * render crop: crop the render at frame coords x SX / x SY with
      SX = 2001/960 = 2.084375,  SY = 1125/540 = 2.083333
    (the render is 2001 px wide because LibreOffice rounds 13.33in*150dpi = 1999.5 up;
     using the render's REAL scale factors avoids any per-axis mismatch).
  * original crop: crop the original at the same FRAME bbox, then LANCZOS-resize to
    the render crop's EXACT pixel dimensions.
  => both members of a pair have identical pixel dimensions and therefore identical
  output_px/frame_px on each axis. No approximation, no 8% drift trap.

REGION CHOICE:
  plot    : THE mandated crop — the non-convex curve plus every trajectory marker
            measured in the original frame: 11 vertical / 9 horizontal gray
            gridlines (x615..811, y115..264), the #00B050 curve (x612-832, y110-264,
            ONE smooth curve), the red initial-point marker (x618-628 y142-152),
            the orange #EE730C arrowhead (x629-648 y115-138), the green #8FFF17
            square at the reached minimum (x628-644 y235-245), and the pale pink
            #F7C9FA "Reach Local Minima" callout (x612-705 y257-296), plus both
            tick-label rows. Region x560-915 y100-312 (frame px).
  table   : the 8-row x 16-value data table with its 5 fill bands and cyan insert
            (x86-869 y320-519) — the densest ink block on the slide.
  center  : the equation callout f(x) = (x^2 cos(x)-x)/10 with its two green
            annotation lines (x244-599 y252-301).
  title   : title + both subtitle lines (x110-470 y55-150).

Banked: qa/slide033/crop_5_<name>_render.png + crop_5_<name>_orig.png
The previous attempt-3 crops (crop_3_*) were cut from render_3.png and are
therefore STALE relative to the attempt-4 rebuild; they are kept as evidence but
the judge legs use crop_5_*.
"""
import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_033.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide033/render_5.png"
QA = f"{DECK}/recreated_pptx/qa/slide033"

orig = Image.open(ORIG).convert("RGB")
rend = Image.open(REND).convert("RGB")
OW, OH = orig.size          # 960 540
RW, RH = rend.size          # 2001 1125
SX, SY = RW / OW, RH / OH   # render px per frame px

REGIONS = {
    "plot": (560, 100, 915, 312,
             "the non-convex curve with its gridlines, the red initial-point marker, "
             "the orange arrowhead, the green square at the reached minimum, the pink "
             "'Reach Local Minima' callout, and both tick-label rows"),
    "table": (80, 316, 875, 523,
              "the 8-row x 16-value data table, its 5 fill bands and cyan insert"),
    "center": (238, 248, 605, 305,
               "the f(x) = (x^2 cos(x)-x)/10 equation callout with the two green "
               "annotation lines"),
    "title": (108, 52, 470, 152,
              "title and both subtitle lines"),
}

print(f"original {OW}x{OH}  render {RW}x{RH}  scale SX={SX:.6f} SY={SY:.6f} "
      f"(protocol ref H_render/540={RH / 540:.6f})")
for name, (x0, y0, x1, y1, desc) in REGIONS.items():
    rc = rend.crop((round(x0 * SX), round(y0 * SY), round(x1 * SX), round(y1 * SY)))
    oc = orig.crop((x0, y0, x1, y1))
    oc2 = oc.resize(rc.size, Image.LANCZOS)
    rp, op = f"{QA}/crop_5_{name}_render.png", f"{QA}/crop_5_{name}_orig.png"
    rc.save(rp); oc2.save(op)
    ex, ey = rc.size[0] / (x1 - x0), rc.size[1] / (y1 - y0)
    ox, oy = oc2.size[0] / (x1 - x0), oc2.size[1] / (y1 - y0)
    print(f"{name:8s} frame bbox ({x0},{y0},{x1},{y1}) -> render {rc.size} / orig {oc2.size} ; "
          f"effective scale x {ex:.6f} vs {ox:.6f}, y {ey:.6f} vs {oy:.6f} ; "
          f"MATCH={'OK' if rc.size == oc2.size else 'MISMATCH'}")
print("crop pairs banked:", ", ".join(f"crop_5_{n}_*" for n in REGIONS))
