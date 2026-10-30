#!/usr/bin/env python3
"""Re-cut slide 051 attempt-5 crop pairs from render_5.png (attempt-3 recipe)."""
from PIL import Image

BASE = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
D = f"{BASE}/recreated_pptx/qa/slide051"
S = 2001 / 960.0

render = Image.open(f"{D}/render_5.png")
orig = Image.open(f"{BASE}/unique_slides/slide_051.jpg")

REGIONS = {
    "mats": (78, 58, 668, 132),
    "aug":  (78, 140, 230, 250),
    "dec":  (276, 138, 862, 335),
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    box = (round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S))
    rc = render.crop(box)
    oc = orig.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(f"{D}/crop_5_{name}_render.png")
    oc.save(f"{D}/crop_5_{name}_orig.png")
    print(name, rc.size)
