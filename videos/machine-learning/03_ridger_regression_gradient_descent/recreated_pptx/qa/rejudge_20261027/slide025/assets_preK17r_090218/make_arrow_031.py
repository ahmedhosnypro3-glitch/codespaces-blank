# Hollow block arrow for slide 031 (left of the param table): PIL-traced
# polygon from unique_slides/slide_031.jpg ink map -> 600dpi transparent PNG.
# LibreOffice's downArrow preset renders shaft-only in this deck's renders
# (measured qa/slide031: box y313 h44 -> ink stops y336, head missing), so the
# arrow ships as an image asset, placed at exact px/600 size like curve_032.
import math
import json
from PIL import Image, ImageDraw

DPI = 600.0
S = DPI / 72.0  # asset px per frame pt

# polygon in local pt (y down), pointing down: w=17, h=37, shaft 11 wide,
# head 17 wide x 10.5 tall (measured off the ink map: barbs y341..345 span
# x151..169, tip (157,351), top cap x162..172 y314..317)
# ink (incl. 3pt stroke) must land in the measured bbox x151.5..174,
# y314..351; the 3pt stroke adds ~3pt to every span, so the polygon is
# drawn ~0.92x of the ink spans
SC = 0.92
cx = 8.5 * SC
W, H = 17.0 * SC, 37.0 * SC
a, b, hh = 5.5 * SC, 8.5 * SC, 10.5 * SC
local = [
    (cx - a, 0.0), (cx + a, 0.0),
    (cx + a, H - hh), (cx + b, H - hh),
    (cx, H), (cx - b, H - hh), (cx - a, H - hh),
]

# rotate 16 deg clockwise (screen coords: bottom tip swings left)
th = math.radians(16.0)
cos, sin = math.cos(th), math.sin(th)
ax, ay = cx, H / 2.0
rot = []
for (X, Y) in local:
    dx, dy = X - ax, Y - ay
    rot.append((dx * cos - dy * sin + ax, dx * sin + dy * cos + ay))

# translate so the outer polygon bbox sits at (153, 315.5)..(172.6, 349.6)
# frame pt (stroke then bleeds ~1.5px to the measured ink bbox
# x151.5..174, y314..351)
xs = [p[0] for p in rot]
ys = [p[1] for p in rot]
tx = 153.0 - min(xs)
ty = 315.5 - min(ys)
poly = [(X + tx, Y + ty) for (X, Y) in rot]

MARGIN = 4.0  # pt of transparent padding around the ink
x0 = min(p[0] for p in poly) - MARGIN
y0 = min(p[1] for p in poly) - MARGIN
x1 = max(p[0] for p in poly) + MARGIN
y1 = max(p[1] for p in poly) + MARGIN
w_px = int(round((x1 - x0) * S))
h_px = int(round((y1 - y0) * S))

im = Image.new("RGBA", (w_px, h_px), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
pts = [((X - x0) * S, (Y - y0) * S) for (X, Y) in poly]
d.polygon(pts, fill=(255, 255, 255, 255))
d.line(pts + [pts[0]], fill=(139, 26, 43, 255), width=int(round(3.0 * S)), joint="curve")
# round the joint nubs at the concave barb corners
r = int(round(1.5 * S))
for (X, Y) in (pts[2], pts[5]):
    d.ellipse([X - r, Y - r, X + r, Y + r], fill=(139, 26, 43, 255))

OUT_PNG = "arrow_031.png"
im.save(OUT_PNG)

side = {
    "path": OUT_PNG,
    "w_px": w_px,
    "h_px": h_px,
    "ink_x0": MARGIN * S, "ink_y0": MARGIN * S,
    "ink_x1": (MARGIN + (x1 - x0 - 2 * MARGIN)) * S,
    "ink_y1": (MARGIN + (y1 - y0 - 2 * MARGIN)) * S,
    "frame_x0": x0, "frame_y0": y0, "frame_x1": x1, "frame_y1": y1,
    "x_in": w_px / DPI, "y_in": h_px / DPI,
    "dpi": int(DPI),
}
with open("arrow_031.json", "w") as f:
    json.dump(side, f)
print("wrote", OUT_PNG, (w_px, h_px), "frame box", (round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)))
