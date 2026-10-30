#!/usr/bin/env python3
"""probe70 — closed-loop PIL verification of the founder-directive annotation on render_6.

Checks (render 2001x1125, scale s = 150/72 render-px per frame-px):
  A. mm-labels: red ink near the frame centroids, PCA angle = the build rot
     (62.8 / 64.5 deg, DESCENDING left->right), separated from the shaft.
  B. dim shafts: straight, angle = the true perpendicular (62.81 / 64.54),
     red (not pale-rose), lower end reaching the blue fitted line (foot ON it).
  C. perpendicularity vs the blue line as MEASURED in the render (diff ~ 90 deg).
  D. two heads per arrow: ink width near t=0 and t=len much larger than mid-shaft.
  E. parallel leaders: angle = the blue line's angle, thin everywhere (NO head).
  F. orange outliers visible over the upper heads.
Expected geometry comes from build/slide_009.js PANELS (frame px).
"""
import math
import numpy as np
from PIL import Image

S = 1125 / 540.0  # render px per frame px

im = np.asarray(Image.open("render_6.png").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 120) & ((r - g) > 110) & ((r - b) > 90)  # red CORE; excludes orange (r-g~90)
blue = (b > 140) & ((b - r) > 80) & ((b - g) > 60)
orange = (r > 200) & (g > 80) & (g < 200) & (b < 100)

fails, notes = [], []


def f2r(v):
    return v * S


def pca_angle(ys, xs):
    """Angle in degrees of the principal axis, atan2(dy,dx), y down, in (-90,90]."""
    y = ys - ys.mean()
    x = xs - xs.mean()
    cov = np.array([[ (x * x).sum(), (x * y).sum()], [ (x * y).sum(), (y * y).sum()]])
    evals, evecs = np.linalg.eigh(cov)
    v = evecs[:, np.argmax(evals)]
    ang = math.degrees(math.atan2(v[1], v[0]))  # (dy, dx), y down
    while ang > 90.0:
        ang -= 180.0
    while ang <= -90.0:
        ang += 180.0
    return ang


def ink_in_band(p0, p1, halfw, t0=0.0, t1=None):
    """Red px within +-halfw (frame px) of segment p0->p1, param range [t0,t1] (frame px)."""
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    if t1 is None:
        t1 = L
    ys, xs = np.where(red)
    # window
    wx0, wx1 = int(f2r(min(x0, x1) - 12)), int(f2r(max(x0, x1) + 12))
    wy0, wy1 = int(f2r(min(y0, y1) - 12)), int(f2r(max(y0, y1) + 12))
    m = (ys >= wy0) & (ys < wy1) & (xs >= wx0) & (xs < wx1)
    ys, xs = ys[m], xs[m]
    fx, fy = xs / S, ys / S
    t = (fx - x0) * ux + (fy - y0) * uy
    d = -( (fx - x0) * uy - (fy - y0) * ux )
    m = (t >= t0) & (t <= t1) & (np.abs(d) <= halfw)
    return ys[m], xs[m], t[m], d[m]


def width_at(p0, u, t, band=6.0):
    """Ink width (frame px) across the line at param t (perpendicular extent)."""
    x0, y0 = p0
    px_, py_ = x0 + u[0] * t, y0 + u[1] * t
    ys, xs = np.where(red)
    wx0, wx1 = int(f2r(px_ - band - 3)), int(f2r(px_ + band + 3))
    wy0, wy1 = int(f2r(py_ - band - 3)), int(f2r(py_ + band + 3))
    m = (ys >= wy0) & (ys < wy1) & (xs >= wx0) & (xs < wx1)
    ys, xs = ys[m], xs[m]
    fx, fy = xs / S, ys / S
    d = -( (fx - px_) * u[1] - (fy - py_) * u[0] )
    m = np.abs(d) <= band
    d = d[m]
    if len(d) == 0:
        return 0.0
    return float(d.max() - d.min() + 1.0 / S)


def fit_blue(p0, p1):
    ys, xs = np.where(blue)
    wx0, wx1 = int(f2r(min(p0[0], p1[0]) - 10)), int(f2r(max(p0[0], p1[0]) + 10))
    wy0, wy1 = int(f2r(min(p0[1], p1[1]) - 10)), int(f2r(max(p0[1], p1[1]) + 10))
    m = (ys >= wy0) & (ys < wy1) & (xs >= wx0) & (xs < wx1)
    ys, xs = ys[m], xs[m]
    if len(ys) < 50:
        return None, 0
    ang = pca_angle(ys.astype(float), xs.astype(float))
    return ang, len(ys)


def dist_pt_line(pt, p0, ang_deg):
    """Distance from pt (frame px) to the line through p0 with direction ang_deg."""
    ux, uy = math.cos(math.radians(ang_deg)), math.sin(math.radians(ang_deg))
    return abs(-( (pt[0] - p0[0]) * uy - (pt[1] - p0[1]) * ux ))


