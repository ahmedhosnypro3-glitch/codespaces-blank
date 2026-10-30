#!/usr/bin/env python3
"""Build an upscaled composite crop of slide 017's two text regions
(top-right label callout + bottom-left piecewise box) for a colour-accurate
vision read of the original."""
from PIL import Image

SRC = "unique_slides/slide_017.jpg"
im = Image.open(SRC).convert("RGB")

label = im.crop((605, 168, 830, 212)).resize((225 * 4, 44 * 4), Image.LANCZOS)
eqbox = im.crop((112, 452, 418, 512)).resize((306 * 4, 60 * 4), Image.LANCZOS)

W = max(label.width, eqbox.width) + 40
H = label.height + eqbox.height + 120
out = Image.new("RGB", (W, H), (255, 255, 255))
out.paste(label, (20, 20))
out.paste(eqbox, (20, label.height + 80))
out.save("recreated_pptx/build/slide017_text_regions_x4.png")
print("saved", out.size)
