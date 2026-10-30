import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide031"
K = 1125 / 540.0


def lum(a):
    return 0.299*a[:, :, 0] + 0.587*a[:, :, 1] + 0.114*a[:, :, 2]


def crop(a, fx0, fy0, fx1, fy1):
    return a[int(round(fy0*K)):int(round(fy1*K)), int(round(fx0*K)):int(round(fx1*K))]


def art(img, fx0, fy0, fx1, fy1, thresh=150, label=""):
    s = crop(img, fx0, fy0, fx1, fy1)
    L = lum(s)
    m = L < thresh
    print("--- %s (frame x%d..%d y%d..%d) ink=%d px ---" % (label, fx0, fx1, fy0, fy1, int(m.sum())))
    for row in m:
        print("  |" + "".join("#" if v else "." for v in row) + "|")


o = Image.open(DECK + "/unique_slides/slide_031.jpg").convert("RGB")
o_up = np.asarray(o.resize((2000, 1125), Image.LANCZOS)).astype(int)
r = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)

for tag, img in [("ORIG", o_up), ("RENDER", r)]:
    art(img, 660, 172, 710, 200, label=tag + " red-dot area (frame 657..665,179..186)")

for tag, img in [("ORIG", o_up), ("RENDER", r)]:
    art(img, 672, 240, 706, 266, label=tag + " green-vertex area (frame 678..700,248..256)")
