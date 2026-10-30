import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(DECK + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)

RED = lambda c: c[0] > 90 and c[0]-c[1] > 35 and c[0]-c[2] > 35
L = lambda c: 0.299*c[0] + 0.587*c[1] + 0.114*c[2]


def red_runs(arr, axis, fixed, lo, hi):
    out, st = [], None
    for i in range(lo, hi):
        c = arr[fixed, i] if axis == "row" else arr[i, fixed]
        v = RED(c)
        if v and st is None: st = i
        elif not v and st is not None: out.append((st, i-1)); st = None
    if st is not None: out.append((st, hi-1))
    return out


print("=== vertical RED runs ===")
for fx in [573, 574, 809, 810]:
    print("  col x=%d: red y-runs (55..340): %s" % (fx, red_runs(o, "col", fx, 55, 340)))
print("=== horizontal RED runs ===")
for fy in [66, 67, 300, 301, 302, 303, 304, 305]:
    print("  row y=%d: red x-runs (565..820): %s" % (fy, red_runs(o, "row", fy, 565, 820)))

print("\n=== dark ink map inside plot box (x575..807) by row band ===")
for y0 in range(60, 320, 10):
    sub = o[y0:y0+10, 575:808]
    Lm = L(sub)
    dark = (Lm < 140).sum()
    # classify
    redm = np.zeros(Lm.shape, bool)
    for dx in range(sub.shape[1]):
        for dy in range(sub.shape[0]):
            redm[dy, dx] = RED(sub[dy, dx])
    print("  y %3d..%3d: dark=%5d red=%5d" % (y0, y0+9, dark, int(redm.sum())))

print("\n=== locate dark TEXT ink in x560..815, y266..310 ===")
sub = o[266:310, 560:815]
Lm = L(sub)
m = Lm < 140
# column profile -> glyph runs
prof = m.sum(axis=0)
on = prof > 0
runs, st = [], None
for i, v in enumerate(on):
    if v and st is None: st = i
    elif not v and st is not None: runs.append((st, i-1)); st = None
if st is not None: runs.append((st, len(on)-1))
print("  dark runs x (frame px):", [(560+a, 560+b) for a, b in runs])
rs = np.nonzero(m.sum(axis=1))[0]
if len(rs):
    print("  dark rows y (frame px): %d..%d" % (266+rs.min(), 266+rs.max()))

print("\n=== vertical GRID lines (gray, x 575..807) full column scan y 66..300 ===")
GRID = lambda c: abs(int(c[0])-204) < 30 and abs(int(c[1])-204) < 30 and abs(int(c[2])-204) < 30
for fx in range(575, 809):
    col = o[66:300, fx]
    cnt = sum(1 for c in col if GRID(c))
    if cnt > 60:
        print("  x=%d grid-ish count %d" % (fx, cnt))
