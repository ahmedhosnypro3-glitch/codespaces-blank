#!/usr/bin/env python3
"""att9 measurement pass 5: W underline check + Iteration-1 box bbox + row-1 left column vs 049 r1."""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
O48 = np.array(Image.open(f"{DECK}/unique_slides/slide_048.jpg").convert("RGB")).astype(int)
O49 = np.array(Image.open(f"{DECK}/unique_slides/slide_049.jpg").convert("RGB")).astype(int)

print("===== 1. 048 row-1 W underline? (x612..634, y172..186) =====")
z = O48[172:187, 610:636]; m = z.sum(axis=2) < 560
ys, xs = np.where(m) if m.any() else (np.array([]), np.array([]))
if len(xs):
    print(f"  ink x{610+xs.min()}..{610+xs.max()} y{172+ys.min()}..{172+ys.max()} npx={m.sum()}")
    rr = m.sum(axis=1)
    print(f"  rows: {[(172+i, int(c)) for i, c in enumerate(rr) if c]}")
else:
    print("  no ink")

print("===== 2. 049 r1 W underline? (x693..725, y170..186) =====")
z = O49[170:187, 691:726]; m = z.sum(axis=2) < 560
ys, xs = np.where(m) if m.any() else (np.array([]), np.array([]))
if len(xs):
    print(f"  ink x{691+xs.min()}..{691+xs.max()} y{170+ys.min()}..{170+ys.max()} npx={m.sum()}")
    rr = m.sum(axis=1)
    print(f"  rows: {[(170+i, int(c)) for i, c in enumerate(rr) if c]}")

print("===== 3. 048 Iteration-1 red box bbox =====")
z = O48[270:315, 75:225]
red = (z[:, :, 0] > z[:, :, 1] + 60) & (z[:, :, 0] > z[:, :, 2] + 60)
ys, xs = np.where(red)
if len(xs):
    print(f"  red fill x{75+xs.min()}..{75+xs.max()} y{270+ys.min()}..{270+ys.max()} npx={red.sum()}")
# white text inside
inner = O48[285:305, 88:212]
wh = inner.sum(axis=2) > 690
ys, xs = np.where(wh) if wh.any() else (np.array([]), np.array([]))
if len(xs):
    print(f"  white text x{88+xs.min()}..{88+xs.max()} y{285+ys.min()}..{285+ys.max()} npx={wh.sum()}")

print("===== 4. 049 r1 left col + triplet (anchor reference, x280..430, y142..200) =====")
z = O49[142:200, 282:428]; m = z.sum(axis=2) < 500
cc = runs = None
import numpy as _np
rr = m.any(axis=1)
ys = [142 + i for i, c in enumerate(rr) if c]
# print per-x-run y bands
for (a, b) in [(run[0], run[1]) for run in
               [(i, j) for i, j in zip(*[_f for _f in [[0]] * 0])]]:
    pass
colsum = m.sum(axis=0)
xruns, s = [], None
for i, v in enumerate(colsum > 0):
    if v and s is None: s = i
    elif not v and s is not None:
        xruns.append((282 + s, 282 + i - 1)); s = None
if s is not None: xruns.append((282 + s, 282 + len(colsum) - 1))
for (a, b) in xruns:
    sub = m[:, a - 282:b - 282 + 1]
    yy, s = [], None
    for i, v in enumerate(sub.any(axis=1)):
        if v and s is None: s = i
        elif not v and s is not None:
            yy.append((142 + s, 142 + i - 1)); s = None
    if s is not None: yy.append((142 + s, 142 + len(sub) - 1))
    print(f"  x{a}..{b} y={yy}")

print("===== 5. 048 r1 '+' '1' '*' full red extent (x670..710, y158..180) =====")
z = O48[140:197, 670:710]
r = (z[:, :, 0] > z[:, :, 1] + 35) & (z[:, :, 0] > z[:, :, 2] + 35) & (z.sum(axis=2) < 660)
ys, xs = np.where(r) if r.any() else (np.array([]), np.array([]))
if len(xs):
    print(f"  red ink x{670+xs.min()}..{670+xs.max()} y{140+ys.min()}..{140+ys.max()} npx={r.sum()}")
    cc = r.any(axis=0)
    xr, s = [], None
    for i, v in enumerate(cc):
        if v and s is None: s = i
        elif not v and s is not None:
            xr.append((670+s, 670+i-1)); s = None
    if s is not None: xr.append((670+s, 670+len(cc)-1))
    print(f"  red x-runs: {xr}")
z2 = O48[140:197, 695:705]
b = z2.sum(axis=2) < 500
ys, xs = np.where(b) if b.any() else (np.array([]), np.array([]))
if len(xs):
    print(f"  '*' black ink x{695+xs.min()}..{695+xs.max()} y{140+ys.min()}..{140+ys.max()} npx={b.sum()}")
