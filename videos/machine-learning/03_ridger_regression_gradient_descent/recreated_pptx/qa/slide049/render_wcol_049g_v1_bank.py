#!/usr/bin/env python3
"""2D stacked bracketed column vector for slide 049's W result column.

Extends the banked render_matrix049.sh (which made the d(xN) matrices) to N rows,
keeping its bracket geometry constants verbatim. Liberation Sans (Arial-metric),
600dpi transparent PNG. The deck's mathtext renderer cannot express a matrix
environment, so this is the house 2D route for stacked bracketed columns.

Args: out.png fontsize_pt color row1 [row2 ...]
Prints the eq_*.json sidecar line: {path,w_px,h_px,w_in,h_in,dpi,fontsize_pt,color,rows}
"""
import sys, json
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
DPI = 600
px = lambda pt: int(round(pt * DPI / 72.0))

out, fs, color, rows = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4:]
fs = int(fs)
font = ImageFont.truetype(FONT, px(fs))
col = (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), 255)

tmp = Image.new("RGBA", (10, 10))
d0 = ImageDraw.Draw(tmp)
bboxes = [d0.textbbox((0, 0), r, font=font) for r in rows]
num_w = max(b[2] - b[0] for b in bboxes)

# geometry constants copied verbatim from render_matrix049.sh
line_h, line_gap, pad_v = px(fs * 1.05), px(fs * 0.22), px(fs * 0.10)
stroke, serif, margin = max(3, px(0.9)), px(2.2), px(2.0)
left_w = margin + stroke + serif
n = len(rows)
W = num_w + 2 * left_w
H = pad_v + n * line_h + (n - 1) * line_gap + pad_v

canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(canvas)
nx = left_w
for i, (r, b) in enumerate(zip(rows, bboxes)):
    y = pad_v + i * (line_h + line_gap)
    d.text((nx - b[0], y - b[1]), r, font=font, fill=col)

by0, by1 = pad_v - px(0.6), H - pad_v + px(0.6)
xb = serif
d.line([(xb, by0), (xb, by1)], fill=col, width=stroke)
d.line([(xb, by0), (xb + serif, by0)], fill=col, width=stroke)
d.line([(xb, by1), (xb + serif, by1)], fill=col, width=stroke)
xr = W - stroke // 2
d.line([(xr, by0), (xr, by1)], fill=col, width=stroke)
d.line([(xr - serif, by0), (xr, by0)], fill=col, width=stroke)
d.line([(xr - serif, by1), (xr, by1)], fill=col, width=stroke)

canvas.save(out)
print(json.dumps({"path": out, "w_px": W, "h_px": H,
                  "w_in": round(W / DPI, 5), "h_in": round(H / DPI, 5),
                  "dpi": DPI, "fontsize_pt": fs, "color": color, "rows": rows}))
