#!/usr/bin/env python3
"""Verify (a) the exact x-extent of each band fill, including the label column,
and (b) the muted-orange band's label-column colour, for slide 033."""
from PIL import Image
import numpy as np, collections

ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg")
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

BANDS = [
    ("D9E275", 217, 226, 119, 334, 367),
    ("D6B2F5", 214, 178, 248, 376, 408),
    ("F7DDC2", 247, 221, 194, 420, 452),
    ("DEAC95", 222, 172, 149, 463, 472),
    ("F7BEC4", 247, 190, 196, 486, 500),
]

for name, R, G, B, y0, y1 in BANDS:
    # x extent of the colour within the band rows, using ANY pixel of that hue
    m = (np.abs(o[:, :, 0] - R) < 26) & (np.abs(o[:, :, 1] - G) < 26) & (np.abs(o[:, :, 2] - B) < 40)
    sub = m[y0:y1 + 1, :]
    colcnt = sub.sum(0)
    filled = np.where(colcnt >= (y1 - y0 + 1) * 0.6)[0]
    print(f"{name} y{y0}-{y1}: filled x-range with >60% rows = "
          f"{filled.min() if len(filled) else '-'}-{filled.max() if len(filled) else '-'}"
          f"  (label col x86-121 fill frac {colcnt[88:120].mean() / (y1 - y0 + 1):.3f})")

print()
print("=== muted-orange band (DEAC95) label column colour ===")
c = collections.Counter()
for y in range(463, 473):
    for x in range(88, 120):
        c[tuple(o[y, x])] += 1
print("  modal:", c.most_common(5))

print()
print("=== row y350 and y392 and y436: what is there (gridline/text)? ===")
for y in [350, 349, 351, 392, 393, 436, 437]:
    cc = collections.Counter(tuple(o[y, x]) for x in range(130, 860, 5))
    print(f"  y{y}: {cc.most_common(2)}")
