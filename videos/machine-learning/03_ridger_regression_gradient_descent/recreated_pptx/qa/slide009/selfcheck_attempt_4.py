#!/usr/bin/env python3
"""Slide 009 self-check attempt 3 (re-run on render_2 after fixes) — closed-loop PIL verification of the 150dpi render
against the banked frame measurements (unique_slides/slide_009.jpg).

Attempt 2 (49/52) cleared the 9 attempt-1 checker bugs. Its 3 remaining FIX
lines were again all CHECKER bugs, each diagnosed with a banked probe:

  10. "LEFT x-axis shaft": the shaft window was x200..860, which straddles both
      panels, so w[1]=848.7 was the RIGHT panel's arrowhead apex, not the LEFT
      one. Fixed: per-panel windows (LEFT x124..440, RIGHT x538..856).
  11. "L BIG disc fill area": I compared a RENDER-pixel count (2112) against a
      FRAME-px^2 area (pi*12.25^2 = 471). The render is 2.0844x2.0833, so the
      conversion is 2112/(SX*SY) = 486.4 frame px^2 vs 471.4 expected (3.2%
      high, inside AA slack). Fixed: convert units.
  12. "no ink between panel bottom and captions": 126 px, and the probe showed
      rows 473..486 are PERFECTLY clean (0 ink px, uniformly panel gray). The
      126 px were the house chrome's LEFT (x57..59) and RIGHT (x900..902) red
      vertical strokes, which span the whole panel height by decree, times 21
      window rows = 63+63 = 126 exactly. Fixed: restrict the window to x60..900.

Attempt 1 returned 40/49 with 9 FIX lines, every one diagnosed as a CHECKER bug
too. The attempt-1 defects and their repairs:

  1. NAVY/BLUE mask collision. Attempt 1's BLUE =
     (b-r>30)&(b-g>30)&(b<260) also matched the navy 000080 panel borders
     (core (0,0,128), AA (154,154,202) and (70,70,159) on the left border;
     (124,124,183) on the RIGHT panel's left border). That contaminated both
     fitted-line bboxes and both LSQ fits. Measured fix: BLUE now requires
     b>200, so navy (b<=190) and every AA neighbour are excluded.
     Re-measured after the fix: LEFT line x140.8..433.4 y198.2..352.8
     (want 141..433 / 198..352); RIGHT line x554.8..849.4 y246.2..389.8
     (want 555..849 / 247..389) — both exact.
  2. Whole-slide windows where per-panel windows were needed. Attempt 1 used
     x100..880 for both fitted lines, so the LEFT span ran into the RIGHT
     panel's border. Now LEFT x100..460, RIGHT x500..862.
  3. AXES tip/along mislabels. For the x-axis shafts the bbox's max-x is the
     arrowhead APEX (LEFT 436 / RIGHT 849), not the axis origin; the RIGHT
     y-axis base is y434 (it meets the x-axis), not y437. Values corrected.
  4. L BIG disc measured as disc-union-diagonal. The diagonal (199,198)->(232,241)
     ends INSIDE the disc, so the attempt-1 window cx+-24.5 read the union
     (d 36.0, centre 228.1,234.5). Now measured by two clean scans that avoid
     the diagonal entirely: a row scan at y=244 (4px below the diagonal's end)
     and a column scan at x=240 (8px right of the diagonal's end).
  5. L diagonal measured as diagonal-union-disc. Now an isolated window
     x196..220, y196..230 that contains only the diagonal (the disc's leftmost
     point is x220.25 at y=241, outside that window), plus an LSQ slope test.
  6. LCAP2/RCAP2 windows (y502..524) caught line 1's descenders (render
     y500.6..503.0). Re-measured caption inks: line1 y488.2..503.0 (orig
     488..504), line2 y507.4..518.9 (orig 507..520). Windows tightened to
     y505..522.
  7. INK predicate flagged the panel-gray background. The gap x466..485 is
     uniformly (233,233,231) = E9E9E7, which satisfies `sum<700`, so every
     one of those 28082 px was counted as "ink". INK now excludes pixels
     within 12 of the panel gray as well as within 40 of white.

Checks (each mirror-measured on the original in the probe bank):
  A. navy chart-panel borders (x span + y span, 2 panels)
  B. grid line positions (sampled)
  C. red axes: shafts + arrowhead apexes
  D. blue fitted lines: span + LSQ endpoints (per panel)
  E. orange data points: 24 centroid presence
  F. red marks: 4 small discs + LEFT big disc (row/col scans) + 2 diagonals
  G. annotation boxes: 4 border edges each
  H. equation ink bbox vs target
  I. captions: ink bbox per line + red keyword split
  J. frame containment (no ink outside the house panel; no top stroke)
"""
import numpy as np
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORIG = os.path.join(DECK, "unique_slides", "slide_009.jpg")
REND = os.path.join(HERE, "render_2.png")

