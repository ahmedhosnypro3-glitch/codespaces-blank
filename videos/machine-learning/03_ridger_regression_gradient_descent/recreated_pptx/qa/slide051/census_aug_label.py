from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'
im = Image.open(f'{deck}/unique_slides/slide_051.jpg').convert('RGB')
px = im.load()

print('== 051 aug label per-column spans x288..336 y70..92 (thr<200) ==')
cols = {}
for x in range(288, 336):
    ys = [y for y in range(70, 92) if sum(px[x, y][:3]) / 3 < 200]
    if ys:
        cols[x] = (min(ys), max(ys), len(ys))

runs = []
cur = None
for x in range(288, 336):
    if x in cols:
        cur = [x, x] if cur is None else [cur[0], x]
    else:
        if cur:
            runs.append(cur); cur = None
if cur:
    runs.append(cur)
for a, b in runs:
    ymin = min(cols[x][0] for x in range(a, b + 1) if x in cols)
    ymax = max(cols[x][1] for x in range(a, b + 1) if x in cols)
    print(f'  x{a}..{b} y{ymin}..{ymax}')

print('== per-row detail y82..90 ==')
for y in range(82, 90):
    xs = [x for x in range(288, 336) if sum(px[x, y][:3]) / 3 < 200]
    if xs:
        print(f'  y{y}: n={len(xs)} x{xs[0]}..{xs[-1]}')
