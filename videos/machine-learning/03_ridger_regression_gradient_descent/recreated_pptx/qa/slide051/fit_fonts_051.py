#!/usr/bin/env python3
"""Fit a font size to the original's measured DEC-row ink widths.

The frame is 960x540 with 1px = 1pt, so a 12pt font is rendered at 12px em.
Ink width is measured with PIL on the candidate font and compared to the
original's measured ink widths.
"""
from PIL import Image, ImageDraw, ImageFont

FONTS = {
    "LiberationSans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "LiberationSans-Bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "LiberationSans-Italic": "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    "Carlito": "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
    "Carlito-Bold": "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf",
    "Carlito-Italic": "/usr/share/fonts/truetype/crosextra/Carlito-Italic.ttf",
}

TARGETS = [
    ("Positive > 0", "LiberationSans", 63),
    ("Negative < 0", "LiberationSans", 69),
    ("Not > 0 , Not < 0", "LiberationSans", 87),
    ("Class I", "LiberationSans-Bold", 40),
    ("Class II", "LiberationSans-Bold", 45),
    ("Undefined Class", "LiberationSans-Bold", 88),
]


def ink_width(text, path, size):
    f = ImageFont.truetype(path, size)
    img = Image.new("L", (400, 60), 255)
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, font=f, fill=0)
    bb = img.point(lambda v: 255 if v < 200 else 0).getbbox()
    return bb[2] - bb[0], bb[3] - bb[1]


for size in (11, 12, 13, 14, 15):
    print("--- %dpt ---" % size)
    for text, fam, target in TARGETS:
        w, h = ink_width(text, FONTS[fam], size)
        print("   %-22s %-20s ink w=%3d (target %3d) h=%2d" % (text, fam, w, target, h))

print("\n--- d(Z1) label candidates (italic d + ( + Z + sub + )) ---")
for fam in ("LiberationSans-Italic", "Carlito-Italic"):
    for size in (11, 12, 13, 14):
        w, h = ink_width("d(Z1)", FONTS[fam], size)
        print("   %-22s %2dpt ink w=%3d h=%2d" % (fam, size, w, h))

print("\n--- '(0 0)' blue candidates ---")
for fam in ("LiberationSans", "Carlito"):
    for size in (11, 12, 13, 14):
        w, h = ink_width("(0 0)", FONTS[fam], size)
        print("   %-22s %2dpt ink w=%3d h=%2d" % (fam, size, w, h))