ren = np.asarray(Image.open(REND).convert("RGB")).astype(int)
H, W, _ = ren.shape
SY, SX = H / 540.0, W / 960.0
print("render %dx%d   scale x %.5f y %.5f" % (W, H, SX, SY))

rR, rG, rB = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
NAVY = (rB - rR > 30) & (rB - rG > 30) & (rB < 190)          # 000080 family
RED = (rR > 100) & (rG < 100) & ((rR - rG) > 60) & ((rR - rB) > 60)  # C00000 family
# FIX 1: b>200 excludes navy (core b=128, AA b=159/183/202)
BLUE = (rB > 200) & (rB - rR > 60) & (rB - rG > 60)          # 0000FF family
ORANGE = (rR > 200) & (rG > 70) & (rG < 190) & (rB < 90) & ((rR - rG) > 60)
# FIX 7: exclude panel gray E9E9E7 (233,233,231) as well as white
INK = (np.abs(ren - 255).max(axis=2) > 40) & \
      (np.abs(ren - np.array([233, 233, 231])).max(axis=2) > 12)

results = []
def chk(name, ok, detail=""):
    results.append((name, ok))
    print("  [%s] %-34s %s" % ("OK " if ok else "FIX", name, detail))

def f2r_y(v): return v * SY
def f2r_x(v): return v * SX
def r2f_y(v): return v / SY
def r2f_x(v): return v / SX

def bbox(mask, fx0, fx1, fy0, fy1):
    """Ink bbox inside a FRAME window, returned in FRAME px."""
    y0, y1 = int(round(fy0 * SY)), int(round(fy1 * SY))
    x0, x1 = int(round(fx0 * SX)), int(round(fx1 * SX))
    y0, x0 = max(0, y0), max(0, x0)
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return (r2f_x(x0 + xs.min()), r2f_x(x0 + xs.max()),
            r2f_y(y0 + ys.min()), r2f_y(y0 + ys.max()))

def d4(got, want, tol=2.0):
    if got is None:
        return False, "MISSING"
    d = [got[0] - want[0], got[1] - want[1], got[2] - want[2], got[3] - want[3]]
    return all(abs(v) <= tol for v in d), "d %+5.1f %+5.1f %+5.1f %+5.1f" % tuple(d)

def span(mask, fx0, fx1, fy):  # x-extent of ink on one row
    row = mask[int(round(fy * SY)), int(round(fx0 * SX)):int(round(fx1 * SX)) + 1]
    xs = np.where(row)[0]
    if len(xs) == 0:
        return None
    return (r2f_x(int(round(fx0 * SX)) + xs.min()), r2f_x(int(round(fx0 * SX)) + xs.max()))

def colspan(mask, fy0, fy1, fx):  # y-extent of ink in one column
    col = mask[int(round(fy0 * SY)):int(round(fy1 * SY)) + 1, int(round(fx * SX))]
    ys = np.where(col)[0]
    if len(ys) == 0:
        return None
    return (r2f_y(int(round(fy0 * SY)) + ys.min()), r2f_y(int(round(fy0 * SY)) + ys.max()))

