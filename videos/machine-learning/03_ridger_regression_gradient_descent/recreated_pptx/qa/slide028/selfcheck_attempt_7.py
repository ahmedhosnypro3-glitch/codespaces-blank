#!/usr/bin/env python3
"""Self-check for slide 028 attempt 7 (render_7.png) — mandatory pre-judge set.

Checks: render size/scale; FRAME CONTAINMENT (content strictly inside the 1F4E79
box, the box's own border excluded); axis colour; band ink; RIPPLE CHECK that the
rendered curve matches the analytic quartic (no sawtooth from polyline joins).
"""
import sys
import numpy as np
from PIL import Image

QA = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028/'
RENDER = QA + 'render_7.png'
ORIG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'

r = np.asarray(Image.open(RENDER).convert('RGB')).astype(int)
o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
H, W = r.shape[:2]
S = H / 540.0
def cv(v): return int(round(v * S))
print(f"render {W}x{H} scale={S:.4f}  original {o.shape[1]}x{o.shape[0]}")
fails = []

rr, gg, bb = r[:, :, 0], r[:, :, 1], r[:, :, 2]
panel = (np.abs(rr - 233) < 16) & (np.abs(gg - 233) < 16) & (np.abs(bb - 231) < 18)
white = (rr > 245) & (gg > 245) & (bb > 245)
content = ~panel & ~white

# ── 1. white chart interior (original fact) ──
inner_white = white[cv(132):cv(504), cv(96):cv(853)].mean()
print(f"chart interior white fraction: {inner_white:.3f}")
if inner_white < 0.55:
    fails.append('chart interior is not white')

# ── 2. FRAME CONTAINMENT ──
# House panel bounds + the 1F4E79 chart box x90..858 y127..508.
# The box's own border (and the badge above it, and the title) are not "content".
box = np.zeros_like(content)
box[cv(90):cv(509), cv(90):cv(859)] = True
border = np.zeros_like(content)
border[cv(125):cv(133), cv(85):cv(864)] = True     # top/bottom of the box
border[cv(505):cv(512), cv(85):cv(864)] = True
border[cv(122):cv(514), cv(85):cv(95)] = True      # left/right of the box
border[cv(122):cv(514), cv(854):cv(864)] = True
badge = np.zeros_like(content); badge[cv(50):cv(95), cv(855):cv(898)] = True
title = np.zeros_like(content); title[cv(60):cv(106), :] = True
inner_content = content & box & ~border & ~badge & ~title
ys, xs = np.where(inner_content)
print(f"chart-content ink bbox: frame x{xs.min()/S:.0f}-{xs.max()/S:.0f} y{ys.min()/S:.0f}-{ys.max()/S:.0f}")
ok_box = xs.min() >= cv(93) and xs.max() <= cv(856) and ys.min() >= cv(130) and ys.max() <= cv(505)
print(f"  strictly inside 1F4E79 box: {'OK' if ok_box else 'FAIL'}")
if not ok_box:
    fails.append('chart content crosses the 1F4E79 box')

housestrokes = np.zeros_like(content)
housestrokes[:, :cv(70)] = True; housestrokes[:, cv(890):] = True; housestrokes[cv(528):, :] = True
outside = content & ~box & ~badge & ~title & ~housestrokes & ~border
ys3, xs3 = np.where(outside)
if len(ys3):
    print(f"  ink OUTSIDE the chart box (excluding badge/title): {outside.sum()} px "
          f"bbox frame x{xs3.min()/S:.0f}-{xs3.max()/S:.0f} y{ys3.min()/S:.0f}-{ys3.max()/S:.0f}")
    if outside.sum() > 50:
        fails.append(f'{outside.sum()} px of ink outside the chart box')
else:
    print("  ink outside the chart box (excl. badge/title): 0")

# house panel containment
strokes = np.zeros_like(content)
strokes[:, :cv(63)] = True; strokes[:, cv(896):] = True; strokes[cv(533):, :] = True
inside = content & ~strokes
ys4, xs4 = np.where(inside)
ok_panel = xs4.min() >= cv(64) and xs4.max() <= cv(895) and ys4.min() >= cv(45) and ys4.max() <= cv(532)
print(f"  inside house panel x64..895 y45..532: {'OK' if ok_panel else 'FAIL'}")
if not ok_panel:
    fails.append('content outside house panel')

# ── 3. axis colour + geometry ──
# Curve stroke is now the measured light cyan 8FC3D1 = (143,195,209). Use a
# cyan-family test (b > r by a wide margin, g high) so it catches both the
# stroke core and the antialiased edge, while excluding the maroon axes.
blue = (bb - rr > 22) & (bb - gg > 6) & (rr < 245) & (gg < 225)
blue &= inside
# The chart box's own 1F4E79 border is blue-dominant too (b-r = 90) and runs the
# full width of the scan, so it must be excluded or it masquerades as curve ink.
boxborder = np.zeros_like(blue)
boxborder[cv(505):cv(512), :] = True
boxborder[cv(125):cv(133), :] = True
boxborder[:, cv(85):cv(95)] = True
boxborder[:, cv(854):cv(864)] = True
blue &= ~boxborder
red = (rr > 150) & (gg < 110) & (bb < 110)
red_in = red & inside
red_in[cv(60):cv(106), :] = False
red_in[cv(50):cv(95), cv(855):cv(898)] = False
print(f"\nblue curve px={blue.sum()}  red-in-chart px={red_in.sum()}")
if red_in.sum() < 2000:
    fails.append('axes are not red')
