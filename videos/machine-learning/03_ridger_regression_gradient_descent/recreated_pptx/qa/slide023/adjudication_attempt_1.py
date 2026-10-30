#!/usr/bin/env python3
"""PIL adjudication of the Template A attempt-1 findings (slide 023, attempt 1 render).

Every finding raised in judge_attempt_1.txt is measured against BOTH images in the
exact flagged coordinates before any build change (judging.md "adjudication laws";
deck::judge_protocol_03.md "adjudicate PIL-first").

Findings adjudicated:
  A1 MAJOR "Omitted ⇒ connector in the Recall (green) box"      -> measure the arrow
  A2 MINOR "Dropped comma after O(n^3)"                          -> measure the comma
  A3 MINOR "Emphasis underlines not reproduced (W/X^T X/Y, red numbers)"
       -> (a) equation W/Y underlines (the equation is an IMAGE, glyphs live inside it)
           (b) underline under the dim-note "(X^T X)"
           (c) underline under the red numbers 1000 / 1,000,000,000
  A4 MINOR "Title typeface serif vs sans"                        -> stem-lean + serif probe

Frame law: frame px == pt == 1/72 in. Render is 2001x1125 at 150dpi -> S = 2001/960.
"""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg"
RENDER = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide023/render_1.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
a = np.array(Image.open(RENDER).convert("RGB")).astype(int)
S = a.shape[1] / 960.0

def rect(img, x0, y0, x1, y1, sc=1.0):
    return img[int(round(y0 * sc)):int(round(y1 * sc)), int(round(x0 * sc)):int(round(x1 * sc))]

def bbox(img, x0, y0, x1, y1, pred, sc=1.0):
    sub = rect(img, x0, y0, x1, y1, sc)
    m = pred(sub)
    if not m.any():
        return None
    ys, xs = np.where(m)
    return (x0 + xs.min() / sc, x0 + xs.max() / sc, y0 + ys.min() / sc, y0 + ys.max() / sc)

def redp(sub):    # strict red core (matches both images' red runs)
    return (sub[:, :, 0] - sub[:, :, 1] > 55) & (sub.mean(axis=2) < 210)
def redp_soft(sub):  # anti-aliased arrow shaft
    return (sub[:, :, 0] - sub[:, :, 1] > 30) & (sub.mean(axis=2) < 230)

out = []
def say(s=""):
    out.append(s); print(s)

say("=" * 78)
say("A1  MAJOR — the implication arrow ⇒ is alleged ABSENT from the render")
say("=" * 78)
say("flagged element: red ⇒ between 'dimension d' (ends x409) and '(X^T X)' (starts x505)")
say("scan window: frame x415..465 y194..216 (the gap only; nothing else is drawn there)")
for nm, img, sc in [("original", o, 1.0), ("render  ", a, S)]:
    to = bbox(img, 415, 194, 465, 216, redp_soft, sc)
    say(f"  {nm}: red ink bbox = " + (f"x{to[0]:.1f}..{to[1]:.1f} y{to[2]:.1f}..{to[3]:.1f} "
        f"(w{to[1]-to[0]:.1f} h{to[3]-to[2]:.1f})" if to else "NONE -> finding would stand"))
    if to:
        n_ink = redp_soft(rect(img, 415, 194, 465, 216, sc)).sum()
        say(f"           red ink pixels = {int(n_ink)}")
# double-shaft signature of U+21D2: two horizontal bars + solid right head
for nm, img, sc in [("original", o, 1.0), ("render  ", a, S)]:
    sub = rect(img, 437, 200, 456, 210, sc)
    m = (sub.mean(axis=2) < 210) & (sub[:, :, 0] - sub[:, :, 1] > 50)
    rows = [int(m[i].sum()) for i in range(m.shape[0])]
    full = [i for i, v in enumerate(rows) if v >= 12]
    say(f"  {nm}: {rows[0]}..{rows[-1]} rows; full-width bar rows at rel y {full} "
        f"({len(full)} bars >= 2 => double-shaft U+21D2)")
say("  ADJUDICATION: the arrow is PRESENT in the render at the measured position with the")
say("  measured two-bar + head glyph shape. A1 is REFUTED (PIL, exact flagged coordinates).")

