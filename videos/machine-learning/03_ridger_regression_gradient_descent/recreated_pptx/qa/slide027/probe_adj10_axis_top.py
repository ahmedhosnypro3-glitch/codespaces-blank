"""PIL-first adjudication of crop_10_axis_top_judge.txt (attempt 10, Template B FAIL).

The crop region is frame(190,170)-(332,292) / 142x122 fpx. Claims adjudicated:
  MAJOR 1  y-axis shaft + arrowhead "solid black medium-weight in IMG1 vs noticeably
           thinner LIGHT-GRAY line with a softer/lighter gray arrowhead in IMG2".
  MAJOR 2  the left curve branch through the purple marker "reads as a predominantly
           straight diagonal that KINKS at the dot" in IMG1 but is "one smooth,
           continuously curved branch" in IMG2; "the only curvature is a faint separate
           gray arc hugging the lower-right of the dot".
Instrument: per-column band-limited centroid residual against the shipped analytic
quadratic (the render) / a dense centre-line walk anchored on the banked trace knots
(the original), 5-pt moving average before the second difference, plus colour/luminance
census of the axis ink and point-geometry of the branch.
All maths in RENDER px per render, reported in frame px (1 fpx = 1 pt).
"""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
REND = QA + "render_10.png"
CX0, CY0, CX1, CY1 = 190, 170, 332, 292          # crop window in frame px


def load(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)
    return a, a.shape[1] / 960.0


def q(x):                                            # shipped quadratic (frame px)
    return -0.00395282 * (x - 450.41) ** 2 + 407.25


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


def spread(a):
    return a.max(axis=2) - a.min(axis=2)


def mad(v, k=5):
    k = np.ones(k) / k
    return np.convolve(v, k, mode="same")


def f(x, s):                                         # frame col -> render col
    return x * s


def band_residual(im, s, lo, hi, band, anchor, exclude=()):
    """Band-limited column centroid residual vs `anchor(x)` (frame px)."""
    L = lum(im)
    S = spread(im)
    m_ink = (L < 70) & (S <= 12)
    xs, res = [], []
    for xf in range(lo, hi + 1):
        if any(a0 <= xf <= a1 for a0, a1 in exclude):
            continue
        x0 = int(round(f(xf, s))) - band
        x1 = int(round(f(xf, s))) + band + 1
        yc = anchor(xf)
        y0 = int(round(f(yc, s))) - int(band * 1.6)
        y1 = int(round(f(yc, s))) + int(band * 1.6) + 1
        sub = m_ink[max(0, y0):y1, max(0, x0):min(x1, im.shape[1])]
        if not sub.any():
            continue
        ys, _ = np.where(sub)
        # only runs whose pixel lies within +-band*0.35 fpx of the anchor -> kill the
        # axis shaft / leader ink that shares this column band
        keep = [(y + y0) for y in ys
                if abs((y + y0) / s - yc) <= band * 0.35]
        if not keep:
            continue
        xs.append(xf)
        res.append(np.mean(keep) / s - yc)
    return np.array(xs), np.array(res)


def chord_bow(xs, ys):
    """Max |departure from the straight chord| over the run, frame px."""
    p0 = np.array([xs[0], ys[0]])
    p1 = np.array([xs[-1], ys[-1]])
    d = p1 - p0
    L = np.hypot(*d)
    n = np.array([-d[1], d[0]]) / L
    pts = np.stack([xs, ys], axis=1)
    return float(np.abs((pts - p0) @ n).max()), float(L)


print("=" * 78)
print("ADJUDICATION — crop_10_axis_top (frame 190..332 x 170..292)")
print("=" * 78)

oa, so = load(ORIG)
ra, sr = load(REND)
print(f"render_10 {ra.shape[1]}x{ra.shape[0]} scale {sr:.5f} (= H/540)")

