"""PIL-first adjudication of slide 004 defects (attempt 5 fix lane).
1px = 1pt on unique_slides/slide_004.jpg (960x540).
"""
from PIL import Image
import numpy as np

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide004/render_4.png"
S = 2001/960.0  # render px per frame px

o = Image.open(ORIG).convert("RGB")
r = Image.open(REND).convert("RGB")
og = np.asarray(o.convert("L"))
a = np.asarray(o).astype(int)


def dark_rows(arr, x0, x1, y0, y1, thr=128):
    sub = arr[y0:y1, x0:x1] < thr
    res = []
    for yy in range(sub.shape[0]):
        s = int(sub[yy].sum())
        if s > 0:
            res.append((yy + y0, s))
    return res


def bbox(arr, x0, x1, y0, y1, thr=128):
    sub = arr[y0:y1, x0:x1] < thr
    ys, xs = np.nonzero(sub)
    if len(ys) == 0:
        return None
    return (int(xs.min()) + x0, int(ys.min()) + y0,
            int(xs.max()) + x0, int(ys.max()) + y0)


def seg_rows(arr, x0, x1, y0, y1, gap=3, thr=128):
    """contiguous row bands containing ink, separated by >=gap empty rows"""
    rows = dark_rows(arr, x0, x1, y0, y1, thr)
    bands = []
    cur = None
    for y, s in rows:
        if cur is None or y - cur[1] < gap:
            cur = [cur[0] if cur else y, y]
        else:
            bands.append(tuple(cur)); cur = [y, y]
    if cur: bands.append(tuple(cur))
    return bands


def col_bands(arr, x0, x1, y0, y1, gap=4, thr=128):
    sub = arr[y0:y1, x0:x1] < thr
    colsum = sub.sum(axis=0)
    bands = []
    cur = None
    for x in range(len(colsum)):
        if colsum[x] > 0:
            if cur is None or x - cur[1] < gap:
                cur = [cur[0] if cur is not None else x, x]
            else:
                bands.append((cur[0]+x0, cur[1]+x0)); cur = [x, x]
        else:
            if cur is not None and x - cur[1] >= gap:
                bands.append((cur[0]+x0, cur[1]+x0)); cur = None
    if cur is not None:
        bands.append((cur[0]+x0, cur[1]+x0))
    return bands


def hexs(vals, k=3):
    seen = {}
    for v in vals:
        seen[v] = seen.get(v, 0) + 1
    out = sorted(seen.items(), key=lambda t: -t[1])[:k]
    return [(c, n) for c, n in out]


print("=" * 70)
print("A. TOP-BOX INK LAYOUT — ORIGINAL")
print("=" * 70)
for name, bx0, bx1 in [("LEFT 'Let Y' box", 80, 396), ("RIGHT 'Let Yhat' box", 427, 746)]:
    print(f"\n--- {name} x{bx0}..{bx1} y99..222 ---")
    bands = seg_rows(og, bx0, bx1, 99, 222)
    print("row bands:", bands)
    for (by0, by1) in bands:
        bb = bbox(og, bx0, bx1, by0, by1 + 2)
        print(f"  band y{by0}..{by1}  bbox={bb}")
        cb = col_bands(og, bx0, bx1, by0, by1 + 2)
        print(f"     col bands (gap4): {cb}")

print()
print("=" * 70)
print("B. COLOR ROLE — per band, dominant saturated colors")
print("=" * 70)
for name, bx0, bx1 in [("LEFT", 80, 396), ("RIGHT", 427, 746)]:
    sub = a[99:222, bx0:bx1]
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    red_mask = (R > 120) & (R - G > 60) & (R - B > 60)
    blue_mask = (B > 120) & (B - R > 40) & (B - G > 20)
    print(f"{name}: red-ish {int(red_mask.sum())}px  blue-ish {int(blue_mask.sum())}px")
    # where is red ink?
    if red_mask.any():
        ys, xs = np.nonzero(red_mask)
        print(f"   red bbox x{xs.min()+bx0}..{xs.max()+bx0} y{ys.min()+99}..{ys.max()+99}")
    if blue_mask.any():
        ys, xs = np.nonzero(blue_mask)
        print(f"   blue bbox x{xs.min()+bx0}..{xs.max()+bx0} y{ys.min()+99}..{ys.max()+99}")

print()
print("=" * 70)
print("C. SUBSCRIPT CASE — left vector")
print("=" * 70)
# vector subscript should be at the lower right of the paren stack
sub = og[150:215, 150:260] < 140
ys, xs = np.nonzero(sub)
if len(ys):
    print("ink in x150..260 y150..215:", len(ys), "bbox x", xs.min()+150, xs.max()+150, "y", ys.min()+150, ys.max()+150)
    for y in range(ys.min()+150, ys.max()+151):
        row = og[y, 150:260] < 140
        if row.any():
            print("  y", y, "cols", [int(c+150) for c in np.nonzero(row)[0]])
else:
    print("no ink; widen")
