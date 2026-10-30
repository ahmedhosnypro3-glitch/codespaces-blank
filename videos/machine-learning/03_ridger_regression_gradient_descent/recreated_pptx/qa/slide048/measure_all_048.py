from PIL import Image

deck = 'videos/machine-learning/03_ridger_regression_gradient_descent'
im = Image.open(f'{deck}/unique_slides/slide_048.jpg').convert('RGB')
px = im.load()

def yext(x0, x1, y0, y1, thr=170):
    ys = [y for y in range(y0, y1) if any(sum(px[x, y][:3]) / 3 < thr for x in range(x0, x1))]
    return (ys[0], ys[-1]) if ys else None

print('== per-row content y-extents (thr<170) ==')
bands = [(139, 197), (197, 272), (272, 330), (330, 395), (404, 461), (461, 528)]
for i, (b0, b1) in enumerate(bands, start=1):
    w_ = yext(694, 710, b0, b1)
    eq = yext(711, 718, b0, b1)
    lp = yext(719, 726, b0, b1)
    dg = yext(727, 742, b0, b1)
    rp = yext(743, 750, b0, b1)
    vt = yext(600, 614, b0, b1)
    dxb = yext(377, 404, b0, b1)      # dx high-bracket bars
    tri = yext(330, 380, b0, b1)      # bare triplet
    print(f'row{i} band {b0}..{b1}: W={w_} =: {eq} lp={lp} digits={dg} rp={rp} verdict={vt} dxbars={dxb} triplet={tri}')

print('== aug title zone x72..248 y140..166: rows + color ==')
for y in range(140, 166):
    xs = [x for x in range(72, 248) if sum(px[x, y][:3]) / 3 < 190]
    if xs:
        samples = [px[x, y] for x in xs[::max(1, len(xs)//5)]][:5]
        print(f'  y{y}: n={len(xs)} x{xs[0]}..{xs[-1]} sample={samples[0]}')

print('== Initial-W underline band x355..440 y66..80 (thr<210) ==')
for y in range(66, 80):
    xs = [x for x in range(355, 440) if sum(px[x, y][:3]) / 3 < 210]
    if xs:
        runs, cur = [], None
        for x in xs:
            if cur and x == cur[1] + 1: cur[1] = x
            else:
                cur = [x, x]; runs.append(cur)
        print(f'  y{y}: ' + ' '.join(f'{a}-{b}' if a != b else str(a) for a, b in runs))

print('== row1 green-ish census x735..800 y145..200 (G-R>10 and G-B>10) ==')
g = [(x, y) for x in range(735, 800) for y in range(145, 200)
     if px[x, y][1] - px[x, y][0] > 10 and px[x, y][1] - px[x, y][2] > 10]
xs = sorted(set(x for x, y in g)); ys = sorted(set(y for x, y in g))
print(f'bbox x{xs[0] if xs else "-"}..{xs[-1] if xs else "-"} y{ys[0] if ys else "-"}..{ys[-1] if ys else "-"} n={len(g)}')
if g:
    cl = {}
    for x, y in g:
        cl.setdefault(x // 5 * 5, []).append((x, y))
    for k in sorted(cl):
        sub = cl[k]
        print(f'  x{k}..{k+4}: n={len(sub)} y{min(y for _, y in sub)}..{max(y for _, y in sub)}')

print('== row1 red-ish census x668..712 y158..180 (R-G>40) ==')
r = [(x, y) for x in range(668, 712) for y in range(158, 180)
     if px[x, y][0] - px[x, y][1] > 40]
xs = sorted(set(x for x, y in r))
print('red x-cols:', xs)

print('== row1 stroke columns detail x640..670, x700..725 ==')
for x0, x1 in ((640, 670), (700, 725)):
    print(f' zone x{x0}..{x1}:')
    for x in range(x0, x1):
        ys = [y for y in range(145, 200) if sum(px[x, y][:3]) / 3 < 170]
        if ys:
            runs, cur = [], None
            for y in ys:
                if cur and y == cur[1] + 1: cur[1] = y
                else:
                    cur = [y, y]; runs.append(cur)
            print(f'  x{x}: ' + ' '.join(f'{a}-{b}' if a != b else str(a) for a, b in runs))
