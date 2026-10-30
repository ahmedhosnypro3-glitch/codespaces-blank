#!/usr/bin/env python3
"""Generate the six topbox band-delimiter arc PNGs (600dpi RGBA) for slide 003,
replacing straight lines per adjudication_att34_topbox.md. Style follows the
judge-certified midcol arcs: 32px wide, hairline stroke, parabolic paren bow.
Geometry: bulge cores at measured x, span y146..263 (h=117pt=975px @600dpi).
Ink colors sampled from the original stroke cores (faint on-fill weight)."""
from PIL import Image, ImageDraw
import math

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens"

im = Image.open(ORIG).convert("RGB")
px = im.load()

# (name, core_x, side)  side L = "(" bulges left, R = ")" bulges right
COLS = [
    ("col1_L", 296.5, "L"), ("col1_R", 331.5, "R"),
    ("col2_L", 373.5, "L"), ("col2_R", 409.0, "R"),
    ("col4_L", 517.5, "L"), ("col4_R", 552.5, "R"),
]

def sample_color(core_x):
    """darkest-stroke avg over clean rows y206..224 (between entry rows)"""
    xi = int(round(core_x))
    samples = []
    for y in range(206, 225):
        for x in range(xi - 2, xi + 3):
            samples.append(px[x, y])
    samples.sort(key=lambda c: sum(c))
    core = samples[:12]
    return tuple(round(sum(c[i] for c in core) / len(core)) for i in range(3))

W, H = 32, 975          # 3.84pt x 117pt at 600dpi
STROKE = 5              # px (~0.6pt)
BOW = 17                # sagitta 17px = 2.04pt at slide scale
MID_X = {"L": 2.5, "R": 29.5}

for name, core_x, side in COLS:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    color = sample_color(core_x) + (255,)
    mid = MID_X[side]
    end = W - 4 - mid      # hook side, keeps stroke inside the canvas
    pts = []
    for i in range(0, 201):
        t = i / 200.0
        y = t * (H - 1)
        # parabola: bulge at middle, hooks at ends
        x = mid + (end - mid) * (2 * t - 1) ** 2
        pts.append((x, y))
    d.line(pts, fill=color, width=STROKE, joint="curve")
    p = "%s/%s.png" % (OUT, name)
    img.save(p)
    ink = sum(1 for y in range(H) for x in range(W) if img.getpixel((x, y))[3] > 0)
    print("%s: color=%s ink_px=%d  place: x=%.2f y=146 w=3.8 h=117 (bulge core %.1f)"
          % (name, color[:3], ink,
             core_x - mid * 72 / 600 if side == "L" else core_x - mid * 72 / 600,
             core_x))
