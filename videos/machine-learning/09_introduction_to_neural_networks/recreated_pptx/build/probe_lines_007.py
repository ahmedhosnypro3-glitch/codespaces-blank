"""Robust line fits + panel border for slide 007 (original frame px)."""
from PIL import Image
import numpy as np

SRC = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

PANEL = (151, 113, 760, 495)
DOTS = {  # cx, cy, r
    'r': [(380, 362), (371, 393), (344, 393), (344, 420), (380, 420)],
    'g': [(397, 175), (464, 175), (464, 220), (530, 254), (464, 265), (412, 266), (412, 299)],
    'b': [(681, 314), (636, 353), (512, 359), (567, 359), (676, 362), (512, 389), (636, 392), (567, 408), (606, 408)],
}
EXCLUDE = [  # x0,y0,x1,y1 boxes to drop (labels, arrowheads, axes)
    (240, 165, 305, 245),   # red d3 label
    (305, 130, 325, 155),   # y-axis arrowhead
    (305, 425, 530, 448),   # x-axis
    (300, 130, 320, 440),   # y-axis
    (495, 435, 560, 500),   # red arrowhead + ve
    (300, 320, 335, 365),   # green arrowhead
    (610, 120, 700, 200),   # blue arrowhead + d2 label
]


def excluded(x, y):
    for x0, y0, x1, y1 in EXCLUDE:
        if x0 <= x <= x1 and y0 <= y <= y1:
            return True
    return False


def fit_line(mask, name, xrange=None):
    xs, ys = [], []
    for x in range(PANEL[0], PANEL[2]):
        if xrange and not (xrange[0] <= x <= xrange[1]):
            continue
        col = np.where(mask[:, x])[0]
        col = col[(col >= PANEL[1]) & (col <= PANEL[3])]
        for y in col:
            if excluded(x, y):
                continue
            xs.append(x)
            ys.append(y)
    xs = np.array(xs, float)
    ys = np.array(ys, float)
    # per-column median to suppress thick blobs, then least squares
    ux = np.unique(xs)
    mx = []
    my = []
    for x in ux:
        v = ys[xs == x]
        if len(v):
            mx.append(x)
            my.append(np.median(v))
    mx = np.array(mx, float)
    my = np.array(my, float)
    m, c = np.polyfit(mx, my, 1)
    resid = my - (m * mx + c)
    print(f'{name}: slope={m:.4f} intercept={c:.2f} rms={resid.std():.2f} '
          f'x={int(mx.min())}..{int(mx.max())} ncols={len(mx)}')
    print(f'    endpoints: ({int(mx.min())},{m*mx.min()+c:.0f}) -> ({int(mx.max())},{m*mx.max()+c:.0f})')
    return m, c


red = (R > 130) & (R - G > 60) & (R - B > 60)
green = (G > 120) & (G - R > 60) & (G - B > 60)
blue = (B > 120) & (B - R > 60) & (B - G > 50)

fit_line(red, 'RED d3(x)', (260, 500))
fit_line(green, 'GREEN d1(x)', (170, 730))
fit_line(blue, 'BLUE d2(x)', (240, 620))

print()
print('panel border scan: columns with >250 non-white px in y 118..490')
nonwhite = (a.sum(axis=2) < 720)
for x in range(140, 775):
    c = int(nonwhite[118:490, x].sum())
    if c > 250:
        print('  col x=', x, 'n=', c)
print('rows with >450 non-white px in x 155..758')
for y in range(105, 505):
    c = int(nonwhite[y, 155:758].sum())
    if c > 450:
        print('  row y=', y, 'n=', c)