# ══════════════════════════════════════════════════════════════════════════════
print("\n== A. NAVY CHART-PANEL BORDERS (frame px) ==")
PANELS = [("LEFT", 95, 465, 110, 471), ("RIGHT", 486.5, 869.5, 110, 471)]
for nm, bx0, bx1, by0, by1 in PANELS:
    strip = NAVY[int(round((by0 - 3) * SY)):int(round((by0 + 4) * SY)),
                 int(round((bx0) * SX)):int(round((bx1) * SX))]
    ys, xs = np.where(strip)
    chk("%s navy span x" % nm, len(xs) > 0 and
        abs(r2f_x(int(round(bx0 * SX)) + xs.min()) - bx0) <= 2 and
        abs(r2f_x(int(round(bx0 * SX)) + xs.max()) - bx1) <= 2,
        "got %s..%s want %.1f..%.1f" % (
            round(r2f_x(int(round(bx0 * SX)) + xs.min()), 1) if len(xs) else "-",
            round(r2f_x(int(round(bx0 * SX)) + xs.max()), 1) if len(xs) else "-", bx0, bx1))
    col = NAVY[int(round(by0 * SY)):int(round((by1 + 3) * SY)),
               int(round((bx0 - 2) * SX)):int(round((bx0 + 3) * SX))]
    ys2, xs2 = np.where(col)
    chk("%s navy span y" % nm, len(ys2) > 0 and
        abs(r2f_y(int(round(by0 * SY)) + ys2.min()) - by0) <= 2 and
        abs(r2f_y(int(round(by0 * SY)) + ys2.max()) - by1) <= 2,
        "got %s..%s want %d..%d" % (
            round(r2f_y(int(round(by0 * SY)) + ys2.min()), 1) if len(ys2) else "-",
            round(r2f_y(int(round(by0 * SY)) + ys2.max()), 1) if len(ys2) else "-", by0, by1))

# ══════════════════════════════════════════════════════════════════════════════
print("\n== B. GRID LINE POSITIONS (sampled, frame px) ==")
GRIDCOL = (np.abs(ren - np.array([216, 216, 214])).max(axis=2) < 45) & \
          (ren.sum(axis=2) < 720)
for nm, col0 in (("LEFT", 103.5), ("RIGHT", 517.5)):
    got = []
    for k in (0, 2, 5, 8, 11, 14):
        want = col0 + 23 * k
        w = bbox(GRIDCOL, want - 2, want + 2, 300, 440)
        got.append((round(w[0], 1), round(w[1], 1)) if w else None)
    chk("%s grid cols" % nm, all(g is not None for g in got),
        "centres %s vs want %s" % ([g[0] for g in got],
        [round(col0 + 23 * k) for k in (0, 2, 5, 8, 11, 14)]))
for k in (0, 3, 6, 9, 12, 15):
    want = 120.5 + 22.4 * k
    w = bbox(GRIDCOL, 200, 300, want - 2, want + 2)
    chk("grid row k=%d" % k, w is not None and abs((w[2] + w[3]) / 2 - want) <= 2.0,
        "got y %s..%s want %.1f" % (round(w[2], 1), round(w[3], 1), want) if w else "MISSING")

# ══════════════════════════════════════════════════════════════════════════════
print("\n== C. RED AXES: SHAFTS + ARROWHEAD APEXES ==")
# FIX 3: for kind=="h" the bbox max-x is the arrowhead apex; the v-axis base is y434
AXES = [("LEFT y-axis", 126.5, 143, 434, "v"), ("LEFT x-axis", 434, 436, 436, "h"),
        ("RIGHT y-axis", 540, 143, 434, "v"), ("RIGHT x-axis", 434, 849, 849, "h")]