# ---------------------------------------------------------------- MAJOR 1: the axis
print("\n### MAJOR 1 — y-axis shaft + arrowhead tone/weight")
print("\nY-axis shaft location (dark-ink column profile, band frame y 300..420 so the")
print("crop's curve branch and labels are outside the window):")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    L = lum(im)
    S = spread(im)
    m = (L < 70) & (S <= 12)
    colcnt = m[int(300 * s):int(420 * s), int(180 * s):int(240 * s)].sum(axis=0)
    cols = np.where(colcnt > 30)[0] / s + 180
    if len(cols):
        runs, k0, prev = [], cols[0], cols[0]
        for c in cols[1:]:
            if c - prev > 1.5:
                runs.append((k0, prev))
                k0 = c
            prev = c
        runs.append((k0, prev))
        print(f"  {tag}: dark col runs (frame px): {[(round(a,1), round(b,1)) for a,b in runs]}")
    # the shaft's ink colour + weight, measured on the cleanest stretch (frame y 300..420)
    if len(cols):
        cx = np.mean([np.mean([a, b]) for a, b in runs]) if runs else 0
        x0, x1 = int(f(cx - 3, s)), int(f(cx + 3, s))
        blk = m[int(300 * s):int(420 * s), x0:x1]
        px = im[int(300 * s):int(420 * s), x0:x1][blk]
        if len(px):
            print(f"    shaft centroid x={cx:.2f} fpx | ink px n={len(px)} | "
                  f"mean RGB ({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f}) | "
                  f"median lum {np.median(0.299*px[:,0]+0.587*px[:,1]+0.114*px[:,2]):.0f} | "
                  f"darkest px lum {lum(im[int(300*s):int(420*s), x0:x1])[blk].min():.0f} | "
                  f"stroke width (cols >59 lum) {np.sum(colcnt/s > 0) if False else ''}"
                  f"{np.unique(np.where(np.tile((lum(im[int(300*s):int(420*s), x0:x1])<70), (1,1)))[1]).size}")

# arrowhead: filled triangle apex frame (223,206), base row 222 x 218..228 (render).
# measure the apex-side ink colour of the original by scanning for the local ink blob
# just above the shaft.
print("\nArrowhead apex ink (topmost dark ink above the shaft, frame x 212..236, y 175..215):")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    L = lum(im)
    S = spread(im)
    m = (L < 90) & (S <= 40)
    sub = m[int(175 * s):int(215 * s), int(212 * s):int(236 * s)]
    if sub.any():
        ys, xs = np.where(sub)
        y0 = ys.min() / s + 175
        y1 = ys.max() / s + 175
        px = im[int(175 * s):int(215 * s), int(212 * s):int(236 * s)][sub]
        print(f"  {tag}: ink bbox y {y0:.1f}..{y1:.1f} x {xs.min()/s+212:.1f}..{xs.max()/s+212:.1f}"
              f" | mean RGB ({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f})"
              f" | lum p10 {np.percentile(0.299*px[:,0]+0.587*px[:,1]+0.114*px[:,2],10):.0f}"
              f" | n={len(px)}")
    else:
        print(f"  {tag}: no ink")

# ------------------------------------------------- MAJOR 2: branch shape vs the marker
print("\n### MAJOR 2 — left branch geometry through the purple marker")
TRACE = [                       # banked attempt-8 trace knots (frame px) for the ORIGINAL
    [253, 230], [254, 236], [255, 242], [256, 246], [259, 252], [262, 272], [268, 280],
    [270, 286], [272, 292], [274, 296], [276, 300], [278, 302],
]
# a smooth guide through those knots, sampled densely, so the band-limited walk of the
# ORIGINAL's own ink stays on the branch (no free nearest-run walk: that jumps onto the
# axis/leader ink, the error that produced verify-attempt-9's false NOT-SMOOTH).
gt = np.array([t[0] for t in TRACE], float)
gs = np.array([t[1] for t in TRACE], float)
gx = np.linspace(gt[0], gt[-1], 400)
guide = np.interp(gx, gt, gs)
# monotone-ish smoothing of the guide (3 passes of a 9-pt box) to kill knot-level steps
for _ in range(3):
    guide = np.convolve(guide, np.ones(9) / 9, mode="same")


