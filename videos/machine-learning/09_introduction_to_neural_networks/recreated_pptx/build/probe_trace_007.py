"""Trace the blue and green decision lines in slide 007's original (frame px)."""
from PIL import Image
import numpy as np

SRC = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
blue = (B > 140) & (B - R > 80) & (B - G > 60)
green = (G > 110) & (G - R > 60) & (G - B > 50)

SKIP = [(495, 435, 560, 500), (300, 320, 340, 365), (610, 120, 700, 200),
        (240, 150, 305, 250), (305, 130, 325, 445)]
DOTS_B = [(681, 314), (636, 353), (512, 359), (567, 359), (676, 362), (512, 389), (636, 392), (567, 408), (606, 408)]
DOTS_G = [(397, 175), (464, 175), (464, 220), (530, 254), (464, 265), (412, 266), (412, 299)]


def near_dot(x, y, dots, r=14):
    return any((x - cx) ** 2 + (y - cy) ** 2 < r * r for cx, cy in dots)


def trace(mask, name, seed_x, seed_y, dots):
    print(f'--- {name}')
    prev = seed_y
    for x in range(seed_x, 145, -5):
        col = np.where(mask[115:492, x])[0] + 115
        col = [int(y) for y in col if abs(y - prev) < 22 and not near_dot(x, y, dots)
               and not any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in SKIP)]
        if col:
            y = int(np.mean(col))
            prev = y
            print(f'  x={x} y={y}')
    print('  ...upward')
    prev = seed_y
    for x in range(seed_x, 770, 5):
        col = np.where(mask[115:492, x])[0] + 115
        col = [int(y) for y in col if abs(y - prev) < 22 and not near_dot(x, y, dots)
               and not any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in SKIP)]
        if col:
            y = int(np.mean(col))
            prev = y
            print(f'  x={x} y={y}')


trace(blue, 'BLUE d2(x)', 500, 330, DOTS_B)
trace(green, 'GREEN d1(x)', 420, 308, DOTS_G)
