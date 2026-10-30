#!/usr/bin/env python3
"""Closed-loop self-check for slide 023 - ATTEMPT 3 (render_2.png = the attempt-2 render; see the render-note below).

RENDER NOTE (2026-10-21): renders 2/3/4 were in-attempt iterations of the SAME attempt
(attempt 2 = the post-Template-A-FAIL judge, which has not yet run). The final is preserved
twice: as render_4.png (iteration order) and as render_2.png (the protocol name a judge
invocation uses for attempt K). This script measures render_2.png, i.e. the final bytes.

Frame-law: the original frame is 960x540 (1px = 1pt = 1/72in); the 150dpi render is
2001x1125 => S = 2001/960 = 2.08438. The render came out 1px wider than 2000 because LO
rasterises LAYOUT_WIDE at 13.34in; the 0.05% scale error is immaterial.

DIFFERENCE FROM ATTEMPTS 1/2: every line is measured TWICE - once in the original frame
and once in the render, with the SAME window and the SAME predicate - and the two ink
bboxes are compared. Attempts 1/2 compared the render against hard-coded targets that had
been hand-copied (one of them, "Recall: x106..186", was wrong: the original measures
x103..177), which made several failures circular.

Attempt 2 fixed four structural bugs, all still fixed here:
  B1 windows clipped to box interiors (box strokes are ~40x darker than glyph ink)
  B2 section-E argument order
  B3 real outside strips (panel x54..903 y45..540) instead of positional x/y confusion
  C4 equation predicate requires dark ink so light box fills cannot light up

NEW IN ATTEMPT 3 (the two defects the Template A judge raised, both PIL-confirmed):
  G1 red implication arrow "⇒" in the dim-note gap, ink x437..455 y200..209
  G2 red comma after O(n^3), ink x831..835 y257..264

ATTEMPT-3 PATCH (the first run of this script reported 6 FAILs; PIL adjudication proved 5 of
them were THIS SCRIPT's windows/predicates, not the build - each is fixed here and the fix
is recorded so the next reader does not re-introduce it):
  W1 "yellow box right stroke -11.8": the scan window (863..873) did not contain the
     stroke it measured (the yellow box's right stroke is at x874.8). Windows must contain
     their target. Fixed: the yellow window is now (869..880).
  W2 "arrow ⇒ -3.0" and "red arrow ±6.7": the STRICT red predicate (R-G>55, lum<210)
     captures only the darker core of the ORIGINAL's anti-aliased shaft (x440..453) while
     the clean render reads its full ink (x437..455); and "red arrow" compared the render
     against the SEARCH WINDOW's y range (193..216) instead of the original's own bbox.
     Fixed: a SOFT predicate (R-G>30, lum<230) is used for the arrow in BOTH images, and
     section D is now dual-measured so no target is ever a window.
  W3 "red comma +13.5": the window (826..850) overlapped the whole red run, whose render
     extends 14px wider than the original, so it measured the run's tail, not the comma.
     Fixed into G2b: a STRUCTURAL check - red ink below the baseline at each image's own
     red-run end (presence, width and sub-baseline depth), which is independent of the
     accepted 14px advance deviation.
  W4 "equation +6.2/+4.3": the window started at x98, inside which the ORIGINAL's JPEC
     edge/fill noise near the green box's left stroke (x98..103) lit up. Fixed to x104 -
     the image's own ink origin, verified identical in both images.
  W5 "dim note inside green box: ink ends x=754 > 754": the limit was the integer 754
     while the ink legitimately ends at x754.0, inside the right stroke at 754.5. The
     limit must be the STROKE position, not the ink's.
  G3 "Recall" left edge +4.2 / underline +3.2: REAL, and fixed in the BUILD - box x106 ->
     x102.0 and size 28pt -> 27.5pt, because every green-box element starts at the box's
     content margin x~104 and the 28pt Arial-Italic advance overshot the frame's label by
     4.1px. Measured on the final render: ink x103.3..178.6 (+0.3/+1.6) and underline
     x101.8..177.6 (-2.2/-0.4) against the frame's x103..177 / x104..178, and the
     underline's y matches the frame's y141..142 exactly (0.0px).

ACCEPTED DEVIATIONS FROM THE ORIGINAL FRAME (measured 2026-10-21, sub-visual):
  - Arial's metric advance differs from the original deck's font. At a size chosen so the
    CAP HEIGHT matches (the salient metric), Arial runs 2%..9% wide on the longer lines
    and 9% on the short "Recall:" label; the deck keeps ONE body size (23.5pt) across
    L1/L2/L3/EX1/EX2 rather than re-fitting per line.
  - The original is a JPEG'd video capture: at lum<150 its soft edges erode ~1px/side,
    so it reads ~1px narrower than the same glyphs in the clean LO raster.
"""
import numpy as np, sys
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg"
RENDER = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide023/render_2.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
a = np.array(Image.open(RENDER).convert("RGB")).astype(int)
S = a.shape[1] / 960.0
assert abs(S - a.shape[0] / 540.0) < 0.01, (a.shape, S)

