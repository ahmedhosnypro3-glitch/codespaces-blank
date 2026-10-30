import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0
ra = np.asarray(R).astype(float)
ro = np.asarray(O).astype(float)


def rlum(x, y):
    return 0.299 * ra[int(y * s), int(x * s), 0] + 0.587 * ra[int(y * s), int(x * s), 1] + 0.114 * ra[int(y * s), int(x * s), 2]


def olum(x, y):
    return 0.299 * ro[y, x, 0] + 0.587 * ro[y, x, 1] + 0.114 * ro[y, x, 2]


def dump(name, lumfn, x0, x1, y0, y1):
    print(f"### {name}")
    for y in range(y0, y1):
        row = "".join("#" if lumfn(x, y) < 160 else ("+" if lumfn(x, y) < 200 else ".") for x in range(x0, x1))
        print(f"{y:4d}| {row}")
    print()


dump("ORIG ell1 x513..617 y213..249", olum, 513, 617, 213, 249)
dump("RENDER ell1 x513..617 y213..249", rlum, 513, 617, 213, 249)
# value glyphs only, between brackets x569..583
dump("ORIG B2 digits x569..584 y276..346", olum, 569, 584, 276, 346)
dump("RENDER B2 digits x569..584 y276..346", rlum, 569, 584, 276, 346)