for nm, a, tip, along, kind in AXES:
    if kind == "v":
        w = bbox(RED, a - 3, a + 3, 150, 440)
        chk("%s shaft" % nm, w is not None and abs((w[0] + w[1]) / 2 - a) <= 1.5 and
            abs(w[3] - along) <= 2.0, "got x %.1f..%.1f y %.1f..%.1f want cx %.1f, base y %d"
            % (w[0], w[1], w[2], w[3], a, along) if w else "MISSING")
    else:
        # FIX 10: per-panel window — a shared window straddles both panels and
        # the LEFT span would read the RIGHT panel's arrowhead apex.
        w = bbox(RED, 124 if nm.startswith("LEFT") else 538,
                 440 if nm.startswith("LEFT") else 856, a - 3, a + 3)
        chk("%s shaft" % nm, w is not None and abs((w[2] + w[3]) / 2 - a) <= 1.5 and
            abs(w[1] - along) <= 2.0, "got x %.1f..%.1f y %.1f..%.1f want cy %.1f, apex x %d"
            % (w[0], w[1], w[2], w[3], a, along) if w else "MISSING")
for nm, wx, wy in (("LEFT up-head apex", 126.5, 142), ("RIGHT up-head apex", 540, 142)):
    w = bbox(RED, wx - 5, wx + 5, 141, 152)
    chk(nm, w is not None and abs(w[2] - wy) <= 2.0,
        "got y %.1f..%.1f want apex y %.1f" % (w[2], w[3], wy) if w else "MISSING")
for nm, wx, wy in (("LEFT right-head apex", 436, 434), ("RIGHT right-head apex", 849, 434)):
    w = bbox(RED, wx - 8, wx + 2, wy - 6, wy + 6)
    chk(nm, w is not None and abs(w[1] - wx) <= 2.0,
        "got x %.1f..%.1f want apex x %.1f" % (w[0], w[1], wx) if w else "MISSING")

# ══════════════════════════════════════════════════════════════════════════════
print("\n== D. BLUE FITTED LINES (span + LSQ endpoints, per panel) ==")
# FIX 2: per-panel windows; FIX 1: BLUE excludes navy
LINES = [("LEFT", 141, 352, 433, 199, 100, 460), ("RIGHT", 555, 389, 849, 247, 500, 862)]
for nm, x0, y0, x1, y1, wx0, wx1 in LINES:
    w = bbox(BLUE, wx0, wx1, 140, 400)
    ok = w is not None and abs(w[0] - x0) <= 2.5 and abs(w[1] - x1) <= 2.5
    y0r, y1r = int(round(140 * SY)), int(round(400 * SY))
    x0r, x1r = int(round(wx0 * SX)), int(round(wx1 * SX))
    sub = BLUE[y0r:y1r, x0r:x1r]
    ys, xs = np.where(sub)
    px = (x0r + xs) / SX
    py = (y0r + ys) / SY
    A = np.vstack([px, np.ones(len(px))]).T
    m, c = np.linalg.lstsq(A, py, rcond=None)[0]
    ex0, ex1 = m * x0 + c, m * x1 + c
    chk("%s fitted line" % nm, ok and abs(ex0 - y0) <= 3 and abs(ex1 - y1) <= 3,
        "span x %.1f..%.1f (want %.1f..%.1f); LSQ y=%.3fx+%.1f -> (%.1f,%.1f),(%.1f,%.1f) "
        "want (%.1f,%.1f),(%.1f,%.1f)" % (w[0], w[1], x0, x1, m, c, x0, ex0, x1, ex1,
                                           x0, y0, x1, y1))

