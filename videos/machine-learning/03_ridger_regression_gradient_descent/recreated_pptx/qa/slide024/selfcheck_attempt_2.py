#!/usr/bin/env python3
"""Self-check for slide 024 (worker w4-s024-20261023T1712; re-run on render_2 for attempt 2).

Mandatory pre-judge self-check (17_worker_instructions.md "MANDATORY PRE-JUDGE
SELF-CHECK" + building.md closed-loop laws), run on the 150dpi render of
recreated_pptx/slide_024_recreated.pptx.

Checker-honesty rules applied (building.md "Closed-loop checker discipline"):
  * the SAME predicate and the SAME slide-space windows are applied to BOTH the
    render and the original (JPEG-antialias halo cancels on both sides);
  * every window is expressed in FRAME px (960x540 = the original's own grid) and
    converted per-image with that image's own scale — never one scale for both;
  * probe boxes are re-derived from THIS build's draw-code constants (the
    ink targets in build/slide_024.js), never from a stale geometry note;
  * the census EXCLUDES the house chrome stroke columns (x<62 / x>897 frame px)
    so content clusters separate instead of merging through the red strokes;
  * a FAIL is a claim: this script prints the raw numbers so a failure can be
    adjudicated rather than obeyed blind.

Checks: A frame containment · B red-ink census + dark-ink census · C per-element
ink bbox vs original · D equations (none) · E '(GD)' paren geometry · F table
(none) · G pen icon presence/containment · H one-band-per-element.
"""
import json
import sys

import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
VID = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = f"{VID}/recreated_pptx/qa/slide024/render_2.png"
ORIG = f"{VID}/unique_slides/slide_024.jpg"
SPEC = f"{VID}/analysis/slide_024_final.json"

PANEL = dict(x0=54, x1=903, y0=45, y1=540)      # frame px (AGENTS.md)
STROKE_COLS = (62, 897)                          # frame px: outside = chrome strokes

TOL = 4.0          # frame px closed-loop tolerance
fails = []
notes = []


def fail(msg):
    fails.append(msg)
    print("   !! FAIL:", msg)


def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(int)


ren = load(RENDER)
ori = load(ORIG)
spec = json.load(open(SPEC))
H, W = ren.shape[:2]
SCALE = {"ren": H / 540.0, "ori": 1.0}          # px per frame px, per image
assert (W, H) == (2001, 1125), f"unexpected render size {W}x{H}"
S_REN = SCALE["ren"]

print(f"render {W}x{H} ({S_REN:.4f} px/frame-px) | original {ori.shape[1]}x{ori.shape[0]} (1.0 px/frame-px)")


# ---------------------------------------------------------------- masks
def red_mask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 90) & ((r - g) > 40) & ((r - b) > 10)


def dark_mask(a):
    """Dark-gray ink (the 404040 pen icon + the badge numeral 333333)."""
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r < 110) & (g < 110) & (b < 110)


def reldark_mask(a):
    """SENSITIVE relative-ink mask: any pixel materially darker than the local
    panel fill (~232 lum). building.md mask law: strict masks on JPEG originals
    systematically drop mid-tone strokes — complement with a sensitive mask.
    Used for the tiny pen icon, whose halo fades to light gray on the original."""
    lum = a.sum(axis=2) / 3.0
    return lum < 200


def to_frame(mask, which):
    """Convert an image-space mask to frame-px coordinates (divide by scale)."""
    return mask, SCALE[which]


def win(mask, which, y0, y1, x0=0, x1=960, x_exclude=None):
    """Apply a slide-space window (frame px) to an image-space mask; returns the
    cropped mask plus the offset so profiles come back in frame px."""
    s = SCALE[which]
    m = mask.copy()
    # rows outside [y0,y1)
    if y0 > 0:
        m[: int(y0 * s), :] = False
    if y1 < 540:
        m[int(y1 * s):, :] = False
    if x0 > 0:
        m[:, : int(x0 * s)] = False
    if x1 < 960:
        m[:, int(x1 * s):] = False
    if x_exclude is not None:
        m[:, : int(x_exclude[0] * s)] = False
        m[:, int(x_exclude[1] * s):] = False
    if not m.any():
        return None
    return m


