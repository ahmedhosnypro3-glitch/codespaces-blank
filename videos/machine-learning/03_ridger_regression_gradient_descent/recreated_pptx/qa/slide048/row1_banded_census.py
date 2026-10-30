from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'
orig = Image.open(f'{deck}/unique_slides/slide_048.jpg').convert('RGB')
px = orig.load()

def runs_x(x0, x1, y0, y1, thr=170):
    out = []
    cur = None
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if sum(px[x, y][:3]) / 3 < thr)
        if n:
            if cur is None:
                cur = [x, x]
            else:
                cur[1] = x
        else:
            if cur:
                out.append(tuple(cur))
                cur = None
    if cur:
        out.append(tuple(cur))
    return out

print('== row1 three y-bands, x640..815, thr<170 ==')
for label, y0, y1 in (('TOP', 148, 163), ('MID', 164, 177), ('BOT', 178, 194)):
    print(f'{label} y{y0}..{y1}:', runs_x(640, 815, y0, y1))

print('== W-underline check x615..645 y172..190, thr<210 ==')
for y in range(172, 190):
    cnt = [(x, px[x, y]) for x in range(615, 645) if sum(px[x, y][:3]) / 3 < 210]
    if cnt:
        print(f'  y{y}: n={len(cnt)} x{cnt[0][0]}..{cnt[-1][0]}')

print('== green census x740..790 y145..200 (R<130, G>110) ==')
g = [(x, y) for x in range(740, 790) for y in range(145, 200)
     if px[x, y][0] < 130 and px[x, y][1] > 110 and px[x, y][2] < 130]
if g:
    xs = sorted(set(x for x, y in g)); ys = sorted(set(y for x, y in g))
    print(f'green bbox x{xs[0]}..{xs[-1]} y{ys[0]}..{ys[-1]} n={len(g)}')
else:
    print('none')

print('== green-sample colors ==')
for x, y in g[:6]:
    print(f'  ({x},{y}) {px[x, y]}')
