#!/usr/bin/env python3
"""Paren-variant stacked column vector for slide 049 (049h adjudication: ALL
049 delimiters are tall parentheses, not house matrix brackets).

Same canvas as qa/slide049/render_wcol_049g.py (certified geometry):
  XB = 18 (left stroke centre, px), XR = XB + gap_pt*600/72
  values centred between the strokes, bracket overshoot OVER=2.2pt past the
  value ink block, stroke 0.9pt
Only change: the straight serif-bracket strokes are replaced by bezier
parentheses (gen_parens044 pattern, S=1.5pt, D=1.0pt) that BOW AT XB/XR —
the bow apex sits on XB/XR and the tips lean inward by D.

Args: out.png fontsize_pt color gap_pt row1 [row2 ...]
Prints a sidecar dict: {path,w_px,h_px,w_in,h_in,dpi,fontsize_pt,color,rows,
ink_left_px,ink_top_px,pt_per_px}
"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
DPI = 600
px = lambda pt: int(round(pt * DPI / 72.0))

OVER_PT = 2.2       # paren overshoot past the value ink block, both sides
STROKE_PT = 1.5     # paren stroke (certified 044 S)
D_PT = 1.0          # bow depth (tips lean in by D from the apex)
XB = 18             # left bow apex, px from the PNG's left edge

out, fs, color, gap_pt, rows = sys.argv[1], float(sys.argv[2]), sys.argv[3], \
    float(sys.argv[4]), sys.argv[5:]
fs = int(fs)
font = ImageFont.truetype(FONT, px(fs))
col = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255)

stroke = max(3, px(STROKE_PT))
over = px(OVER_PT)
span_px = px(gap_pt)
XR = XB + span_px
CX = (XB + XR) / 2.0

tmp = Image.new("RGBA", (10, 10))
d0 = ImageDraw.Draw(tmp)


def ink_box(text):
    probe = Image.new("RGBA", (1600, 400), (0, 0, 0, 0))
    ImageDraw.Draw(probe).text((400, 120), text, font=font, fill=col)
    x0, y0, x1, y1 = probe.getbbox()
    return x0 - 400, y0 - 120, x1 - 400, y1 - 120


bboxes = [ink_box(r) for r in rows]

value_top = over
value_bot = max(value_top + i * px(16.4) + (b[3] - b[1]) for i, b in enumerate(bboxes))
by0, by1 = 0, value_bot + over
W = XR + stroke // 2 + 3
H = by1 + 1

canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(canvas)
for i, (r, b) in enumerate(zip(rows, bboxes)):
    y = value_top + i * px(16.4)
    x = CX - (b[2] - b[0]) / 2.0 - b[0]
    d.text((x, y - b[1]), r, font=font, fill=col)


def bezier_x(t, x_apex, x_tip):
    return (1 - t) ** 2 * x_tip + 2 * (1 - t) * t * (2 * x_apex - x_tip) \
        + t ** 2 * x_apex


def draw_paren(x_apex_px, side):
    dpt = px(D_PT)
    tip = x_apex_px - dpt if side == "lp" else x_apex_px + dpt
    t = np.linspace(0.0, 1.0, 400)
    xs = bezier_x(t, x_apex_px, tip)
    ys = np.linspace(0, by1, 400)
    pts = list(zip(xs, ys))
    d.line(pts, fill=col, width=stroke, joint="curve")
    r = stroke // 2
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=col)


draw_paren(XB, "lp")
draw_paren(XR, "rp")

canvas.save(out)
a = np.array(canvas)[:, :, 3]
ys_i, xs_i = np.nonzero(a > 30)
print(json.dumps({"path": out, "w_px": W, "h_px": H,
                  "w_in": round(W / DPI, 5), "h_in": round(H / DPI, 5),
                  "dpi": DPI, "fontsize_pt": fs, "color": color, "rows": rows,
                  "ink_left_px": int(xs_i.min()), "ink_top_px": int(ys_i.min()),
                  "pt_per_px": 72.0 / DPI}))
