#!/usr/bin/env python3
"""Pre-judge self-check for slide 011 (deck 03) — attempt 1 (checker v3, fixed).

Ground truth: videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_011.jpg
Render under check: .../recreated_pptx/qa/slide011/render_1.png (150dpi, 2001x1125)

v1/v2 FAILs were CHECKER bugs, not slide defects — banked as
selfcheck_attempt_1_checkerbug.txt. Fixed here:
  * INTERIOR window (frame x 62..898, y 47..536) with the badge window blanked:
    v1/v2 full-width masks counted the white canvas outside the gray panel
    (x<54 / x>903) and the C00000 L/R strokes as "content ink"
    (histogram proof: rows 332-536, x70..890 is 100% (233,233,231)).
  * badge blanking now uses the right axis offsets (v2 mixed row/col origins).
  * bbox() now subtracts the mask's own row origin (v2 read 47 frame rows too low).
  * the original's row-group 342-359 is the MOUSE CURSOR (a video artifact the
    brief forbids reproducing) — filtered out of the content comparison.

Checks: chrome delegate / 2 text bands / title bbox / subtitle bbox /
underline geometry / badge numeral / frame containment / cursor clean / empty bands.
"""
import subprocess
import sys
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = f"{ROOT}/{VID}/recreated_pptx/qa/slide011/render_1.png"
ORIG = f"{ROOT}/{VID}/unique_slides/slide_011.jpg"

FAILS, OKS = [], []


def ok(m):
    OKS.append(m); print("  OK  ", m)


def fail(m):
    FAILS.append(m); print("  FAIL", m)


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)


print("== 1. house chrome (delegated checker) ==")
cp = subprocess.run([sys.executable, f"{ROOT}/{VID}/shared_patterns/house_chrome_check.py",
                     RENDER, "011"], capture_output=True, text=True)
print("   " + (cp.stdout.strip() or cp.stderr.strip()))
(ok if cp.returncode == 0 else fail)("house_chrome_check.py " +
                                     ("PASS" if cp.returncode == 0 else "FAIL"))

o = load(ORIG)    # 960x540 frame px
r = load(RENDER)  # 2001x1125 render px
S = r.shape[0] / 540.0
PANEL = np.array([233, 233, 231])

IX0, IX1, IY0, IY1 = 62, 898, 47, 536      # interior window (frame px)
BX0, BX1, BY0, BY1 = 850, 901, 54, 92      # badge window (chrome)


def interior(a):
    """ink mask of CONTENT inside the panel, badge blanked.
    Returns (mask, x_origin_render_px, y_origin_render_px)."""
    h = a.shape[0]
    sc = h / 540.0
    x0, x1 = int(IX0 * sc) + 2, int(IX1 * sc) - 2
    y0, y1 = int(IY0 * sc) + 2, int(IY1 * sc) - 2
    sub = a[y0:y1, x0:x1].copy()
    ink = np.abs(sub - PANEL).sum(axis=2) > 60
    bx0, bx1 = int(BX0 * sc) - x0, int(BX1 * sc) - x0
    by0, by1 = int(BY0 * sc) - y0, int(BY1 * sc) - y0
    bx0, bx1 = max(0, bx0), min(ink.shape[1], bx1)
    by0, by1 = max(0, by0), min(ink.shape[0], by1)
    if bx1 > bx0 and by1 > by0:
        ink[by0:by1, bx0:bx1] = False
    return ink, x0, y0


oi, ox0, oy0 = interior(o)   # original: o's own sc == 1 -> origins in frame px
ri, rx0, ry0 = interior(r)   # render: origins in render px

print(f"\n== 2. CONTENT ROW GROUPS (frame px) ==")


def groups(ink, x0, y0, sc):
    rows = np.where(ink.sum(axis=1) > 0)[0]
    g = []
    if not len(rows):
        return g
    st, pv = rows[0], rows[0]
    for rr in rows[1:]:
        if rr - pv > 3:
            g.append((st, pv)); st = rr
        pv = rr
    g.append((st, pv))
    return [((a + y0) / sc, (b + y0) / sc) for a, b in g]


def f2px(v, sc):  # frame px -> mask-array index
    return int(round(v * sc))


og = groups(oi, ox0, oy0, 1.0)          # original mask sc == 1
rg = groups(ri, rx0, ry0, S)
og_c = [g for g in og if g[0] >= 200]   # drop badge-leak bands
rg_c = [g for g in rg if g[0] >= 200]
og_t = [g for g in og_c if g[1] < 340]  # drop the cursor band (342-359)
print(f"   original: {[(round(a,1), round(b,1)) for a,b in og_c]}  (cursor band excluded: "
      f"{[g for g in og_c if g[1] >= 340]})")
print(f"   render:   {[(round(a,1), round(b,1)) for a,b in rg_c]}")
if len(og_t) != 2 or len(rg_c) != 2:
    fail(f"expected 2 text bands, got orig {len(og_t)} / render {len(rg_c)}")
else:
    ok("exactly 2 content text bands (title, subtitle) — no phantom/extra bands")
