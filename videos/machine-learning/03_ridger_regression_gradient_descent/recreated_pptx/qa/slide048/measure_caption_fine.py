from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'
S = 2001 / 960

orig = Image.open(f'{deck}/unique_slides/slide_048.jpg').convert('RGB')
r10 = Image.open(f'{deck}/recreated_pptx/qa/slide048/render_10.png').convert('RGB')

def profile(img, x0, x1, y0, y1, thr=170, scale=1.0, label=''):
    px = img.load()
    print(f'== {label} x{x0}..{x1} y{y0}..{y1} ==')
    prev = False
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if sum(px[x, y][:3]) / 3 < thr)
        if n:
            os = f' orig-space y{y/scale:.0f}' if scale != 1.0 else ''
            print(f'  y{y} ink={n}{os}')

# caption hunt: left column top area
profile(orig, 60, 300, 25, 55, label='ORIG caption zone')
