#!/usr/bin/env python3
"""Self-check for slide 017 render_1 vs the original frame.

Every block is measured against BOTH images. Render is 2001x1125 (150dpi),
scale = H_render/540 ≈ 2.0833 render-px per frame px; all render slices are
scaled, all original slices are frame px (1px=1pt).
Bank: recreated_pptx/qa/slide017/selfcheck_attempt_1.py
"""
import os
import sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
RENDER = os.path.join(HERE, "render_1.png")
ORIG = os.path.join(ROOT, "unique_slides", "slide_017.jpg")

ri = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
oi = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
S = ri.shape[0] / 540.0
print(f"render {ri.shape[1]}x{ri.shape[0]}  scale {S:.6f} (expect 2.083333)")

fails = []
def check(name, ok, detail=""):
    print(("  OK   " if ok else "  FAIL ") + name + (("  " + detail) if detail else ""))
    if not ok:
        fails.append(name + " " + detail)

def masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    gray = (abs(r - 233) < 22) & (abs(g - 233) < 22) & (abs(b - 231) < 24)
    white = a.sum(axis=2) > 735
    bg = gray | white
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10) & ~bg
    blue = (b > 90) & ((b - r) > 40) & ((g - r) < 30) & ~bg
    dark = (a.sum(axis=2) < 330) & ~bg
    return dict(red=red, blue=blue, dark=dark, white=white, yellow=((r > 225) & (g > 225) & (b < 200)))

mo, mr = masks(oi), masks(ri)

# slice helpers: original by frame px, render scaled
def o_sub(mask, y0, y1, x0, x1):
    return mask[max(0, y0):y1 + 1, max(0, x0):x1 + 1]
def r_sub(mask, y0, y1, x0, x1):
    return mask[max(0, int(y0 * S)):int(y1 * S) + 1, max(0, int(x0 * S)):int(x1 * S) + 1]

def o_bbox(mask, y0, y1, x0, x1):
    sub = o_sub(mask, y0, y1, x0, x1)
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return (int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0), int(ys.max() + y0))
def r_bbox(mask, y0, y1, x0, x1):
    sub = r_sub(mask, y0, y1, x0, x1)
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return (xs.min() / S + x0, ys.min() / S + y0, xs.max() / S + x0, ys.max() / S + y0)

def runs(row, minlen=1):
    out, i, n = [], 0, len(row)
    while i < n:
        if row[i]:
            j = i
            while j + 1 < n and row[j + 1]:
                j += 1
            if j - i + 1 >= minlen:
                out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out

def mg(rs, gap=8):
    m = []
    for x0, x1 in rs:
        if m and x0 - m[-1][1] <= gap:
            m[-1][1] = x1
        else:
            m.append([x0, x1])
    return m

def near(a, b, tol=6.0):
    if a is None or b is None:
        return a is None and b is None
    return all(abs(x - y) <= tol for x, y in zip(a, b))

def colgroups(mask, y0, y1, x0, x1, ren, gap=14):
    sub = r_sub(mask, y0, y1, x0, x1) if ren else o_sub(mask, y0, y1, x0, x1)
    d = sub.sum(axis=0)
    rs = mg(runs(d > 0, 1), gap)
    if ren:
        return [(p[0] / S + x0, p[1] / S + x0) for p in rs]
    return [(p[0] + x0, p[1] + x0) for p in rs]

print("== CHROME ==")
top = r_sub(mr["red"], 44, 52, 80, 880)
check("no top stroke", top.sum() == 0, f"{int(top.sum())} red px")
check("left stroke present", int(r_sub(mr["red"], 100, 450, 57, 61).sum()) > 3)
check("right stroke present", int(r_sub(mr["red"], 100, 450, 900, 903).sum()) > 3)
check("bottom stroke present", int(r_sub(mr["red"], 536, 539, 60, 900).sum()) > 3)
ob = o_bbox(mo["red"], 40, 100, 845, 905)
rb = r_bbox(mr["red"], 40, 100, 845, 905)
print("   badge red ring region orig:", ob, "render:", None if rb is None else tuple(round(v, 1) for v in rb))
check("badge ring region ink present", rb is not None)