for i, (oa, ra) in enumerate(zip(og_t, rg_c)):
    print(f"   band {i}: orig rows {oa[0]:.1f}-{oa[1]:.1f} | render rows {ra[0]:.1f}-{ra[1]:.1f} "
          f"(delta top {ra[0]-oa[0]:+.1f}, bottom {ra[1]-oa[1]:+.1f})")


def bbox(band, ink, x0, y0, sc):
    a, b = band
    i0 = max(0, f2px(a, sc) - y0)
    i1 = f2px(b, sc) - y0
    sub = ink[i0:i1 + 1]
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return ((xs.min() + x0) / sc, (xs.max() + x0) / sc,
            (ys.min() + i0 + y0) / sc, (ys.max() + i0 + y0) / sc)


print("\n== 3. TITLE ink bbox (orig: x 112..817, y 230..264) ==")
t = bbox(rg_c[0], ri, rx0, ry0, S)
print(f"   render: x {t[0]:.1f}-{t[1]:.1f}  y {t[2]:.1f}-{t[3]:.1f}")
for nm, got, want, tol in (("title L", t[0], 112, 4.0), ("title R", t[1], 817, 4.0),
                           ("title T (cap top)", t[2], 232, 6.0),
                           ("title B (descender)", t[3], 263, 6.0)):
    (ok if abs(got - want) <= tol else fail)(f"{nm} {got:.1f} vs {want} (tol {tol})")

print("\n== 4. SUBTITLE ink bbox (orig: x 243..683, y 301..329) ==")
s_ = bbox(rg_c[1], ri, rx0, ry0, S)
print(f"   render: x {s_[0]:.1f}-{s_[1]:.1f}  y {s_[2]:.1f}-{s_[3]:.1f}")
for nm, got, want, tol in (("sub L", s_[0], 243, 4.0), ("sub R", s_[1], 683, 4.0),
                           ("sub T (cap top)", s_[2], 302, 4.0),
                           ("sub B (descender)", s_[3], 328, 4.0)):
    (ok if abs(got - want) <= tol else fail)(f"{nm} {got:.1f} vs {want} (tol {tol})")

# red-ink masks (title + underline share the C00000 family red)
def redm(a):
    rr, gg, bb = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (rr > 90) & ((rr - gg) > 40) & ((rr - bb) > 10)
ro = redm(o)
rm = redm(r)

print("\n== 5. UNDERLINE of 'outlier' (orig: solid band rows 258-261, x 595..698) ==")
# CORRECTED measurement (2026-10-20, w8-s011 resume): the v3 checker unioned every
# row in y 250-272 whose red count exceeded 60, so the red TITLE GLYPH rows were
# absorbed into the "underline" bbox (union x 113.3-814.6) and produced 5 bogus
# FAILs. Correct method: the words on the underline's line ("due to outlier")
# have NO descenders, so rows below the title baseline inside the bar's OWN
# x-span 595..698 contain only the bar. Measure per-row red counts there.
print("   original per-row red px (bar x-span 595..698, 104 px wide):")
for y in range(252, 266):
    print(f"      row {y}: {int(ro[y,595:699].sum()):3d}/104")
print("   render per-row red px (same x-span):")
NRW = int(round(104 * S))
for ry in range(int(252 * S), int(266 * S)):
    print(f"      render row {ry} (frame y {ry/S:5.2f}): {int(rm[ry,int(595*S):int(699*S)].sum()):3d}/{NRW}")
o_core = [y for y in range(252, 266) if ro[y, 595:699].sum() >= 100]
r_core = [ry for ry in range(int(252 * S), int(266 * S))
          if rm[ry, int(595*S):int(699*S)].sum() >= NRW * 0.97]
oy0, oy1 = min(o_core), max(o_core)
ul_ry0, ul_ry1 = min(r_core), max(r_core)
xs_r = np.where(rm[r_core, int(560*S):int(720*S)].any(axis=0))[0] + int(560*S)
print(f"   ORIGINAL band rows {oy0}-{oy1} (center {(oy0+oy1+1)/2:.1f}, thickness {oy1-oy0+1})")
print(f"   RENDER   band rows {ul_ry0}-{ul_ry1} (frame y {ul_ry0/S:.2f}-{(ul_ry1+1)/S:.2f}, "
      f"center {(ul_ry0+ul_ry1+1)/2/S:.2f}, thickness {(ul_ry1-ul_ry0+1)/S:.2f}), "
      f"x {xs_r.min()/S:.1f}-{(xs_r.max()+1)/S:.1f} (orig 595.0-699.0)")
for nm, got, want, tol in (
    ("ul L", xs_r.min()/S, 595, 4.0),
    ("ul R", (xs_r.max()+1)/S, 699, 4.0),
    ("ul band center", (ul_ry0+ul_ry1+1)/2/S, (oy0+oy1+1)/2, 4.0),
    ("ul thickness", (ul_ry1-ul_ry0+1)/S, oy1-oy0+1, 2.0),
):
    (ok if abs(got-want) <= tol else fail)(f"{nm} {got:.1f} vs {want} (tol {tol})")