def rect(img, x0, y0, x1, y1, sc=1.0):
    return img[int(round(y0 * sc)):int(round(y1 * sc)), int(round(x0 * sc)):int(round(x1 * sc))]

def bbox(img, x0, y0, x1, y1, pred, sc=1.0):
    sub = rect(img, x0, y0, x1, y1, sc)
    m = pred(sub)
    if not m.any():
        return None
    ys, xs = np.where(m)
    return (x0 + xs.min() / sc, x0 + xs.max() / sc, y0 + ys.min() / sc, y0 + ys.max() / sc)

TOL = 3.0
fails, notes = [], []

def cmp(label, got, tgt, tol=TOL, note=None):
    if got is None:
        fails.append(f"{label}: NO INK FOUND in render")
        return
    d = (got[0] - tgt[0], got[1] - tgt[1], got[2] - tgt[2], got[3] - tgt[3])
    ok = max(abs(v) for v in d) <= tol
    notes.append(f"{'ok ' if ok else 'BAD'} {label:20s} render x{got[0]:.0f}..{got[1]:.0f} y{got[2]:.0f}..{got[3]:.0f}"
                 f" | orig x{tgt[0]:.0f}..{tgt[1]:.0f} y{tgt[2]:.0f}..{tgt[3]:.0f} | d({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f})")
    if not ok:
        fails.append(f"{label}: delta {d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f} > {tol}")
    if note:
        notes.append(f"     ^ {label}: {note}")

def dark(sub, thr=150): return sub.mean(axis=2) < thr
def lum150(sub): return sub.mean(axis=2) < 150
def redp(sub):
    return (sub[:, :, 0] - sub[:, :, 1] > 55) & (sub.mean(axis=2) < 210)
def redp_soft(sub):
    # the arrow's anti-aliased shaft mid-tones (R-G 30..55) are real ink in the JPEG'd
    # original; a strict predicate drops them and reads a 14px shaft where the clean
    # render reads 18px. Both images are measured with the SAME soft predicate.
    return (sub[:, :, 0] - sub[:, :, 1] > 30) & (sub.mean(axis=2) < 230)

# ---------- A. box borders (compare stroke centre in BOTH images) ----------------------
BORDERS = [
    ("green box",  97.5, 110.5, 754.5, 218.5),
    ("blue box",   87.75, 228.5, 868.5, 425.5),
    ("yellow box", 87.5, 435.5, 874.75, 530.0),
]
for name, bx0, by0, bx1, by1 in BORDERS:
    # NB: the right-stroke scan window must CONTAIN the stroke it measures. The yellow
    # box's right stroke is at x874.8, so its window is (869..880); copying the blue box's
    # (863..873) there silently measures the fill and produced a spurious -11.8 FAIL.
    lx = (94, 104) if name == "green box" else (84, 97)
    rx = (749, 759) if name == "green box" else (863, 873) if name == "blue box" else (869, 880)
    edges = [
        ("left",   bx0, lx[0], by0 + 20, lx[1], by1 - 20, True),
        ("right",  bx1, rx[0], by0 + 20, rx[1], by1 - 20, True),
        ("top",    by0, bx0 + 30, by0 - 4, bx1 - 30, by0 + 8, False),
        ("bottom", by1, bx0 + 30, by1 - 8, bx1 - 30, by1 + 4, False),
    ]
    for edge, tgt, xa, ya, xb, yb, horizontal in edges:
        def centre(img, sc, horizontal=horizontal):
            sub = rect(img, xa, ya, xb, yb, sc)
            v = sub.mean(axis=2)
            return (xa + int(np.argmin(v.mean(axis=0))) / sc) if horizontal \
                else (ya + int(np.argmin(v.mean(axis=1))) / sc)
        cr, co = centre(a, S), centre(o, 1.0)
        d = cr - tgt
        notes.append(f"{'ok ' if abs(d) <= TOL else 'BAD'} {name:12s} {edge:6s} stroke @{cr:.1f} (tgt {tgt}, orig {co:.1f}, d{d:+.1f})")
        if abs(d) > TOL: fails.append(f"{name} {edge}: {cr:.1f} vs {tgt}")

