# Bank Procedure B crop pairs for slide 032: render vs original, same slide-space
# bbox, effective scale matched per axis (protocol step 2-3).
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide032"
render = Image.open(QA + "/render_4.png").convert("RGB")
orig = Image.open(NS + "/unique_slides/slide_032.jpg").convert("RGB")
RW, RH = render.size
OW, OH = orig.size
sx, sy = RW / 960.0, RH / 540.0  # frame-px -> render-px, per axis

REGIONS = [
    ("graph", (565, 58, 818, 300),
     "plot box of f(x)=(x-5)^2+1: blue quadratic curve, gridlines, black axes + ticks, "
     "red vertical at x=5, black y=10 chord, green point (5,1), red point (~2.6,7)"),
    ("table", (290, 322, 608, 535),
     "iteration table: 5 colour bands holding 8 rows (x, f(x), x-delta, f(x-delta), "
     "x+delta, f(x+delta), slope, next x) x 6 data columns"),
    ("callouts", (372, 176, 560, 342),
     "equation callout stack: red-bordered equation box, 'X = 5', EFFFE2 min-value box, "
     "F7C9FA steps box, magenta down-arrow"),
    ("params", (68, 170, 216, 259),
     "parameter table: step 0.4 / initial X 3 / delta 0.1, three full-width coloured rows"),
]

for name, (x0, y0, x1, y1), _desc in REGIONS:
    rx0, ry0 = round(x0 * sx), round(y0 * sy)
    rx1, ry1 = round(x1 * sx), round(y1 * sy)
    rc = render.crop((rx0, ry0, rx1, ry1))
    oc = orig.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(QA + "/crop_4_%s_render.png" % name)
    oc.save(QA + "/crop_4_%s_orig.png" % name)
    print("cropped %-9s frame=(%d,%d,%d,%d) out=%dx%d scale=%.4f/%.4f"
          % (name, x0, y0, x1, y1, rc.size[0], rc.size[1],
             rc.size[0] / (x1 - x0), rc.size[1] / (y1 - y0)))
