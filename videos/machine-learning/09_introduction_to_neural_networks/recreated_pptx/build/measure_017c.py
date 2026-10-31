"""Precise geometry for slide 017: callout box extents, text spans, curve endpoints."""
from PIL import Image
import numpy as np

P = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
     "09_introduction_to_neural_networks/unique_slides/slide_017.jpg")
a = np.asarray(Image.open(P).convert("RGB")).astype(int)


def scanline(y, x0, x1, bg=None):
    out = []
    prev = None
    for x in range(x0, x1):
        c = tuple(a[y, x])
        if c != prev:
            out.append((x, c))
            prev = c
    return out


def vscan(x, y0, y1):
    out = []
    prev = None
    for y in range(y0, y1):
        c = tuple(a[y, x])
        if c != prev:
            out.append((y, c))
            prev = c
    return out


def edges(xs, thresh):
    """Group a boolean profile into runs, print run boundaries."""
    runs = []
    st = None
    for i, v in enumerate(xs):
        if v and st is None:
            st = i
        elif not v and st is not None:
            runs.append((st, i - 1))
            st = None
    if st is not None:
        runs.append((st, len(xs) - 1))
    return [r for r in runs if r[1] - r[0] + 1 >= thresh]


# --- callout box 1 (top right): scan row y=181 for the fill
row = a[181, 560:920]
m = (row[:, 0] > 200) & (row[:, 0] - row[:, 2] > 5)
print("box1 row181 runs:", edges(m, 8))
col = a[150:220, 700]
m2 = (col[:, 0] > 200) & (col[:, 0] - col[:, 2] > 5)
print("box1 col700 runs:", [(r[0] + 150, r[1] + 150) for r in edges(m2, 4)])

# --- bottom-left box: scan row y=466
row = a[466, 90:450]
m = (row[:, 0] > 200) & (row[:, 0] - row[:, 2] > 5)
print("boxBL row466 runs:", edges(m, 8))
col = a[430:505, 300]
m2 = (col[:, 0] > 200) & (col[:, 0] - col[:, 2] > 5)
print("boxBL col300 runs:", [(r[0] + 430, r[1] + 430) for r in edges(m2, 4)])

# --- bottom-right box: scan row y=466
row = a[466, 450:790]
m = (row[:, 0] > 200) & (row[:, 0] - row[:, 2] > 5)
print("boxBR row466 runs:", edges(m, 8))
col = a[430:505, 640]
m2 = (col[:, 0] > 200) & (col[:, 0] - col[:, 2] > 5)
print("boxBR col640 runs:", [(r[0] + 430, r[1] + 430) for r in edges(m2, 4)])

# --- callout fill color (clean interior samples)
for lbl, pt in [("box1 fill", (700, 190)), ("box1 fill2", (860, 181)),
                ("boxBL fill", (400, 450)), ("boxBR fill", (715, 450)),
                ("bg", (700, 300)), ("panel fill", (400, 130))]:
    print(lbl, pt, tuple(a[pt[1], pt[0]]))

# --- text spans in bottom-left box: red ink (prefix F(x) = and values),
#     black ink (label + conditions), row by row
sub = a[440:495, 105:425].astype(int)
rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
red = (rr - gg > 40) & (rr - bb > 40)
blk = (rr < 100) & (gg < 100) & (bb < 100)
for name, m in (("red", red), ("black", blk)):
    prof = m.sum(axis=1)
    print("boxBL", name, "rows>2:", [(i + 440, int(prof[i])) for i in range(len(prof)) if prof[i] > 2])
    prof = m.sum(axis=0)
    print("boxBL", name, "cols>1:", [(i + 105, int(prof[i])) for i in range(len(prof)) if prof[i] > 1])
