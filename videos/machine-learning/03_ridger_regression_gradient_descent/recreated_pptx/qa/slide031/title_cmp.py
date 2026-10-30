import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide031"
ORIG = DECK + "/unique_slides/slide_031.jpg"
K = 1125 / 540.0

o_img = Image.open(ORIG).convert("RGB")
o = np.asarray(o_img.resize((2000, 1125), Image.LANCZOS)).astype(int)   # matched scale
r9 = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)


def lum(a):
    return 0.299*a[:, :, 0] + 0.587*a[:, :, 1] + 0.114*a[:, :, 2]


def title_ink(a, thresh=150):
    """mask of saturated title ink (red/green/blue) in band y58..95, x40..620"""
    y0, y1, x0, x1 = int(58*K), int(95*K), int(40*K), int(620*K)
    L = lum(a)[y0:y1, x0:x1]
    s = a[y0:y1, x0:x1]
    ink = (L < thresh) & (
        ((s[:, :, 0]-s[:, :, 1] > 40) & (s[:, :, 0]-s[:, :, 2] > 40)) |
        ((s[:, :, 1]-s[:, :, 0] > 25) & (s[:, :, 1]-s[:, :, 2] > 25)) |
        ((s[:, :, 2]-s[:, :, 0] > 25) & (s[:, :, 2]-s[:, :, 1] > 25)))
    return ink, x0


for tag, a in [("ORIGINAL", o), ("RENDER_9", r9)]:
    ink, x0 = title_ink(a)
    on = ink.sum(axis=0) > 0
    runs, st = [], None
    for i, v in enumerate(on):
        if v and st is None: st = i
        elif not v and st is not None: runs.append((st, i-1)); st = None
    if st is not None: runs.append((st, len(on)-1))
    print("=== %s title: ink x %.1f..%.1f frame px, %d glyph runs" %
          (tag, x0/K + runs[0][0]/K, x0/K + runs[-1][1]/K, len(runs)))
    print("   runs:", ["%.1f-%.1f" % (x0/K+a/K, x0/K+b/K) for a, b in runs])
    rs = np.nonzero(ink.sum(axis=1))[0]
    print("   ink rows y %.1f..%.1f (render-px rows %d..%d)" % (58+rs[0]/K, 58+rs[-1]/K, rs[0], rs[-1]))
    # per-run centre of mass to align
    print()

# pixel-correlate the two title bands after aligning ink bboxes
def norm_band(a):
    y0, y1, x0, x1 = int(58*K), int(95*K), int(40*K), int(620*K)
    ink, _ = title_ink(a)
    ys, xs = np.nonzero(ink)
    return ink[ys.min():ys.max()+1, xs.min():xs.max()+1], (x0+xs.min())/K, 58+ys.min()/K


oi, ox, oy = norm_band(o)
ri, rx, ry = norm_band(r9)
print("orig ink box w x h: %d x %d  (frame %.1f x %.1f)" % (oi.shape[1], oi.shape[0], oi.shape[1]/K, oi.shape[0]/K))
print("rend ink box w x h: %d x %d  (frame %.1f x %.1f)" % (ri.shape[1], ri.shape[0], ri.shape[1]/K, ri.shape[0]/K))
H = max(oi.shape[0], ri.shape[0]); W = max(oi.shape[1], ri.shape[1])
A = np.zeros((H, W), bool); B = np.zeros((H, W), bool)
A[:oi.shape[0], :oi.shape[1]] = oi
B[:ri.shape[0], :ri.shape[1]] = ri
print("overlap IoU (bbox aligned, no shift):", (A & B).sum() / (A | B).sum())
best = 0
for dx in range(-30, 31):
    for dy in range(-12, 13):
        C = np.zeros((H+80, W+80), bool)
        C[40:40+B.shape[0], 40:40+B.shape[1]] = B
        D = np.zeros((H+80, W+80), bool)
        D[40+dy:40+dy+A.shape[0], 40+dx:40+dx+A.shape[1]] = A
        u = (C & D).sum() / (C | D).sum()
        if u > best:
            best = u; bestd = (dx, dy)
print("best IoU after shift: %.3f at dx=%d dy=%d (render px)" % (best, bestd[0], bestd[1]))
