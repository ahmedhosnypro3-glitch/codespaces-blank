"""Cut attempt-9 Procedure B crop pairs at matched effective scale.
Render: native 150dpi (2001x1125). Original: LANCZOS-upscaled by the SAME
factor so out_px/frame_px is equal on both images.
"""
from PIL import Image

DECK = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
QA = DECK + "/recreated_pptx/qa/slide004/"
ORIG = DECK + "/unique_slides/slide_004.jpg"
REND = QA + "render_9.png"

SX = 2001 / 960.0   # render px per frame px (x)
SY = 1125 / 540.0   # render px per frame px (y)

regions = {
    # att9: let-box assets PIL-composed at measured geometry (bars, underlines,
    # red subscript); region unchanged from att8
    "let_boxes": (75, 750, 94, 226, "the two top 'Let Y' / 'Let Yhat' boxes with their matrices and label captions"),
    # att9: duplicate-Required run deleted, W/Y recolored red
    "where_block": (490, 890, 230, 375, "Where block: 4 lines incl. the three X/Y/W facts with the => arrows"),
}

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")

for name, (x0, x1, y0, y1, desc) in regions.items():
    rw = int(round((x1 - x0) * SX))
    rh = int(round((y1 - y0) * SY))
    rc = r.crop((int(round(x0 * SX)), int(round(y0 * SY)),
                 int(round(x0 * SX)) + rw, int(round(y0 * SY)) + rh))
    oc = o.crop((x0, y0, x1, y1)).resize((rw, rh), Image.LANCZOS)
    rc.save(QA + f"crop_9_{name}_render.png")
    oc.save(QA + f"crop_9_{name}_orig.png")
    with open(QA + f"crop_9_{name}_desc.txt", "w", encoding="utf-8") as f:
        f.write(desc + "\n")
    print(f"{name}: frame x{x0}..{x1} y{y0}..{y1} -> {rw}x{rh}px  "
          f"eff-scale render={rw/(x1-x0):.4f}/{rh/(y1-y0):.4f}  orig matched")
