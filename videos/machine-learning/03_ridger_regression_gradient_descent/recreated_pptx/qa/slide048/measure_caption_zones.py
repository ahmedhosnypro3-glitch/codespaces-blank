from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'

def bands(img, x0, x1, y0, y1, thr=170):
    px = img.load()
    out = []
    cur = None
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if sum(px[x, y][:3]) / 3 < thr)
        if n:
            if cur is None:
                cur = [y, y, n]
            else:
                cur[1] = y
                cur[2] += n
        else:
            if cur:
                out.append(tuple(cur))
                cur = None
    if cur:
        out.append(tuple(cur))
    return out

orig = Image.open(f'{deck}/unique_slides/slide_048.jpg').convert('RGB')
r10 = Image.open(f'{deck}/recreated_pptx/qa/slide048/render_10.png').convert('RGB')
print('orig', orig.size, 'render', r10.size)

print('== ORIG x60..600 y40..210 text bands ==')
for y0, y1, n in bands(orig, 60, 600, 40, 210):
    print(f'  y{y0}..{y1} ink={n}')

print('== RENDER10 x60*2.084..600*2.084 y40..210 (render px) ==')
for y0, y1, n in bands(r10, int(60 * 2.084), int(600 * 2.084), int(40 * 2.084), int(210 * 2.084)):
    print(f'  y{y0}..{y1} ink={n}  orig-space y{y0/2.084:.1f}..{y1/2.084:.1f}')
