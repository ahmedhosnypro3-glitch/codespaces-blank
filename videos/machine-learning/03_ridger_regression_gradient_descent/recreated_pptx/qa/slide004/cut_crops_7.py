"""Cut the attempt-7 Procedure B crop pair for the right-hand 'Where:' block.

Region bbox is the deck's own measured one (crop_pairs_004_v4.py: where_block
x490..890, y230..375 in 960x540 frame px). Both images are cut at the SAME
slide-space region; the original crop is LANCZOS-upscaled to the render crop's
pixel size so output_px/frame_px is equal on both axes.
"""
from PIL import Image

DECK = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent")
QA = DECK + "/recreated_pptx/qa/slide004/"
ORIG = DECK + "/unique_slides/slide_004.jpg"
REND = QA + "render_7.png"

X0, Y0, X1, Y1 = 490, 230, 890, 375
DESC = "Where block: 4 lines incl. the three X/Y/W facts with the => arrows"

orig = Image.open(ORIG).convert("RGB")
rend = Image.open(REND).convert("RGB")
SX = rend.size[0] / 960.0
SY = rend.size[1] / 540.0

fw, fh = X1 - X0, Y1 - Y0
rw, rh = int(round(fw * SX)), int(round(fh * SY))
rx, ry = int(round(X0 * SX)), int(round(Y0 * SY))

rc = rend.crop((rx, ry, rx + rw, ry + rh))
oc = orig.crop((X0, Y0, X1, Y1)).resize((rw, rh), Image.LANCZOS)
rc.save(QA + "crop_7_where_block_render.png")
oc.save(QA + "crop_7_where_block_orig.png")
with open(QA + "crop_7_where_block_desc.txt", "w", encoding="utf-8") as f:
    f.write(DESC + "\n")

print("where_block: frame x%d..%d y%d..%d" % (X0, X1, Y0, Y1))
print("  render crop %dx%d  orig crop %dx%d" % (rc.size[0], rc.size[1], oc.size[0], oc.size[1]))
print("  effective scale render=%.4f/%.4f orig=%.4f/%.4f"
      % (rc.size[0] / fw, rc.size[1] / fh, oc.size[0] / fw, oc.size[1] / fh))
