#!/usr/bin/env python3
"""Clean ink-profile comparison: original's disputed cells vs its own agreed cells.

For each cell we compute a horizontal ink profile (per-column ink count inside
the cell's y-line band) and compare the *shape* of the disputed profile against
the profiles of cells with known content. Zero-assumption: no font rendering,
no threshold gymnastics — just comparing the original to itself.
"""
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
A = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
L = A.mean(axis=2)

# .bg estimate per cell = median of the band's background (lightest 40%)
def profile(x0, y0, x1, y1, pad=1):
    reg = L[y0:y1, x0:x1]
    bg = np.percentile(reg, 60)          # band interior is mostly background
    return (reg < bg - 40).astype(int)   # ink mask at a fixed contrast margin


def show(x0, y0, x1, y1, label):
    m = profile(x0, y0, x1, y1)
    cols = m.sum(axis=0)
    print(f"  {label:22s} ink={m.sum():4d} profile={list(cols)}")


print("=" * 110)
print("Y-LINE ink profiles (original frame px), one profile per test cell")
print("=" * 110)

# geometry
NOREG = (207, 377)
R3 = (391, 637)
R10 = (649, 892)
XTW = 58.0

def boxes(xa, xb):
    return [(int(xa + i * XTW) + 2, int(xa + (i + 1) * XTW) - 2) for i in range(3)]

# y-line bands: measured text-line bands per group (midpoints of the last line band)
YB = {
    (1,): (258, 268), (2,): (365, 376), (3,): (474, 485),
}
GROUPS = [1, 2, 3]

KNOWN = {
    ("NOREG", 1): ["y=60", "y=80", "y=100"],
    ("R3", 1): ["y=59", "y=78.7", "y=98.4"],
    ("R3", 2): ["y=34.1", "y=45.1", "y=56.1"],
    ("R3", 3): ["y=26.2", "y=34.4", "y=42.5"],
    ("R10", 1): ["y=57.4", "y=76.5", "y=95.6"],
    ("R10", 2): ["y=34.6", "y=46", "y=57.4"],
    ("R10", 3): ["y=26.8", "y=35.4", "y=44.1"],
}

allcells = {}
for cn, (xa, xb) in [("NOREG", NOREG), ("R3", R3), ("R10", R10)]:
    bx = boxes(xa, xb)
    for gi in GROUPS:
        y0, y1 = YB[(gi,)]
        for bi, (a, b) in enumerate(bx):
            allcells[(cn, gi, bi)] = (a, b, y0, y1)

print("\n--- KNOWN cells (all lanes agree) ---")
for (cn, gi), vals in KNOWN.items():
    for bi, v in enumerate(vals):
        a, b, y0, y1 = allcells[(cn, gi, bi)]
        show(a, y0, b, y1, f"{cn} g{gi} b{bi+1} [{v}]")

print("\n--- DISPUTED cells (NOREG g2: hypA 60/80/100 | hypB 32.4/42.3/52.3) ---")
for bi in range(3):
    a, b, y0, y1 = allcells[("NOREG", 2, bi)]
    show(a, y0, b, y1, f"NOREG g2 b{bi+1}")

print("\n--- DISPUTED cells (NOREG g3: hypA 60/80/100 | hypB 24.4/31.2/38) ---")
for bi in range(3):
    a, b, y0, y1 = allcells[("NOREG", 3, bi)]
    show(a, y0, b, y1, f"NOREG g3 b{bi+1}")

print("\n--- reference: 3-digit values (y=100, y=98.4, y=95.6) for ink magnitude ---")
for key, v in [(("NOREG", 1, 2), "y=100"), (("R3", 1, 2), "y=98.4"), (("R10", 1, 2), "y=95.6")]:
    a, b, y0, y1 = allcells[key]
    show(a, y0, b, y1, f"{key[0]} g{key[1]} b{key[2]+1} [{v}]")

print("\n--- reference: 2-digit values (y=60, y=80, y=59, y=46) ---")
for key, v in [(("NOREG", 1, 0), "y=60"), (("NOREG", 1, 1), "y=80"),
               (("R3", 1, 0), "y=59"), (("R10", 2, 1), "y=46"),
               (("R3", 2, 1), "y=45.1"), (("R10", 2, 1), "y=46")]:
    a, b, y0, y1 = allcells[key]
    show(a, y0, b, y1, f"{key[0]} g{key[1]} b{key[2]+1} [{v}]")

print("\n--- summary: total ink per cell ---")
print("  known 3-digit (y=100/98.4/95.6):",
      [profile(*allcells[k][:2], allcells[k][2], allcells[k][3]).sum()
       for k in [("NOREG",1,2),("R3",1,2),("R10",1,2)]])
print("  known 2-digit (y=60/80/59/46):",
      [profile(*allcells[k][:2], allcells[k][2], allcells[k][3]).sum()
       for k in [("NOREG",1,0),("NOREG",1,1),("R3",1,0),("R10",2,1)]])
print("  known 4-char+dp (y=78.7/34.1/57.4):",
      [profile(*allcells[k][:2], allcells[k][2], allcells[k][3]).sum()
       for k in [("R3",1,1),("R3",2,0),("R10",1,0),("R10",2,0),("R3",2,2),("R10",2,2)]])
print("  DISPUTED NOREG g2:", [profile(*allcells[("NOREG",2,b)][:2], allcells[("NOREG",2,b)][2], allcells[("NOREG",2,b)][3]).sum() for b in range(3)])
print("  DISPUTED NOREG g3:", [profile(*allcells[("NOREG",3,b)][:2], allcells[("NOREG",3,b)][2], allcells[("NOREG",3,b)][3]).sum() for b in range(3)])
