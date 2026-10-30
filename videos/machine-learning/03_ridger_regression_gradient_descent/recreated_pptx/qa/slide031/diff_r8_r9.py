import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide031"
K = 1125 / 540.0


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)


r8 = load(QA + "/render_8.png")
r9 = load(QA + "/render_9.png")
print("r8", r8.shape, "r9", r9.shape)
d = np.abs(r8 - r9).max(axis=2)
print("changed px:", int((d > 12).sum()), "of", d.shape[0] * d.shape[1])
ys, xs = np.nonzero(d > 12)
if len(ys):
    print("bbox render px: x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    print("bbox FRAME px: x %.1f..%.1f y %.1f..%.1f" % (xs.min()/K, xs.max()/K, ys.min()/K, ys.max()/K))
    # cluster into bands by y
    rows = np.zeros(1125, int)
    for y in ys:
        rows[y] += 1
    bands, st = [], None
    for i, v in enumerate(rows):
        if v > 0 and st is None:
            st = i
        elif v == 0 and st is not None:
            bands.append((st, i - 1)); st = None
    if st is not None:
        bands.append((st, 1124))
    print("changed row bands (frame px):")
    for a, b in bands:
        if b - a < 2:
            continue
        sel = (ys >= a) & (ys <= b)
        print("  y %.1f..%.1f  x %.1f..%.1f  (%d px)" %
              (a/K, b/K, xs[sel].min()/K, xs[sel].max()/K, int(sel.sum())))
