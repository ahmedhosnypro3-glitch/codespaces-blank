#!/usr/bin/env python3
# Mouse-pointer cursor PNG for slide 010, 600 dpi transparent, tip pointing up-left.
# Spec region [0.171,0.609,0.206,0.680] normalized -> 0.46655 x 0.5325 in.
import json, os
from PIL import Image, ImageDraw

DPI = 600
W_IN = (0.206 - 0.171) * 13.33   # 0.46655
H_IN = (0.680 - 0.609) * 7.5     # 0.5325
w_px = round(W_IN * DPI)
h_px = round(H_IN * DPI)

# classic pointer polygon, unit coords, tip at (0,0) pointing up-left
poly = [(0.00, 0.00), (0.00, 0.80), (0.20, 0.61), (0.34, 0.95),
        (0.46, 0.90), (0.32, 0.56), (0.58, 0.56)]
scale = min(w_px / 0.60, h_px / 0.98)
pts = [(x * scale, y * scale) for x, y in poly]

img = Image.new("RGBA", (w_px, h_px), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
outline = [(x + 2, y + 2) for x, y in pts]
d.polygon(outline, fill=(255, 255, 255, 255))
d.polygon(pts, fill=(0, 0, 0, 255))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cursor.png")
img.save(out)
meta = {"w_in": w_px / DPI, "h_in": h_px / DPI, "w_px": w_px, "h_px": h_px}
with open(out + ".json", "w") as f:
    json.dump(meta, f, indent=2)
print(out, meta)
