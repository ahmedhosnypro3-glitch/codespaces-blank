"""Slide 031 fix-driver measurements: tick labels, plot box, annotation box vs original."""
import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide031"
K = 1125 / 540.0

o_img = Image.open(DECK + "/unique_slides/slide_031.jpg").convert("RGB")
o = np.asarray(o_img.resize((2000, 1125), Image.LANCZOS)).astype(int)
r = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


def dark(a, fx0, fy0, fx1, fy1, t=150):
    """dark-ink mask over a frame-px window; returns mask in RENDER res coords"""
    x0, x1, y0, y1 = int(fx0 * K), int(fx1 * K), int(fy0 * K), int(fy1 * K)
    L = lum(a)[y0:y1, x0:x1]
    return L < t, (x0, y0)


def runs(m, gap=6):
    on = m.sum(axis=0) > 0
    out, st = [], None
    for i, v in enumerate(on):
        if v and st is None:
            st = i
        elif not v and st is not None:
            out.append((st, i - 1)); st = None
    if st is not None:
        out.append((st, len(on) - 1))
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged


def fr(m, ox, oy):
    """mask runs -> frame px x extents"""
    return [(ox + a / K, ox + b / K) for a, b in runs(m)]


def yrows(m, oy):
    rs = np.nonzero(m.sum(axis=1))[0]
    if not len(rs):
        return None
    return (oy + rs.min() / K, oy + rs.max() / K)


print("############ Y TICK LABELS: window x515..570 (left of plot border 573) ############")
for nm, img in [("ORIG", o), ("REND", r)]:
    m, (ox, oy) = dark(img, 515, 75, 570, 275)
    print("  %-5s x-runs: %s" % (nm, ["%.1f-%.1f" % t for t in fr(m, ox, oy)]))
    print("        y-rows: %s" % (yrows(m, oy),))
    # separate bands per grid line
    for gy in [87, 146, 206, 265]:
        mm, (ox2, oy2) = dark(img, 515, gy - 13, 570, gy + 7)
        rr = fr(mm, ox2, oy2)
        rr = [t for t in rr if not (t[0] < 566 and t[1] < 575 and abs(t[0] - 565) < 3)]
        print("        grid y=%d: %s" % (gy, ["%.1f-%.1f" % t for t in rr]))

print("\n############ Y TICK LABELS INSIDE plot: window x576..640 ############")
for nm, img in [("ORIG", o), ("REND", r)]:
    for gy in [87, 146, 206, 265]:
        mm, (ox2, oy2) = dark(img, 576, gy - 13, 640, gy + 7)
        rr = [t for t in fr(mm, ox2, oy2) if t[1] - t[0] > 2]
        print("  %-5s grid y=%d: %s" % (nm, gy, ["%.1f-%.1f" % t for t in rr]))

print("\n############ X TICK LABELS: window y268..296 ############")
for nm, img in [("ORIG", o), ("REND", r)]:
    m, (ox, oy) = dark(img, 574, 268, 808, 296)
    print("  %-5s x-runs: %s" % (nm, ["%.1f-%.1f" % t for t in fr(m, ox, oy)]))
    print("        y-rows: %s" % (yrows(m, oy),))

print("\n############ PLOT BOX vertical red borders (colour runs) ############")


def redruns(a, axis, fixed, lo, hi, tol=60):
    out, st = [], None
    for i in range(int(lo * K), int(hi * K)):
        c = a[i, fixed] if axis == "row" else a[fixed, i]
        v = (int(c[0]) - int(c[1]) > tol) and (int(c[0]) - int(c[2]) > tol) and c[0] > 80
        if v and st is None:
            st = i
        elif not v and st is not None:
            out.append((st, i - 1)); st = None
    if st is not None:
        out.append((st, int(hi * K) - 1))
    v = ((out[0][0] + 0) / K, (out[-1][1] + 0) / K)
    return ["%.1f-%.1f" % (a0 / K, b0 / K) for a0, b0 in out if b0 / K - a0 / K > 2]


for nm, a in [("ORIG", o), ("REND", r)]:
    print("  %-5s col x=573: %s" % (nm, redruns(a, "col", int(573 * K), 60, 320)))
    print("        col x=809: %s" % redruns(a, "col", int(809 * K), 60, 320))
    print("        row y=66 : %s" % redruns(a, "row", int(66 * K), 560, 820))
    print("        row y=310: %s" % redruns(a, "row", int(310 * K), 560, 820))
    print("        row y=267: %s" % redruns(a, "row", int(267 * K), 560, 820))

