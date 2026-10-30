#!/usr/bin/env python3
"""Slide 030 PIL adjudication baseline (worker w030-finish-20261024).

Render: recreated_pptx/qa/slide030/render_6.png 2001x1125 @150dpi.
Scale render->frame px: *960/2001 = 0.4798 (SX), *540/1125 = 0.48 (SY).
All canonical values are frame px (960x540, 1px = 1pt) measured from
unique_slides/slide_030.jpg. Noisy rows/cols (<3 ink px) are rejected before
measuring.
"""
import numpy as np
from PIL import Image

V = "videos/machine-learning/03_ridger_regression_gradient_descent"
REND = f"{V}/recreated_pptx/qa/slide030/render_6.png"
ORIG = f"{V}/unique_slides/slide_030.jpg"

rend = np.asarray(Image.open(REND).convert("RGB")).astype(int)
orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
H, W = rend.shape[:2]
SX = W / 960.0
SY = H / 540.0
print(f"== slide 030 measurement (w030-finish) ==")
print(f"render {W}x{H}  SX={SX:.4f} SY={SY:.4f}   orig {orig.shape[1]}x{orig.shape[0]}")


def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return {
        "dark": (r < 120) & (g < 120) & (b < 120),
        "red": (r - g > 60) & (r - b > 40) & (r > 110),
        "green": (g - r > 40) & (g - b > 40) & (g > 100),
        "blue": (b - r > 30) & (b - g > 15) & (b > 120),
        "purple": (r - g > 25) & (b - g > 25) & (b > 120),
        "navy": (b > 90) & (b - r > 50) & (b - g > 50) & (r < 130),
    }


mr, mo = masks(rend), masks(orig)


def clean(mask, min_ink=3):
    """Reject noisy rows/cols with <min_ink px."""
    m = mask.copy()
    colsum = m.sum(axis=0)
    rowsum = m.sum(axis=1)
    m[:, colsum < min_ink] = False
    m[rowsum < min_ink, :] = False
    return m


def win(x0, y0, x1, y1, shape):
    h, w = shape[:2]
    return (int(x0 * SX), int(y0 * SY), min(int(x1 * SX), w), min(int(y1 * SY), h))


def bbox(mask, box):
    X0, Y0, X1, Y1 = win(*box, rend.shape)
    sub = clean(mask[Y0:Y1, X0:X1])
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return (round((xs.min() + X0) / SX, 1), round((ys.min() + Y0) / SY, 1),
            round((xs.max() + X0) / SX, 1), round((ys.max() + Y0) / SY, 1))


# ------------------------------------------------- 1. INK CENSUS (frame px)
print("\n== 1. ink census (ink px, frame-px equivalent) ==")
for name in ("dark", "red", "green", "blue", "purple", "navy"):
    rc = int(mr[name].sum() / (SX * SY))
    oc = int(clean(mo[name]).sum())
    print(f"  {name:6s} render={rc:6d}  orig={oc:6d}  ratio={rc/max(oc,1):.2f}")

# ------------------------------------------------- 2. REGION ALIGNMENT
print("\n== 2. region bboxes (frame px) render vs orig ==")
regions = {
    "title":        ((55, 55, 600, 100), ("dark", "red", "green")),
    "param_table":  ((90, 185, 260, 300), ("dark", "navy")),
    "upper_eq_box": ((390, 175, 545, 220), ("red", "dark")),
    "green_box":    ((340, 225, 565, 292), ("green", "red", "blue", "dark")),
    "callout":      ((325, 282, 580, 335), ("purple",)),
    "plot_frame":   ((560, 55, 825, 322), ("red",)),
    "arrow":        ((150, 285, 215, 355), ("red",)),
    "iter_table":   ((70, 315, 665, 540), ("navy", "dark")),
}
for name, (box, ms) in regions.items():
    rm = np.zeros(rend.shape[:2], bool)
    om = np.zeros(orig.shape[:2], bool)
    for m in ms:
        rm |= mr[m]
        om |= clean(mo[m])
    rb, ob = bbox(rm, box), bbox(om, box)
    if rb and ob:
        dx, dy = rb[0] - ob[0], rb[1] - ob[1]
        dw, dh = (rb[2] - rb[0]) - (ob[2] - ob[0]), (rb[3] - rb[1]) - (ob[3] - ob[1])
        print(f"  {name:14s} render={rb}  orig={ob}  delta=({dx:+.1f},{dy:+.1f}) dsize=({dw:+.1f},{dh:+.1f})")
    else:
        print(f"  {name:14s} render={rb}  orig={ob}  (missing on one side)")

