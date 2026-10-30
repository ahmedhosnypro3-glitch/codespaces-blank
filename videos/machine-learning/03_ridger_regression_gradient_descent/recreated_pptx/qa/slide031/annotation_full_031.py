# Full width raster of the annotation box interior in ORIGINAL vs CURRENT render.
# Row-wise ink-column profiles at 1px, so both text bands, their gap, and the
# box interior can be read off exactly and compared.
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide031"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(QA + "/render_cur.png").convert("RGB")).astype(int)
SX = 2001 / 960.0

BOX = (243, 250, 807, 287)  # frame x0,y0,x1,y1 of the box ink (to be verified)


def find_box(a, sc):
    # green saturated px -> box border
    g = (a[:, :, 1] > a[:, :, 0] + 20) & (a[:, :, 1] > a[:, :, 2] + 20)
    sub = g[int(243 * sc):int(288 * sc), int(245 * sc):int(810 * sc)]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None
    return (int(245 + xs.min() / sc), int(243 + ys.min() / sc),
            int(245 + xs.max() / sc), int(243 + ys.max() / sc))


print("=== box bbox (green px, frame coords) ===")
print("   ORIG ", find_box(O, 1.0))
print("   REND ", find_box(R, SX))


def rowprof(tag, a, x0, x1, y0, y1, sc, ink):
    print("\n--- %s : ink cols per row (x %d..%d, y %d..%d) ---" % (tag, x0, x1, y0, y1))
    out = []
    for fy in range(y0, y1):
        cols = [fx for fx in range(x0, x1) if ink(a[int(round(fy * sc)), int(round(fx * sc))])]
        if cols:
            runs = []
            s = cols[0]; p = cols[0]
            for c in cols[1:]:
                if c <= p + 2:
                    p = c
                else:
                    runs.append((s, p)); s = c; p = c
            runs.append((s, p))
            out.append((fy, runs))
            print("   y%3d n=%3d runs: %s" % (fy, len(cols), " ".join("%d-%d" % r for r in runs)))
    return out


def o_ink(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    return max(p) < 200


def r_ink(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    return max(p) < 205


rowprof("ORIGINAL", O, 250, 807, 244, 292, 1.0, o_ink)
rowprof("RENDER", R, 250, 807, 244, 292, SX, r_ink)
