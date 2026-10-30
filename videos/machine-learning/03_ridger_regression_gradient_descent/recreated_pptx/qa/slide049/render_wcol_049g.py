#!/usr/bin/env python3
"""2D stacked bracketed column vector for slide 049's W result column (v2).

Geometry is set from the PIL measurement of unique_slides/slide_049.jpg
(per-row value ink, bracket stroke centres, line pitch):

  value line pitch 16.4pt   (original ink pitch, 3 lines -> 41.0pt ink block)
  bracket strokes  21.7pt apart, values centred between them
  bracket overshoot 2.2pt above and below the value ink block
  bracket stroke 0.9pt, serif tips 2.2pt (house matrix style)

The PNG's top pixel row is the bracket's top ink row, so the caller can place
the column by its bracket top. 600dpi transparent PNG.

Args: out.png fontsize_pt color row1 [row2 ...]
Prints the eq_*.json sidecar line: {path,w_px,h_px,w_in,h_in,dpi,fontsize_pt,color,rows}
"""
import sys, json
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
DPI = 600
px = lambda pt: int(round(pt * DPI / 72.0))

PITCH_PT = 16.4     # original value line pitch
OVER_PT = 2.2       # bracket overshoot past the value ink block, both sides
STROKE_PT = 0.9
SERIF_PT = 2.2
XB = 18             # left bracket stroke centre, px from the PNG's left edge
XR = 199            # right bracket stroke centre (181px = 21.72pt span)

out, fs, color, rows = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4:]
fs = int(fs)
font = ImageFont.truetype(FONT, px(fs))
col = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255)

stroke, serif = max(3, px(STROKE_PT)), px(SERIF_PT)
pitch = px(PITCH_PT)
over = px(OVER_PT)
CX = (XB + XR) / 2.0

tmp = Image.new("RGBA", (10, 10))
d0 = ImageDraw.Draw(tmp)


def ink_box(text):
    """True ink bbox of one rendered line, relative to its draw origin."""
    probe = Image.new("RGBA", (1600, 400), (0, 0, 0, 0))
    ImageDraw.Draw(probe).text((400, 120), text, font=font, fill=col)
    x0, y0, x1, y1 = probe.getbbox()
    return x0 - 400, y0 - 120, x1 - 400, y1 - 120


bboxes = [ink_box(r) for r in rows]

value_top = over
value_bot = max(value_top + i * pitch + (b[3] - b[1]) for i, b in enumerate(bboxes))
by0, by1 = 0, value_bot + over
W = XR + stroke // 2 + 3
H = by1 + 1

canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(canvas)
for i, (r, b) in enumerate(zip(rows, bboxes)):
    y = value_top + i * pitch
    x = CX - (b[2] - b[0]) / 2.0 - b[0]
    d.text((x, y - b[1]), r, font=font, fill=col)

d.line([(XB, by0 + stroke // 2), (XB, by1 - stroke // 2)], fill=col, width=stroke)
d.line([(XB, by0), (XB + serif, by0)], fill=col, width=stroke)
d.line([(XB, by1), (XB + serif, by1)], fill=col, width=stroke)
d.line([(XR, by0 + stroke // 2), (XR, by1 - stroke // 2)], fill=col, width=stroke)
d.line([(XR - serif, by0), (XR, by0)], fill=col, width=stroke)
d.line([(XR - serif, by1), (XR, by1)], fill=col, width=stroke)

canvas.save(out)
print(json.dumps({"path": out, "w_px": W, "h_px": H,
                  "w_in": round(W / DPI, 5), "h_in": round(H / DPI, 5),
                  "dpi": DPI, "fontsize_pt": fs, "color": color, "rows": rows}))
