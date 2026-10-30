# Precise ink geometry of the two top "Let" boxes on ORIGINAL vs RENDER_4.
# 960x540 frame space (1px = 1pt). Render is 150dpi -> H_render/540 render px
# per frame px; row/col results are reported back in FRAME coordinates.
import numpy as np
from PIL import Image

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)
REND = Image.open("recreated_pptx/qa/slide004/render_4.png").convert("RGB")
SC = REND.size[1] / 540.0
print("render scale (render px per frame px): %.6f size=%s" % (SC, REND.size))
R = np.asarray(REND).astype(int)


def masks(a):
    return {
        "red":  (a[:, :, 0] > 150) & (a[:, :, 1] < 120) & (a[:, :, 2] < 120),
        "blue": (a[:, :, 2] > 130) & (a[:, :, 0] < 130) & (a[:, :, 1] < 170),
        "dark": a.sum(axis=2) < 330,
    }


def runs(idx, cnt, minc=1):
    out, s, p = [], None, None
    for a, c in zip(idx, cnt):
        if c >= minc:
            if s is None:
                s = a
            p = a
        else:
            if s is not None:
                out.append((int(s), int(p)))
                s = None
    if s is not None:
        out.append((int(s), int(p)))
    return out


def rep(name, img, box, sc=1.0, minr=3, minc=3):
    x0, y0, x1, y1 = [int(round(v * sc)) for v in box]
    reg = img[y0:y1, x0:x1]
    print("\n--- %s frame-box %s ---" % (name, box))
    for k, mk in masks(reg).items():
        rr = runs(np.arange(y0, y1), mk.sum(axis=1), minr * sc)
        cc = runs(np.arange(x0, x1), mk.sum(axis=0), minc * sc)
        f = lambda v: round(v / sc, 1)
        print("  %-5s rows: %s" % (k, [(f(a), f(b)) for a, b in rr]))
        print("  %-5s cols: %s" % (k, [(f(a), f(b)) for a, b in cc]))


rep("ORIG Box1 (Y) interior", ORIG, (84, 103, 390, 220))
rep("ORIG Box2 (Yhat) interior", ORIG, (431, 103, 742, 220))
rep("REND Box1 interior", R, (84, 103, 390, 220), sc=SC)
rep("REND Box2 interior", R, (431, 103, 742, 220), sc=SC)

# Row-by-row text bands (any ink) inside each original box, min run 6 px.
def bands(name, img, box, sc=1.0, minc=4):
    x0, y0, x1, y1 = [int(round(v * sc)) for v in box]
    reg = img[y0:y1, x0:x1].sum(axis=2) < 700  # any non-white ink
    print("\n=== %s: per-row ink runs (frame px, min run 6) ===" % name)
    for yy in range(reg.shape[0]):
        cc = runs(np.arange(x0, x1), reg[yy].astype(int), minc * sc)
        cc = [(round(a / sc), round(b / sc)) for a, b in cc]
        if cc:
            print("  y%5.1f %s" % (yy / sc, cc))


bands("ORIG Box1", ORIG, (84, 103, 390, 220))
bands("ORIG Box2", ORIG, (431, 103, 742, 220))
