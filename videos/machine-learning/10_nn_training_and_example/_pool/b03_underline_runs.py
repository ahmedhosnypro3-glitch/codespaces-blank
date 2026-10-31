#!/usr/bin/env python3
"""Precise horizontal underline-run detection in original slide_006 subtitle band."""
from PIL import Image

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/'
im = Image.open(NS + 'unique_slides/slide_006.jpg').convert('RGB')
W, H = im.size
px = im.load()


def dark_blue(x, y):
    r, g, b = px[x, y]
    return b > 90 and b - r > 45 and g < 120


print('horizontal dark-blue runs >=8px, rows y=344..362 (original 960x540):')
for y in range(344, 363):
    runs = []
    x = 190
    while x < 740:
        if dark_blue(x, y):
            s = x
            while x < 740 and dark_blue(x, y):
                x += 1
            if x - s >= 8:
                runs.append((s, x - 1, x - s))
        else:
            x += 1
    if runs:
        print(f'  y={y}: ' + ' '.join(f'{a}-{b}({w})' for a, b, w in runs))

print()
print('audit word map for reference: "previous" 378-475, "output" 578-652, text 198-723')
