#!/usr/bin/env python3
"""Selfcheck render_5.png (build_attempt_4.js) against the original frame 032.

All expected values come from MY ground-up measurement (MEASUREMENTS_STEP1.md),
not from the inherited notes. Closed-loop gates run BEFORE any judge dispatch.
"""
import numpy as np
from collections import Counter
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = V + "/unique_slides/slide_032.jpg"
REND = V + "/recreated_pptx/qa/slide032/render_5.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
S = r.shape[0] / 540.0
print(f"render {r.shape[1]}x{r.shape[0]}  scale render/frame = {S:.4f}")
fails = []


def cv(v):
    return int(round(v * S))


def occ(name, x0, y0, x1, y1, expect_min=None):
    out = {}
    for tag, im in (("ORIG", o), ("REND", r)):
        H = im.shape[0]
        sc = H / 540.0
        sub = im[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]
        rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
        mx = np.maximum(np.maximum(rr, gg), bb)
        mn = np.minimum(np.minimum(rr, gg), bb)
        sat = mx - mn
        ink = int(((sat > 45) | (mx < 110)).sum())
        out[tag] = ink
    print(f"  {name:>22} ORIG ink={out['ORIG']:>6}  REND ink={out['REND']:>6}"
          f"  ratio={out['REND']/max(1,out['ORIG']):.2f}")
    return out


print("\n=== 1. FRAME / REGION CONTAINMENT (measured boxes) ===")
print("  measured ink boxes (frame px):")
print("   title          x 80..559  y 63..88")
print("   param table    x 76..208  y 178..251")
print("   plot interior  x 576..806 y 69..264   (strokes to y310)")
print("   callout col    x 330..600 y 184..320")
print("   arrow          x 349..372 y 317..355")
print("   iter table     x 298..600 y 330..527")
occ("title band", 70, 58, 570, 95)
occ("param table", 70, 172, 215, 256)
occ("plot area", 570, 60, 812, 315)
occ("callout col", 325, 178, 605, 325)
occ("arrow box", 344, 312, 378, 360)
occ("iter table", 293, 325, 605, 532)

print("\n=== 2. HOUSE CHROME (verified separately: PASS) ===")

print("\n=== 3. PARAMETER TABLE ROW FILLS (measured: E8FFD5 / F7BFC2 / FBFF0B) ===")
for label, y0, y1 in [("row1 step", 182, 200), ("row2 initX", 207, 224), ("row3 delta", 232, 245)]:
    res = []
    for tag, im in (("ORIG", o), ("REND", r)):
        H = im.shape[0]
        sc = H / 540.0
        sub = im[int(y0 * sc):int(y1 * sc), int(150 * sc):int(195 * sc)].reshape(-1, 3)
        sub = sub[sub.sum(axis=1) > 420]
        dom = Counter(map(tuple, sub)).most_common(1)[0][0] if len(sub) else (0, 0, 0)
        res.append("#%02X%02X%02X" % dom)
    print(f"  {label:>12} ORIG {res[0]}  REND {res[1]}")
    if res[0] != res[1]:
        fails.append(f"param fill {label}: {res[0]} vs {res[1]}")

print("\n=== 4. PLOT GEOMETRY on the RENDER (measured expectations) ===")
# axes / red vertical extend to y310 ; red band at y309
sc = r.shape[0] / 540.0
def dark_col(x_frame, y0, y1):
    x = int(x_frame * sc)
    sub = r[int(y0 * sc):int(y1 * sc), x - 1:x + 2]
    return int((sub.min(axis=2) < 120).sum())
for tag, x, y0, y1 in [("black y-axis x=631", 631, 267, 306),
                       ("red x=5 x=687.5", 687.5, 267, 306)]:
    n = dark_col(x, y0, y1)
    print(f"  {tag:>20}: {n} dark rows in y{y0}..{y1} (expect >{(y1-y0)*0.8:.0f})")
    if n < (y1 - y0) * 0.8:
        fails.append(f"{tag} does not extend below the plot ({n} rows)")
# red band at y309
sub = r[int(309 * sc), int(574 * sc):int(808 * sc)]
redband = int(((sub[:, 0] - sub[:, 1] > 40) & (sub[:, 0] - sub[:, 2] > 40)).sum())
print(f"  red band y=309: {redband}/{sub.shape[0]} render px red (expect >80%)")
if redband < sub.shape[0] * 0.8:
    fails.append(f"red band at y309 too sparse ({redband}/{sub.shape[0]})")
# black chord at y=146
sub = r[int(146 * sc), int(576 * sc):int(806 * sc)]
chord = int((sub.min(axis=1) < 110).sum())
print(f"  black chord y=146: {chord}/{sub.shape[0]} render px dark (expect >70%)")
if chord < sub.shape[0] * 0.7:
    fails.append(f"black y=10 chord too short ({chord}/{sub.shape[0]})")
# white interior still ends at y265
sub = r[int(268 * sc):int(300 * sc), int(600 * sc):int(800 * sc)]
wh = int(((sub > 240).all(axis=2)).sum())
print(f"  white below plot y268..299: {wh}/{sub[:,:,0].size} px white (expect >80%)")
# no tick labels below the plot (frame y276..292) -> should have NO glyph ink
tl = r[int(274 * sc):int(296 * sc), int(556 * sc):int(826 * sc)]
ink = int(((tl.max(axis=2) - tl.min(axis=2) > 45) | (tl.max(axis=2) < 110)).sum())
print(f"  tick-label zone y274..295: {ink} ink px (expect ~0 — the frame has none)")
if ink > 40:
    fails.append(f"fabricated tick labels present ({ink} ink px)")

