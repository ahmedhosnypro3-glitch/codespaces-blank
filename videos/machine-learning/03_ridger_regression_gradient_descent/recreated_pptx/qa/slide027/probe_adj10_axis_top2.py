"""Second axis_top measurement pass (attempt 10 adjudication).

pass 1 (probe_adj10_axis_top.py) found NO dark ink (lum<70, spread<=12) along the
ORIGINAL's axis shaft in the band frame y 300..420, x 180..240 while the render's
shaft is pure black there. This pass locates the ORIGINAL's axis with a relaxed mask,
measures its tone/width honestly (and the render's), isolates the arrowhead ink away
from the "Cost" label, and traces the ORIGINAL's left branch with a relaxed dark mask so
the crop judge's branch-shape claim can be measured against the render's quadratic."""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
REND = QA + "render_10.png"


def load(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(float)
    return a, a.shape[1] / 960.0


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


def spread(a):
    return a.max(axis=2) - a.min(axis=2)


oa, so = load(ORIG)
ra, sr = load(REND)
print(f"scale orig {so:.5f} render {sr:.5f}")

# ---- 1. locate the y-axis shaft in both images (frame y 300..420, x 195..245) --------
print("\n### y-axis shaft: column census in frame y 300..420, x 195..245")
print("(a = pure black, b = mid grey) — three ink classes by luminance")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    L = lum(im)[int(300 * s):int(420 * s), int(195 * s):int(245 * s)]
    S = spread(im)[int(300 * s):int(420 * s), int(195 * s):int(245 * s)]
    for name, m in (("lum<70", L < 70), ("70..150", (L >= 70) & (L < 150)),
                    ("150..255", L >= 150)):
        cnt = m.sum(axis=0)
        cols = np.where(cnt > 60)[0]
        if len(cols):
            runs, k0, prev = [], cols[0], cols[0]
            for c in cols[1:]:
                if c - prev > 2:
                    runs.append((k0, prev)); k0 = c
                prev = c
            runs.append((k0, prev))
            print(f"  {tag} {name:8s}: col runs (frame px) "
                  f"{[(round(r[0]/s+195,1), round(r[1]/s+195,1)) for r in runs]}")
        else:
            print(f"  {tag} {name:8s}: none")

print("\n### shaft tone/width at its own column, frame y 320..410 (no labels, no curve)")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    L = lum(im); S = spread(im)
    # darkest vertical ink run in x 195..245 across the band
    band = L[int(320 * s):int(410 * s), int(195 * s):int(245 * s)]
    Sb = S[int(320 * s):int(410 * s), int(195 * s):int(245 * s)]
    ink = (band < 160) & (Sb < 60)
    colfrac = ink.sum(axis=0) / ink.shape[0]
    hit = np.where(colfrac > 0.5)[0]
    if not len(hit):
        print(f"  {tag}: no column >50% ink in the band")
        continue
    # contiguous run around the strongest column
    c0 = c1 = hit[int(np.argmax(colfrac[hit]))]
    while colfrac[max(0, c0 - 1)] > 0.5: c0 -= 1
    while colfrac[min(len(colfrac) - 1, c1 + 1)] > 0.5: c1 += 1
    cx = (c0 + c1) / 2 / s + 195
    w = (c1 - c0 + 1) / s
    sub = im[int(320 * s):int(410 * s), int((cx - 4) * s):int((cx + 4) * s)]
    Ls = lum(sub); Ss = spread(sub)
    px = sub[Ls < 200]
    core = sub[(Ls < 90) & (Ss < 40)]
    print(f"  {tag}: axis centre x={cx:.2f} | drawn width {w:.2f} fpx | "
          f"ink(<200) n={len(px)} mean RGB "
          f"({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f})"
          f" | core(<90 lum) n={len(core)} mean RGB "
          f"({core[:,0].mean():.0f},{core[:,1].mean():.0f},{core[:,2].mean():.0f})"
          f" | core lum p50 {np.median(0.299*core[:,0]+0.587*core[:,1]+0.114*core[:,2]) if len(core) else float('nan'):.0f}")

# ---- 2. arrowhead: isolate from "Cost" -----------------------------------------------
print("\n### 'Cost' label position (dark-red ink, frame x 195..270, y 168..200)")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    m = (R > 90) & (R < 200) & (G < 70) & (B < 70)
    m[:int(168 * s), :] = False; m[int(200 * s):, :] = False
    ys, xs = np.where(m)
    k = (xs / s >= 195) & (xs / s <= 270)
    if k.sum():
        print(f"  {tag}: bbox x {xs[k]/s + 195 - 195:.1f}..{xs[k].max()/s:.1f} "
              f"y {ys[k].min()/s:.1f}..{ys[k].max()/s:.1f} n={int(k.sum())}")
    else:
        print(f"  {tag}: none")

print("\n### arrowhead ink, window frame x 214..232 y 200..220 (below 'Cost', above base)")
print("### the filled triangle apex is (223,206), base row 222, in the render")
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    L = lum(im); S = spread(im)
    y0, y1, x0, x1 = (int(v * s) for v in (200, 220, 214, 232))
    sub = im[y0:y1, x0:x1]
    Ls = lum(sub); Ss = spread(sub)
    for name, m in (("lum<60", Ls < 60), ("60..140", (Ls >= 60) & (Ls < 140)),
                    ("140..215", (Ls >= 140) & (Ls < 215))):
        if m.any():
            ys, xs = np.where(m)
            px = sub[m]
            print(f"  {tag} {name:8s}: n={int(m.sum()):5d} bbox "
                  f"x{xs.min()/s+214:.1f}..{xs.max()/s+214:.1f} "
                  f"y{ys.min()/s+200:.1f}..{ys.max()/s+200:.1f} mean RGB "
                  f"({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f})")
        else:
            print(f"  {tag} {name:8s}: n=0")

# ---- 3. the ORIGINAL's left branch, relaxed dark mask --------------------------------
print("\n### left branch centre-line (relaxed ink: lum<120 & spread<45), frame x 244..300")
print("### band +-12 fpx around the render's analytic quadratic as the anchor, EXCLUDING")


def q(x):
    return -0.00395282 * (x - 450.41) ** 2 + 407.25


def mad(v, k=5):
    return np.convolve(v, np.ones(k) / k, mode="same")


def trace(im, s, anchor, lo, hi, band, exclude):
    L = lum(im); S = spread(im)
    m = (L < 120) & (S < 45)
    xs, res = [], []
    for xf in range(lo, hi + 1):
        if any(a0 <= xf <= a1 for a0, a1 in exclude):
            continue
        x0 = int(round(xf * s)) - band; x1 = int(round(xf * s)) + band + 1
        yc = anchor(xf)
        y0 = int(round(yc * s)) - int(band * 1.3); y1 = int(round(yc * s)) + int(band * 1.3) + 1
        sub = m[max(0, y0):y1, max(0, x0):min(x1, im.shape[1])]
        if not sub.any():
            continue
        ys, _ = np.where(sub)
        ys = ys + y0
        keep = [y for y in ys if abs(y / s - yc) <= band * 0.45]
        if not keep:
            continue
        xs.append(xf); res.append(np.mean(keep) / s - yc)
    return np.array(xs), np.array(res)


print("### the dashed-leader collar x 261..264, and the dot-1 disc x 256..270")
EX = [(261, 264), (256, 270)]
for tag, im, s in (("ORIG", oa, so), ("REND", ra, sr)):
    xs, res = trace(im, s, q, 244, 300, 12, EX)
    if not len(xs):
        print(f"  {tag}: no ink")
        continue
    d2 = np.diff(np.diff(mad(res)))
    ys = np.array([q(x) + r for x, r in zip(xs, res)])
    # chord bow
    p0, p1 = np.array([xs[0], ys[0]]), np.array([xs[-1], ys[-1]])
    d = p1 - p0; L = float(np.hypot(*d)); n = np.array([-d[1], d[0]]) / L
    bow = float(np.abs((np.stack([xs, ys], 1) - p0) @ n).max())
    print(f"  {tag}: n_cols={len(xs)} | residual rms {np.sqrt((res**2).mean()):.3f} "
          f"max {np.abs(res).max():.3f} fpx | 2nd-diff rms {np.sqrt((d2**2).mean()):.4f} "
          f"max|d2| {np.abs(d2).max():.3f} (quantisation floor ~0.30) | "
          f"chord x{xs[0]}..{xs[-1]} len {L:.1f} bow {bow:.2f} fpx")
    for a, b in ((244, 252), (254, 262), (272, 286), (288, 300)):
        k = (xs >= a) & (xs <= b)
        if k.sum() >= 3:
            sl = np.polyfit(xs[k], ys[k], 1)[0]
            print(f"       x {a}..{b}: slope {sl:+.2f}")