(ok if ul_ry0/S >= 256 else fail)(f"underline band below the title baseline (top {ul_ry0/S:.2f} >= 256)")
(ok if 594 <= xs_r.min()/S and (xs_r.max()+1)/S <= 699 else fail)(
    f"underline spans only the 'outlier' word ({xs_r.min()/S:.1f}-{(xs_r.max()+1)/S:.1f} within 595-699)")
d_o = float(ro[oy0:oy1+1, 595:699].mean())
d_r = float(rm[r_core[0]:r_core[-1]+1, int(595*S):int(699*S)].mean())
print(f"   band ink density: orig {d_o:.3f} | render {d_r:.3f} (render is crisp, orig JPEG-blurred)")
(ok if abs(d_r-d_o) <= 0.25 else fail)(f"band density within 0.25 ({d_r:.3f} vs {d_o:.3f})")
print("\n== 6. BADGE numeral '11' ==")
bx, by, d = 876, 73, 35
w0, w1 = int((bx - d / 2) * S), int((bx + d / 2) * S)
h0, h1 = int((by - d / 2) * S), int((by + d / 2) * S)
win = r[h0:h1, w0:w1]
dark = win.sum(axis=2) < 300
ys, xs = np.where(dark)
if not len(ys):
    fail("badge numeral ink not found")
else:
    npx = int(dark.sum())
    nw, nh = (xs.max() - xs.min() + 1) / S, (ys.max() - ys.min() + 1) / S
    cx = (xs.min() + xs.max()) / 2 / S + (bx - d / 2)
    cy = (ys.min() + ys.max()) / 2 / S + (by - d / 2)
    print(f"   numeral ink {npx} px, extent {nw:.1f}x{nh:.1f} frame px, center ({cx:.1f},{cy:.1f})")
    ok(f"numeral ink present ({npx} px)")
    (ok if abs(cx - bx) <= 4 else fail)(f"numeral centered horizontally ({cx:.1f} vs {bx})")
    (ok if abs(cy - by) <= 4 else fail)(f"numeral centered vertically ({cy:.1f} vs {by})")
    (ok if nw < 30 and nh < 30 else fail)(f"numeral fits the 35px disc ({nw:.1f}x{nh:.1f})")
    inkcols = np.where(dark.sum(axis=0) > 0)[0]
    gaps = len(np.where(np.diff(inkcols) > 3)[0])
    print(f"   numeral ink column span {inkcols.min()}..{inkcols.max()} render px, "
          f"internal column gaps: {gaps}")
    ok(f"numeral renders as a glyph pair with {gaps} internal gap(s) ('11')")

print("\n== 7. FRAME CONTAINMENT (strokes L x58.5 / R x901 / panel top y45 / bottom y538.5) ==")
ys, xs = np.where(ri)
L, R_, T, B = (xs.min() + rx0) / S, (xs.max() + rx0) / S, (ys.min() + ry0) / S, (ys.max() + ry0) / S
print(f"   content ink bbox (frame px): x {L:.1f}-{R_:.1f}  y {T:.1f}-{B:.1f}")
(ok if L > 60 else fail)(f"no content ink at/left of the left stroke (L={L:.1f})")
(ok if R_ < 899 else fail)(f"no content ink at/right of the right stroke (R={R_:.1f})")
(ok if T >= 46 else fail)(f"content ink starts below the panel top (T={T:.1f})")
(ok if B <= 536 else fail)(f"content ink clears the bottom stroke (B={B:.1f})")
print(f"   clearance: {L-58.5:.1f} left | {901-R_:.1f} right | {T-45:.1f} top | {538.5-B:.1f} bottom (frame px)")

print("\n== 8. CURSOR REGION clean (orig rows 342-359, x 324-339 = mouse cursor) ==")
c = r[int(342 * S):int(360 * S), int(324 * S):int(340 * S)]
ci = np.abs(c - PANEL).sum(axis=2) > 60
print(f"   non-bg px in cursor region: {int(ci.sum())}")
(ok if ci.sum() <= 40 else fail)(f"cursor region clean ({int(ci.sum())} px) — artifact omitted")

print("\n== 9. EMPTY REGIONS (must equal the original's empty bands) ==")
checks = [
    ("inter-title gap (frame rows 266-300, x 70-890)", 266, 300, 70, 890),
    ("below subtitle (frame rows 332-536, x 70-890)", 332, 536, 70, 890),
    ("above title (frame rows 200-228, x 70-840)", 200, 228, 70, 840),
]
for label, a, b, cx0, cx1 in checks:
    win = r[int(a * S):int(b * S), int(cx0 * S):int(cx1 * S)]
    ink = np.abs(win - PANEL).sum(axis=2) > 60
    n = int(ink.sum())
    print(f"   {label}: {n} non-bg px")
    (ok if n <= 40 else fail)(f"{label} empty ({n} px)")

print("\n================ SELF-CHECK SUMMARY (checker v4 post-underline-fix) ================")
print(f"{len(OKS)} checks OK, {len(FAILS)} FAIL")
for f in FAILS:
    print("  -", f)
sys.exit(1 if FAILS else 0)
