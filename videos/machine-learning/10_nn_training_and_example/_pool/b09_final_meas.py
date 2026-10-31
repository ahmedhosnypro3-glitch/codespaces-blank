# b09: final precise measurements for slide_018 rebuild.
from PIL import Image
import numpy as np

A = np.asarray(Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_018.jpg').convert('RGB')).astype(int)

def bbox(x0, y0, x1, y1, pred, label):
    ys, xs = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(A[y, x]): ys.append(y); xs.append(x)
    if not ys: print(f'{label:28s} EMPTY'); return None
    print(f'{label:28s} x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)}  w={max(xs)-min(xs)+1} h={max(ys)-min(ys)+1}')
    return (min(xs), min(ys), max(xs), max(ys))

dark = lambda c: c[0] < 120 and c[1] < 120 and c[2] < 120
green = lambda c: c[1] - c[0] > 18 and c[1] > 120 and c[2] < c[1] - 15
blue = lambda c: c[2] > 90 and c[2] - c[0] > 45 and c[2] - c[1] > 45 and c[0] < 150
red = lambda c: c[0] > 110 and c[0] - c[1] > 55 and c[0] - c[2] > 40
mag = lambda c: c[0] > 90 and c[1] < 90 and c[2] > 80 and c[0] - c[1] > 45 and c[2] - c[1] > 40

print('--- class label column (x774..828) ---')
bbox(774, 74, 828, 96, green, 'class1 green text')
bbox(774, 100, 828, 125, dark, 'class2 dark text')
bbox(774, 126, 828, 150, dark, 'class2b dark text')
bbox(774, 150, 828, 178, dark, 'classm dark text')
bbox(774, 100, 828, 178, dark, 'class2+2m dark all')

print('--- output label column (x700..750) ---')
bbox(700, 74, 750, 96, blue, 'output1 blue')
bbox(700, 112, 750, 138, blue, 'output2 blue')
bbox(700, 155, 750, 182, blue, 'output3 blue')

print('--- error bar red row profile (x758..773) ---')
runs, cur = [], None
for y in range(60, 200):
    n = sum(1 for x in range(758, 774) if red(A[y, x]))
    if n:
        if cur and y == cur[1] + 1: cur[1] = y
        else:
            if cur: runs.append(cur)
            cur = [y, y]
    else:
        if cur: runs.append(cur); cur = None
if cur: runs.append(cur)
print('red row runs:', runs)
for a, b in runs:
    xs = [x for y in range(a, b + 1) for x in range(758, 774) if red(A[y, x])]
    print(f'  y{a}-{b} x{min(xs)}-{max(xs)} h={b-a+1}')

print('--- magenta elements ---')
bbox(366, 186, 380, 204, mag, 'bottomleft circle')
bbox(492, 172, 520, 204, mag, 'mid circle')
bbox(582, 180, 608, 204, mag, 'right circle')
bbox(376, 190, 408, 202, mag, 'bottomleft text')
print('--- green bottom rect ---')
bbox(552, 184, 576, 208, green, 'bottom green rect')
print('--- panel edges ---')
for y in (70, 100, 140, 195):
    xs = [x for x in range(340, 800) if abs(A[y, x][0]-218) < 12 and abs(A[y, x][1]-206) < 12 and abs(A[y, x][2]-194) < 12]
    if xs: print(f'cream row y={y}: x{min(xs)}-{max(xs)}')
for x in (370, 500, 740):
    ys = [y for y in range(40, 230) if abs(A[y, x][0]-218) < 12 and abs(A[y, x][1]-206) < 12 and abs(A[y, x][2]-194) < 12]
    if ys: print(f'cream col x={x}: y{min(ys)}-{max(ys)}')
print('--- rose line ---')
bbox(896, 60, 906, 210, lambda c: c[0] > 170 and c[0] - c[1] > 20 and c[1] - c[2] < 40 and c[2] > 130, 'rose vert line')
print('--- up arrows / white arrow ---')
bbox(455, 180, 490, 208, lambda c: c[0] < 190 and c[1] < 190 and c[2] < 190, 'dark arrow region')
