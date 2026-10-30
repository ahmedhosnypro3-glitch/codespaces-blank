#!/usr/bin/env python3
"""Cut the slide-044 zoomed crop pairs at matched effective scale (render 2.0844x)."""
from PIL import Image

QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044")
ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg")
RENDER = QA + "/render_1.png"

rim = Image.open(RENDER).convert("RGB")
oim = Image.open(ORIG).convert("RGB")
S = rim.size[0] / 960.0
print("render px per frame px = %.4f" % S)

# frame-px regions (slide space, with padding)
REGIONS = {
    "lefttables": (66, 52, 252, 312, "left tables + blue top band + red Iteration 3 badge"),
    "eqstack":    (272, 136, 856, 532, "the six d(x_i) computation bands"),
    "centretext": (236, 52, 730, 132, "centre text: Initial W bracket, Step eta, class-check matrix, rule"),
}

for name, (x0, y0, x1, y1, desc) in REGIONS.items():
    ow, oh = x1 - x0, y1 - y0
    rw, rh = int(round(ow * S)), int(round(oh * S))
    rc = rim.crop((int(round(x0 * S)), int(round(y0 * S)),
                   int(round(x0 * S)) + rw, int(round(y0 * S)) + rh))
    oc = oim.crop((x0, y0, x1, y1)).resize((rw, rh), Image.LANCZOS)
    rc.save(f"{QA}/crop_1_{name}_render.png")
    oc.save(f"{QA}/crop_1_{name}_orig.png")
    print(f"{name}: frame {ow}x{oh} -> render crop {rc.size}, orig crop {oc.size} "
          f"(eff scale {rc.size[0]/ow:.4f} vs {oc.size[0]/ow:.4f}) | {desc}")
