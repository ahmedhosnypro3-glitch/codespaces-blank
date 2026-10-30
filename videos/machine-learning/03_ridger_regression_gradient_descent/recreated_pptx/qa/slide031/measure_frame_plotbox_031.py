import numpy as np
from PIL import Image

im = Image.open('unique_slides/slide_031.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

# ---- 1. plot borders: full-span dark lines within the plot hull ----
# hull from white-region scan
dark = a.sum(axis=2) < 330          # near-black
sub = dark[60:275, 570:815]
cc = sub.sum(axis=0)
rr = sub.sum(axis=1)
print('=== vertical near-black columns (x, count) ===')
for i, c in enumerate(cc):
    if c > 60:
        print('  x=%d count=%d' % (570 + i, c))
print('=== horizontal near-black rows (y, count) ===')
for i, c in enumerate(rr):
    if c > 60:
        print('  y=%d count=%d' % (60 + i, c))

# ---- 2. grid lines: gray ~ (170-220) with flat channels ----
grayish = (abs(a[:, :, 0] - a[:, :, 1]) < 12) & (abs(a[:, :, 1] - a[:, :, 2]) < 12) \
          & (a[:, :, 0] > 170) & (a[:, :, 0] < 225)
sub2 = grayish[68:268, 575:810]
cc2 = sub2.sum(axis=0)
rr2 = sub2.sum(axis=1)
print('=== gray vertical grid candidates (x, count) ===')
for i, c in enumerate(cc2):
    if c > 100:
        print('  x=%d count=%d' % (575 + i, c))
print('=== gray horizontal grid candidates (y, count) ===')
for i, c in enumerate(rr2):
    if c > 100:
        print('  y=%d count=%d' % (68 + i, c))

# ---- 3. green point (5,1) and red point (3,9) ----
def cluster(mask, name):
    ys, xs = np.nonzero(mask)
    if not len(xs):
        print('  %s: NOT FOUND' % name)
        return
    print('  %s: bbox x %d..%d y %d..%d  center (%.0f,%.0f) n=%d'
          % (name, xs.min(), xs.max(), ys.min(), ys.max(),
             xs.mean(), ys.mean(), len(xs)))

print('=== point clusters (plot region) ===')
reg = np.zeros((H, W), bool)
reg[60:280, 560:830] = True
g = (a[:, :, 1] > 90) & (a[:, :, 0] < 110) & (a[:, :, 2] < 110) & reg      # green
r = (a[:, :, 0] > 140) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90) & reg       # red
b = (a[:, :, 2] > 120) & (a[:, :, 0] < 90) & (a[:, :, 1] < 110) & reg      # blue
cluster(g, 'green')
cluster(r, 'red')
cluster(b, 'blue (parabola)')

# ---- 4. black horizontal segment from (3,9) to (7,9) ----
# find rows inside the plot whose dark run is long but not full-width
print('=== partial dark horizontal runs (segment candidates) ===')
for y in range(70, 268):
    row = dark[y, 575:810]
    # longest run
    best = 0; cur = 0; start = 0; beststart = 0
    for i, v in enumerate(row):
        if v:
            if cur == 0:
                start = i
            cur += 1
            if cur > best:
                best = cur; beststart = start
        else:
            cur = 0
    if 40 < best < 200:
        print('  y=%d  run len=%d  x %d..%d' % (y, best, 575 + beststart, 575 + beststart + best - 1))
