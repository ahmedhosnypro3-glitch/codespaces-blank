import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"


def groups(arr, scale, x0, y0, x1, y1, thresh=120, gap=3):
    sub = arr[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    lum = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    m = lum < thresh
    colsum = m.sum(axis=0)
    on = colsum > 0
    out, st = [], None
    for i, v in enumerate(on):
        if v and st is None:
            st = i
        elif not v and st is not None:
            out.append((st, i - 1)); st = None
    if st is not None:
        out.append((st, len(on) - 1))
    # merge groups closer than `gap`
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged, m, sub


def art(m, a, b, label):
    sub = m[:, a:b + 1]
    print("  %-8s x %d..%d (w=%d)" % (label, a, b, b - a + 1))
    for row in sub:
        print("    |" + "".join("#" if v else "." for v in row) + "|")


o = np.asarray(Image.open(DECK + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(DECK + "/recreated_pptx/qa/slide031/render_9.png").convert("RGB")).astype(int)
SC = 1125 / 540.0

for name, arr, sc, bx in [
    ("ORIGINAL eq", o, 1.0, (400, 528)),
    ("RENDER  eq", r, SC, (404, 528)),
]:
    print("================", name, "================")
    g, m, sub = groups(arr, sc, bx[0], 186, bx[1], 210)
    print("groups:", len(g))
    for i, (a, b) in enumerate(g):
        art(m, a, b, "g%d" % i)
