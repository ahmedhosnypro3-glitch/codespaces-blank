import json
from PIL import Image

im = Image.open('unique_slides/slide_018.jpg').convert('RGB')
W, H = im.size
px = im.load()

def scan(pred, box, label):
    x0, y0, x1, y1 = box
    hits = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(px[x, y]):
                hits.append((x, y))
    if not hits:
        print(label, 'NO HITS')
        return []
    # cluster by 12px proximity
    clusters = []
    for p in hits:
        for c in clusters:
            if abs(p[0] - c[0][0]) < 12 and abs(p[1] - c[0][1]) < 12:
                c.append(p)
                break
        else:
            clusters.append([p])
    out = []
    for c in clusters:
        xs = [p[0] for p in c]
        ys = [p[1] for p in c]
        out.append({'n': len(c), 'x0': min(xs), 'x1': max(xs),
                    'y0': min(ys), 'y1': max(ys)})
    out.sort(key=lambda d: d['x0'])
    print(label, json.dumps(out))
    return out

mag = lambda p: p[0] > 130 and p[2] > 110 and p[1] < 90
red = lambda p: p[0] > 130 and p[1] < 80 and p[2] < 90
dark = lambda p: sum(p) < 330

scan(mag, (360, 150, 560, 215), 'MAGENTA lower band')
scan(red, (360, 150, 560, 215), 'RED lower band')
scan(dark, (360, 185, 560, 212), 'DARK ink lower band')
scan(mag, (360, 60, 900, 150), 'MAGENTA diagram band')
scan(dark, (360, 185, 430, 210), 'DARK text near first magenta')
