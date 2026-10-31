"""Extract exact geometry of slide 007's diagram: colors, dots, lines, hatches, axes."""
from PIL import Image
import numpy as np
from scipy import ndimage

SRC = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def bbox(mask, label, min_size=40):
    m = mask.copy()
    m[:115] = False
    m[493:] = False
    m[:, :152] = False
    m[:, 760:] = False
    lab, n = ndimage.label(m)
    objs = ndimage.find_objects(lab)
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    out = []
    for i, sl in enumerate(objs):
        if sizes[i] < min_size:
            continue
        ys, xs = sl
        out.append((int(sizes[i]), (xs.start, xs.stop - 1, ys.start, ys.stop - 1)))
    out.sort(reverse=True)
    print(f'--- {label}: {len(out)} blobs')
    for s, bb in out[:40]:
        print(f'    n={s:6d} bbox x{bb[0]}-{bb[1]} y{bb[2]}-{bb[3]}')


yellow = (R > 230) & (G > 230) & (B < 120)
bbox(yellow, 'YELLOW (C labels + badge)', min_size=200)

darkred = (R > 110) & (R - G > 60) & (R - B > 60) & (G < 90)
bbox(darkred, 'DARK RED (lines, arrowheads, dots)', min_size=60)

brightgreen = (G > 150) & (G - R > 80) & (G - B > 80)
bbox(brightgreen, 'GREEN (dots, labels, line)', min_size=60)

brightblue = (B > 150) & (B - R > 80) & (B - G > 60)
bbox(brightblue, 'BLUE (dots, labels, line)', min_size=60)

pink = (R > 165) & (R < 240) & (G > 60) & (G < 170) & (B > 70) & (B < 190) & (R - G > 45) & (R - B > 35)
bbox(pink, 'PINK hatch', min_size=200)

ltgreen = (R > 190) & (G > 230) & (B > 170) & (B < 245) & (R - B > 20)
bbox(ltgreen, 'LIGHT GREEN hatch', min_size=200)

ltblue = (B > 215) & (R > 140) & (R < 215) & (G > 140) & (G < 220) & (B - R > 40)
bbox(ltblue, 'LIGHT BLUE hatch', min_size=200)