# ------------------------------------------------- 3. PARABOLA RIPPLE
print("\n== 3. parabola: one smooth arc + vertex/arms ==")
# render: parabolaBlue 4F81BD inside the plot box
X0, Y0, X1, Y1 = win(565, 60, 820, 315, rend.shape)
sub = rend[Y0:Y1, X0:X1]
r_, g_, b_ = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
pmask = (b_ - r_ > 25) & (b_ - g_ > 8) & (b_ > 90)
pmask = clean(pmask)
ys, xs = np.where(pmask)
if len(xs):
    fx = xs / SX + 565
    fy = ys / SY + 60
    order = np.argsort(fx)
    fx, fy = fx[order], fy[order]
    # collapse to one y per x column (median)
    cols = {}
    for x, y in zip(np.round(fx, 1), fy):
        cols.setdefault(x, []).append(y)
    cx = np.array(sorted(cols))
    cy = np.array([np.median(cols[k]) for k in cx])
    step = 0.1
    d1 = np.diff(cy) / step
    d2 = np.diff(d1) / step
    print(f"  render parabola: {len(cx)} sampled cols, x span {cx.min():.1f}..{cx.max():.1f} (frame px)")
    print(f"  render vertex ~ x={cx[np.argmin(cy)]:.1f} y={cy.min():.1f} frame px")
    print(f"  render second-difference ripple: max|d2|={np.abs(d2).max():.3f} mean|d2|={np.abs(d2).mean():.3f} (smooth arc -> ~2*UY_per_unit^2)")
    # arms slope symmetry: left vs right arm slope magnitude at equal |x-vertex|
    print(f"  render topmost ink y={cy.min():.1f} (plot top 65)")
# orig: blue-ish parabola
om_blue = clean(mo["blue"])
X0o, Y0o, X1o, Y1o = int(565), int(60), min(820, orig.shape[1]), min(315, orig.shape[0])
subo = orig[Y0o:Y1o, X0o:X1o]
r2, g2, b2 = subo[:, :, 0], subo[:, :, 1], subo[:, :, 2]
pmo = (b2 - r2 > 20) & (b2 - g2 > 5) & (b2 > 80)
ys, xs = np.where(clean(pmo))
if len(xs):
    ox = xs + X0o
    oy = ys + Y0o
    print(f"  orig parabola: x span {ox.min()}..{ox.max()}  top y={oy.min()}  bottom y={oy.max()}")
    print(f"  orig vertex-ish: min y at x={ox[np.argmin(oy)]}")
else:
    print("  orig parabola: no blue-classified ink (colour differs — inspect)")

# ------------------------------------------------- 4. ITERATION TABLE GRID
print("\n== 4. iteration table structure ==")
for label, im, m in (("render", rend, clean(mr["navy"])), ("orig", orig, clean(mo["navy"]))):
    X0, Y0, X1, Y1 = (int(70 * SX), int(315 * SY), int(665 * SX), int(540 * SY)) if label == "render" else (70, 315, 665, 540)
    sub = m[Y0:Y1, X0:X1]
    colsum = sub.sum(axis=0)
    rowsum = sub.sum(axis=1)
    vlines = [i for i in range(len(colsum)) if colsum[i] > 0.35 * sub.shape[0]]
    hlines = [i for i in range(len(rowsum)) if rowsum[i] > 0.35 * sub.shape[1]]
    print(f"  {label:6s} navy-stroke cols with >35% height: {len(vlines)}  rows with >35% width: {len(hlines)}")

# ------------------------------------------------- 5. INK OUTSIDE PANEL
print("\n== 5. house panel containment ==")
content = np.zeros(rend.shape[:2], bool)
for m in mr.values():
    content |= clean(m)
X0, Y0, X1, Y1 = win(0, 0, 960, 540, rend.shape)
sub = content[Y0:Y1, X0:X1]
left = sub[:, :int(58 * SX)].sum()
right = sub[:, int(901 * SX):].sum()
above = sub[:int(45 * SY), :].sum()
below = sub[int(538 * SY):, :].sum()
print(f"  content ink outside panel: left={left} right={right} above={above} below={below} (0 expected for left/right/above)")
print("\nMEASUREMENT DONE")