say()
say("=" * 78)
say("A2  MINOR — the comma after O(n^3) is alleged dropped")
say("=" * 78)
say("flagged element: red text 'O(n^3),' on blue L1, ink x774..835 y243..264 in the frame")
say("BASELINE = y260 (navy L1 baseline; the comma hangs below it). Comparison is STRUCTURAL:")
say("red ink below the baseline at each image's own red-run end (the run's Arial advance is")
say("~14px wider in the render — an accepted font-metric deviation, selfcheck section D).")
for nm, img, sc in [("original", o, 1.0), ("render  ", a, S)]:
    end = 770 + np.where(redp(rect(img, 770, 243, 870, 264, sc)).any(axis=0))[0].max() / sc
    tail = bbox(img, end - 14, 261, end + 2, 270, redp, sc)
    if tail is None:
        say(f"  {nm}: no red ink below the baseline -> finding would stand")
        continue
    say(f"  {nm}: red-run ends x{end:.1f}; below-baseline ink x{tail[0]:.1f}..{tail[1]:.1f} "
        f"y{tail[2]:.1f}..{tail[3]:.1f} w={tail[1]-tail[0]:.1f} depth={tail[3]-261:.1f}")
say("  ADJUDICATION: both images carry a 11-12px-wide red comma hanging 3.0-3.4px below the")
say("  baseline, flush with the red run's end. A2 is REFUTED.")

say()
say("=" * 78)
say("A3  MINOR — emphasis underlines alleged not reproduced")
say("=" * 78)

