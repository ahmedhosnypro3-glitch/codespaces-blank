#!/usr/bin/env python3
"""Full-res red-stroke census in the ORIGINAL slide_025.jpg TR panel (x616..880 y115..318),
and in a render (argv[1], default render_k15.png at 2001x1125) scaled to slide px.
Reports every red comp with bbox, area, slope class (horizontal if dy<=2, vertical if dx<=2,
else diagonal with slope), so TR strokes can be matched one-to-one."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027"
RENDER = sys.argv[1] if len(sys.argv) > 1 else RJ + "/slide025/render_k15.png"

TR = (616, 115, 880, 318)

def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

def census(a, box, border=6, min_area=6):
    x0, y0, x1, y1 = box
    p = a[y0:y1, x0:x1]
    rm = redmask(p)
    rm[:border] = False; rm[-border:] = False; rm[:, :border] = False; rm[:, -border:] = False
    lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_area:
            continue
        w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        if h <= 2 and w >= 8:
            kind = "horiz"
        elif w <= 2 and h >= 8:
            kind = "vert"
        else:
            kind = "diag slope=%.2f" % ((ys.max() - ys.min()) / max(w - 1, 1))
        out.append((len(xs), x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), w, h, kind))
    return sorted(out, key=lambda t: (t[2], t[1]))

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
print("== ORIG TR red comps ==")
for c in census(orig, TR):
    print("  area=%d x%d..%d y%d..%d (w%d h%d) %s" % c)

ren_img = Image.open(RENDER).convert("RGB")
SX, SY = ren_img.size[0] / 960.0, ren_img.size[1] / 540.0
ren = np.array(ren_img.crop((0, 0, int(960 * SX), int(540 * SY))).resize((960, 540), Image.BILINEAR)).astype(np.int32)
print("== RENDER %s TR red comps (downscaled; thin 1pt lines may vanish) ==" % RENDER)
for c in census(ren, TR):
    print("  area=%d x%d..%d y%d..%d (w%d h%d) %s" % c)

# also full-res render census (scale comp coords back to slide px)
print("== RENDER full-res TR red comps mapped to slide px ==")
x0, y0, x1, y1 = TR
p = np.array(ren_img.crop((int(x0 * SX), int(y0 * SY), int(np.ceil(x1 * SX)), int(np.ceil(y1 * SY))))).astype(np.int32)
rm = redmask(p)
b = int(6 * SX)
rm[:b] = False; rm[-b:] = False; rm[:, :b] = False; rm[:, -b:] = False
lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
out = []
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 6:
        continue
    w, h = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    if h <= 2 * SY and w >= 8 * SX:
        kind = "horiz"
    elif w <= 2 * SX and h >= 8 * SY:
        kind = "vert"
    else:
        kind = "diag slope=%.2f" % ((ys.max() - ys.min()) / max(w - 1, 1) / (SY / SX))
    out.append((len(xs), x0 + xs.min() / SX, y0 + ys.min() / SY, x0 + xs.max() / SX, y0 + ys.max() / SY, w / SX, h / SY, kind))
for c in sorted(out, key=lambda t: (t[2], t[1])):
    print("  area=%d x%.0f..%.0f y%.0f..%.0f (w%.0f h%.0f) %s" % c)
print("DONE")
