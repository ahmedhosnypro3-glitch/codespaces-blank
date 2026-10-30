#!/usr/bin/env python3
"""Full rule + text-line census of the original with a lower ink threshold."""
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
A = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
L = A.mean(axis=2)
H, W = L.shape

def census_rows(y0, y1, x0, x1, thr, minn, label):
    print(f"\n=== {label} (thr<{thr}, >= {minn} px) ===")
    reg = L[y0:y1, x0:x1] < thr
    for i in range(reg.shape[0]):
        n = reg[i].sum()
        if n >= minn:
            xs = np.where(reg[i])[0]
            # find contiguous spans
            spans = []
            s = xs[0]
            p = xs[0]
            for v in xs[1:]:
                if v - p > 3:
                    spans.append((x0 + s, x0 + p))
                    s = v
                p = v
            spans.append((x0 + s, x0 + p))
            print(f"  y={y0+i}: n={n} spans={spans}")

def census_cols(y0, y1, x0, x1, thr, minn, label):
    print(f"\n=== {label} (thr<{thr}, >= {minn} px) ===")
    reg = L[y0:y1, x0:x1] < thr
    for j in range(reg.shape[1]):
        n = reg[:, j].sum()
        if n >= minn:
            ys = np.where(reg[:, j])[0]
            spans = []
            s = ys[0]; p = ys[0]
            for v in ys[1:]:
                if v - p > 3:
                    spans.append((y0 + s, y0 + p)); s = v
                p = v
            spans.append((y0 + s, y0 + p))
            print(f"  x={x0+j}: n={n} spans={spans}")

# Vertical rules in the table body, lower threshold
census_cols(168, 524, 55, 905, 165, 120, "VERTICAL rules table body")
# Horizontal rules
census_rows(168, 530, 60, 900, 165, 250, "HORIZONTAL rules table body")

print("\n=== TEXT LINE bands: NO REG x130..380 (thr<140, >=3px rows) ===")
reg = L[168:524, 130:380] < 140
rows = reg.sum(axis=1)
cur = None
for i, v in enumerate(rows):
    if v >= 3:
        if cur is None:
            cur = [i, i, v]
        else:
            cur[1] = i; cur[2] = max(cur[2], v)
    else:
        if cur is not None and cur[1] - cur[0] >= 2:
            print(f"  y{168+cur[0]}..{168+cur[1]} (h={cur[1]-cur[0]+1}) maxrow={cur[2]}")
        cur = None
if cur:
    print(f"  y{168+cur[0]}..{168+cur[1]} (h={cur[1]-cur[0]+1}) maxrow={cur[2]}")

print("\n=== TEXT LINE bands: RIDGE3 x384..640 ===")
reg = L[168:524, 384:640] < 140
rows = reg.sum(axis=1)
cur = None
for i, v in enumerate(rows):
    if v >= 3:
        if cur is None:
            cur = [i, i, v]
        else:
            cur[1] = i; cur[2] = max(cur[2], v)
    else:
        if cur is not None and cur[1] - cur[0] >= 2:
            print(f"  y{168+cur[0]}..{168+cur[1]} (h={cur[1]-cur[0]+1}) maxrow={cur[2]}")
        cur = None
if cur:
    print(f"  y{168+cur[0]}..{168+cur[1]} (h={cur[1]-cur[0]+1}) maxrow={cur[2]}")