def profile(which, mask):
    """Ink bbox of a mask, in FRAME px."""
    s = SCALE[which]
    rows = mask.sum(axis=1)
    cols = mask.sum(axis=0)
    rr = np.where(rows > 0)[0]
    cc = np.where(cols > 0)[0]
    if not len(rr):
        return None
    return dict(y0=rr.min() / s, y1=rr.max() / s, x0=cc.min() / s, x1=cc.max() / s,
                total=int(mask.sum()), rows=rows, cols=cols)


def clusters_f(mask, which, min_gap_f=6.0):
    """Row clusters in FRAME px, gap threshold in frame px."""
    s = SCALE[which]
    rows = mask.sum(axis=1)
    ys = np.where(rows > 0)[0]
    if not len(ys):
        return []
    gap = min_gap_f * s
    out = []
    start = prev = ys[0]
    for y in ys[1:]:
        if y - prev > gap:
            out.append((start / s, prev / s))
            start = y
        prev = y
    out.append((start / s, prev / s))
    return out


def colgroups_f(mask, which, min_gap_f=3.0):
    """Column groups in FRAME px (glyph-level segmentation inside a window)."""
    s = SCALE[which]
    cols = np.where(mask.sum(axis=0) > 0)[0]
    if not len(cols):
        return []
    gap = min_gap_f * s
    groups = []
    start = prev = cols[0]
    for c in cols[1:]:
        if c - prev > gap:
            groups.append((start / s, prev / s))
            start = c
        prev = c
    groups.append((start / s, prev / s))
    return groups


def sub_band(mask, which, y0, y1, x0, x1):
    """Vertical extent of ink inside a sub-window, in FRAME px."""
    s = SCALE[which]
    m = mask.copy()
    m[: int(y0 * s), :] = False
    m[int(y1 * s):, :] = False
    m[:, : int(x0 * s)] = False
    m[:, int(x1 * s):] = False
    ys = np.where(m.sum(axis=1) > 0)[0]
    if not len(ys):
        return None
    return ys.min() / s, ys.max() / s


r_red, r_dark = red_mask(ren), dark_mask(ren)
o_red, o_dark = red_mask(ori), dark_mask(ori)
print(f"red ink totals:  render {int(r_red.sum()):6d} | original {int(o_red.sum()):6d}")
print(f"dark ink totals: render {int(r_dark.sum()):6d} | original {int(o_dark.sum()):6d}")

# ================================================================ A. CONTAINMENT
print("\nA. FRAME CONTAINMENT")
for name, m in (("red", r_red), ("dark", r_dark)):
    op = m.copy()
    y0 = int(PANEL["y0"] * S_REN)
    x0, x1 = int(PANEL["x0"] * S_REN), int(PANEL["x1"] * S_REN)
    op[y0:, x0:x1 + 1] = False
    n = int(op.sum())
    loc = ""
    if n:
        ys, xs = np.where(op)
        loc = f" at frame x {xs.min()/S_REN:.0f}..{xs.max()/S_REN:.0f}, y {ys.min()/S_REN:.0f}..{ys.max()/S_REN:.0f}"
    print(f"   {name:5s} content ink outside the house panel: {n} px{loc}")
    if n:
        fail(f"A frame containment: {n} {name} px of ink outside the panel{loc}")
top = win(r_red, "ren", 0, 44, 55, 902)
if top is not None and top.sum() > 0:
    fail(f"A: red ink in the band above the panel ({int(top.sum())} px) — this deck has NO top stroke")
else:
    print("   top band (y0..44) bare of red — correct (no top stroke on this deck)")
# the pen icon must not touch the bottom-stroke band
icon_bot = win(r_dark, "ren", 495, 537, 440, 520)
print(f"   (G containment pre-note) icon band + bottom stroke checked in G")

# ================================================================ B. CENSUS
print("\nB. INK CENSUS (chrome stroke columns x<62 / x>897 excluded)")
EXPECTED = [("title", 223, 269),
            ("and", 294, 322), ("subtitle2", 349, 381)]