def guide_fn(xf):
    return float(np.interp(xf, gx, guide))


print("\nLeft branch centre-line residual (band +-14 fpx, dark ink lum<70 spread<=12),")
print("frame x 244..300 — i.e. the exact stretch the crop judge described:")
for tag, im, s, anchor in (("ORIG", oa, so, guide_fn), ("REND", ra, sr, q)):
    xs, res = band_residual(im, s, 244, 300, 14, anchor,
                            exclude=[(262, 263)])   # dashed leader collar
    if not len(xs):
        print(f"  {tag}: no ink found")
        continue
    d2 = np.diff(np.diff(mad(res)))
    print(f"  {tag}: n={len(xs)} cols | residual rms {np.sqrt((res**2).mean()):.3f} "
          f"max {np.abs(res).max():.3f} fpx | 2nd-diff rms {np.sqrt((d2**2).mean()):.4f} "
          f"max {np.abs(d2).max():.3f} (quantisation floor ~0.30)")
    ys = np.array([anchor(x) + r for x, r in zip(xs, res)])
    bow, L = chord_bow(xs, ys)
    print(f"       chord from x={xs[0]} to x={xs[-1]} (len {L:.1f} fpx): max bow "
          f"{bow:.2f} fpx  (a quadratic bows |a|*L^2/8 = "
          f"{0.00395282*L*L/8 if tag=='REND' else 0:.2f} fpx on the render)")

print("\nBranch slope across the same stretch (frame px/fpx) — a quadratic's slope is a")
print("straight line in x; the original's arms flatten slower, which is what makes the")
print("fitted quadratic read 'straight' over this window:")
for tag, im, s, anchor in (("ORIG", oa, so, guide_fn), ("REND", ra, sr, q)):
    xs, res = band_residual(im, s, 244, 300, 14, anchor, exclude=[(262, 263)])
    if not len(xs):
        continue
    ys = np.array([anchor(x) + r for x, r in zip(xs, res)])
    for lo, hi in ((244, 250), (258, 268), (276, 300)):
        k = (xs >= lo) & (xs <= hi)
        if k.sum() < 3:
            continue
        sl = np.polyfit(xs[k], ys[k], 1)[0]
        print(f"  {tag} x {lo}..{hi}: slope {sl:+.2f}  "
              f"(y {ys[k].min():.0f}..{ys[k].max():.0f})")

# the grey ink next to the marker: dashed leader vs connector
print("\nGrey-violet ink census in the crop (spread<=12, lum 100..200): where is the grey")
print("ink relative to dot 1 (263.12,263.41)?  The judge called the north-west blob")
print("'a faint separate gray arc hugging the lower-right of the dot'.")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    L = lum(im)
    S = spread(im)
    m = (S <= 12) & (L >= 100) & (L <= 200)
    ys, xs = np.where(m)
    fx = xs / s
    fy = ys / s
    for name, (x0, x1, y0, y1) in (
            ("NW of dot1 (leader collar)", (252, 268, 233, 258)),
            ("S-SE of dot1 (connector 1->2)", (264, 282, 264, 292)),
            ("W of dot1", (215, 252, 232, 258))):
        k = (fx >= x0) & (fx <= x1) & (fy >= y0) & (fy <= y1)
        print(f"  {tag} {name}: n={int(k.sum())} px"
              + (f" bbox x {fx[k].min():.0f}..{fx[k].max():.0f} y {fy[k].min():.0f}..{fy[k].max():.0f}"
                 if k.sum() else ""))

print("\n### VERDICT INPUTS")
print("MAJOR 1: measured shaft/arrow tone above (compare mean RGB / lum).")
print("MAJOR 2: second differences + chord bow above; the shipped curve is one analytic")
print("        quadratic, so a kink is impossible by construction.")
