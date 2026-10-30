#!/usr/bin/env python3
"""Self-checks for slide 050 render_1.png (150dpi, 2001x1125).
Frame px = render px / (2001/960) = render px / 2.0833.
Checks: equation regions contain ink; content elements stay inside their frames;
measured marker positions carry the right colours; chrome already PASSed.
"""
from PIL import Image
import numpy as np

REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide050/render_1.png"
im = Image.open(REND).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
SC = W / 960.0
print("render size", W, H, "scale(render px per frame px) =", round(SC, 4))


def box(fx0, fy0, fx1, fy1):
    return a[int(fy0 * SC):int(fy1 * SC), int(fx0 * SC):int(fx1 * SC)]


def ink_count(b, thr=235):
    lum = b.mean(axis=2)
    return int((lum < thr).sum())


def frac(b, thr=235):
    return ink_count(b, thr) / float(b.shape[0] * b.shape[1])


fails = []
checks = []


def chk(name, cond, detail=""):
    checks.append((name, bool(cond), detail))
    if not cond:
        fails.append(name)


# ---- equation PNGs must land (ink present in every equation region) ----
EQ_REGIONS = {
    "eq_initialW": (266, 63, 266 + 107, 63 + 23),      # 1.483in = 106.8px wide, 0.317in=22.8px
    "eq_eta": (270, 73, 270 + 32, 73 + 14),
    "eq_Z1": (322, 99, 322 + 20, 99 + 22),
    "eq_Z2": (432, 99, 432 + 20, 99 + 22),
    "eq_Z3": (542, 99, 542 + 20, 99 + 22),
    "eq_finalW_pink": (748, 95, 748 + 67, 95 + 26),
}
for k, (x0, y0, x1, y1) in EQ_REGIONS.items():
    f = frac(box(x0, y0, x1, y1))
    chk("ink " + k, f > 0.02, "ink frac=%.3f" % f)

# ---- frame containment: no ink outside the navy box for the top band ----
# navy box is x68..719 y54..130; the caption box x66..240 y134..248; chart x312..824 y173..481
for name, (x0, y0, x1, y1), pad in [
    ("navy_box", (68, 54, 719, 130), 6),
    ("caption_box", (66, 134, 240, 248), 6),
    ("chart", (312, 173, 824, 481), 4),
    ("pink_box", (743, 58, 830, 171), 5),
    ("red_box", (84, 278, 213, 305), 5),
]:
    b = box(x0 - pad, y0 - pad, x1 + pad, y1 + pad)
    # the outer margin ring (pad wide) must be free of content ink except the box's own border
    top = b[: int(pad * SC), :]
    bot = b[-int(pad * SC):, :]
    lef = b[:, : int(pad * SC)]
    rig = b[:, -int(pad * SC):]
    for side, sl in (("top", top), ("bottom", bot), ("left", lef), ("right", rig)):
        f = frac(sl, thr=200)
        chk("contain %s %s margin" % (name, side), f < 0.06, "ink frac=%.3f" % f)

# ---- chart markers present with right colours ----
def marker_ok(data_x, data_y, want, kind, tol=6):
    px = 362.7 + 52.725 * data_x
    py = 428.7 - 30.671 * data_y
    b = box(px - tol, py - tol, px + tol, py + tol)
    flat = b.reshape(-1, 3)
    w = np.array([int(want[i:i + 2], 16) for i in (0, 2, 4)])
    d = np.abs(flat - w).sum(axis=1)
    best = d.min()
    n = int((d < 60).sum())
    chk("marker %s(%d,%d)" % (kind, data_x, data_y), n > 10, "match px=%d mindist=%d" % (n, best))


for (x, y) in [(1, 1), (2, 1), (2, 2)]:
    marker_ok(x, y, "1C3D5E", "blue-square")
for (x, y) in [(5, 4), (6, 5), (6, 6)]:
    marker_ok(x, y, "FF94FF", "magenta-diamond")
marker_ok(7, 6, "D2000F", "red-triangle")
marker_ok(0, 0, "D2000F", "red-blob")

# decision line: red pixels along the fitted line
def line_px(frac_t):
    x0d, y0d = -0.51, 5.42
    x1d, y1d = 6.19, -1.31
    return (362.7 + 52.725 * (x0d + frac_t * (x1d - x0d)),
            428.7 - 30.671 * (y0d + frac_t * (y1d - y0d)))


for t in (0.15, 0.5, 0.85):
    px, py = line_px(t)
    b = box(px - 5, py - 5, px + 5, py + 5)
    flat = b.reshape(-1, 3)
    red = (flat[:, 0] > 110) & (flat[:, 0] - flat[:, 1] > 30) & (flat[:, 0] - flat[:, 2] > 30)
    chk("decision line t=%.2f" % t, int(red.sum()) > 15, "red px=%d" % int(red.sum()))

# ---- gridlines at measured y values (7,6,5,3,2,1,0) and NOT at 4 ----
for gy in (7, 6, 5, 3, 2, 1, 0):
    py = 428.7 - 30.671 * gy
    b = box(500, py - 1.5, 700, py + 1.5)
    flat = b.reshape(-1, 3)
    grey = (np.abs(flat[:, 0] - flat[:, 1]) < 12) & (np.abs(flat[:, 1] - flat[:, 2]) < 12) & \
           (flat[:, 0] > 180) & (flat[:, 0] < 245)
    chk("gridline y=%d" % gy, int(grey.sum()) > 60, "grey px=%d" % int(grey.sum()))

# ---- print ----
print()
for name, ok, detail in checks:
    print("%-4s %-34s %s" % ("PASS" if ok else "FAIL", name, detail))
print()
print("TOTAL %d checks, %d failed" % (len(checks), len(fails)))
if fails:
    print("FAILED:", ", ".join(fails))