print("\n############ ANNOTATION BOX edges ############")
GREENR = lambda c: (int(c[1]) - int(c[0]) > 25) and (int(c[1]) - int(c[2]) > 25)


def grnruns(a, axis, fixed, lo, hi):
    out, st = [], None
    for i in range(int(lo * K), int(hi * K)):
        c = a[i, fixed] if axis == "row" else a[fixed, i]
        v = GREENR(c)
        if v and st is None:
            st = i
        elif not v and st is not None:
            out.append((st, i - 1)); st = None
    if st is not None:
        out.append((st, int(hi * K) - 1))
    return ["%.1f-%.1f" % (a0 / K, b0 / K) for a0, b0 in out if b0 / K - a0 / K > 2]


for nm, a in [("ORIG", o), ("REND", r)]:
    print("  %-5s ann col x=244: %s" % (nm, grnruns(a, "col", int(244 * K), 240, 295)))
    print("        ann row y=244: %s" % grnruns(a, "row", int(244 * K), 240, 580))
    print("        ann row y=289: %s" % grnruns(a, "row", int(289 * K), 240, 580))
    print("        ann row y=290: %s" % grnruns(a, "row", int(290 * K), 240, 580))

print("\n############ GREEN MARKER at vertex ############")
for nm, a in [("ORIG", o), ("REND", r)]:
    m = (np.abs(a[:, :, 0].astype(int) - 0) <= 70) & (np.abs(a[:, :, 1].astype(int) - 128) <= 70) & \
        (np.abs(a[:, :, 2].astype(int) - 0) <= 70)
    m = m[int(240 * K):int(265 * K), int(640 * K):int(745 * K)]
    ys, xs = np.nonzero(m)
    if len(xs):
        print("  %-5s x %.1f..%.1f y %.1f..%.1f (%d px)" %
              (nm, 640 + xs.min() / K, 640 + xs.max() / K, 240 + ys.min() / K, 240 + ys.max() / K, m.sum()))
    else:
        print("  %-5s NONE" % nm)

print("\n############ WHITE FILL coverage of plot interior (row y=255, x574..808) ############")
for nm, a in [("ORIG", o), ("REND", r)]:
    row = a[int(255 * K), int(574 * K):int(808 * K)]
    # count non-white
    nonwhite = int((np.abs(row - 255).max(axis=1) > 6).sum())
    print("  %-5s non-white px at y=255 in plot interior: %d" % (nm, nonwhite))

print("\n############ PARABOLA blue extent ############")
for nm, a in [("ORIG", o), ("REND", r)]:
    m = (a[:, :, 2].astype(int) - a[:, :, 0].astype(int) > 25) & (lum(a) < 200)
    m = m[int(66 * K):int(311 * K), int(575 * K):int(808 * K)]
    ys, xs = np.nonzero(m)
    if len(xs):
        print("  %-5s x %.1f..%.1f y %.1f..%.1f (%d px)" %
              (nm, 575 + xs.min() / K, 575 + xs.max() / K, 66 + ys.min() / K, 66 + ys.max() / K, m.sum()))
    else:
        print("  %-5s NONE" % nm)

print("\n############ BLACK CHORD (y=10 line) ############")
for nm, a in [("ORIG", o), ("REND", r)]:
    m = lum(a) < 130
    m = m[int(140 * K):int(155 * K), int(575 * K):int(808 * K)]
    ys, xs = np.nonzero(m)
    if len(xs):
        print("  %-5s x %.1f..%.1f y %.1f..%.1f (%d px)" %
              (nm, 575 + xs.min() / K, 575 + xs.max() / K, 140 + ys.min() / K, 140 + ys.max() / K, m.sum()))

print("\n############ RED DOT ############")
for nm, a in [("ORIG", o), ("REND", r)]:
    m = (a[:, :, 0].astype(int) > 150) & (a[:, :, 0].astype(int) - a[:, :, 1] > 60) & \
        (a[:, :, 0].astype(int) - a[:, :, 2] > 60)
    m = m[int(174 * K):int(192 * K), int(648 * K):int(672 * K)]
    ys, xs = np.nonzero(m)
    if len(xs):
        print("  %-5s x %.1f..%.1f y %.1f..%.1f (%d px)" %
              (nm, 648 + xs.min() / K, 648 + xs.max() / K, 174 + ys.min() / K, 174 + ys.max() / K, m.sum()))
    else:
        print("  %-5s NONE" % nm)