CHARTS = [
    dict(
        name="LEFT",
        outlier=(197.5, 145.0), foot=(269.43, 285.03), u=(0.45691, 0.88951),
        ang=62.81, plen=157.42, head_low_h=7.5, head_up_h=9.0,
        tail=(176.5, 155.79), blue=(141, 351, 433, 201), blue_ang=-27.19,
        label_roi=(180, 185, 245, 236), label_target=(208.7, 213.4),
        label_spec=(210.0, 212.0), label_rot=62.8, disc=(232.5, 241.0),
    ),
    dict(
        name="RIGHT",
        outlier=(611.0, 145.0), foot=(694.59, 320.53), u=(0.42993, 0.90286),
        ang=64.54, plen=194.42, head_low_h=8.0, head_up_h=9.0,
        tail=(591.0, 154.52), blue=(555, 387, 849, 247), blue_ang=-25.46,
        label_roi=(615, 200, 662, 270), label_target=(637.0, 237.0),
        label_spec=(637.0, 237.0), label_rot=64.5, disc=None,
    ),
]

for c in CHARTS:
    n = c["name"]
    u = c["u"]
    out = c["outlier"]
    foot = c["foot"]

    # ── B. shaft ────────────────────────────────────────────────────────────
    ys, xs, t, d = ink_in_band(out, foot, 2.2, t0=10, t1=c["plen"] - c["head_low_h"] - 2)
    if len(ys) < 40:
        fails.append(f"{n}: shaft ink too sparse ({len(ys)} px in corridor)")
    else:
        ang = pca_angle(ys.astype(float), xs.astype(float))
        resid = d - d.mean()
        rg = float((r[ys, xs] - g[ys, xs]).mean())
        notes.append(f"{n} shaft: n={len(ys)} angle={ang:.2f} (exp {c['ang']}) "
                     f"resid_std={resid.std():.2f}px r-g={rg:.0f}")
        if abs(ang - c["ang"]) > 2.0:
            fails.append(f"{n}: shaft angle {ang:.2f} vs perpendicular {c['ang']}")
        if resid.std() > 1.6:
            fails.append(f"{n}: shaft not straight (resid std {resid.std():.2f})")
        if rg < 100:
            fails.append(f"{n}: shaft ink not RED (mean r-g {rg:.0f}) — pale-rose remnant?")

    # foot ON the line: nearest red px (t > plen-8) to the fitted blue line
    bang, bn = fit_blue((c["blue"][0], c["blue"][1]), (c["blue"][2], c["blue"][3]))
    if bang is None:
        fails.append(f"{n}: blue line not found in render")
    else:
        if abs(bang - c["blue_ang"]) > 2.0:
            fails.append(f"{n}: blue angle {bang:.2f} vs expected {c['blue_ang']}")
        ys2, xs2, t2, d2 = ink_in_band(out, foot, 2.2, t0=c["plen"] - 9, t1=c["plen"])
        if len(ys2) == 0:
            fails.append(f"{n}: no red ink at the shaft foot")
        else:
            fx, fy = xs2 / S, ys2 / S
            dists = [dist_pt_line((x, y), (c["blue"][0], c["blue"][1]), bang) for x, y in zip(fx, fy)]
            notes.append(f"{n} foot: min dist red->blue {min(dists):.2f}px (n={len(ys2)})")
            if min(dists) > 3.0:
                fails.append(f"{n}: shaft foot {min(dists):.2f}px off the blue line (must be ON it)")
        # perpendicularity as measured
        diff = (c["ang"] - bang) % 180
        notes.append(f"{n} perpendicularity: shaft-blue = {diff:.2f} deg")
        if abs(diff - 90.0) > 3.0:
            fails.append(f"{n}: shaft not orthogonal to blue as rendered ({diff:.2f} deg)")

    # ── D. two heads ────────────────────────────────────────────────────────
    w_mid = width_at(out, u, (10 + c["plen"] - c["head_low_h"] - 2) / 2)
    w_low = width_at(out, u, c["plen"] - c["head_low_h"] / 2)
    w_up = width_at(out, u, c["head_up_h"] / 2 + 1.5)
    notes.append(f"{n} widths: mid={w_mid:.2f} lowHead={w_low:.2f} upHead={w_up:.2f}")
    if w_low < w_mid + 2.0:
        fails.append(f"{n}: LOWER head missing/too small (w {w_low:.2f} vs shaft {w_mid:.2f})")
    if w_up < w_mid + 2.0:
        fails.append(f"{n}: UPPER head missing/too small (w {w_up:.2f} vs shaft {w_mid:.2f})")

    # ── E. parallel leader: angle = blue, thin everywhere ───────────────────
    tys, txs, tt, td = ink_in_band(c["tail"], out, 2.0, t0=3.5, t1=None)
    tlen = math.hypot(out[0] - c["tail"][0], out[1] - c["tail"][1])
    if len(tys) < 15:
        fails.append(f"{n}: parallel leader ink too sparse ({len(tys)})")
    else:
        tang = pca_angle(tys.astype(float), txs.astype(float))
        notes.append(f"{n} leader: n={len(tys)} angle={tang:.2f} (blue {bang:.2f})")
        if abs(((tang - bang + 90) % 180) - 90) > 2.5:
            fails.append(f"{n}: leader not parallel to blue ({tang:.2f} vs {bang:.2f})")
        # width profile — no arrowhead along the leader body. The last few px before
        # the outlier are the junction with the DIM arrow's upper head (that head's
        # apex legitimately sits on the outlier), so they are sampled as a note only.
        ldir = ((out[0] - c["tail"][0]) / tlen, (out[1] - c["tail"][1]) / tlen)
        prof = []
        for tq in np.linspace(3.0, tlen - 1.5, 10):
            prof.append((float(tq), width_at(c["tail"], ldir, float(tq), band=4.0)))
        wmax = max(w for _, w in prof if _ <= tlen - 7.0)
        wjunc = prof[-1][1]
        notes.append(f"{n} leader width profile: "
                     + " ".join(f"t{t:.0f}={w:.1f}" for t, w in prof)
                     + f" | body max {wmax:.2f} junction {wjunc:.2f}")
        if wmax > 4.5:
            fails.append(f"{n}: leader carries a widening (arrowhead?) max w {wmax:.2f}")

    # ── A. label ────────────────────────────────────────────────────────────
    x0, y0, x1, y1 = c["label_roi"]
    ys3, xs3 = np.where(red[int(f2r(y0)):int(f2r(y1)), int(f2r(x0)):int(f2r(x1))])
    ys3 = ys3 + int(f2r(y0))
    xs3 = xs3 + int(f2r(x0))
    fx, fy = xs3 / S, ys3 / S
    # exclude shaft pixels (within 5 frame px of the shaft centerline) and the
    # LEFT chart's big red disc (it is chart content, not label ink)
    du = (fx - out[0]) * u[0] + (fy - out[1]) * u[1]
    dv = -( (fx - out[0]) * u[1] - (fy - out[1]) * u[0] )
    keep = np.abs(dv) > 5.0
    if c.get("disc"):
        dcx, dcy = c["disc"]
        keep &= np.hypot(fx - dcx, fy - dcy) > 15.0
    fxk, fyk = fx[keep], fy[keep]
    if len(fxk) < 60:
        fails.append(f"{n}: label ink too sparse after shaft filter ({len(fxk)})")
    else:
        ang = pca_angle(fyk, fxk)
        cy_, cx_ = fyk.mean(), fxk.mean()
        descends = ang > 5
        notes.append(f"{n} label: n={len(fxk)} centroid=({cx_:.1f},{cy_:.1f}) "
                     f"spec={c['label_spec']} frame_ink={c['label_target']} "
                     f"angle={ang:.2f} (exp {c['label_rot']})")
        # anchor: the founder's own label centre (the spec cx/cy); the frame-ink
        # centroid is a note (the LEFT one is shaft-contaminated on the frame).
        if math.hypot(cx_ - c["label_spec"][0], cy_ - c["label_spec"][1]) > 5.0:
            fails.append(f"{n}: label centroid ({cx_:.1f},{cy_:.1f}) off spec centre "
                         f"{c['label_spec']} by "
                         f"{math.hypot(cx_-c['label_spec'][0], cy_-c['label_spec'][1]):.1f}px")
        if not descends:
            fails.append(f"{n}: label angle {ang:.2f} not descending (must run along the arrow)")
        if abs(ang - c["label_rot"]) > 7.0:
            fails.append(f"{n}: label angle {ang:.2f} far from arrow angle {c['label_rot']}")

    # ── F. outlier visibility ───────────────────────────────────────────────
    ox, oy = out
    win = np.s_[int(f2r(oy - 6)):int(f2r(oy + 6)), int(f2r(ox - 6)):int(f2r(ox + 6))]
    n_orn = int(orange[win].sum())
    notes.append(f"{n} outlier orange px in 12px window: {n_orn}")
    if n_orn < 20:
        fails.append(f"{n}: orange outlier not visible over the upper head ({n_orn} px)")

print("── probe70 notes ──")
for x in notes:
    print("  ", x)
print("── probe70 verdict ──")
if fails:
    print("FAIL")
    for x in fails:
        print("  -", x)
    raise SystemExit(1)
print("PASS — annotation matches the founder construction")
