from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'
im = Image.open(f'{deck}/unique_slides/slide_048.jpg').convert('RGB')
px = im.load()

def wprofile(label, x0, x1, y0, y1):
    print(f'== {label} x{x0}..{x1} y{y0}..{y1} (thr<200) ==')
    rows = []
    for y in range(y0, y1):
        xs = [x for x in range(x0, x1) if sum(px[x, y][:3]) / 3 < 200]
        if xs:
            rows.append((y, len(xs), xs[0], xs[-1]))
    if not rows:
        print('  none'); return
    ytop, ybot = rows[0][0], rows[-1][0]
    for y, n, a, b in rows:
        print(f'  y{y}: n={n} x{a}..{b}')

# rows 2-6 bands from handoff: (197,272)(272,330)(330,395)(404,461)(461,528)
# W column at x697..706; W sits in upper-middle of each band
for i, (b0, b1) in enumerate([(197, 272), (272, 330), (330, 395), (404, 461), (461, 528)], start=2):
    wprofile(f'row {i} W', 694, 710, b0 + 15, b0 + 45)

# row 1 W for side-by-side
wprofile('row 1 W', 615, 631, 160, 182)
