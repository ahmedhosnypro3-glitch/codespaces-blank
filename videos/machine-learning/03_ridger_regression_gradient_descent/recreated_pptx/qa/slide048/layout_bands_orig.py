from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'
orig = Image.open(f'{deck}/unique_slides/slide_048.jpg').convert('RGB')
px = orig.load()

bands = []
cur = None
gap = 0
for y in range(25, 535):
    n = sum(1 for x in range(58, 902) if sum(px[x, y][:3]) / 3 < 170)
    if n:
        if cur is None:
            cur = [y, y, n]
        else:
            cur[1] = y
            cur[2] += n
    else:
        if cur:
            gap += 1
            if gap >= 3:
                bands.append(tuple(cur))
                cur = None
                gap = 0
        else:
            gap = 0
if cur:
    bands.append(tuple(cur))

for y0, y1, n in bands:
    # horizontal extent of this band
    xs = [x for x in range(58, 902) for yy in (range(y0, y1 + 1)) if sum(px[x, yy][:3]) / 3 < 170]
    print(f'y{y0}..{y1} ink={n} x{min(xs)}..{max(xs)}')
