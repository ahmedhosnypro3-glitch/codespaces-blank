"""Locate slide 007 panel borders + axes via maroon-density profiles."""
from PIL import Image
import numpy as np

SRC = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
maroon = (R > 140) & (R - G > 70) & (R - B > 70)

print('columns x with >20 maroon px in y 120..480:')
colcount = maroon[120:480, :].sum(axis=0)
prev = False
for x in range(120, 820):
    c = int(colcount[x])
    on = c > 20
    if on:
        print(f'  x={x} n={c}')
print('rows y with >30 maroon px in x 120..780:')
rowcount = maroon[:, 120:780].sum(axis=1)
for y in range(80, 540):
    c = int(rowcount[y])
    if c > 30:
        print(f'  y={y} n={c}')
