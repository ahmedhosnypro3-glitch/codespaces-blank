import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide031"
K = 1125 / 540.0

o = np.asarray(Image.open(DECK + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
o_up = np.asarray(Image.open(DECK + "/unique_slides/slide_031.jpg").convert("RGB")
                  .resize((2000, 1125), Image.LANCZOS)).astype(int)
r = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)


def lum(a):
    return 0.299*a[:, :, 0] + 0.587*a[:, :, 1] + 0.114*a[:, :, 2]


def crop(a, fx0, fy0, fx1, fy1):
    return a[int(round(fy0*K)):int(round(fy1*K)), int(round(fx0*K)):int(round(fx1*K))]


def dark_runs(m, gap=8):
    on = m.sum(axis=0) > 0
    out, st = [], None
    for i, v in enumerate(on):
        if v and st is None: st = i
        elif not v and st is not None: out.append((st, i-1)); st = None
    if st is not None: out.append((st, len(on)-1))
    m2 = []
    for a, b in out:
        if m2 and a - m2[-1][1] <= gap: m2[-1] = (m2[-1][0], b)
        else: m2.append((a, b))
    return m2


def report(tag, win, thresh=120):
    """win = (fx0,fy0,fx1,fy1) frame px"""
    fx0, fy0, fx1, fy1 = win
    lo = lum(crop(o_up, fx0, fy0, fx1, fy1))
    lr = lum(crop(r, fx0, fy0, fx1, fy1))
    mo = lo < thresh
    mr = lr < thresh
    go = dark_runs(mo)
    gr = dark_runs(mr)
    def stats(m, g):
        if not len(np.nonzero(m)[0]):
            return "EMPTY"
        ys, xs = np.nonzero(m)
        return "x %.1f..%.1f y %.1f..%.1f (%d px, %d runs)" % (
            fx0 + xs.min()/K, fx0 + xs.max()/K, fy0 + ys.min()/K, fy0 + ys.max()/K,
            len(xs), len(g))
    print("%-22s ORIG    %s" % (tag, stats(mo, go)))
    print("%-22s RENDER  %s" % ("", stats(mr, gr)))
    return (mo, mr), (go, gr), (fx0, fy0)


def colour_stats(tag, win, rgb, tol):
    fx0, fy0, fx1, fy1 = win
    def msk(img):
        s = crop(img, fx0, fy0, fx1, fy1)
        return (np.abs(s[:, :, 0]-rgb[0]) <= tol) & (np.abs(s[:, :, 1]-rgb[1]) <= tol) & \
               (np.abs(s[:, :, 2]-rgb[2]) <= tol)
    for nm, img in [("orig", o_up), ("render", r)]:
        m = msk(img)
        ys, xs = np.nonzero(m)
        if len(xs):
            print("  %-6s %-7s %-7s x %.1f..%.1f y %.1f..%.1f  (%d px)" %
                  (tag, nm, "(%d,%d,%d)/%d" % (rgb[0], rgb[1], rgb[2], tol),
                   fx0+xs.min()/K, fx0+xs.max()/K, fy0+ys.min()/K, fy0+ys.max()/K, len(xs)))
        else:
            print("  %-6s %-7s NONE" % (tag, nm))


print("### ANNOTATION LINE 1 (frame x245..810, y244..264)")
report("ann line1", (245, 244, 810, 264))
print("\n### ANNOTATION LINE 2 (frame x245..810, y265..288)")
report("ann line2", (245, 265, 810, 288))
print("\n### '(5,1)' LABEL region (frame x480..565, y240..268)")
report("(5,1) label", (480, 240, 565, 268), thresh=120)
print("\n### BOUNCING label (frame x370..520, y305..335)")
report("Bouncing", (370, 305, 520, 335))

print("\n### GRAPH COLOURS (window frame x575..808, y68..266)")
colour_stats("parabola", (575, 68, 808, 266), (0, 0, 255), 60)
colour_stats("green pt", (575, 68, 808, 266), (0, 128, 0), 60)
colour_stats("red pt", (575, 68, 808, 266), (255, 0, 0), 90)
colour_stats("black", (575, 68, 808, 266), (0, 0, 0), 60)

print("\n### PARAM TABLE (frame x78..166, y173..220)")
report("param table", (78, 173, 166, 220))

print("\n### MAIN TABLE first data cell col (frame x143..195, y350..375) - row0")
report("mtable r0", (143, 350, 195, 375))

print("\n### CONTAINMENT: ink outside panel strokes / crossing borders")
# panel strokes: left x58.5, right x901, bottom y538.5
for nm, img in [("orig", o_up), ("render", r)]:
    L = lum(img)
    # strict dark ink (not the red strokes) inside panel x60..897, y44..536
    inside = L[44*int(K):536*int(K), 60*int(K):897*int(K)]
    print("  %-7s dark px (<120) inside panel: %d" % (nm, int((inside < 120).sum())))
# title band ink left of x80 (should be none except panel stroke)
print("\n### TITLE left overflow check (frame x60..78, y60..90)")
for nm, img in [("orig", o_up), ("render", r)]:
    s = crop(img, 60, 60, 78, 90)
    Lm = lum(s) < 150
    print("  %-7s ink px in x60..78: %d" % (nm, int(Lm.sum())))
