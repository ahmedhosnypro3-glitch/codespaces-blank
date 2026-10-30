import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
nonwhite = (r < 245) | (g < 245) | (b < 245)

# The three row bands (from label boxes at y96..125 upper; and W brackets at
# y126..253 / y265..389 / y402..528).
BANDS = [(126, 253), (265, 390), (402, 528)]

for bi, (y0, y1) in enumerate(BANDS, 1):
    print(f"===== ROW BAND {bi}: y{y0}..{y1} =====")
    seg = nonwhite[y0:y1 + 1, 165:470]
    cnt = seg.sum(axis=0)
    # vertical gridlines = columns whose ink spans most of the band height
    h = y1 - y0 + 1
    cols = np.where(cnt > h * 0.5)[0]
    # group
    groups = []
    if len(cols):
        s = p = cols[0]
        for x in cols[1:]:
            if x - p <= 3:
                p = x
            else:
                groups.append((s, p))
                s = p = x
        groups.append((s, p))
    print("  vlines:", [(165 + a, 165 + c) for a, c in groups])

    # horizontal gridlines
    seg2 = nonwhite[y0:y1 + 1, 165:470]
    cnt2 = seg2.sum(axis=1)
    rows = np.where(cnt2 > 250)[0]
    groups2 = []
    if len(rows):
        s = p = rows[0]
        for y in rows[1:]:
            if y - p <= 3:
                p = y
            else:
                groups2.append((s, p))
                s = p = y
        groups2.append((s, p))
    print("  hlines:", [(y0 + a, y0 + c) for a, c in groups2])

# right test tables
print()
for bi, (y0, y1) in enumerate(BANDS, 1):
    print(f"===== TEST BAND {bi}: y{y0}..{y1} x700..880 =====")
    seg = nonwhite[y0:y1 + 1, 700:880]
    cnt = seg.sum(axis=0)
    h = y1 - y0 + 1
    cols = np.where(cnt > h * 0.5)[0]
    groups = []
    if len(cols):
        s = p = cols[0]
        for x in cols[1:]:
            if x - p <= 3:
                p = x
            else:
                groups.append((s, p))
                s = p = x
        groups.append((s, p))
    print("  vlines:", [(700 + a, 700 + c) for a, c in groups])
    cnt2 = seg.sum(axis=1)
    rows = np.where(cnt2 > 60)[0]
    groups2 = []
    if len(rows):
        s = p = rows[0]
        for y in rows[1:]:
            if y - p <= 3:
                p = y
            else:
                groups2.append((s, p))
                s = p = y
        groups2.append((s, p))
    print("  hlines:", [(y0 + a, y0 + c) for a, c in groups2])
