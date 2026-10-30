#!/usr/bin/env python3
# Tight terminal-Y underline measurement in the eq_zoom crop pair.
# Strategy: locate the rightmost glyph cluster's ink columns, then for the region
# spanning its last ~20 columns, print the vertical ink-row profile of BOTH crops so a
# thin underline bar under the glyph (present in ORIG, absent in RENDER) is visible.
import numpy as np
from PIL import Image

P = 'videos/machine-learning/03_ridger_regression_gradient_descent'
QA = f'{P}/recreated_pptx/qa/slide023'

RC = np.asarray(Image.open(f'{QA}/crop_1_eq_zoom_render.png').convert('RGB')).astype(np.int16)
OC = np.asarray(Image.open(f'{QA}/crop_1_eq_zoom_orig.png').convert('RGB')).astype(np.int16)

def lum(a):
    return a[..., 0] + a[..., 1] + a[..., 2]

def colcounts(a, thr=420):
    m = lum(a) < thr
    return m.sum(axis=0), m  # per-column ink pixel count

def vertical_window(a, tag):
    m = lum(a) < 420
    colink = m.sum(axis=0)
    w = m.shape[1]
    # find last column with a solid glyph (>=6 ink px tall)
    solid = np.where(colink >= 6)[0]
    x_last = int(solid[-1]) if len(solid) else w - 1
    x0 = max(0, x_last - 24)
    print(f'--- {tag}: last solid glyph column x={x_last}; examine columns {x0}..{x_last} ---')
    sub = m[:, x0:x_last + 1]
    prof = sub.sum(axis=1)
    for yy in range(sub.shape[0]):
        bar = int(prof[yy])
        glyph = '#' * min(40, bar)
        if bar > 0:
            print(f'   y={yy:3d} {bar:3d} {glyph}')
    print()

vertical_window(RC, 'RENDER')
vertical_window(OC, 'ORIGINAL')
