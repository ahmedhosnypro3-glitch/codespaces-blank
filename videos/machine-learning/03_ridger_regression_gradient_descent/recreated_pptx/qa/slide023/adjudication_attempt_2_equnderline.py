#!/usr/bin/env python3
# ADJ: eq_zoom crop-pair MAJOR #1 "missing underline on the final Y".
# Question: does the ORIGINAL truly underline the terminal Y, and did the JUDGED
# render_1.png omit it (real defect) or does render_1 already match (judge false-POSITIVE)?
# Also compare the CURRENT 22:05-rebuilt eq asset vs what is inside render_1.png.
import numpy as np
from PIL import Image

P = 'videos/machine-learning/03_ridger_regression_gradient_descent'
QA = f'{P}/recreated_pptx/qa/slide023'

RC = np.asarray(Image.open(f'{QA}/crop_1_eq_zoom_render.png').convert('RGB')).astype(np.int16)
OC = np.asarray(Image.open(f'{QA}/crop_1_eq_zoom_orig.png').convert('RGB')).astype(np.int16)
print('eq_zoom crop sizes  render', RC.shape, ' orig', OC.shape)

def inkbar_rows(a):
    # dark ink mask (near-black text/strokes)
    lum = a[..., 0] + a[..., 1] + a[..., 2]
    return lum < 420

def rightmost_underline(a, tag):
    h, w, _ = a.shape
    # rightmost 16% of the crop width = terminal "... X^T Y" region
    x0 = int(w * 0.84)
    sub = a[:, x0:, :]
    mask = inkbar_rows(sub)
    rows = mask.sum(axis=1)
    tw = sub.shape[1]
    # an underline = a row whose dark-run covers > 60% of the symbol width in one bar
    # report the widest single-row dark run and its y
    best = (0, -1)
    for yy in range(mask.shape[0]):
        row = mask[yy]
        # longest contiguous dark run in this row
        cur = bestr = 0
        for v in row:
            cur = cur + 1 if v else 0
            if cur > bestr:
                bestr = cur
        if bestr > best[0]:
            best = (bestr, yy)
    frac = best[0] / max(1, tw)
    print(f'  {tag:8s} rightmost-band w={tw}: widest single-row dark run = {best[0]} px '
          f'({frac*100:.0f}% of band) at crop-y {best[1]} / H {h}')
    return best, frac

print('== terminal-Y underline scan (rightmost band) ==')
br, fr = rightmost_underline(RC, 'RENDER')
bo, fo = rightmost_underline(OC, 'ORIGINAL')

print()
print('== per-y dark-run profile near the baseline of the terminal symbol ==')
def profile(a, tag):
    h, w, _ = a.shape
    x0 = int(w * 0.84)
    mask = inkbar_rows(a[:, x0:, :])
    tw = mask.shape[1]
    print(f'  {tag}: (band width {tw}) rows with dark-run >= 40% of band:')
    for yy in range(mask.shape[0]):
        row = mask[yy]
        cur = bestr = 0
        for v in row:
            cur = cur + 1 if v else 0
            if cur > bestr:
                bestr = cur
        if bestr >= 0.40 * tw:
            print(f'     y={yy:3d}  run={bestr} ({bestr/tw*100:.0f}%)')
profile(RC, 'RENDER')
profile(OC, 'ORIGINAL')

print()
print('== does the CURRENT (22:05) eq asset already carry the Y underline? ==')
eq = np.asarray(Image.open(f'{P}/recreated_pptx/build/assets/eq_023_main.png').convert('RGBA'))
print('  eq_023_main.png size', eq.shape[:2])
alpha = eq[..., 3]
rgb = eq[..., :3]
dark = (alpha > 40) & ((rgb[..., 0] + rgb[..., 1] + rgb[..., 2]) < 420)
w = dark.shape[1]
x0 = int(w * 0.84)
prof = dark[:, x0:].sum(axis=1)
tw = w - x0
print(f'  asset rightmost-band width {tw}; rows with dark-fill >= 40% band (underline bars):')
for yy in range(dark.shape[0]):
    if prof[yy] >= 0.40 * tw:
        print(f'     y={yy:3d} fill={prof[yy]} ({prof[yy]/tw*100:.0f}%)')
