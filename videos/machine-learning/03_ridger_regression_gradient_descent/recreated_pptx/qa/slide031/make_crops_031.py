# Bank Procedure B crop pairs: render vs original, same slide-space bbox,
# effective scale matched per axis (protocol step 2-3).
from PIL import Image
import os
NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide031"
render = Image.open(QA + "/render_1.png").convert("RGB")
orig   = Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")
RW, RH = render.size
OW, OH = orig.size
sx, sy = RW / 960.0, RH / 540.0   # frame-px -> render-px, per axis

REGIONS = [
    ("table",     (55, 342, 901, 538), "main density table, 8 rows x 1 label col + 16 data cols, y~350-530"),
    ("graph",     (565, 58, 817, 275), "plot box of f(x)=(x-5)^2+1: blue parabola, black chord, red+green points, tick grid"),
    ("topblock",  (36, 52, 648, 342),  "title lines, parameter table, formula box, annotation box"),
]
for name, (x0, y0, x1, y1), _desc in REGIONS:
    rx0, ry0 = round(x0 * sx), round(y0 * sy)
    rx1, ry1 = round(x1 * sx), round(y1 * sy)
    rc = render.crop((rx0, ry0, rx1, ry1))
    oc = orig.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(QA + "/crop_1_%s_render.png" % name)
    oc.save(QA + "/crop_1_%s_orig.png" % name)
    print("cropped %-9s frame=(%d,%d,%d,%d) out=%dx%d scale=%.4f/%.4f"
          % (name, x0, y0, x1, y1, rc.size[0], rc.size[1],
             rc.size[0] / (x1 - x0), rc.size[1] / (y1 - y0)))