def census(mask, which, label):
    # window y45..537: the 537..539 bottom-stroke band is CHROME (it survives the
    # x-exclusion because the stroke spans cols 58..902) and is not content.
    m = win(mask, which, 45, 537, 0, 960, x_exclude=STROKE_COLS)
    if m is None:
        print(f"   {label}: no ink")
        return []
    cl = clusters_f(m, which, 6.0)
    print(f"   {label} ({len(cl)} clusters):", [(round(a), round(b)) for a, b in cl])
    return cl


r_cl = census(r_red, "ren", "render red")
o_cl = census(o_red, "ori", "orig   red")
if len(r_cl) != len(EXPECTED):
    fail(f"B: render shows {len(r_cl)} red content clusters, expected {len(EXPECTED)} "
         f"(title, 'and', subtitle2) — a text element may be missing or merged")
else:
    for (lbl, ya, yb), (a, b) in zip(EXPECTED, r_cl):
        d = max(abs(a - ya), abs(b - yb))
        tag = "ok" if d <= 6 else "OFF"
        print(f"   {lbl:14s} render y {a:6.1f}..{b:6.1f}  expected {ya}..{yb}  ({tag}, d={d:.1f})")
        if d > 6:
            notes.append(f"B: '{lbl}' band y {a:.1f}..{b:.1f} vs expected {ya}..{yb} (d {d:.1f} frame px)")

r_icl = census(r_dark, "ren", "render dark")
o_icl = census(o_dark, "ori", "orig   dark")

# ================================================================ C. TEXT BANDS
print("\nC. PER-ELEMENT INK BBOX vs ORIGINAL (same windows both images, tol 4 frame px)")
BANDS = [
    ("title",     red_mask,  215, 280, 240, 725, (242, 718, 224, 268)),
    ("and",       red_mask,  285, 330, 430, 530, (451, 508, 294, 321)),
    ("subtitle2", red_mask,  340, 392, 190, 790, (201, 759, 350, 380)),
    ("pen icon",  reldark_mask, 495, 537, 450, 495, (462, 480, 505, 525)),
]
for label, mfun, ya, yb, xa, xb, exp in BANDS:
    out = {}
    for which, m in (("ren", mfun(ren)), ("ori", mfun(ori))):
        p = profile(which, win(m, which, ya, yb, xa, xb))
        out[which] = p
    pr, po = out["ren"], out["ori"]
    if pr is None or po is None:
        fail(f"C: {label}: no ink (render={'yes' if pr else 'NO'}, orig={'yes' if po else 'NO'})")
        continue
    cx_r, cy_r = (pr["x0"] + pr["x1"]) / 2, (pr["y0"] + pr["y1"]) / 2
    cx_o, cy_o = (po["x0"] + po["x1"]) / 2, (po["y0"] + po["y1"]) / 2
    dx, dy = cx_r - cx_o, cy_r - cy_o
    dw = (pr["x1"] - pr["x0"]) - (po["x1"] - po["x0"])
    dh = (pr["y1"] - pr["y0"]) - (po["y1"] - po["y0"])
    print(f"   {label:10s} ren cx {cx_r:7.1f} cy {cy_r:7.1f} w {pr['x1']-pr['x0']+1:5.1f} h {pr['y1']-pr['y0']+1:5.1f} | "
          f"ori cx {cx_o:7.1f} cy {cy_o:7.1f} w {po['x1']-po['x0']+1:5.1f} h {po['y1']-po['y0']+1:5.1f} | "
          f"d(c) {dx:+5.1f},{dy:+5.1f} d(wh) {dw:+5.1f},{dh:+5.1f}")
    if abs(dx) > TOL or abs(dy) > TOL:
        fail(f"C: {label} ink CENTER off by {dx:+.1f},{dy:+.1f} frame px (tol {TOL})")
    if abs(dw) > TOL or abs(dh) > TOL:
        fail(f"C: {label} ink EXTENT differs by {dw:+.1f},{dh:+.1f} frame px (tol {TOL})")

# ================================================================ D. EQUATIONS
eq = spec["verbatim_text"].get("equations") or []
print(f"\nD. equations: verbatim_text.equations = {eq} — "
      + ("none to assert (recorded)" if not eq else "MUST BE ASSERTED"))
if eq:
    fail("D: spec declares equations; this build has no equation region (must not judge with an empty equation box)")

