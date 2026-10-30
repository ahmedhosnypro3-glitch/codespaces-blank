import os
from PIL import Image
D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
CROPS = {
  "048": [
    ("topband",  (60, 48, 740, 135)),
    ("aug_iter", (58, 135, 265, 315)),
    ("calc_r12", (268, 135, 860, 275)),
    ("calc_r56", (268, 400, 860, 532)),
  ],
  "049": [
    ("topband",  (60, 48, 740, 135)),
    ("aug_stop", (58, 140, 265, 400)),
    ("calc_r12", (268, 135, 860, 275)),
    ("calc_r56", (268, 398, 860, 532)),
  ],
  "050": [
    ("topbox",     (60, 48, 740, 135)),
    ("pinkbox",    (735, 50, 845, 180)),
    ("aug_caption",(55, 130, 255, 255)),
    ("chart",      (300, 165, 835, 495)),
    ("redstop",    (70, 270, 260, 405)),
  ],
  "051": [
    ("topcard",   (60, 48, 740, 135)),
    ("aug_redbox",(55, 140, 255, 312)),
    ("dec_r1",    (268, 133, 860, 200)),
    ("dec_r23",   (268, 200, 860, 335)),
  ],
}
for n, crops in CROPS.items():
    src = Image.open(f"{D}/unique_slides/slide_{n}.jpg").convert("RGB")
    assert src.size == (960, 540), src.size
    out = f"{D}/recreated_pptx/qa/slide{n}/prephase/crops"
    for name, box in crops:
        c = src.crop(box)
        c2 = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
        c2.save(f"{out}/crop_{n}_{name}_orig.png")
        print(f"slide{n} {name}: box={box} size={c2.size}")
