"""Fine maps of red-family ink in the original slide 007 panel."""
from PIL import Image
import numpy as np

SRC = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
pure = (R > 215) & (G < 130) & (B < 130)          # #ff0000-ish lines/arrowheads
maroon = (R > 150) & (R < 220) & (G < 90) & (B < 90)  # #c00000 borders/axes

def show(mask, label):
    print(f'=== {label} ===')
    for y in range(112, 500, 4):
        print(f'{y:3d} ' + ''.join('#' if mask[y, x] else '.' for x in range(152, 764, 4)))
    print('    ' + ''.join('|' if ((152 + i * 4) % 100) == 0 else ' ' for i in range(153)))

show(pure, 'PURE RED (lines, dots, arrowheads)')
show(maroon, 'MAROON (borders, axes)')
