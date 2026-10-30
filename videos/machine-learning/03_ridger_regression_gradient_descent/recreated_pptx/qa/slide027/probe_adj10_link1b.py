"""dot_sequence MINOR 1, measured properly: the FIRST connector's own path in each image,
with the two dot halos and the dashed leader excluded so only the connector's own ink is
sampled. Renders the build's claim (arcs fitted to the original's visible arc-ink) against
the original's actual ink for interval 1 (the interval the crop judge drew)."""
import numpy as np
from PIL import Image

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide027/"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_027.jpg"
REN = QA + "render_10.png"
P0 = np.array([263.12, 263.41]); P2 = np.array([283.64, 309.88])
d = P2 - P0; L = float(np.hypot(*d)); u = d / L
n = np.array([u[1], -u[0]])            # normal: positive = up-right (away from the curve,
# the curve sits 3.3 fpx ABOVE the chord midpoint, so the away side is down-left?? check:
def q(x): return -0.00395282 * (x - 450.41) ** 2 + 407.25
mid = (P0 + P2) / 2
print(f"normal {n} ; curve at chord-mid x={mid[0]:.1f} -> y={q(mid[0]):.1f}; "
      f"chord-mid y={mid[1]:.1f}  => curve is {'ABOVE' if q(mid[0])<mid[1] else 'BELOW'} "
      f"the chord by {abs(q(mid[0])-mid[1]):.1f} fpx")
NWAY = n if q(mid[0]) < mid[1] else -n   # point from the chord TOWARD the curve
NAWAY = -NWAY
print(f"NWAY (toward curve) = {NWAY} ; NAWAY = {NAWAY}")


def load(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(float)
    return a, a.shape[1] / 960.0


def chain_mask(im):
    L = 0.299 * im[:, :, 0] + 0.587 * im[:, :, 1] + 0.114 * im[:, :, 2]
    S = im.max(axis=2) - im.min(axis=2)
    return (S <= 16) & (L >= 120) & (L <= 215)


for tag, p in (("ORIG", ORIG), ("REND", REN)):
    im, s = load(p)
    m = chain_mask(im)
    rows = []
    for t in np.linspace(0.06, 0.96, 46):
        base = P0 + t * d
        vals = []
        for off in np.arange(2.0, 17.01, 0.25):      # away side only (the curve side is
            pt = base + off * NAWAY                # excluded by starting at +2)
            x, y = int(round(pt[0] * s)), int(round(pt[1] * s))
            if 0 <= x < im.shape[1] and 0 <= y < im.shape[0] and m[y, x]:
                vals.append(off)
        if vals:
            rows.append((t, float(np.mean(vals)), float(np.median(vals)), len(vals)))
    ts = np.array([r[0] for r in rows])
    mn = np.array([r[1] for r in rows])
    md = np.array([r[2] for r in rows])
    print(f"\n### {tag}: connector-1 ink, offsets measured on the AWAY side of the chord")
    print("   t    mean off (NAWAY, fpx)   median   n")
    for (t, mm, md_, c) in rows[::3]:
        print(f"  {t:4.2f}   {mm:+6.2f}              {md_:+6.2f}   {c}")
    # fit a quadratic in s to the mean-offset profile
    if len(ts) >= 5:
        c2 = np.polyfit(ts, mn, 2)
        fit = np.polyval(c2, ts)
        bow = float(np.max(np.abs(fit - np.interp(ts, [ts[0], ts[-1]],
                                                  [fit[0], fit[-1]]))))
        print(f"   quadratic fit of mean-offset profile: a={c2[0]:.2f} "
              f"(chord units) -> bow {bow:.2f} fpx ; residual rms "
              f"{np.sqrt(((mn-fit)**2).mean()):.2f}")
        print(f"   profile: mid(t=0.5 approx) mean off {np.interp(0.5, ts, mn):+.2f} fpx ; "
              f"max mean off {mn.max():+.2f} at t={ts[np.argmax(mn)]:.2f}")
        # the built arc for comparison (only meaningful for REND, but compute for both)
        print(f"   built render arc at t=0.5 sits 13.64 fpx off the chord on the away side")
    # the arrowhead zone: mean offset in the last 15% (the head sits 6.3-6.6 fpx from P2)
    tf = ts[ts > 0.86]
    if len(tf):
        print(f"   offsets near the target (t>0.86): {np.mean(mn[ts>0.86]):+.2f} mean "
              f"(the head tip is 6.3-6.6 fpx from the target centre)")
