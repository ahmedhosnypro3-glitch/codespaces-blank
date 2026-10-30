import sys
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_048.jpg').convert('RGB')
px = im.load()
X0, X1, Y0, Y1 = 600, 815, 140, 200

def ink(x, y, thr=170):
    r, g, b = px[x, y]
    return (r + g + b) / 3 < thr

# per-column ink counts (tall runs = verticals/parens; short = text)
cols = {}
for x in range(X0, X1):
    rows = [y for y in range(Y0, Y1) if ink(x, y)]
    if rows:
        cols[x] = (min(rows), max(rows), len(rows))

# group adjacent columns into runs
runs = []
cur = None
for x in range(X0, X1):
    if x in cols:
        if cur is None:
            cur = [x, x]
        else:
            cur[1] = x
    else:
        if cur:
            runs.append(cur)
            cur = None
if cur:
    runs.append(cur)

print("== column runs (x-range, tallest y-span, total ink) ==")
for a, b in runs:
    ymin = min(cols[x][0] for x in range(a, b + 1) if x in cols)
    ymax = max(cols[x][1] for x in range(a, b + 1) if x in cols)
    tot = sum(cols[x][2] for x in range(a, b + 1) if x in cols)
    # per-column y-spans inside the run (to expose dashed vs solid)
    spans = {}
    for x in range(a, b + 1):
        if x in cols:
            lo, hi, _ = cols[x]
            spans.setdefault((lo, hi), []).append(x)
    print(f"x{a}..{b} y{ymin}..{ymax} ink={tot}")
    for (lo, hi), xs in sorted(spans.items()):
        mark = ''
        if hi - lo >= 20:
            # dashed check: gaps in the column
            gaps = sum(1 for y in range(lo, hi) if not ink(xs[0], y))
            mark = f" tall({'DASHED gaps=' + str(gaps) if gaps > 3 else 'solid'})"
        print(f"   y{lo}..{hi} cols={xs if len(xs) < 8 else str(xs[0]) + '..' + str(xs[-1])}{mark}")

# red census
print("== red px (R>140, G<110, B<110) ==")
reds = [(x, y) for x in range(X0, X1) for y in range(Y0, Y1)
        if px[x, y][0] > 140 and px[x, y][1] < 110 and px[x, y][2] < 110]
if reds:
    xs = sorted(set(x for x, y in reds))
    ys = sorted(set(y for x, y in reds))
    print(f"bbox x{xs[0]}..{xs[-1]} y{ys[0]}..{ys[-1]} n={len(reds)}")
    # cluster by x-gaps
    cl = [[xs[0], xs[0]]]
    for x in xs[1:]:
        if x - cl[-1][1] <= 3:
            cl[-1][1] = x
        else:
            cl.append([x, x])
    for a, b in cl:
        sub = [(x, y) for x, y in reds if a <= x <= b]
        yy = sorted(set(y for x, y in sub))
        print(f"  cluster x{a}..{b} y{yy[0]}..{yy[-1]} n={len(sub)}")
else:
    print("none")
