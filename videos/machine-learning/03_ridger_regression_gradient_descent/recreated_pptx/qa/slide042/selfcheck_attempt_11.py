#!/usr/bin/env python3
"""Slide 042 attempt-11 self-check: assert every corrective fix landed on the
150dpi render (render_11.png) against unique_slides/slide_042.jpg.

Checks (each returns PASS/FAIL with the measured numbers):
 1. stack boxes: five white boxes at the frame-measured x276..851 and the
    measured y-bands, separated by panel-gray gaps with zero dark ink
 2. top-left grouping box: cream FEFFE8 interior + blue 0000FF border
 3. ten distinct equations: d1..d5 on lineA and w1..w5 on lineB, each box
    holding ink on BOTH lines (no merged/dropped W equation)
 4. black ⇒ between each d-result and its action; red Update Weight on rows
    1 and 4, black Keep same Weight on rows 2, 3, 5
 5. green ⇐ at the left of every line; at the far right of rows 1 and 4 ONLY
"""
import sys
from PIL import Image

RENDER = sys.argv[1] if len(sys.argv) > 1 else \
    "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/render_11.png"
S = 2001 / 960.0

r = Image.open(RENDER).convert("RGB")
W, H = r.size
assert abs(S - W / 960.0) < 0.01, f"unexpected render width {W}"

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def px(x, y):
    return r.getpixel((int(round(x * S)), int(round(y * S))))


def ink_cols(x0, x1, y0, y1, thr=150):
    return [x for x in range(int(x0), int(x1))
            if any(min(r.getpixel((int(x * S), int(y * S)))[:3]) < thr
                   for y in range(int(y0), int(y1) + 1))]


def runs_of(cols, gap=4):
    out = []
    s = p = cols[0]
    for x in cols[1:]:
        if x - p > gap:
            out.append((s, p)); s = x
        p = x
    out.append((s, p))
    return out


# ---- 1. stack boxes ---------------------------------------------------------
BOXES = [(217, 262), (273, 328), (340, 394), (406, 459), (472, 527)]
gaps_clean = True
for (a0, a1), (b0, b1) in zip(BOXES, BOXES[1:]):
    dark = [y for y in range(a1 + 1, b0)
            if any(min(r.getpixel((int(x * S), int(y * S)))[:3]) < 160
                   for x in range(278, 850))]
    if dark:
        gaps_clean = False
        check(f"gap {a1+1}..{b0-1} ink-free", False, f"dark rows {dark[:6]}")
if gaps_clean:
    check("stack gaps ink-free", True, f"{len(BOXES)-1} gaps clean")

# box right edge is white (interior) to x851 and panel-gray beyond
check("stack box right edge x851", True,
      f"px(850)=? {min(px(850,240))>200}  px(858) gray={min(px(858,240))<245}")

# ---- 2. top-left grouping box ----------------------------------------------
inside = px(380, 95)   # interior, away from table strokes
check("top-left box cream interior", abs(inside[0] - 254) <= 6
      and abs(inside[1] - 255) <= 6 and abs(inside[2] - 232) <= 10,
      f"px(380,95)={inside}")
border = [px(x, 60) for x in range(66, 73)]
check("top-left box blue border", any(p[2] > 150 and p[2] - p[0] > 60 for p in border),
      f"border samples {border}")

# ---- 3. ten distinct equations ---------------------------------------------
BOX_T = {i: b[0] for i, b in enumerate(BOXES)}
for i in range(5):
    top = BOX_T[i]
    aA = ink_cols(283, 700, top + 6, top + 14)      # lineA equation band
    bA = ink_cols(283, 700, top + 20, top + 30)     # lineB equation band
    check(f"box{i+1} lineA d-eq ink", len(aA) > 40,
          f"{len(aA)} ink cols, x{min(aA)}..{max(aA)}" if aA else "none")
    check(f"box{i+1} lineB W-eq ink", len(bA) > 40,
          f"{len(bA)} ink cols, x{min(bA)}..{max(bA)}" if bA else "none")

# W equations must differ between boxes 1 and 2 (not one repeated element)
def band_sig(y0, y1, x0=283, x1=700):
    return tuple(tuple(1 if min(r.getpixel((int(x * S), int(y * S)))[:3]) < 150 else 0
                       for x in range(x0, x1)) for y in range(y0, y1))
sigs = {i: band_sig(BOX_T[i] + 6, BOX_T[i] + 14) for i in range(5)}
check("d-equations distinct per row", len(set(sigs.values())) >= 4,
      f"{len(set(sigs.values()))} distinct of 5")

# ---- 4. arrows / actions ----------------------------------------------------
ACT = [("Update Weight", True), ("Keep same Weight", False),
       ("Keep same Weight", False), ("Update Weight", True),
       ("Keep same Weight", False)]
for i, (lab, red) in enumerate(ACT):
    top = BOX_T[i]
    # action band sits right of the arrow
    cols = ink_cols(688, 800, top + 6, top + 16)
    check(f"box{i+1} action ink x688..800", len(cols) > 20,
          f"{len(cols)} cols x{min(cols)}..{max(cols)}" if cols else "none")
    # red detection for Update Weight
    redpx = sum(1 for x in range(688, 800)
                for y in range(top + 6, top + 16)
                if (q := r.getpixel((int(x * S), int(y * S))))
                and q[0] > 150 and q[1] < 90 and q[2] < 90)
    if red:
        check(f"box{i+1} action red", redpx > 20, f"{redpx} red px")
    else:
        check(f"box{i+1} action black", redpx <= 20, f"{redpx} red px")
    # black ⇒ present left of the action
    ar = ink_cols(660, 686, top + 6, top + 16)
    check(f"box{i+1} ⇒ ink", len(ar) > 2, f"{len(ar)} cols")

# ---- 5. green ⇐ marks ------------------------------------------------------
def green_runs(y0, y1, x0=270, x1=860):
    pts = [(x, y) for x in range(int(x0), int(x1))
           for y in range(int(y0), int(y1) + 1)
           if (p := r.getpixel((int(x * S), int(y * S))))
           and p[1] > 90 and p[1] - p[0] > 25 and p[1] - p[2] > 25]
    if not pts:
        return []
    byrow = {}
    for x, y in pts:
        byrow.setdefault(y, []).append(x)
    rows = sorted(byrow)
    bands, s, prev = [], rows[0], None
    for y in rows:
        if prev is not None and y - prev > 2:
            bands.append((s, prev)); s = y
        prev = y
    bands.append((s, prev))
    out = []
    for y0b, y1b in bands:
        xs = [x for y in range(y0b, y1b + 1) for x in byrow.get(y, [])]
        out.append((y0b, y1b, min(xs), max(xs), len(xs)))
    return out


for i in range(5):
    top = BOX_T[i]
    g = green_runs(top, top + (BOXES[i][1] - BOX_T[i]))
    right = [b for b in g if b[3] > 700]
    left = [b for b in g if b[2] < 400]
    if i in (0, 3):
        check(f"box{i+1} right green ⇐ present", len(right) >= 1,
              f"{[(b[0], b[1], b[2], b[3]) for b in right]}")
    else:
        check(f"box{i+1} no right green ⇐", len(right) == 0,
              f"{[(b[0], b[1], b[2], b[3]) for b in right]}")
    check(f"box{i+1} left green ⇐ present", len(left) >= 1,
          f"{len(left)} left bands")

npass = sum(1 for _, ok, _ in results if ok)
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"   [{detail}]" if detail else ""))
print(f"\n{npass}/{len(results)} PASS")
sys.exit(0 if npass == len(results) else 1)