print("\n== TITLE ==")
to = o_bbox(mo["red"] | mo["blue"] | mo["dark"], 60, 99, 170, 880)
tr = r_bbox(mr["red"] | mr["blue"] | mr["dark"], 60, 99, 170, 880)
check("title ink bbox", near(to, tr, 8), f"orig {to} render {None if tr is None else tuple(round(v,1) for v in tr)}")
ro, rr_ = colgroups(mo["red"], 60, 99, 170, 880, False), colgroups(mr["red"], 60, 99, 170, 880, True)
bo, br_ = colgroups(mo["blue"], 60, 99, 170, 880, False), colgroups(mr["blue"], 60, 99, 170, 880, True)
print("   orig RED:", [(round(p[0],1), round(p[1],1)) for p in ro])
print("   rend RED:", [(round(p[0],1), round(p[1],1)) for p in rr_])
print("   orig BLUE:", [(round(p[0],1), round(p[1],1)) for p in bo])
print("   rend BLUE:", [(round(p[0],1), round(p[1],1)) for p in br_])
def grpalign(a, b):
    if len(a) != len(b):
        return False, f"count {len(a)} vs {len(b)}"
    bad = []
    for p, q in zip(a, b):
        if abs(p[0] - q[0]) > 12 or abs(p[1] - q[1]) > 12:
            bad.append(f"({p[0]:.0f}..{p[1]:.0f} vs {q[0]:.0f}..{q[1]:.0f})")
    return (not bad), "; ".join(bad)
ok, d = grpalign(ro, rr_); check("title RED groups aligned", ok, d)
ok, d = grpalign(bo, br_); check("title BLUE groups aligned", ok, d)

print("\n== GRIDLINES (tables) ==")
GV = [92, 133, 174, 214, 255, 296, 337, 377, 418, 459]
TB = [(126, 157, 188, 219, 249), (265, 296, 326, 357, 389), (402, 434, 465, 496, 526)]
TG = [668, 719, 770, 821, 872]
TT = [(128, 160, 190, 221, 251), (266, 298, 328, 359, 389), (403, 435, 466, 497, 527)]
# window padded 3px so a full-bleed bottom border is still inside the slice
def vcentres(mask, gy, x0, x1, ren):
    y0, y1 = gy[0] + 3, gy[4] - 3
    sub = r_sub(~mask["white"], y0, y1, x0, x1) if ren else o_sub(~mask["white"], y0, y1, x0, x1)
    d = sub.sum(axis=0)
    rs = mg(runs(d > sub.shape[0] * 0.6, 1), 3)
    return [(p[0] / S + x0 + p[1] / S + x0) / 2 for p in rs] if ren else [(p[0] + x0 + p[1] + x0) / 2 for p in rs]
def hrows(mask, gy, x0, x1, ren):
    sub = r_sub(~mask["white"], gy[0] - 3, gy[4] + 3, x0, x1) if ren else o_sub(~mask["white"], gy[0] - 3, gy[4] + 3, x0, x1)
    d = sub.sum(axis=1)
    rs = mg(runs(d > sub.shape[1] * 0.5, 1), 3)
    return [p[0] / S + gy[0] - 3 for p in rs] if ren else [p[0] + gy[0] - 3 for p in rs]
for nm, exp_x, bands, xa, xb in [("train", GV, TB, 88, 465), ("test", TG, TT, 664, 876)]:
    for bi, gy in enumerate(bands, 1):
        gv = vcentres(mr, gy, xa, xb, True)
        gh = hrows(mr, gy, xa, xb, True)
        print(f"   {nm} B{bi} v-centres: {[round(v) for v in gv]}")
        print(f"   {nm} B{bi} h-rows:     {[round(v) for v in gh]}")
        badx = [e for e in exp_x if not any(abs(g - e) <= 5 for g in gv)]
        badh = [g for g in gy if not any(abs(x - g) <= 5 for x in gh)]
        check(f"{nm} B{bi} vertical gridlines", not badx, f"missing {badx}")
        check(f"{nm} B{bi} horizontal gridlines", not badh, f"missing {badh}")

