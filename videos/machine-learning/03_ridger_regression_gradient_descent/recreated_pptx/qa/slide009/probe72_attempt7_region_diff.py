#!/usr/bin/env python3
"""probe72 — attempt-7 region diff: render_7 vs certified attempt-5 pixels.

Renders being compared (both 150dpi LO, 2001x1125):
  A = certified_attempt5_reconstructed.png (pre_fix_backup_af0598c8.pptx — the
      judge-certified bytes, re-rendered after the original render_5.png gap)
  B = render_7.png (attempt 7 = founder-annotation fix + restored house chrome)

Laws this bank satisfies:
  - eq_left / eq_right / cap_left / cap_right must show 0 changed px, so the
    attempt-5 crop certificates for those four regions remain VALID.
  - annotation zones + any chrome-zone deltas are EXPECTED (owner feedback fix
    + the drifted-then-restored chrome module) and are reported, not scored.

Region map (frame px, 960x540) from selfcheck_attempt_5.py.
"""
import numpy as np
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A = np.asarray(Image.open(os.path.join(HERE, "certified_attempt5_reconstructed.png")).convert("RGB")).astype(int)
B = np.asarray(Image.open(os.path.join(HERE, "render_7.png")).convert("RGB")).astype(int)
print("A certified:", A.shape, " B attempt7:", B.shape)
assert A.shape == B.shape, "size mismatch"
H, W, _ = B.shape
SY, SX = H / 540.0, W / 960.0

changed = (np.abs(A - B).max(axis=2) > 12)
n = int(changed.sum())
print("global changed px (tol 12): %d" % n)

def region(x0, y0, x1, y1):
    X0, Y0, X1, Y1 = int(x0 * SX), int(y0 * SY), int(x1 * SX), int(y1 * SY)
    return changed[Y0:Y1, X0:X1]

REGIONS = {
    "eq_left":     (208, 140, 325, 183),
    "eq_right":    (625, 140, 742, 183),
    "cap_left":    (87, 476, 441, 534),
    "cap_right":   (494, 476, 850, 534),
    "chart_left":  (87, 102, 473, 480),
    "chart_right": (478, 102, 878, 480),
    "annotation_L": (150, 150, 320, 320),
    "annotation_R": (580, 185, 750, 355),
    "badge":       (855, 52, 897, 94),
    "title":       (60, 25, 845, 55),
}

fails = []
print()
print("%-14s %8s" % ("region", "chgd px"))
for k, (x0, y0, x1, y1) in REGIONS.items():
    c = int(region(x0, y0, x1, y1).sum())
    area = int(region(x0, y0, x1, y1).size)
    print("%-14s %8d   (%.2f%% of region)" % (k, c, 100.0 * c / area))
    if k in ("eq_left", "eq_right", "cap_left", "cap_right") and c != 0:
        fails.append(k)

print()
if fails:
    print("VERDICT: FAIL — zero-diff regions changed: %s" % ", ".join(fails))
else:
    print("VERDICT: PASS — eq_left/eq_right/cap_left/cap_right 0 changed px "
          "(attempt-5 crop certificates for those regions remain valid); "
          "all other deltas are the owner-feedback annotation fix and the "
          "restored chrome.")
