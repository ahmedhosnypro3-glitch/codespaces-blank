#!/usr/bin/env python3
"""ASCII map of the subtitle underline band: original vs v1/v3 renders."""
from PIL import Image

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/'


def band(path, x0, x1, y0, y1, step, label):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    px = im.load()
    print(f'=== {label} band x{x0}-{x1} y{y0}-{y1} step{step} (image {W}x{H})')
    for y in range(y0, y1 + 1, step):
        row = ''
        for x in range(x0, x1 + 1, step):
            best = 0
            for yy in range(y, min(y + step, y1 + 1)):
                for xx in range(x, min(x + step, x1 + 1)):
                    r, g, b = px[xx, yy]
                    sat = b - r
                    if sat > 40 and b > 100:
                        best = max(best, sat)
            row += '#' if best > 120 else ('+' if best > 60 else ('.' if best > 25 else ' '))
        print(f'  y{y:4d} |{row}|')


band(NS + 'unique_slides/slide_006.jpg', 190, 740, 326, 356, 2, 'ORIGINAL slide_006')
band(NS + 'qa/slide006/rejudge/b03/render_b03-1.png', 560, 1430, 322, 368, 5, 'RENDER v1')
band(NS + 'qa/slide006/rejudge/b03/render_v3-1.png', 560, 1430, 322, 368, 5, 'RENDER v3')