# ══════════════════════════════════════════════════════════════════════════════
print("\n== E. ORANGE DATA POINTS (24 centroids, d=7.5) ==")
POINTS = {
 "LEFT": [(197.5,145.0),(188.5,355.5),(176.5,380.5),(242.5,327.5),(260.5,333.5),(294.0,333.5),
          (324.0,290.0),(328.5,332.0),(381.5,301.5),(397.5,249.0),(421.5,255.0),(233.5,362.0)],
 "RIGHT": [(611.0,145.0),(601.5,355.5),(589.5,380.5),(656.0,327.0),(674.0,333.5),(707.5,333.5),
           (737.5,290.0),(741.5,332.0),(794.0,302.0),(810.0,249.0),(834.5,255.0),(647.0,362.0)],
}
for nm, pts in POINTS.items():
    bad = []
    for (cx, cy) in pts:
        w = bbox(ORANGE, cx - 7, cx + 7, cy - 7, cy + 7)
        if w is None:
            bad.append((cx, cy, "missing")); continue
        gcx, gcy = (w[0] + w[1]) / 2, (w[2] + w[3]) / 2
        if abs(gcx - cx) > 3 or abs(gcy - cy) > 3:
            bad.append((cx, cy, "at %.1f,%.1f" % (gcx, gcy)))
    chk("%s 12 orange points" % nm, not bad, "all within 3 frame px" if not bad else str(bad))

# ══════════════════════════════════════════════════════════════════════════════
print("\n== F. RED MARKS ==")
# small discs: isolated windows (no other red within +-d)
for nm, cx, cy, d in (("L disc1", 186.5, 155.0, 10.0), ("L disc2", 247.0, 289.0, 9.0),
                      ("R disc1", 603.0, 150.0, 9.0), ("R disc2", 679.0, 320.5, 9.5)):
    w = bbox(RED, cx - d, cx + d, cy - d, cy + d)
    if w is None:
        chk(nm, False, "MISSING"); continue
    gcx, gcy = (w[0] + w[1]) / 2, (w[2] + w[3]) / 2
    gd = max(w[1] - w[0], w[3] - w[2])
    chk(nm, abs(gcx - cx) <= 3 and abs(gcy - cy) <= 3 and abs(gd - d) <= 3,
        "centre %.1f,%.1f (want %.1f,%.1f) d %.1f (want %.1f)" % (gcx, gcy, cx, cy, gd, d))

# FIX 4: LEFT big disc via two scans that dodge the diagonal.
# The diagonal (199,198)->(232,241) ENDS at the disc's centre, so any bbox over
# the disc also catches it. Row y=244 is 3px below the diagonal's end; column
# x=240 is 8px right of it. Expected chord at y=244 (r=12.25, dy=-3):
#   half = sqrt(12.25^2 - 3^2) = 11.87 -> x 220.6..244.4, centre 232.5, span 23.7
# Expected chord at x=240 (dx=+7.5): half = sqrt(12.25^2-7.5^2) = 9.68 -> y 231.3..250.7
rw = span(RED, 205, 262, 244)
ok = rw is not None and abs((rw[0] + rw[1]) / 2 - 232.5) <= 2.0 and abs((rw[1] - rw[0]) - 23.7) <= 3.5
chk("L BIG disc row y=244", ok,
    "x %.2f..%.2f centre %.2f span %.2f (want centre 232.5 span 23.7)"
    % (rw[0], rw[1], (rw[0] + rw[1]) / 2, rw[1] - rw[0]) if rw else "MISSING")
cw = colspan(RED, 222, 260, 240)
ok = cw is not None and abs((cw[0] + cw[1]) / 2 - 241.0) <= 2.0 and abs((cw[1] - cw[0]) - 19.4) <= 3.5
chk("L BIG disc col x=240", ok,
    "y %.2f..%.2f centre %.2f span %.2f (want centre 241.0 span 19.4)"
    % (cw[0], cw[1], (cw[0] + cw[1]) / 2, cw[1] - cw[0]) if cw else "MISSING")
# area sanity: red px in the disc's own disc-shaped window vs pi*r^2 = 471
discwin = RED[int(round(229 * SY)):int(round(253 * SY)) + 1,
              int(round(221 * SX)):int(round(244 * SX)) + 1]
# FIX 11: the window is in RENDER px; convert to frame px^2 before comparing
apx = discwin.sum() / (SX * SY)
chk("L BIG disc fill area", abs(apx - 471.4) <= 0.12 * 471.4,
    "red area %.1f frame px^2 vs pi*12.25^2 = 471.4" % apx)