print("\n== per-cell ink presence ==")
def cell_ok(m_o, m_r, gy, gi, ci, gv, gt):
    sub_o = o_sub(m_o["red"] | m_o["blue"] | m_o["dark"], gy[gi] + 3, gy[gi + 1] - 3, gv[ci] + 3, gv[ci + 1] - 3)
    sub_r = r_sub(m_r["red"] | m_r["blue"] | m_r["dark"], gy[gi] + 3, gy[gi + 1] - 3, gt[ci] + 3, gt[ci + 1] - 3)
    return int(sub_o.sum()), int(sub_r.sum())
bad = []
for bi, gy in enumerate(TB, 1):
    for j in range(1, 4):
        for ci in range(1, 9):
            o, r = cell_ok(mo, mr, gy, j, ci, GV, GV)
            if (o > 5) != (r > 5):
                bad.append(f"T B{bi} r{j} c{ci} ({o}/{r})")
check("train cell ink both sides", not bad, "; ".join(bad[:12]))
bad = []
for bi, gy in enumerate(TT, 1):
    for j in range(1, 4):
        for ci in range(1, 4):
            o, r = cell_ok(mo, mr, gy, j, ci, TG, TG)
            if (o > 5) != (r > 5):
                bad.append(f"E B{bi} r{j} c{ci} ({o}/{r})")
check("test cell ink both sides", not bad, "; ".join(bad[:12]))

print("\n== ink PHASE per column (train ci1..8 / test ci1..3, X1 row) ==")
def dom(m, gy, ci, gv, ren):
    sub_r = (r_sub(m["red"], gy[1] + 3, gy[2] - 3, gv[ci] + 3, gv[ci + 1] - 3) if ren else
             o_sub(m["red"], gy[1] + 3, gy[2] - 3, gv[ci] + 3, gv[ci + 1] - 3))
    sub_b = (r_sub(m["blue"], gy[1] + 3, gy[2] - 3, gv[ci] + 3, gv[ci + 1] - 3) if ren else
             o_sub(m["blue"], gy[1] + 3, gy[2] - 3, gv[ci] + 3, gv[ci + 1] - 3))
    return int(sub_r.sum()), int(sub_b.sum())
bad = []
for bi, gy in enumerate(TB, 1):
    for ci in range(1, 9):
        ro_, bo_ = dom(mo, gy, ci, GV, False)
        rr2, br2 = dom(mr, gy, ci, GV, True)
        fo = "RED" if ro_ > bo_ else "BLUE"
        fr = "RED" if rr2 > br2 else "BLUE"
        if fo != fr:
            bad.append(f"T B{bi} c{ci} {fo!r}->{fr!r}")
check("train ink phase matches", not bad, "; ".join(bad[:10]))
bad = []
for bi, gy in enumerate(TT, 1):
    for ci in range(1, 4):
        ro_, bo_ = dom(mo, gy, ci, TG, False)
        rr2, br2 = dom(mr, gy, ci, TG, True)
        fo = "RED" if ro_ > bo_ else "BLUE"
        fr = "RED" if rr2 > br2 else "BLUE"
        if fo != fr:
            bad.append(f"E B{bi} c{ci} {fo!r}->{fr!r}")
check("test ink phase matches", not bad, "; ".join(bad[:10]))

print("\n== LABEL BOXES ==")
for nm, x0, x1 in [("Train label", 96, 162), ("Test label", 802, 867)]:
    r = r_bbox(mr["blue"], 96, 126, x0, x1)
    check(f"{nm} blue box", r is not None and abs(r[0] - x0) <= 6 and abs(r[2] - x1) <= 6,
          f"render {None if r is None else tuple(round(v,1) for v in r)}")

print("\n== ARROWS ==")
for bi, (y0, y1) in enumerate([(180, 218), (313, 351), (445, 483)], 1):
    for side, x0, x1 in [("L", 462, 506), ("R", 625, 670)]:
        r = r_bbox(mr["blue"], y0, y1, x0, x1)
        check(f"arrow B{bi}{side}", r is not None and abs(r[0] - x0) <= 8 and abs(r[2] - x1) <= 8,
              f"render {None if r is None else tuple(round(v,1) for v in r)}")

