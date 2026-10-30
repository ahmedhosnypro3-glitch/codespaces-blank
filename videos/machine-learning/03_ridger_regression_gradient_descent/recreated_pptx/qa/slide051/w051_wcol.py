#!/usr/bin/env python3
"""wcol-style stacked column with CORRECT-direction bezier parens.

Layout per render_wcol_049p.py (certified): LiberationSans digits, PITCH_PT row
pitch, 2.2pt paren overshoot past the value block, S=1.5pt stroke.
Parens per gen_parens049.py direction (belly = leftmost for lp at middle,
tips lean INWARD by D=1.0pt) — render_wcol_049p drew mirrored strokes.

usage: w051_wcol.py out.png fontsize_pt color gap_pt row1 [row2 ...]
Prints sidecar JSON with ink metrics (pt_per_px 0.12).
"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
DPI = 600
px = lambda pt: int(round(pt * DPI / 72.0))

OVER_PT = float(__import__("os").environ.get("W051_OVER_PT", "1.5"))
STROKE_PT = 1.5
D_PT = 1.0
PITCH_PT = 16.0
XB = 18  # lp belly-centre, px from PNG left edge

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
value_bot = max(value_top + i * px(PITCH_PT) + (b[3] - b[1]) for i, b in enumerate(bboxes))
by1 = value_bot + over
W = int(XR + stroke // 2 + 3)
H = int(by1 + 1)

canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(canvas)
for i, (r, b) in enumerate(zip(rows, bboxes)):
    y = value_top + i * px(PITCH_PT)
    x = CX - (b[2] - b[0]) / 2.0 - b[0]
    d.text((x, y - b[1]), r, font=font, fill=col)


def bezier_x(t, x_tip, x_ctrl):
    return (1 - t) ** 2 * x_tip + 2 * (1 - t) * t * x_ctrl + t ** 2 * x_tip


def draw_paren(x_belly_px, side):
    dpt = px(D_PT)
    # lp: belly (leftmost) at x_belly, tips lean RIGHT (inward) by dpt
    # rp: belly (rightmost) at x_belly, tips lean LEFT (inward) by dpt
    if side == "lp":
        x_belly, x_tip = x_belly_px, x_belly_px + dpt
    else:
        x_belly, x_tip = x_belly_px, x_belly_px - dpt
    x_ctrl = 2 * x_belly - x_tip
    t = np.linspace(0.0, 1.0, 400)
    xs = bezier_x(t, x_tip, x_ctrl)
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
                  "ink_left_px": int(xs_i.min()), "ink_right_px": int(xs_i.max()),
                  "ink_top_px": int(ys_i.min()), "ink_bot_px": int(ys_i.max()),
                  "pt_per_px": 72.0 / DPI}))