# FIX 5: LEFT diagonal in an ISOLATED window (disc cannot reach it)
for nm, x0, y0, x1, y1, wx0, wx1, wy0, wy1, wslope in (
        ("L diagonal", 199, 198, 232, 241, 196, 220, 196, 230, 43.0 / 33.0),
        ("R diagonal", 626, 208, 646, 264, 623, 650, 205, 267, 56.0 / 20.0)):
    w = bbox(RED, wx0, wx1, wy0, wy1)
    ok = w is not None and abs(w[0] - x0) <= 2.5 and abs(w[2] - y0) <= 2.5
    # LSQ slope over the isolated mask
    y0r, y1r = int(round(wy0 * SY)), int(round(wy1 * SY))
    x0r, x1r = int(round(wx0 * SX)), int(round(wx1 * SX))
    sub = RED[y0r:y1r, x0r:x1r]
    ys, xs = np.where(sub)
    sl = None
    if len(xs) > 2:
        a, _b = np.polyfit((x0r + xs) / SX, (y0r + ys) / SY, 1)
        sl = a
    chk(nm, ok and sl is not None and abs(sl - wslope) <= 0.10,
        "bbox x %.1f..%.1f y %.1f..%.1f n=%d slope %s want %.4f"
        % (w[0], w[1], w[2], w[3], len(xs),
           "n/a" if sl is None else "%.4f" % sl, wslope) if w else "MISSING")

# ══════════════════════════════════════════════════════════════════════════════
print("\n== G. ANNOTATION BOXES (border edges, frame px) ==")
BOXINF = (np.abs(ren - np.array([237, 251, 250])).max(axis=2) < 30)
BOXBRD = (ren.sum(axis=2) < 690) & (rB - rR > 5)
for nm, bx, by, bw, bh in (("LEFT box", 216.5, 148, 100, 26), ("RIGHT box", 633.5, 148, 100, 27)):
    chk("%s fill present" % nm,
        bbox(BOXINF, bx + 4, bx + bw - 4, by + 4, by + bh - 4) is not None,
        "interior measured")
    w = bbox(BOXBRD, bx - 2, bx + 3, by + 2, by + bh - 2)
    okL = w is not None and abs(w[0] - bx) <= 1.5
    w2 = bbox(BOXBRD, bx + bw - 3, bx + bw + 2, by + 2, by + bh - 2)
    okR = w2 is not None and abs(w2[1] - (bx + bw)) <= 1.5
    w3 = bbox(BOXBRD, bx + 2, bx + bw - 2, by - 2, by + 3)
    okT = w3 is not None and abs(w3[2] - by) <= 1.5
    w4 = bbox(BOXBRD, bx + 2, bx + bw - 2, by + bh - 3, by + bh + 2)
    okB = w4 is not None and abs(w4[3] - (by + bh)) <= 1.5
    chk("%s 4 border edges" % nm, okL and okR and okT and okB,
        "L %s R %s T %s B %s" % (okL, okR, okT, okB))

# ══════════════════════════════════════════════════════════════════════════════
print("\n== H. EQUATION INK (STIX, fs=14.5) vs measured ==")
EQINK = (ren.sum(axis=2) < 560)
for nm, ex0, ex1, ey0, ey1 in (("LEFT eq", 226, 307, 155, 167), ("RIGHT eq", 643, 723, 155, 167)):
    bx = 210 if nm.startswith("LEFT") else 628
    w = bbox(EQINK, bx, bx + 115, 145, 175)
    ok, det = d4(w, (ex0, ex1, ey0, ey1), tol=3.0)
    chk(nm, ok, det + (" got x %.1f..%.1f y %.1f..%.1f" % (w[0], w[1], w[2], w[3]) if w else " MISSING"))

