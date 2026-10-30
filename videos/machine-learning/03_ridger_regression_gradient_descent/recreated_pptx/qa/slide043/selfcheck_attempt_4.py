#!/usr/bin/env python3
"""MANDATORY pre-judge selfcheck for slide 043 — attempt 4 render.

Verifies the four PIL-measured fixes against unique_slides/slide_043.jpg:
  FIX 1 top-left class row colour (C1 red / C2 blue)
  FIX 2 class-check matrix: ONE tall paren pair per Z1 column spanning both entries
  FIX 3 aug heading containment inside the box
  FIX 4 legend line colour (C1 red / C2 blue / Zero green / rest black)
Plus regressions: equation bands, frame containment, table cells.
Run: python3 selfcheck_attempt_4.py
"""
import numpy as np
from PIL import Image

V = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide043"
O = np.asarray(Image.open(f"{V}/unique_slides/slide_043.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(f"{Q}/render_4.png").convert("RGB")).astype(int)
SX, SY = R.shape[1] / 960.0, R.shape[0] / 540.0
fails = []


def ink(a):
    lum = a.sum(2) / 3.0
    sat = a.max(2) - a.min(2)
    return (lum < 175) | (sat > 45)


def rr(x0, y0, x1, y1):
    return R[int(y0 * SY):int(y1 * SY), int(x0 * SX):int(x1 * SX)]


def rb(x0, y0, x1, y1):
    m = ink(rr(x0, y0, x1, y1))
    ys, xs = np.where(m)
    return None if len(xs) == 0 else (round(xs.min() / SX + x0, 1), round(ys.min() / SY + y0, 1),
                                     round(xs.max() / SX + x0, 1), round(ys.max() / SY + y0, 1))


def ob(x0, y0, x1, y1):
    m = ink(O[y0:y1, x0:x1])
    ys, xs = np.where(m)
    return None if len(xs) == 0 else (int(xs.min()) + x0, int(ys.min()) + y0,
                                      int(xs.max()) + x0, int(ys.max()) + y0)


def col(z):
    return (int(((z[:, :, 0] > 90) & (z[:, :, 0] - z[:, :, 1] > 40)).sum()),
            int(((z[:, :, 1] > 90) & (z[:, :, 1] - z[:, :, 0] > 40) & (z[:, :, 1] - z[:, :, 2] > 40)).sum()),
            int(((z[:, :, 2] > 90) & (z[:, :, 2] - z[:, :, 0] > 40)).sum()))


# ---- FIX 1: top-left class row ----
print("FIX 1 — top-left class row colour (frame y108..126)")
ro, go, bo = col(O[108:126, 80:140]); rr_, gr_, br_ = col(rr(80, 108, 140, 126))
print(f"   ORIG x1..x3 (C1): red={ro} blue={bo}   REND: red={rr_} blue={br_}")
ro2, go2, bo2 = col(O[108:126, 140:220]); rr2, gr2, br2 = col(rr(140, 108, 220, 126))
print(f"   ORIG x4..x6 (C2): red={ro2} blue={bo2}   REND: red={rr2} blue={br2}")
ok = rr_ > 20 and rr_ > br_ and br2 > 20 and br2 > rr2
print(f"   -> {'PASS' if ok else 'FAIL'}")
if not ok:
    fails.append("class-row colour")

# ---- FIX 2: matrix delimiters ----
print("\nFIX 2 — class-check matrix parens span both entries (frame y78..112)")
for cx, nm in [(605, "col1"), (628, "col2"), (651, "col3")]:
    o = ob(cx - 16, 78, cx + 16, 112)
    r = rb(cx - 16, 78, cx + 16, 112)
    span = (r[3] - r[1]) if r else 0
    ok = r and span >= 22
    print(f"   {nm}: ORIG {o} | REND {r} span={span if r else 0:.1f} -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        fails.append(f"matrix {nm}")

# ---- FIX 3: aug heading containment ----
print("\nFIX 3 — aug heading inside box (box right edge 246)")
h = rb(74, 143, 250, 162)
print(f"   REND {h} | ORIG {ob(74, 143, 250, 162)}")
ok = h and h[2] <= 245
print(f"   -> {'PASS' if ok else 'FAIL'}")
if not ok:
    fails.append("aug heading overflow")

# ---- FIX 4: legend colours ----
print("\nFIX 4 — legend line (frame y104..122); original runs red x239..253, blue x312..326, green x395..423")
for nm, (a, b) in [("C1", (239, 252)), ("C2", (312, 325)), ("Zero", (395, 423))]:
    ro_, go_, bo_ = col(O[104:122, a:b])
    rr3, gr3, br3 = col(rr(a, 104, b, 122))
    print(f"   {nm} x{a}..{b}: ORIG r/g/b={ro_}/{go_}/{bo_}  REND={rr3}/{gr3}/{br3}")
ok = (col(rr(239, 104, 252, 122))[0] > 10 and col(rr(312, 104, 325, 122))[2] > 10
      and col(rr(395, 104, 423, 122))[1] > 10 and col(rr(256, 104, 310, 122))[0] < 15)
print(f"   -> {'PASS' if ok else 'FAIL'}")
if not ok:
    fails.append("legend colour")

# ---- regressions ----
print("\nREGRESSION — equation bands")
bands = [(150, 200), (215, 265), (278, 325), (345, 395), (411, 456), (477, 522)]
for i, (y0, y1) in enumerate(bands):
    d, w = rb(280, y0, 478, y1), rb(616, y0, 812, y1)
    pr = int(ink(rr(280, y0, 478, y1)).sum())
    ok = d and w and pr > 0
    print(f"   band {i+1}: d-ink={d} w-ink={w} px={pr} -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        fails.append(f"eq band {i+1}")

print("\nREGRESSION — frame containment + table cells")
c = rb(60, 47, 900, 537)
print(f"   content ink bbox {c} (must be inside x57..902 y45..539)")
if c and (c[0] < 57 or c[2] > 902 or c[1] < 45 or c[3] > 539):
    fails.append("frame containment")
    print("   -> FAIL")
else:
    print("   -> PASS")
cols = [94, 117, 139, 161, 184, 206]
missing = [(ri, cx) for ri, y in enumerate((69, 84, 98, 118)) for cx in cols if not rb(cx - 9, y - 7, cx + 9, y + 8)]
print(f"   top-left table cells missing: {missing if missing else 'none (24/24 inked)'}")
if missing:
    fails.append("table cells")

print()
print("RESULT:", "ALL PASS" if not fails else f"FAILS: {fails}")
