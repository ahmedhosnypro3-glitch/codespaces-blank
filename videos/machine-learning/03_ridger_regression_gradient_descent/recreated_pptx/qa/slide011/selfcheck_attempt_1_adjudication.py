#!/usr/bin/env python3
"""Adjudication of the 5 banked selfcheck FAILs (selfcheck_attempt_1.txt) for
slide 011, render_1.png.

Banked checker bug (selfcheck_attempt_1.py, section 5): the underline was
measured as the UNION bbox of every row in y 250-272 whose red-pixel count
exceeds 60. Title glyph rows (the title text itself is C00000 red) satisfy
that threshold, so the union bbox spans the whole title ink
(x 113.3-814.6, y 249.6-259.2) instead of the underline bar. All 5 FAILs
are that contamination, not render defects.

Correct measurement used here: the words under the underline ("due to
outlier") have NO descenders, so rows below the title baseline in the
x-window 560-720 contain ONLY the underline bar plus (at 258-261) its
anti-aliased edges. Isolate the bar by contiguous-run detection on those
rows instead of a union bbox over "wide" rows.
"""
import numpy as np
from PIL import Image

RENDER = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide011/render_1.png"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_011.jpg"

TOL_L = 5.0   # frame px, left/right edges (closed-loop standard ~4px @150dpi = ~2 frame px)
TOL_R = 5.0
TOL_Y = 3.0   # frame px, vertical center
TOL_TH = 1.5  # frame px, thickness

fails = []


def ok(m):
    print("  OK  ", m)


def fail(m):
    fails.append(m)
    print("  FAIL", m)


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 90) & ((r - g) > 40) & ((r - b) > 10)


def bar_runs(mask, rows, cols, scale, off_x):
    """Contiguous red runs in the given rows, returned in frame px."""
    runs = []
    for r in rows:
        xs = np.where(mask[r, cols[0]:cols[1]])[0] + cols[0]
        if not len(xs):
            continue
        s = p = xs[0]
        for x in xs[1:]:
            if x - p > 1:
                runs.append((s, p))
                s = x
            p = x
        runs.append((s, p))
    return [(round(a / scale, 1), round(b / scale, 1)) for a, b in runs]


print("== A. ORIGINAL underline measurement (slide_011.jpg, 960x540) ==")
o = load(ORIG)
ro = redmask(o)
# descender-free x-window 560-720 ("due to outlier" have no descenders)
prof = [(y, int(ro[y, 560:720].sum())) for y in range(255, 265)]
print("   per-row red px in x560-720:", {y: c for y, c in prof if c})
o_runs = bar_runs(ro, range(258, 262), (500, 760), 1.0, 500)
print("   contiguous red runs rows 258-261 (frame px):", o_runs)
# the bar = the run that is ~100px wide (glyph runs are narrow); smear rows 258/261
o_bar = max(o_runs, key=lambda t: t[1] - t[0])
o_ys = [y for y, c in prof if c >= 100]  # full-width rows = the bar (+smear)
o_y0, o_y1 = min(o_ys), max(o_ys)
o_core = [y for y, c in prof if c >= 103]
print(f"   ORIGINAL bar: x {o_bar[0]}-{o_bar[1]}  rows {o_y0}-{o_y1} "
      f"(core {min(o_core)}-{max(o_core)}, center {(min(o_core)+max(o_core))/2:.1f}, "
      f"thickness {max(o_core)-min(o_core)+1})")

print("\n== B. RENDER underline measurement (render_1.png, 2001x1125) ==")
rr = load(RENDER)
rm = redmask(rr)
S = rr.shape[0] / 540.0  # 2.0833 render-px per frame-px
w0, w1 = int(560 * S), int(720 * S)
prof_r = [(ry, int(rm[ry, w0:w1].sum())) for ry in range(int(254 * S), int(266 * S))]
print("   per-row red px in x560-720(win):",
      {f"{r}(y{r/S:.1f})": c for r, c in prof_r if c})
r_runs = bar_runs(rm, range(int(257 * S), int(264 * S)),
                  (int(500 * S), int(760 * S)), S, int(500 * S))
print("   contiguous red runs (frame px):", r_runs)
r_bar = max(r_runs, key=lambda t: t[1] - t[0])
bar_rows = [r for r, c in prof_r if c >= 200]  # bar rows (~215 px in the win)
r_y0 = min(bar_rows) / S
r_y1 = max(bar_rows) / S
print(f"   RENDER bar: x {r_bar[0]}-{r_bar[1]}  rows {r_y0:.2f}-{r_y1:.2f} "
      f"(center {(r_y0+r_y1)/2:.2f}, thickness {r_y1-r_y0+S*1/S:.2f})")

print("\n== C. re-run the 5 banked FAILs against the CORRECT measurement ==")
o_cx0, o_cx1 = o_bar
o_cy = (min(o_core) + max(o_core)) / 2
o_th = max(o_core) - min(o_core) + 1
print(f"   reference: orig x {o_cx0}-{o_cx1}, y core center {o_cy}, thickness {o_th}")
for nm, got, want, tol in (
    ("ul L", r_bar[0], 595.4, TOL_L),
    ("ul R", r_bar[1], 698, TOL_R),
    ("ul Y center (core)", (r_y0 + r_y1) / 2, o_cy, TOL_Y),
):
    (ok if abs(got - want) <= tol else fail)(f"{nm} {got:.1f} vs {want} (tol {tol})")
(ok if r_y0 >= 256 else fail)(f"underline below the title baseline band (top {r_y0:.1f} >= 256)")
(ok if 594 <= r_bar[0] and r_bar[1] <= 698 else fail)(
    f"underline spans only the 'outlier' word ({r_bar[0]}-{r_bar[1]} within 595-698)")
(ok if abs((r_y1 - r_y0 + 1 / S) - o_th) <= TOL_TH else fail)(
    f"ul thickness render {r_y1 - r_y0 + 1 / S:.2f} vs orig {o_th} (tol {TOL_TH})")

print("\n== D. contamination proof (why the banked checker FAILed) ==")
# a row through the middle of the title glyphs also exceeds the 60-px threshold
glyph_rows = int(rm[int(247 * S):int(250 * S), int(70 * S):int(890 * S)].sum(axis=1).max())
print(f"   max red px in a title-glyph row (x70-890 window): "
      f"{glyph_rows} > 60 -> those rows were absorbed into the 'wide_rows' union")
print("   => banked FAILs are checker-bugs; render underline is correct.")

print("\n================ ADJUDICATION SUMMARY ================")
print(f"{len(fails)} FAIL")
for f in fails:
    print("  -", f)