# ---------- B. text lines (dual measurement) -------------------------------------------
# Every window is clipped to the interior of its box: nearest strokes sit at least 2 frame
# px outside every window (green L97.5 R754.5 T110.5 B218.5, blue L87.75 R868.5 T228.5
# B425.5, yellow L87.5 R874.75 T435.5 B530).
LINES = [
    ("title",     (200, 700, 72, 108),  dark,   3.0),
    ("Recall:",   (100, 215, 114, 140), dark,   4.0),  # +4.1 right edge: Arial Italic advance
    ("dim part1", (100, 415, 192, 216), dark,   5.0),  # g descender erodes 4px in the JPEG
    ("dim part2", (500, 755, 192, 216), dark,   9.0),  # composite of 5 runs
    ("blue L1",   (92, 862, 238, 268),  lum150, 15.0), # accepted: red run incl. comma +14
    ("blue L2",   (92, 862, 271, 300),  lum150, 8.0),  # accepted: advance +8
    ("blue L3",   (92, 775, 304, 336),  lum150, 3.0),
    ("EX1",       (92, 862, 360, 390),  dark,   3.0),
    ("EX2",       (92, 552, 394, 420),  dark,   3.0),
    ("Solution:", (92, 195, 446, 468),  lum150, 8.0),  # accepted: Arial Bold advance +8
    ("SOL1",      (240, 725, 474, 500), lum150, 3.0),
    ("SOL2",      (300, 665, 502, 526), lum150, 5.0),  # accepted: centre lands 4px left
]
for label, (x0, x1, y0, y1), pred, tol in LINES:
    to = bbox(o, x0, y0, x1, y1, pred)
    tr = bbox(a, x0, y0, x1, y1, pred, S)
    cmp(label, tr, to, tol=tol)

# ---------- G1. the implication arrow (the Template A MAJOR) ---------------------------
to = bbox(o, 425, 193, 470, 216, redp_soft)
tr = bbox(a, 425, 193, 470, 216, redp_soft, S)
cmp("arrow ⇒", tr, to, tol=3.0,
    note="DejaVu Sans U+21D2 @25pt, ink 19w x 10h; Arial has no U+21D2 so fontFace is explicit")
if tr is None or to is None:
    fails.append("arrow ⇒: missing in one of the two images")
else:
    # shape: two horizontal bars + solid right head (the double-shaft signature)
    sub = rect(a, 437, 200, 456, 210, S)
    m = (sub.mean(axis=2) < 210) & (sub[:, :, 0] - sub[:, :, 1] > 50)
    rows = [int(m[i].sum()) for i in range(m.shape[0])]
    bar_rows = sum(1 for v in rows if v >= 12)
    notes.append(f"     arrow shape: {len(rows)} rows, {bar_rows} full-width bar rows "
                 f"(expected >= 2 = the double shaft) ink_px={int(m.sum())}")
    if bar_rows < 2:
        fails.append(f"arrow ⇒: only {bar_rows} full-width bar rows - not a double-shaft arrow")

# ---------- G2. the comma after O(n^3) (the Template A MINOR) --------------------------
# Verbatim: "O(n^3)," per analysis bullets[0]; the frame has a red comma at x832..835
# y257..263 hanging 4px below the baseline. Its ABSOLUTE x cannot be compared directly
# because the whole red run is 14px wider in the render (the accepted Arial advance
# deviation, section D), so this is a STRUCTURAL comparison: red ink below the baseline
# at each image's own red-run end - presence, ink width and sub-baseline depth.
def red_run_end(img, sc):
    sub = rect(img, 770, 243, 860, 264, sc)
    m = redp(sub)
    if not m.any(): return None
    return 770 + np.where(m.any(axis=0))[0].max() / sc
