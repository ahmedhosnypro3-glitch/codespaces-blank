#!/usr/bin/env python3
"""Map underline runs to words in original slide_006 subtitle (word-gap segmentation)."""
from PIL import Image

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/'
im = Image.open(NS + 'unique_slides/slide_006.jpg').convert('RGB')
px = im.load()


def ink(x, y):
    r, g, b = px[x, y]
    return (r + g + b) < 690 and (b - r) > 30  # blue-ish ink


X0, X1 = 190, 740
# column ink profile over text-body rows
cols = []
for x in range(X0, X1):
    n = sum(1 for y in range(333, 348) if ink(x, y))
    cols.append(n > 3)
# segment into words by gaps >= 7px
words = []
x = 0
while x < len(cols):
    if cols[x]:
        s = x
        gap = 0
        while x < len(cols):
            if not cols[x]:
                gap += 1
                if gap >= 7:
                    break
            else:
                gap = 0
            x += 1
        words.append((X0 + s, X0 + x - 1 - (gap if gap else 0)))
    x += 1
print('word segments (x-range, width):')
ws = []
for a, b in words:
    if b - a >= 6:
        ws.append((a, b))
        print(f'  {a:4d}-{b:4d}  w={b-a+1}')


def runs(row_y, minw=6):
    out = []
    x = X0
    while x < X1:
        c = sum(1 for dx in range(0, 1) for dy in (0, 1) if ink(x + dx, row_y + dy))
        if ink(x, row_y) and (gray(x, row_y)):
            s = x
            while x < X1 and ink(x, row_y) and gray(x, row_y):
                x += 1
            if x - s >= minw:
                out.append((s, x - 1))
        else:
            x += 1
    return out


def gray(x, y):
    r, g, b = px[x, y]
    # underline is dark blue but distinct from glyph: low saturation vs body? keep blue test
    return b - r > 45 and b < 190


print()
print('underline runs y=350:')
ul = runs(350)
print('  ', ul)
print()
print('mapping underline -> overlapped words:')
for a, b in ul:
    hit = [(wa, wb) for wa, wb in ws if not (wb < a or wa > b)]
    cov = []
    for wa, wb in hit:
        ov = max(0, min(b, wb) - max(a, wa) + 1)
        cov.append(f'{wa}-{wb}:{ov}px')
    print(f'  underline {a}-{b} -> {cov}')
