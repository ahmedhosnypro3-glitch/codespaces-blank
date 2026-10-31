#!/usr/bin/env python3
"""PIL adjudication for slide 006: underline scope + ink geometry (original vs renders)."""
from PIL import Image

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/'


def load(p, scale=1.0):
    im = Image.open(p).convert('RGB')
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    return im


def classify(px):
    r, g, b = px
    if r > 110 and r < 225 and g < 80 and b < 80:
        return 'red'
    if b > 110 and r < 110 and g < 140:
        return 'blue'
    return None


def report(path, label):
    im = load(path)
    W, H = im.size
    px = im.load()
    boxes = {'red': [W, H, -1, -1], 'blue': [W, H, -1, -1]}
    rows_blue = {}
    for y in range(H):
        for x in range(W):
            c = classify(px[x, y])
            if not c:
                continue
            b = boxes[c]
            if x < b[0]:
                b[0] = x
            if y < b[1]:
                b[1] = y
            if x > b[2]:
                b[2] = x
            if y > b[3]:
                b[3] = y
            if c == 'blue':
                rows_blue.setdefault(y, []).append(x)
    print(f'--- {label} ({W}x{H})')
    for c, b in boxes.items():
        if b[2] < 0:
            print(f'  {c}: none')
        else:
            print(f'  {c} ink bbox x{b[0]}..{b[2]} y{b[1]}..{b[3]} '
                  f'(norm x {b[0]/W:.3f}..{b[2]/W:.3f}, y {b[1]/H:.3f}..{b[3]/H:.3f})')
    # underline strokes: rows where blue pixels form short horizontal runs below text
    ys = sorted(rows_blue)
    print('  blue row spans (y, count, xmin..xmax):')
    for y in ys:
        xs = rows_blue[y]
        runs = []
        s = p = xs[0]
        for x in xs[1:]:
            if x - p > 3:
                runs.append((s, p))
                s = x
            p = x
        runs.append((s, p))
        if y > (b := boxes['blue'][1]) and len(runs) and max(r[1] - r[0] for r in runs) < (W * 0.5):
            if any(r[1] - r[0] > 3 for r in runs):
                print(f'    y={y} n={len(xs)} runs={runs[:6]}')


report(NS + 'unique_slides/slide_006.jpg', 'ORIGINAL slide_006.jpg 960x540')
report(NS + 'qa/slide006/rejudge/b03/render_b03-1.png', 'RENDER v1 (certified) 2001x1125')
report(NS + 'qa/slide006/rejudge/b03/render_v3-1.png', 'RENDER v3 (new) 2001x1125')