print("\n=== 5. CALLOUT BOXES on the RENDER ===")
for tag, y in [("box2 top border y234", 234), ("box2 bottom border y279", 279)]:
    sub = r[int(y * sc), int(372 * sc):int(538 * sc)]
    grn = int(((sub[:, 1] - sub[:, 0] > 20) & (sub[:, 1] - sub[:, 2] > 20)).sum())
    print(f"  {tag:>24}: {grn}/{sub.shape[0]} green px (expect >80%)")
    if grn < sub.shape[0] * 0.8:
        fails.append(f"{tag} missing green border ({grn})")
sub = r[int(305 * sc), int(334 * sc):int(596 * sc)]
pk = int(((sub[:, 0] > 220) & (sub[:, 1] > 150) & (sub[:, 2] > 190)).sum())
print(f"  box3 band y=305 x334..596: {pk}/{sub.shape[0]} pink px (expect >80%)")
if pk < sub.shape[0] * 0.8:
    fails.append(f"box3 band too narrow ({pk})")

print("\n=== 6. ARROW (crimson, x349..372 y317..355) ===")
sub = r[int(318 * sc):int(354 * sc), int(348 * sc):int(374 * sc)]
crim = int(((sub[:, :, 0] - sub[:, :, 1] > 40) & (sub[:, :, 0] - sub[:, :, 2] > 30)).sum())
print(f"  crimson ink in the arrow box: {crim} px (expect >150)")
if crim < 150:
    fails.append(f"arrow ink too sparse ({crim})")
mag = int(((sub[:, :, 0] > 100) & (sub[:, :, 1] < 90) & (sub[:, :, 2] > 100)
           & (np.abs(sub[:, :, 0] - sub[:, :, 2]) < 60)).sum())
print(f"  C000C0-family magenta in the arrow box: {mag} px (expect ~0 — none in the frame)")
if mag > 60:
    fails.append(f"magenta arrow still present ({mag} px)")

print("\n=== 7. CURVE — one smooth analytic parabola, second-difference ripple ===")
rr, gg, bb = r[:, :, 0], r[:, :, 1], r[:, :, 2]
blue = (bb - rr > 60) & (bb - gg > 30) & (bb > 120)
ys_, xs_ = np.where(blue[int(70 * sc):int(264 * sc), int(576 * sc):int(806 * sc)])
col = {}
for y, x in zip(ys_, xs_):
    col.setdefault(int(x), []).append(int(y) + int(70 * sc))
if len(col) > 30:
    xs = sorted(col)
    cy = np.array([np.median(col[x]) for x in xs], dtype=float)
    d2 = np.diff(cy, 2)
    print(f"  curve cols {xs[0]}..{xs[-1]} ({len(xs)} cols, render px)")
    print(f"  second-difference std={np.std(d2):.3f} px  max|d2|={np.abs(d2).max():.3f} px")
    print(f"  frame y range {cy.min()/sc:.0f}..{cy.max()/sc:.0f}")
    print(f"  vertex (frame): x={xs[int(np.argmin(cy))]/sc:.1f} y={cy.min()/sc:.1f}"
          f"   (measured 687.5 / 254.5)")
    if np.abs(d2).max() > 6:
        fails.append(f"curve ripple {np.abs(d2).max():.2f} px — not one smooth curve")
else:
    fails.append(f"only {len(col)} curve columns — TOO SPARSE / not one curve")

print("\n=== 8. ITERATION TABLE BAND FILLS on the RENDER ===")
for label, y0, y1 in [("olive", 348, 380), ("lavender", 391, 420),
                      ("peach", 435, 464), ("green", 476, 490), ("salmon", 501, 514)]:
    res = []
    for tag, im in (("ORIG", o), ("REND", r)):
        H = im.shape[0]
        sc = H / 540.0
        sub = im[int(y0 * sc):int(y1 * sc), int(170 * sc):int(300 * sc)].reshape(-1, 3)
        sub = sub[sub.sum(axis=1) > 420]
        dom = Counter(map(tuple, sub)).most_common(1)[0][0] if len(sub) else (0, 0, 0)
        res.append("#%02X%02X%02X" % dom)
    ok = "OK " if res[0] == res[1] else "DIFF"
    print(f"  {label:>9} {ok} ORIG {res[0]}  REND {res[1]}")

print("\n=== 9. TITLE COLOUR RUNS (measured red x81..247 / green x258..434 / blue x445..559) ===")
for tag, x0, x1 in [("red", 90, 240), ("green", 270, 430), ("blue", 450, 555)]:
    sub = r[int(74 * sc):int(80 * sc), int(x0 * sc):int(x1 * sc)]
    rr2, gg2, bb2 = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    if tag == "red":
        n = int(((rr2 - gg2 > 50) & (rr2 - bb2 > 50)).sum())
    elif tag == "green":
        n = int(((gg2 - rr2 > 40) & (gg2 - bb2 > 40)).sum())
    else:
        n = int(((bb2 - rr2 > 60) & (bb2 - gg2 > 30)).sum())
    print(f"  {tag:>6} run x{x0}..{x1}: {n} coloured px")
    if n < 40:
        fails.append(f"title {tag} run missing ({n} px)")

print("\n" + "=" * 60)
if fails:
    print("SELFCHECK: %d FAILURE(S)" % len(fails))
    for f in fails:
        print("  - " + f)
else:
    print("SELFCHECK: PASS (all closed-loop gates green)")
print("=" * 60)