for nm, xc in [('left y-axis', 158), ('right y-axis', 510)]:
    n = red[:, cv(xc) - 2:cv(xc) + 3].sum()
    print(f"  {nm}: red px at x{xc}±2 = {n}")
    if n < 200:
        fails.append(f'{nm} missing')
for nm, yc in [('left x-axis', 442), ('right x-axis', 438)]:
    n = red[cv(yc) - 2:cv(yc) + 3, :].sum()
    print(f"  {nm}: red px at y{yc}±2 = {n}")
    if n < 200:
        fails.append(f'{nm} missing')

# ── 4. RIPPLE CHECK ──
# For each column, take the blue run whose centre is nearest the analytic quartic.
# Then assert (a) the rendered centre tracks the model within 2px and (b) the trace
# is monotone on each arm — a sawtooth from polyline joins would break both.
print("\n=== RIPPLE CHECK (rendered curve vs analytic quartic) ===")
# Coefficients high->low: [a4,a3,a2,a1,a0] (order of build/slide_028.js).
LEFT_FIT = (1.257813992130e-06, -1.380428744223e-03, 5.367079591099e-01, -8.662429049860e+01, 5.186743353907e+03)
RIGHT_FIT = (1.280248111588e-06, -3.212513553308e-03, 2.991242381533e+00, -1.224430887994e+03, 1.862054178402e+05)
def model(f, x):
    y = 0.0
    for v in f: y = y * x + v          # Horner, matches the JS build
    return y
for nm, f, x0, x1, vx in [('LEFT ', LEFT_FIT, 161, 383, 275), ('RIGHT', RIGHT_FIT, 514, 737, 628)]:
    # (a) PRESENCE: for every column, some blue run must sit within 5px of the
    #     analytic prediction -> the curve is complete, continuous and un-offset.
    # (b) MONOTONICITY: trace the run nearest the model and assert the y-centre
    #     moves monotonically in the arm's direction (a parabola is monotone per
    #     arm); wobbles beyond ~5% would be polyline-join sawtooth.
    worst = 0.0
    trace = []
    missing = []
    # Markers are discs sitting ON the curve, same colour: they flatten the trace
    # into plateaux and can hide the true centre. Restrict the trace to the y
    # window around the model +/- 10px so neither a marker plateau nor the box
    # border can be picked as "the curve".
    for x in range(x0, x1 + 1):
        ylo = max(0, cv(model(f, x)) - cv(10))
        yhi = min(r.shape[0], cv(model(f, x)) + cv(10))
        col = np.where(blue[ylo:yhi, cv(x)])[0]
        if not len(col):
            missing.append(x)
            continue
        col = col + ylo
        runs = []; s = col[0]; p = col[0]
        for y in col[1:]:
            if y - p > 1: runs.append((s, p)); s = y
            p = y
        runs.append((s, p))
        pred = cv(model(f, x))
        # Nearest EDGE of any blue run: a dot marker straddling the prediction
        # cannot mask a displaced curve, and a displaced curve cannot hide behind one.
        def edge_gap(t):
            if t[0] <= pred <= t[1]:
                return 0          # the run straddles the prediction
            return min(abs(t[0] - pred), abs(t[1] - pred))
        d = min(edge_gap(t) for t in runs)
        worst = max(worst, d)
        best = min(runs, key=lambda t: abs((t[0] + t[1]) / 2 - pred))
        trace.append((x, (best[0] + best[1]) / 2))
    Y = np.array([t[1] for t in trace]); X = np.array([t[0] for t in trace])
    dy = np.diff(Y)
    arm = np.where(X[:-1] <= vx, 1, -1)
    # A marker disc flattens the trace: a zero step is not a direction violation.
    nz = dy != 0
    wob = float((np.sign(dy[nz]) != arm[nz]).sum()) / max(int(nz.sum()), 1)
    print(f"  {nm}: cols traced={len(trace)} missing-cols={missing}  "
          f"worst ink-gap from quartic={worst:.0f}px (150dpi)")
    print(f"        monotone-wobble={wob:.1%} (zero-step marker plateaux ignored)  "
          f"max adjacent step={np.abs(dy[nz]).max():.0f}px")
    if worst > 5:
        fails.append(f'{nm} curve off the analytic quartic by {worst:.0f}px')
    # The draw endpoints (x0/x1) antialias against white, so their first step
    # can land outside the cyan mask. Allow the two end columns only.
    interior = [x for x in missing if x not in (x0, x1)]
    if interior:
        fails.append(f'{nm} curve has gaps at interior columns {interior[:8]}')
    if wob > 0.05:
        fails.append(f'{nm} curve sawtooth {wob:.0%}')

# ── 5. band ink present ──
for nm, (x0, y0, x1, y1) in {
    'title': (0, 72, 960, 100),
    'heading L': (216, 176, 396, 208),
    'heading R': (565, 176, 745, 208),
    'Loss L': (114, 214, 152, 234),
    'Loss R': (466, 211, 504, 231),
    'xlabel L': (243, 450, 377, 470),
    'xlabel R': (578, 446, 712, 466),
}.items():
    n = content[cv(y0):cv(y1), cv(x0):cv(x1)].sum()
    print(f"  {nm:9s} ink={n}")
    if n == 0:
        fails.append(f'no ink in {nm} band')

print("\n=== RESULT ===")
if fails:
    print("FAIL:", fails); sys.exit(1)
print("SELF-CHECK PASS — containment, white interior, red axes, smooth analytic curves")