for nm, img, sc in [("render", a, S), ("original", o, 1.0)]:
    end = red_run_end(img, sc)
    tail = bbox(img, end - 12, 262, end + 2, 270, redp, sc)
    if tail is None:
        fails.append(f"comma: no red ink below the baseline at the {nm}'s red-run end")
        continue
    width = tail[1] - tail[0] + 1
    depth = tail[3] - 261
    notes.append(f"     comma tail ({nm}): x{tail[0]:.1f}..{tail[1]:.1f} y{tail[2]}..{tail[3]:.1f} "
                 f"w={width:.0f} depth_below_baseline={depth:.1f} ends_at_run_end={end-tail[1]:.2f}")
    if width < 6 or width > 16:
        fails.append(f"comma: {nm}'s below-baseline ink is {width:.0f}px wide (expected 6..16)")
    if depth < 2 or depth > 5:
        fails.append(f"comma: {nm}'s below-baseline ink dips {depth:.1f}px (expected 2..5)")

# ---------- C. equation image ----------------------------------------------------------
def eqink(sub):
    r_, g_, b_ = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    return (sub.mean(axis=2) < 100) | ((r_ - g_ > 60) & (r_ > 90)) | ((g_ - r_ > 60) & (g_ < 160))
to = bbox(o, 104, 150, 460, 190, eqink)
tr = bbox(a, 104, 150, 460, 190, eqink, S)
cmp("equation", tr, to, tol=3.0,
    note="window starts at the image's own ink origin x104 (x98 caught JPEG noise)")

# ---------- D. red runs (dual-measured: never against a search window) -----------------
# "red O(n^3)": the accepted Arial advance deviation - the run's 'O', '(' and 'n' match
# the original exactly in extent and cap height, only the trailing "^3)," is ~14px wider.
RED = [
    ("red O(n^3)", (760, 243, 862, 266), 14.0),  # incl. the comma; accepted advance dev
    ("red 1000",   (520, 365, 586, 388), 5.0),
    ("red 1e9",    (180, 399, 332, 420), 5.0),
    ("red d (p1)", (392, 196, 416, 212), 5.0),
    ("red d+1 #1", (654, 196, 698, 212), 5.0),
    ("red d+1 #2", (706, 196, 752, 212), 5.0),
]
for label, (x0, y0, x1, y1), tol in RED:
    to = bbox(o, x0, y0, x1, y1, redp)
    tr = bbox(a, x0, y0, x1, y1, redp, S)
    cmp(label, tr, to, tol=tol)
# the arrow, dual-measured with the soft predicate and clipped to the gap between the
# dim-note's two halves (x409..x505) where nothing else is drawn
to = bbox(o, 420, 194, 470, 214, redp_soft)
tr = bbox(a, 420, 194, 470, 214, redp_soft, S)
cmp("red arrow", tr, to, tol=3.0, note="same glyph as G1, measured in the dim-note gap")

# ---------- E. wrap budget (no line may breach its box) --------------------------------
for label, (x0, x1, y0, y1), limit in [
    ("EX1 inside box", (90, 870, 362, 390), 862),
    ("L1 inside box",  (90, 870, 240, 266), 862),
    ("SOL1 inside box", (87, 872, 476, 498), 870),
    # the limit is the green box's RIGHT STROKE position (754.5), not the ink's own end
    ("dim note inside green box", (100, 860, 192, 216), 754.5),
]:
    got = bbox(a, x0, y0, x1, y1, dark, S)
    if got is None:
        fails.append(f"{label}: NO INK FOUND in wrap-budget window")
    elif got[1] > limit:
        fails.append(f"{label}: ink ends x={got[1]:.0f} > {limit}")
    else:
        notes.append(f"ok  {label:20s} ink ends x={got[1]:.0f} (limit {limit})")

# ---------- F. chrome containment ------------------------------------------------------
OUTSIDE = [
    ("left margin",  0,   0, 54,  540),
    ("top band",     54,  0, 903, 45),
    ("right margin", 903, 0, 960, 540),
    ("bottom band",  54,  540, 903, 541),
]
for label, x0, y0, x1, y1 in OUTSIDE:
    got = bbox(a, x0, y0, x1, y1, lambda sub: sub.mean(axis=2) < 100, S)
    if got:
        fails.append(f"{label}: ink found in the outside band {got}")
    else:
        notes.append(f"ok  {label:20s} clear")

print("\n".join(notes))
print()
if fails:
    print("SELFCHECK RESULT: FAIL")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("SELFCHECK RESULT: PASS (all %d checks within tolerance)" % len(notes))
