import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide031"
K = 1125 / 540.0


def load(p, up=False):
    im = Image.open(p).convert("RGB")
    if up:
        im = im.resize((2000, 1125), Image.LANCZOS)
    return np.asarray(im).astype(int)


o_up = load(DECK + "/unique_slides/slide_031.jpg", up=True)
r = load(QA + "/render_9.png")


def lum(a):
    return 0.299*a[:, :, 0] + 0.587*a[:, :, 1] + 0.114*a[:, :, 2]


def scan_row(img, fy, fx0, fx1, thresh=170):
    """return list of dark runs in that row, in FRAME px"""
    y = int(round(fy*K))
    x0, x1 = int(round(fx0*K)), int(round(fx1*K))
    L = lum(img)[y, x0:x1]
    on = L < thresh
    runs, st = [], None
    for i, v in enumerate(on):
        if v and st is None: st = i
        elif not v and st is not None: runs.append((st, i-1)); st = None
    if st is not None: runs.append((st, len(on)-1))
    return [(fx0+a/K, fx0+b/K) for a, b in runs]


def scan_col(img, fx, fy0, fy1, thresh=170):
    x = int(round(fx*K))
    y0, y1 = int(round(fy0*K)), int(round(fy1*K))
    L = lum(img)[y0:y1, x]
    on = L < thresh
    runs, st = [], None
    for i, v in enumerate(on):
        if v and st is None: st = i
        elif not v and st is not None: runs.append((st, i-1)); st = None
    if st is not None: runs.append((st, len(on)-1))
    return [(fy0+a/K, fy0+b/K) for a, b in runs]


print("===== ORIGINAL frame: horizontal border map (x230..820) =====")
for fy in [66, 67, 244, 245, 265, 266, 267, 288, 289, 290]:
    print("  row y=%d dark runs: %s" % (fy, scan_row(o_up, fy, 230, 820)))

print("\n===== RENDER frame: horizontal border map (x230..820) =====")
for fy in [66, 67, 244, 245, 265, 266, 267, 288, 289, 290]:
    print("  row y=%d dark runs: %s" % (fy, scan_row(r, fy, 230, 820)))

print("\n===== ORIGINAL: vertical border map (y230..300) =====")
for fx in [243, 244, 573, 574, 808, 809, 810, 811, 812]:
    print("  col x=%d dark runs: %s" % (fx, scan_col(o_up, fx, 230, 300)))

print("\n===== RENDER: vertical border map (y230..300) =====")
for fx in [243, 244, 573, 574, 808, 809, 810, 811, 812]:
    print("  col x=%d dark runs: %s" % (fx, scan_col(r, fx, 230, 300)))