# ================================================================ E. DELIMITERS
print("\nE. TITLE '(GD)' PARENTHESIS GEOMETRY (must span the enclosed glyphs, not sit on them)")
for which, m in (("ren", r_red), ("ori", o_red)):
    bandm = win(m, which, 215, 282, 618, 725)
    if bandm is None:
        fail(f"E: {which}: no ink in the '(GD)' region")
        continue
    g = colgroups_f(bandm, which, 3.0)
    print(f"   {which}: column groups (frame px):", [(round(a, 1), round(b, 1)) for a, b in g])
    # '(' is the first group on the left of 'GD'; ')' the last. Identify by
    # position: the enclosed 'GD' ink sits between them.
    if len(g) >= 3:
        lp, rp_ = g[0], g[-1]
        lps, rps = lp, rp_
        ext_l = sub_band(m, which, 215, 282, lps[0] - 1, lps[1] + 1)
        ext_r = sub_band(m, which, 215, 282, rps[0] - 1, rps[1] + 1)
        ext_gd = sub_band(m, which, 215, 282, g[1][0], g[-2][1])
        print(f"   {which}: '(' x {lps[0]:.0f}..{lps[1]:.0f} y {ext_l[0]:.0f}..{ext_l[1]:.0f} (h {ext_l[1]-ext_l[0]:.1f})")
        print(f"   {which}: ')' x {rps[0]:.0f}..{rps[1]:.0f} y {ext_r[0]:.0f}..{ext_r[1]:.0f} (h {ext_r[1]-ext_r[0]:.1f})")
        print(f"   {which}: 'GD' enclosed ink y {ext_gd[0]:.0f}..{ext_gd[1]:.0f}")
        for side, ext in (("(", ext_l), (")", ext_r)):
            top_gap = ext[0] - ext_gd[0]
            bot_gap = ext_gd[1] - ext[1]
            # parentheses legitimately descend BELOW the baseline (their bowls
            # hang below x-height); they must not be TRUNCATED short of the
            # enclosed ink, and their strokes must not overlap the 'GD' ink.
            if ext[0] > ext_gd[0] + 1.5:
                fail(f"E: {which}: '{side}' top ({ext[0]:.1f}) truncates above the enclosed ink top ({ext_gd[0]:.1f})")
    else:
        notes.append(f"E: {which}: only {len(g)} column groups in the '(GD)' region — inspect manually")

# horizontal clearance: the paren strokes must not sit ON the GD glyphs
for which, m in (("ren", r_red), ("ori", o_red)):
    bandm = win(m, which, 250, 265, 618, 725)   # mid-height of GD
    g = colgroups_f(bandm, which, 3.0) if bandm is not None else []
    if len(g) >= 3:
        gap_l = g[1][0] - g[0][1]
        gap_r = g[-1][0] - g[-2][1]
        print(f"   {which}: paren-to-GD horizontal clearance at mid-height: left {gap_l:.1f} px, right {gap_r:.1f} px")
        if gap_l < 1.0 or gap_r < 1.0:
            fail(f"E: {which}: paren stroke sits ON the enclosed text (clearance left {gap_l:.1f}, right {gap_r:.1f} px)")

# ================================================================ F. TABLE
print("\nF. table: none on this slide (3 single-line text elements + 1 icon + chrome) — recorded, not asserted")

# ================================================================ G. ICON
print("\nG. PEN ICON (600dpi PNG embedded at exact px/600 size; spec color 404040)")
r_rel = reldark_mask(ren)
o_rel = reldark_mask(ori)
band_ren = win(r_dark, "ren", 495, 537, 440, 520)
if band_ren is not None:
    cl = clusters_f(band_ren, "ren", 6.0)
    if len(cl) != 1:
        fail(f"G: {len(cl)} dark clusters in the bottom band (expected 1 pen icon)")
    else:
        print(f"   exactly one dark cluster in the bottom band: y {cl[0][0]:.1f}..{cl[0][1]:.1f}")

