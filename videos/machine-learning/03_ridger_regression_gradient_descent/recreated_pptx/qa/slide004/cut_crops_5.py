"""Cut attempt-5 Procedure B crop pairs at matched effective scale.
Render: native 150dpi (2.0844 render-px per frame-px in x, 2.0833 in y).
Original: LANCZOS-upscaled by the SAME factor so out_px/frame_px is equal.
"""
from PIL import Image

DECK = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
QA = DECK + "/recreated_pptx/qa/slide004/"
ORIG = DECK + "/unique_slides/slide_004.jpg"
REND = QA + "render_7.png"

SX = 2001 / 960.0   # render px per frame px (x)
SY = 1125 / 540.0   # render px per frame px (y)

regions = {
    # both top "Let" boxes — the MAJOR-alignment region
    "let_boxes": (75, 750, 94, 226, "the two top 'Let Y' / 'Let Yhat' boxes with their matrices and label captions"),
    # Remember callout
    "remember": (780, 886, 96, 157, "the Remember callout box with the ||a||2 = a^T a equation"),
}

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")

for name, (x0, x1, y0, y1, desc) in regions.items():
    # ~8px padding already baked into the bbox values
    rw = int(round((x1 - x0) * SX))
    rh = int(round((y1 - y0) * SY))
    rc = r.crop((int(round(x0 * SX)), int(round(y0 * SY)),
                 int(round(x0 * SX)) + rw, int(round(y0 * SY)) + rh))
    # original: 1:1 crop then LANCZOS upscale to the SAME pixel size
    oc = o.crop((x0, y0, x1, y1)).resize((rw, rh), Image.LANCZOS)
    rc.save(QA + f"crop_7_{name}_render.png")
    oc.save(QA + f"crop_7_{name}_orig.png")
    # region description for the --capture line
    with open(QA + f"crop_7_{name}_desc.txt", "w", encoding="utf-8") as f:
        f.write(desc + "\n")
    print(f"{name}: frame x{x0}..{x1} y{y0}..{y1} -> {rw}x{rh}px  "
          f"eff-scale render={rw/(x1-x0):.4f}/{rh/(y1-y0):.4f}  orig matched")
    print(f"   saved crop_7_{name}_render.png {rc.size} + crop_7_{name}_orig.png {oc.size}")
