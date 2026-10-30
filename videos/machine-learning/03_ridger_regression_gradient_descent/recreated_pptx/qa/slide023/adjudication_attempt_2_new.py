#!/usr/bin/env python3
# Template-A attempt_2 new MINORs, PIL-first (960x540 frame, 1px=1pt).
# Render is 150dpi 2001x1125 -> render_px = frame_px * (1125/540) = 2.08333...
import math
from PIL import Image
import numpy as np

P = 'videos/machine-learning/03_ridger_regression_gradient_descent'
QA = f'{P}/recreated_pptx/qa/slide023'
S = 1125.0 / 540.0  # render px per frame px

orig = Image.open(f'{P}/unique_slides/slide_023.jpg').convert('RGB')
rend = Image.open(f'{QA}/render_1.png').convert('RGB')
O = np.asarray(orig).astype(np.int16)
R = np.asarray(rend).astype(np.int16)


def render_win(fx0, fy0, fx1, fy1):
    return slice(int(round(fy0*S)), int(round(fy1*S))), slice(int(round(fx0*S)), int(round(fx1*S)))

def frame_win(fx0, fy0, fx1, fy1):
    return slice(fy0, fy1), slice(fx0, fx1)


def is_navy(a):
    return (a[..., 2] > a[..., 0] + 30) & (a[..., 2] > 70) & (a[..., 0] < 120) & (a[..., 1] < 90)


def is_red(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 120) & (r - g > 50) & (r - b > 50)


def longest_run(bools_row):
    best = cur = 0
    for v in bools_row:
        cur = cur + 1 if v else 0
        if cur > best:
            best = cur
    return best


print('==== ADJ-new-A: underline beneath (X^T X) in the dimension line ====')
print('   dim-part2 ink frame-x 505..754, baseline ~211 (banked). Scan a band')
print('   from the text baseline down toward the solve box top (frame-y 216..300).')
# ORIGINAL (frame px)
yi, xi = frame_win(505, 216, 760, 300)
band_o = O[yi, xi]
dark_o = band_o.sum(axis=2) < 380
# thin only: a real underline is a 2-4px tall, >=120px wide dark bar
best_o = (0, 0)
for yy in range(dark_o.shape[0]):
    run = longest_run(dark_o[yy])
    if run > best_o[0]:
        best_o = (run, 216 + yy)
# RENDER (render px). Underline region matches effective scale, any real bar >=120*S px wide.
ys, xs = render_win(505, 216, 760, 300)
band_r = R[ys, xs]
dark_r = (band_r.sum(axis=2) < 380)
run_len = [longest_run(dark_r[yy]) for yy in range(dark_r.shape[0])]
best_r = max(range(len(run_len)), key=lambda k: run_len[k])
print(f'   ORIGINAL: longest dark run in band = {best_o[0]} px at frame-y {best_o[1]}')
print(f'   RENDER  : longest dark run in band = {run_len[best_r]} px at render-y {216+best_r} (frame-eq y {(216+best_r)/S:.1f})')
# a genuine underline here would be >=120 frame px. M5 used 150 as its bar threshold.
print(f'   threshold: an underline bar spanning "(X^T X)" (ink width ~ {754-505} px) is >=120 frame px')
print(f'   -> original {"HAS a bar" if best_o[0] >= 120 else "has NO bar (max run << 120)"}')
print(f'   -> render   {"HAS a bar" if run_len[best_r] >= int(120*S) else "has NO bar (max run < 120*S)"}')

print()
print('==== ADJ-new-B: red/bold "Matrix inversion" highlight in the solution line ====')
print('   solution-box interior frame-x 90..872, frame-y 436..528 (banked M2 window)')
yi, xi = frame_win(90, 436, 872, 528)
sol_o = O[yi, xi]
red_O = int(is_red(sol_o).sum())
navy_O = int(is_navy(sol_o).sum())
ys, xs = render_win(90, 436, 872, 528)
sol_r = R[ys, xs]
red_R = int(is_red(sol_r).sum())
navy_R = int(is_navy(sol_r).sum())
print(f'   RENDER solution interior : red px = {red_R}, navy px = {navy_R}')
print(f'   ORIGINAL solution interior: red px = {red_O}, navy px = {navy_O}')
# Check for any near-reddish or bold-weight break across the whole solution region:
# a bolded word's ink density vs its neighbours on the same line is the weight signal.
print('   -> if the ORIGINAL truly marks "Matrix inversion" red, red_O must be >> 0.')
print(f'   -> original red px = {red_O} => {"RED PRESENT" if red_O > 50 else "NO red highlight in the original"}')

print()
print('==== ADJ-new-B2: robust red-vs-not predicate comparison (recompute M2 window) ====')
# Re-run the exact M2 window to confirm the banked redscan conclusion still holds
for name, img, win in [('ORIGINAL', O, frame_win(90, 436, 872, 528)),
                       ('RENDER',   R, render_win(90, 436, 872, 528))]:
    sub = img[win]
    print(f'   {name:8s} red>{120,r-g>50,r-b>50}={int(is_red(sub).sum()):6d}  '
          f'red>{170,r-g>70,r-b>60}={int((((sub[...,0]>170)&(sub[...,0]-sub[...,1]>70)&(sub[...,0]-sub[...,2]>60))).sum()):6d}')
