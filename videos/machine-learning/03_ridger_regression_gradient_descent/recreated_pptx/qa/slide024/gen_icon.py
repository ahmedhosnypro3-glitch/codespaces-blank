#!/usr/bin/env python3
"""Generate the slide-024 bottom-center pen icon as a 600dpi transparent PNG
(build/assets/icon_024_pen.png) for embedding at exact px/600 size.

Measured from unique_slides/slide_024.jpg (qa/slide024/measure_frame.py,
measure_frame_2.py): a tiny dark pen glyph at slide-space bbox x 464..479,
y 506..522 (loose ink), strict core x 465..469 y 506..513 (nib) + diagonal
shaft centerline (466.5,513) -> (475,521.5). Darkest px (468,511)=(15,15,15);
dense core family 15..75 gray => stroke color 404040 (spec value, frame-
corroborated). Shape: pen NIB (small triangle, apex up-left) + diagonal
SHAFT running down-right — a pen/pencil at ~50 degrees, NOT a mouse cursor
(cursor arrows have a large filled head + short tail; measured is a small
4px nib + 13px shaft — ratio is pen-like).

Canvas: slide-space window x0=462.5, y0=504.5, w=17.52, h=19.56 slide px
(= 146x163 px at 600dpi). Embed in pptxgenjs at EXACT w=146/600, h=163/600.
"""
from PIL import Image, ImageDraw

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/icon_024_pen.png"
DPI = 600.0
X0, Y0 = 462.5, 504.5          # slide-space px of canvas top-left
CW, CH = 146, 163              # canvas px at 600dpi (17.52 x 19.56 slide px)
S = DPI / 72.0                 # 8.3333 png px per slide px

def P(slide_x, slide_y):
    return ((slide_x - X0) * S, (slide_y - Y0) * S)

img = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
GRAY = (64, 64, 64, 255)  # 404040

# nib: filled triangle, apex up-left, widening to its base — measured blob
# spans x 464..470, y 506..513 (darkest core (467..469, 510..512))
d.polygon([P(466.0, 505.8), P(464.4, 511.5), P(470.0, 512.8)], fill=GRAY)

# shaft: thick diagonal line, round caps — measured centerline (466.5,513)
# -> (475.0, 521.5), perpendicular width ~2.4 slide px
d.line([P(466.9, 511.8), P(475.2, 521.6)], fill=GRAY,
       width=int(round(2.4 * S)), joint="curve")
# round the shaft caps manually (ImageDraw.line caps are flat)
r = int(round(1.2 * S))
for (cx, cy) in ((466.9, 511.8), (475.2, 521.6)):
    x, y = P(cx, cy)
    d.ellipse([x - r, y - r, x + r, y + r], fill=GRAY)

img.save(OUT)
print("wrote", OUT, img.size)
