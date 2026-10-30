from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'

def wprof(label, path, x0, x1, y0, y1, scale=1.0):
    im = Image.open(path).convert('RGB')
    px = im.load()
    print(f'== {label} x{x0}..{x1} y{y0}..{y1} ==')
    for oy in range(y0, y1):
        y = int(oy * scale)
        xs = [int(x / scale) for x in range(int(x0 * scale), int(x1 * scale))
              if sum(px[x, y][:3]) / 3 < 200]
        if xs:
            print(f'  y{oy}: n={len(xs)} x{xs[0]}..{xs[-1]}')

# 051 aug-box "Initial W" label zone (handoff: x296..326 y74..95)
wprof('051 orig aug W', f'{deck}/unique_slides/slide_051.jpg', 294, 330, 72, 92)
# 049 aug-box "Initial W" label zone (certified build: underline x365..422 = Initial only)
wprof('049 orig aug W', f'{deck}/unique_slides/slide_049.jpg', 360, 428, 60, 90)
