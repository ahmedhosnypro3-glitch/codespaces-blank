#!/usr/bin/env python3
"""probe66 - chart-interior tone map + 4x zoomed crops of the annotation clusters.

Tone map: 'W' = >=253 (white), 'I' = 238..252 (chart interior F5F5F5), '.' other.
Purpose: find out whether the original draws an opaque white label background
(which would hide a dimension shaft running behind the text).
"""
import numpy as np
from PIL import Image

BASE = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/")
im = Image.open(BASE + "unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)

for tag, x0, y0, x1, y1 in (("LEFT", 100, 115, 460, 470),
                            ("RIGHT", 492, 115, 866, 470)):
    print(f"===== {tag} interior tone (step 10, x{x0}..{x1} y{y0}..{y1}) =====")
    print("      " + "".join(str((x // 10) % 10) for x in range(x0, x1 + 1, 10)))
    print("      " + "".join(str(x % 10) for x in range(x0, x1 + 1, 10)))
    for y in range(y0, y1 + 1, 10):
        row = ""
        for x in range(x0, x1 + 1, 10):
            r, g, b = a[y, x]
            if r >= 253 and g >= 253 and b >= 253:
                row += "W"
            elif 238 <= r <= 252 and 238 <= g <= 252 and 238 <= b <= 252:
                row += "I"
            else:
                row += "."
        print(f"  {y:3d} {row}")

print()
print("sample interior pixels:")
for (x, y) in [(120, 250), (300, 300), (210, 182), (250, 250), (215, 190),
               (205, 200), (620, 300), (640, 200), (640, 230), (700, 280)]:
    print(f"   ({x},{y}) {tuple(a[y, x])}")

# 4x zoomed crops of the annotation clusters (LANCZOS)
crops = {
    "probe66_L_annot_4x.png": (150, 120, 290, 300),
    "probe66_R_annot_4x.png": (570, 120, 720, 340),
}
for name, box in crops.items():
    c = im.crop(box).resize(((box[2] - box[0]) * 4, (box[3] - box[1]) * 4), Image.LANCZOS)
    c.save(BASE + "recreated_pptx/qa/slide009/" + name)
    print(f"saved {name} {c.size} from box {box}")