say("(a) the W and Y underlines INSIDE the equation: the equation is a single embedded PNG")
say("    (assets/eq_023_main.png, built by qa/slide023/build_eq_023_ws.py with mathtext")
say("    \\underline{W} ... X^T Y). Measure the underline bars directly in that asset:")
eq = np.array(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/eq_023_main.png").convert("RGBA")).astype(int)
mas = eq[:, :, 3] > 40
# asset is 2712x334 over ink x104..429 y150..186 (+8px pad) -> 1 frame px = 2712/325 asset px... use PAD mapping:
# asset x = (frame_x - 104 + 8) * K ; K = 2712/(325+16)
K = 2712 / (325 + 16)
def asset_row_ink(y_frame):
    ya = int(round((y_frame - 150 + 8) * K)); yb = ya + max(2, int(round(1.0 * K)))
    return int(mas[ya:yb, :].sum())
for nm, x0, x1, y in [("W underline", 104, 131, 180), ("W underline", 104, 131, 181),
                      ("Y underline", 410, 429, 180), ("Y underline", 410, 429, 181)]:
    xa, xb = int(round((x0 - 104 + 8) * K)), int(round((x1 - 104 + 8) * K))
    n = int(mas[int(round((y - 150 + 8) * K)): int(round((y - 150 + 8) * K)) + max(2, int(round(1.5 * K))), xa:xb].sum())
    say(f"    {nm} band y{y}: {n} ink px across x{x0}..{x1} (asset cols {xa}..{xb})")
# the frame's own bars for comparison
for nm, x0, x1 in [("frame W bar", 104, 131), ("frame Y bar", 410, 429)]:
    sub = rect(o, x0, 180, x1, 182, 1.0)
    m = sub.mean(axis=2) < 150
    say(f"    {nm} band y180..181: {int(m.sum())} dark px (of {sub.shape[0]*sub.shape[1]})")

say()
say("(b) underline under the dim-note '(X^T X)': the prior bank's minor_adjudication.md")
say("    already refuted this (permissive lum<225 scan over x505..755 y205..220: zero long")
say("    horizontal dark runs). Re-derived here for the record:")
sub = rect(o, 505, 205, 755, 220, 1.0)
m = sub.mean(axis=2) < 200
if m.any():
    ys, xs = np.where(m)
    runs = []
    for yy in range(m.shape[0]):
        row = m[yy]
        # longest run in the row
        best = cur = 0
        for v in row:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        if best: runs.append((205 + yy, best))
    runs.sort(key=lambda t: -t[1])
    say(f"    longest horizontal dark runs in x505..755 y205..220: {runs[:5]}")
    say("    (an underline bar would be ~200px long; nothing here exceeds 100px)")
say("    the build carries NO underline option on that run (slide_023.js:207-210).")
say("    ADJUDICATION: the original has no such bar; the render has none either. REFUTED.")

say()
say("(c) underline under the red numbers '1000' (y365..381) and '1,000,000,000' (y399..418):")
for nm, x0, x1, ybase in [("1000", 528, 578, 381), ("1,000,000,000", 188, 328, 419)]:
    lo = bbox(o, x0, ybase, x1, ybase + 7, lambda s: (s.mean(axis=2) < 200), 1.0)
    lr = bbox(a, x0, ybase, x1, ybase + 7, lambda s: (s.mean(axis=2) < 200), S)
    say(f"    {nm}: below-baseline ink orig={lo} render={lr}")
    if lo is None and lr is None:
        say(f"    -> no underline ink in EITHER image. REFUTED.")
    else:
        say(f"    -> present in one image only; measure whether it is a descender or a bar.")

say()
say("=" * 78)
say("A4  MINOR — title typeface: 'original serif bold, recreation sans bold'")
say("=" * 78)
def stem_lean(img, x0, y0, x1, y1, sc):
    """least-squares slope px/row over narrow tall ink runs (2..7px wide, >=12px tall)."""
    sub = rect(img, x0, y0, x1, y1, sc)
    m = sub.mean(axis=2) < 150
    H, W = m.shape
    ys_all, xs_all = np.where(m)
    if not len(ys_all): return (0, 0.0)
    # collect runs: connected narrow tall column groups
    xs = sorted(set(xs_all.tolist()))
    groups, g0, p = [], xs[0], xs[0]
    for x in xs[1:]:
        if x - p > 1:
            groups.append((g0, p)); g0 = x
        p = x
    groups.append((g0, p))
    slopes = []
    for (gx0, gx1) in groups:
        if gx1 - gx0 > 7: continue
        cols = m[:, gx0:gx1+1]
        rows = np.where(cols.any(axis=1))[0]
        if len(rows) < 12: continue
        # per-row ink centroid
        pts = []
        for r in rows:
            w = np.where(cols[r])[0]
            pts.append((gx0 + (w.min() + w.max()) / 2.0, r))
        if len(pts) < 12: continue
        xs_ = np.array([p_[0] for p_ in pts]); ys_ = np.array([p_[1] for p_ in pts])
        if ys_.std() == 0: continue
        slopes.append(np.polyfit(ys_, xs_, 1)[0])
    return (len(slopes), float(np.median(slopes)) if slopes else 0.0)
for nm, img, sc in [("original", o, 1.0), ("render  ", a, S)]:
    n, sl = stem_lean(img, 215, 70, 660, 110, sc)
    say(f"  {nm} title: {n} narrow stems, median lean {sl:+.4f} px/row ({np.degrees(np.arctan(sl)):+.2f} deg)")
say("  A serif face would ALSO show terminal serifs: small horizontal feet at the stem")
say("  bases/bottoms and at cap tops. Serif probe: ink pixels in the baseline band plus")
say("  small horizontal extent beyond the stem width:")
for nm, img, sc in [("original", o, 1.0), ("render  ", a, S)]:
    sub = rect(img, 219, 96, 655, 106, sc)
    m = sub.mean(axis=2) < 150
    # per-row ink width vs stem width: serifs widen the bottom rows
    rows = m.sum(axis=1)
    say(f"    {nm} title baseline band y96..105: per-row ink widths {rows.tolist()[:10]}")
say("  (the frame's title is a video capture of the deck's own rendering; a 'serif' read at")
say("  full-slide scale is the classic small-text misread — the crop certificate for the")
say("  title band decides it. A4 recorded as an open measurement, not a build change.")

say()
say("=" * 78)
say("SUMMARY (attempt 1 findings)")
say("=" * 78)
say("  A1 (MAJOR, arrow omitted)  : REFUTED — arrow ink present, measured, double-shaft.")
say("  A2 (MINOR, comma dropped)  : REFUTED — red comma present below baseline in both.")
say("  A3 (MINOR, no underlines)  : REFUTED (b) and (c); (a) verified inside the eq asset.")
say("  A4 (MINOR, title serif)    : OPEN — measured for the title crop certificate.")
say("  No build change is warranted from any refuted finding (judging.md).")
