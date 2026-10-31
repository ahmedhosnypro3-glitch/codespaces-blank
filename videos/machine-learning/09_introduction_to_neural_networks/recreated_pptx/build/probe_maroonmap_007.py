"""Fine maroon map of slide 007 panel (3px cells) to read axes, lines, arrowheads."""
from PIL import Image
import numpy as np

SRC = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
maroon = (R > 140) & (R - G > 70) & (R - B > 70)
pink = (R > 150) & (R - G > 40) & (R - G < 70) & (R - B > 30)

for y in range(108, 502, 4):
    row = ''
    for x in range(150, 764, 3):
        if maroon[y, x]:
            row += '#'
        elif pink[y, x]:
            row += '~'
        else:
            row += '.'
    print(f'{y:3d} {row}')
print('    ' + ''.join(str((150 + i * 3) // 100 % 10) for i in range(205)))