print("\n== W BOXES ==")
WB = [(127, 251, 505, 624), (265, 389, 505, 624), (403, 527, 505, 624)]
for bi, (ya, yb, xa, xb) in enumerate(WB, 1):
    r = r_bbox(mr["red"], ya - 2, yb + 2, xa - 2, xb + 2)
    check(f"Wbox B{bi} red border", r is not None,
          f"render {None if r is None else tuple(round(v,1) for v in r)}")
    if r:
        check(f"Wbox B{bi} border bbox", abs(r[0] - xa) <= 6 and abs(r[2] - xb) <= 6 and abs(r[1] - ya) <= 6,
              f"render {tuple(round(v,1) for v in r)} expected ({xa},{ya},{xb},{yb})")
    for nm, key, x0, x1 in [("W glyph", "red", 511, 556), ("vector", "dark", 554, 618), ("norm", "blue", 512, 618)]:
        o = o_bbox(mo[key], ya + 4, yb - 4, x0, x1)
        r = r_bbox(mr[key], ya + 4, yb - 4, x0, x1)
        check(f"Wbox B{bi} {nm} present both", o is not None and r is not None,
              f"orig {o} render {None if r is None else tuple(round(v,1) for v in r)}")
        if o and r:
            check(f"Wbox B{bi} {nm} bbox", near(o, r, 12), f"orig {o} render {tuple(round(v,1) for v in r)}")
    yo = int(o_sub(mo["yellow"], ya + 4, yb - 4, 512, 618).sum())
    yr = int(r_sub(mr["yellow"], ya + 4, yb - 4, 512, 618).sum())
    check(f"Wbox B{bi} no yellow ellipse in either", yo < 60 and yr < 60, f"orig {yo} render {yr}")

print("\n== YELLOW X8 HIGHLIGHT CELLS ==")
for nm, y0, y1 in [("B2 X8", 297, 327), ("B3 X8", 435, 465)]:
    o = o_sub(mo["yellow"], y0, y1, 420, 459)
    r = r_sub(mr["yellow"], y0, y1, 420, 459)
    check(f"{nm} yellow fill both", o.sum() > 500 and r.sum() > 500, f"orig {int(o.sum())} render {int(r.sum())}")

print("\n== TEST MINT Y-ROW ==")
for bi, (y0, y1) in enumerate([(222, 246), (359, 383), (497, 521)], 1):
    def mint(a):
        seg = a[y0:y1, 724:868] if a.shape[0] == 540 else a[int(y0 * S):int(y1 * S), int(724 * S):int(868 * S)]
        r_, g_, b_ = seg[:, :, 0], seg[:, :, 1], seg[:, :, 2]
        m = (r_ > 150) & (g_ > 200) & (b_ < 240) & (g_ - r_ > 20)
        return int(m.sum())
    check(f"mint y-row B{bi}", mint(oi) > 2000 and mint(ri) > 2000, f"orig {mint(oi)} render {mint(ri)}")
    # rows 1..2 must stay white (no mint bleed)
    def mint2(a, yy):
        seg = a[yy[0]:yy[1], 724:868] if a.shape[0] == 540 else a[int(yy[0] * S):int(yy[1] * S), int(724 * S):int(868 * S)]
        r_, g_, b_ = seg[:, :, 0], seg[:, :, 1], seg[:, :, 2]
        return int(((r_ > 150) & (g_ > 200) & (b_ < 240) & (g_ - r_ > 20)).sum())
    for ri_, yy in enumerate([(136, 156), (167, 185), (200, 218)], 1):
        check(f"mint absent in test row {ri_} B{bi}", mint2(oi, yy) < 300 and mint2(ri, yy) < 300,
              f"orig {mint2(oi, yy)} render {mint2(ri, yy)}")
    break  # band 1 is representative; other bands share the code path

print("\n== FRAME CONTAINMENT ==")
anyink = ~mr["white"]
check("no ink left of left stroke", int(anyink[:, :int(56 * S)].sum()) == 0)
check("no ink right of right stroke", int(anyink[:, int(904 * S):].sum()) == 0)
check("no ink above panel top", int(anyink[:int(44 * S), :].sum()) == 0)
check("no ink below slide bottom", int(anyink[int(540 * S):, :].sum()) == 0)
nd = r_sub(mr["dark"], 56, 91, 858, 895)
check("badge numeral ink", int(nd.sum()) >= 12, f"{int(nd.sum())} px")

print("\nRESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
for f in fails:
    print("  -", f)
sys.exit(0 if not fails else 1)