# ══════════════════════════════════════════════════════════════════════════════
print("\n== I. CAPTIONS (ink bbox per line + red keyword split) ==")
# FIX 6: line-2 windows start at y505 (line 1's descenders end at y503.0 in the
# render / y504 in the original)
CAPS = [("LCAP1 red keyword", RED, 100, 175, 483, 508, 109, 160),
        ("LCAP1 black remainder", None, 160, 425, 483, 508, 165, 419),
        ("LCAP2 whole line", None, 70, 460, 505, 522, 178, 350),
        ("RCAP1 red keyword", RED, 512, 620, 483, 508, 523, 610),
        ("RCAP1 black remainder", None, 608, 830, 483, 508, 615, 819),
        ("RCAP2 whole line", None, 560, 790, 505, 522, 568, 774)]
for nm, mask, wx0, wx1, wy0, wy1, ex0, ex1 in CAPS:
    m = mask if mask is not None else (INK & (np.abs(ren - np.array([51, 51, 51])).max(axis=2) < 90))
    w = bbox(m, wx0, wx1, wy0, wy1)
    if w is None:
        chk(nm, False, "MISSING"); continue
    ok = abs(w[0] - ex0) <= 4 and abs(w[1] - ex1) <= 4 and (w[2] - wy0) >= -3 and (w[3] - wy1) <= 3
    chk(nm, ok, "got x %.1f..%.1f y %.1f..%.1f want x %d..%d in y %d..%d"
        % (w[0], w[1], w[2], w[3], ex0, ex1, wy0, wy1))

# ══════════════════════════════════════════════════════════════════════════════
print("\n== J. FRAME CONTAINMENT ==")
topband = INK[int(0):int(round(45 * SY)), :]
tsum = topband.sum()
badge_zone = INK[int(round(52 * SY)):int(round(94 * SY)),
                 int(round(848 * SX)):int(round(905 * SX))].sum()
chk("no stray ink above panel top", tsum <= badge_zone,
    "ink px above y45 = %d ; badge zone = %d" % (tsum, badge_zone))
chk("no ink left of panel", INK[:, :int(round(54 * SX)) - 8].sum() == 0,
    "%d px" % INK[:, :int(round(54 * SX)) - 8].sum())
chk("no ink right of panel", INK[:, int(round(903 * SX)) + 8:].sum() == 0,
    "%d px" % INK[:, int(round(903 * SX)) + 8:].sum())
capsum = INK[int(round(480 * SY)):, :].sum()
chk("caption row ink inside panel", capsum > 0, "%d px of caption ink below y480" % capsum)
topstrip = RED[int(round(45 * SY)):int(round(50 * SY)),
               int(round(60 * SX)):int(round(900 * SX))]
chk("NO top stroke (deck law)", topstrip.sum() == 0, "%d red px in the top strip" % topstrip.sum())
# FIX 7: INK no longer counts panel gray, so this gap check is meaningful
gap = INK[int(round(115 * SY)):int(round(470 * SY)),
          int(round(467 * SX)):int(round(485 * SX))]
chk("inter-panel gap clean", gap.sum() < 200, "%d ink px in the x467..485 gap (panel gray excluded)" % gap.sum())
# extra: no chart ink BELOW the panel bottom (y>472) other than captions (y>=485)
# FIX 12: restrict to x60..900 — the house chrome's LEFT (x57..59) and RIGHT
# (x900..902) red strokes span the whole panel height by decree and contribute
# exactly 21 rows x 3 cols x 2 = 126 px to any full-width window here.
below = INK[int(round(473 * SY)):int(round(483 * SY)),
            int(round(60 * SX)):int(round(900 * SX))].sum()
chk("no ink between panel bottom and captions", below == 0,
    "%d ink px in y473..483, x60..900 (house strokes excluded)" % below)

# ══════════════════════════════════════════════════════════════════════════════
nok = sum(1 for _, o in results if o)
print("\n== SUMMARY: %d/%d checks OK ==" % (nok, len(results)))
if nok != len(results):
    print("FAILURES:")
    for nm, o in results:
        if not o:
            print("   -", nm)
print("VERDICT:", "PASS" if nok == len(results) else "FIX NEEDED")
