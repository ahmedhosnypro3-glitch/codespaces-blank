#!/usr/bin/env python3
"""Verify the 3 fixes in render_3.png against unique_slides/slide_043.jpg."""
import numpy as np
from PIL import Image

V = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
O = np.asarray(Image.open(f"{V}/unique_slides/slide_043.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide043/render_3.png").convert("RGB")).astype(int)
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


# ---- FIX 1: class-row colour ----
print("FIX 1 — class-row colour")
for lbl, zone in [("ORIG x1..x3", O[108:126, 80:140]), ("REND x1..x3", rr(80, 108, 140, 126)),
                  ("ORIG x4..x6", O[108:126, 140:220]), ("REND x4..x6", rr(140, 108, 220, 126))]:
    red = int(((zone[:, :, 0] > 90) & (zone[:, :, 0] - zone[:, :, 1] > 40)).sum())
    blue = int(((zone[:, :, 2] > 90) & (zone[:, :, 2] - zone[:, :, 0] > 40)).sum())
    print(f"   {lbl}: red={red} blue={blue}")
r1 = int(((rr(80, 108, 140, 126)[:, :, 0] > 90) & (rr(80, 108, 140, 126)[:, :, 0] - rr(80, 108, 140, 126)[:, :, 1] > 40)).sum())
b1 = int(((rr(140, 108, 220, 126)[:, :, 2] > 90) & (rr(140, 108, 220, 126)[:, :, 2] - rr(140, 108, 220, 126)[:, :, 0] > 40)).sum())
ok1 = r1 > 20 and b1 > 20
print(f"   -> {'PASS' if ok1 else 'FAIL'} (render C1 red={r1}, C2 blue={b1})")
if not ok1:
    fails.append("class-row colour")

# ---- FIX 2: matrix delimiters span both rows ----
print("\nFIX 2 — class-check matrix parens span both entries")
for cx, nm in [(605, "col1"), (628, "col2"), (651, "col3")]:
    o = ob(cx - 16, 78, cx + 16, 112)
    r = rb(cx - 16, 78, cx + 16, 112)
    print(f"   {nm}: ORIG ink bbox {o}  |  REND {r}")
    # the paren span must be ~ the whole two-entry stack (>=24 frame px tall)
    if r is None or (r[3] - r[1]) < 22:
        fails.append(f"matrix {nm} delimiter span")
        print(f"   -> FAIL span {(r[3]-r[1]) if r else 0}")
    else:
        print(f"   -> PASS span {round(r[3]-r[1],1)} frame px")
# count distinct horizontal runs of the paren strokes
for cx, nm in [(605, "col1")]:
    m = ink(rr(cx - 16, 78, cx + 16, 112))
    rows = [j for j in range(m.shape[0]) if m[j].sum() > 0]
    print(f"   {nm} REND rows with ink: {len(rows)} of 34 (ORIG: 28)")
    if len(rows) < 20:
        fails.append(f"matrix {nm} continuity")

# ---- FIX 3: aug heading inside box ----
print("\nFIX 3 — aug heading containment")
h = rb(74, 143, 250, 162)
print(f"   REND heading ink bbox: {h}  (box right edge 246)")
print(f"   ORIG heading ink bbox: {ob(74, 143, 250, 162)}")
if h is None or h[2] > 245:
    fails.append("aug heading overflow")
    print("   -> FAIL")
else:
    print("   -> PASS")

# ---- regression: equation bands still inked ----
print("\nREGRESSION — equation bands + overall containment")
bands = [(150, 200), (215, 265), (278, 325), (345, 395), (411, 456), (477, 522)]
for i, (y0, y1) in enumerate(bands):
    d = rb(280, y0, 478, y1)
    w = rb(616, y0, 812, y1)
    pr = int(ink(rr(280, y0, 478, y1)).sum())
    ok = d and w and pr > 0
    print(f"   band {i+1}: d={d} w={w} render_ink={pr} -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        fails.append(f"eq band {i+1}")
c = rb(60, 47, 900, 537)
print(f"   content ink bbox: {c} (must be inside x57..902 y45..539)")
if c and (c[0] < 57 or c[2] > 902 or c[1] < 45 or c[3] > 539):
    fails.append("frame containment")
    print("   -> FAIL")
else:
    print("   -> PASS")

# ---- table cells ----
print("\nREGRESSION — top-left table cells")
cols = [94, 117, 139, 161, 184, 206]
missing = [(ri, cx) for ri, y in enumerate((69, 84, 98, 118)) for cx in cols if not rb(cx - 9, y - 7, cx + 9, y + 8)]
print(f"   missing cells: {missing if missing else 'none (24/24 inked)'}")
if missing:
    fails.append("table cells")

print()
print("RESULT:", "ALL PASS" if not fails else f"FAILS: {fails}")