# BOTH masks on the icon band, so a strict-vs-sensitive mask bias is visible
print("   icon band measurement, both masks (tol for extent: 6 frame px):")
for mname, mfun, mren, mori in (
        ("strict dark (<110)", dark_mask, r_dark, o_dark),
        ("sensitive relative (<200 lum)", reldark_mask, r_rel, o_rel)):
    bre = win(mren, "ren", 495, 537, 450, 495)
    bor = win(mori, "ori", 495, 537, 450, 495)
    pr = profile("ren", bre) if bre is not None else None
    po = profile("ori", bor) if bor is not None else None
    if pr is None:
        fail(f"G: NO ink in the bottom-center icon band with the {mname} mask — pen icon missing (BLOCKER class)")
        continue
    line = (f"   {mname:28s} ren x {pr['x0']:.0f}..{pr['x1']:.0f} y {pr['y0']:.0f}..{pr['y1']:.0f} "
            f"(w {pr['x1']-pr['x0']+1:.1f} h {pr['y1']-pr['y0']+1:.1f}, {pr['total']} px)")
    if po is not None:
        line += (f" | ori x {po['x0']:.0f}..{po['x1']:.0f} y {po['y0']:.0f}..{po['y1']:.0f} "
                 f"(w {po['x1']-po['x0']+1:.1f} h {po['y1']-po['y0']+1:.1f}, {po['total']} px)")
        dcx = (pr["x0"] + pr["x1"]) / 2 - (po["x0"] + po["x1"]) / 2
        dcy = (pr["y0"] + pr["y1"]) / 2 - (po["y0"] + po["y1"]) / 2
        dw = (pr["x1"] - pr["x0"]) - (po["x1"] - po["x0"])
        dh = (pr["y1"] - pr["y0"]) - (po["y1"] - po["y0"])
        line += f" | d(c) {dcx:+.1f},{dcy:+.1f} d(wh) {dw:+.1f},{dh:+.1f}"
        if abs(dcx) > TOL or abs(dcy) > TOL:
            fail(f"G: icon center off by {dcx:+.1f},{dcy:+.1f} frame px with the {mname} mask (tol {TOL})")
    print(line)
    # containment checks on the strict-mask render extent (the crispest)
    if mname.startswith("strict"):
        if pr["y1"] > 537:
            fail(f"G: icon ink reaches y {pr['y1']:.1f} — touching/crossing the bottom stroke band (frame containment)")
        if pr["y0"] < 45 or pr["x1"] > 903:
            fail("G: icon ink outside the house panel")
# also verify the icon's own embed box (from the build's draw constants) is inside
EMBED = dict(x0=462.5, x1=480.0, y0=504.5, y1=524.1)   # build/slide_024.js addImage
print(f"   build embed box (frame px): x {EMBED['x0']}..{EMBED['x1']}, y {EMBED['y0']}..{EMBED['y1']}")
if EMBED["y1"] > PANEL["y1"] or EMBED["x1"] > PANEL["x1"] or EMBED["x0"] < PANEL["x0"]:
    fail("G: the icon's embed box extends outside the house panel")
if EMBED["y1"] > 537:
    fail(f"G: the icon's embed box bottom ({EMBED['y1']}) crosses the bottom-stroke band (537) — frame containment")
else:
    print("   icon embed box inside the panel and clear of the bottom-stroke band")

# ================================================================ H. WRAP CHECK
print("\nH. ONE-BAND-PER-ELEMENT (single-line boxes; assert no wrap spillover)")
for label, ya, yb in (("title", 210, 285), ("and", 288, 340), ("subtitle2", 344, 395)):
    m = win(r_red, "ren", ya, yb, 0, 960, x_exclude=STROKE_COLS)
    if m is None:
        fail(f"H: {label}: no ink in its band")
        continue
    cl = clusters_f(m, "ren", 5.0)
    print(f"   {label:10s} render sub-bands (y>1px ink): {[(round(a,1), round(b,1)) for a, b in cl]}")
    if len(cl) != 1:
        fail(f"H: {label} renders {len(cl)} ink bands (expected exactly 1) — a line wrapped or a box is misplaced")

# ================================================================ SUMMARY
print("\n" + "=" * 72)
if fails:
    print(f"SELF-CHECK: FAIL ({len(fails)})")
    for f in fails:
        print("  -", f)
    for n in notes:
        print("  ~", n)
    sys.exit(1)
print("SELF-CHECK: PASS")
for n in notes:
    print("  ~", n)
sys.exit(0)
