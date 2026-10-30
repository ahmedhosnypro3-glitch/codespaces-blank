# PIL adjudication of judge_attempt_4 MINOR findings 4, 5, 6 against the ORIGINAL.
import numpy as np
from PIL import Image

O = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)


def fill(box):
    x0, y0, x1, y1 = box
    reg = O[y0:y1, x0:x1]
    # median of the brightest 60% (text-free interior)
    lum = reg.sum(axis=2)
    thr = np.percentile(lum, 60)
    sel = reg[lum >= thr]
    return tuple(int(v) for v in np.median(sel, axis=0))


print("=== F4: fill colours (original) ===")
print("Objective box x78..302 y242..301 :", fill((85, 248, 295, 296)))
print("Error box     x78..486 y306..365 :", fill((85, 312, 480, 360)))
print("Formula box   x78..486 y464..522 :", fill((85, 470, 480, 517)))
print("Define box    x75..660 y387..448 :", fill((82, 392, 650, 443)))
print("Where box     x494..884 y232..371:", fill((500, 240, 878, 365)))
print("Box1 fill     x80..395 y99..222  :", fill((86, 106, 388, 216)))
print("Remember box  x784..880 y100..152:", fill((788, 104, 876, 148)))
print("build values: PALE FFFDDA(249,253,218) SALMON FAEBD7 PALEBL DBE9FC WHITE FFFFFF")

print("\n=== F5: underline bars (dark-ink horizontal runs in caption bands) ===")


def hruns(box, minlen=6):
    x0, y0, x1, y1 = box
    reg = O[y0:y1, x0:x1]
    m = reg.sum(axis=2) < 400  # dark ink only
    out = []
    for yy in range(m.shape[0]):
        run, s = None, None
        for i, v in enumerate(m[yy]):
            if v and s is None:
                s = i
            elif not v and s is not None:
                if i - s >= minlen:
                    out.append((round((x0 + s) / 1.0, 1), round((x0 + i - 1) / 1.0, 1), y0 + yy))
                s = None
        if s is not None and m.shape[1] - s >= minlen:
            out.append((round((x0 + s) / 1.0, 1), round((x0 + m.shape[1] - 1) / 1.0, 1), y0 + yy))
    # group by row
    byrow = {}
    for a, b, y in out:
        byrow.setdefault(y, []).append((a, b))
    return [(y, v) for y, v in sorted(byrow.items())]


print("-- 'from Model Yhat=XW' band, box2 x569..736 y162..190 (caption + sub-caption) --")
for y, v in hruns((569, 160, 736, 192)):
    print("   y=%d %s" % (y, v))
print("-- 'Yhat = XW' first line of Where block x500..600 y244..270 --")
for y, v in hruns((500, 242, 610, 272)):
    print("   y=%d %s" % (y, v))
print("-- Objective 'Yhat=Y' band x84..300 y262..292 (underline already added) --")
for y, v in hruns((84, 260, 300, 294)):
    print("   y=%d %s" % (y, v))

print("\n=== F6: Remember box construction (row bands x784..880) ===")
for y in range(100, 156, 4):
    row = O[y, 784:880]
    lum = row.sum(axis=1)
    dark = int((lum < 400).sum())
    blue = int(((row[:, 2] > 130) & (row[:, 0] < 140)).sum())
    print("  y=%d  dark_px=%2d  blue_px=%2d  median=%s" % (y, dark, blue, tuple(int(v) for v in np.median(row, axis=0))))
