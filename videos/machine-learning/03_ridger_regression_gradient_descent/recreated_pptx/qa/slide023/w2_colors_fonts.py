#!/usr/bin/env python3
"""w2 colour census + font-size fits. READ-ONLY on the frame."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from collections import Counter

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)

F = {'r': '/usr/share/fonts/TTF/Arial.TTF', 'b': '/usr/share/fonts/TTF/Arialbd.TTF',
     'i': '/usr/share/fonts/TTF/Ariali.TTF', 'bi': '/usr/share/fonts/TTF/Arialbi.TTF'}


def hx(c):
    return ''.join('%02X' % max(0, min(255, int(round(v)))) for v in c)


def modal(y0, y1, x0, x1, n=4, step=1):
    seg = a[y0:y1 + 1, x0:x1 + 1:step].reshape(-1, 3)
    return Counter(map(tuple, seg.tolist())).most_common(n)


def dark_core(y0, y1, x0, x1, frac=0.3):
    """median colour of the darkest frac of pixels (halo-excluded text colour)."""
    seg = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3).astype(int)
    lum = seg.sum(axis=1)
    k = max(8, int(len(seg) * frac))
    sel = seg[np.argsort(lum)[:k]]
    return tuple(int(v) for v in np.median(sel, axis=0))


print("== FILLS (text-free interior modal) ==")
print("  green box  y150..180 x300..700 :", modal(150, 180, 300, 700))
print("  blue  box  y350..420 x150..850 :", modal(350, 420, 150, 850))
print("  yellow box y460..520 x300..860 :", modal(460, 520, 300, 860))
print("  panel gray y60..100  x300..700 :", modal(60, 100, 300, 700))
print("== BORDERS ==")
print("  green top   y110..111 x300..600:", modal(110, 111, 300, 600))
print("  green left  x98..99  y160..190:", modal(160, 190, 98, 99))
print("  green right x754..755 y160..190:", modal(160, 190, 754, 755))
print("  green bot   y218..219 x300..600:", modal(218, 219, 300, 600))
print("  blue top    y228..229 x300..600:", modal(228, 229, 300, 600))
print("  blue left   x88..89  y300..400:", modal(300, 400, 88, 89))
print("  blue right  x867..869 y300..400:", modal(300, 400, 867, 869))
print("  blue bot    y425..426 x300..600:", modal(425, 426, 300, 600))
print("  yell top    y435..436 x300..600:", modal(435, 436, 300, 600))
print("  yell left   x86..87  y460..520:", modal(460, 520, 86, 87))
print("  yell right  x873..875 y460..520:", modal(460, 520, 873, 875))
print("  yell bot    y529..531 x300..600:", modal(529, 531, 300, 600))
print("== TEXT CORES (darkest 30% median) ==")
for name, y0, y1, x0, x1 in [
        ("title", 76, 106, 220, 655), ("recall", 115, 140, 104, 178),
        ("dim1", 194, 216, 104, 394), ("dim2 red part", 194, 214, 655, 750),
        ("blue L1", 240, 262, 98, 840), ("blue L2", 274, 296, 97, 840),
        ("blue L3", 308, 330, 97, 761), ("ex L1 black", 362, 384, 96, 520),
        ("ex L1 red", 362, 384, 527, 578), ("ex L2 black", 396, 418, 96, 186),
        ("ex L2 red", 396, 418, 187, 328), ("sol label", 447, 465, 97, 177),
        ("sol L1", 476, 494, 246, 710), ("sol L2", 504, 521, 313, 649)]:
    print(f"  {name:16s} core={dark_core(y0, y1, x0, x1)}  hex={hx(dark_core(y0, y1, x0, x1))}")

print("\n== FONT SIZE FITS (total advance vs measured ink width) ==")
CASES = [
    ("title", "Inverse of High Dimension Matrix", 435),
    ("recall", "Recall:", 74),
    ("dim1", "if Feature vectors are of dimension d", 290),
    ("dim2", "(X^T X) is of size d+1 x d+1", 308),
    ("blueL1", "The standard matrix inversion algorithm has a time complexity of O(n^3),", 741),
    ("blueL2", "which means that the computation time increases rapidly with the size of the matrix", 744),
    ("blueL3", "(increasing cubically with the number of components).", 665),
    ("exL1", "For Example: if Features vector is of size 1000 then Inverse", 758),
    ("exL2", "calculation is or order 1,000,000,000 which is impractical", 446),
    ("solLab", "Solution:", 80),
    ("solL1", "Instead of using Least Squares with Matrix inversion,", 465),
    ("solL2", "use Gradient Descent iterative solution", 336),
]
for name, text, w in CASES:
    best = []
    for st in F:
        for s in np.arange(10, 46, 0.25):
            f = ImageFont.truetype(F[st], int(s * 8))
            d = ImageDraw.Draw(Image.new('L', (10, 10)))
            adv = d.textlength(text, font=f) / 8.0
            best.append((abs(adv - w), s, st, adv))
    best.sort()
    print(f"  {name:8s} w={w}: " + "  ".join(f"{st}{s:.2f}pt(adv={a:.0f},d={e:.1f})" for e, s, st, a in best[:3]))
