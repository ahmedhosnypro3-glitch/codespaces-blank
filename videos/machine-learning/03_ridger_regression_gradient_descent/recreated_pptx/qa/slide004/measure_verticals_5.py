# Locate tall vertical strokes (parentheses) and text bands in the two top boxes.
import numpy as np
from PIL import Image

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)
RIM = Image.open("recreated_pptx/qa/slide004/render_4.png").convert("RGB")
SC = RIM.size[1] / 540.0
R = np.asarray(RIM).astype(int)


def ink(a):
    return a.sum(axis=2) < 700


def tall_verticals(m, box, sc=1.0, minfrac=0.5):
    x0, y0, x1, y1 = box
    reg = m[y0:y1, x0:x1]
    h = reg.shape[0]
    colhits = reg.sum(axis=0)
    out = []
    for i, n in enumerate(colhits):
        if n >= minfrac * h:
            out.append((x0 + i, int(n)))
    # group consecutive columns
    groups = []
    for c, n in out:
        if groups and c - groups[-1][-1][0] <= 2:
            groups[-1].append((c, n))
        else:
            groups.append([(c, n)])
    return [(g[0][0], g[-1][0], sum(x[1] for x in g) // len(g)) for g in groups]


def bands(m, box, sc=1.0, minrun=6):
    x0, y0, x1, y1 = box
    reg = m[y0:y1, x0:x1]
    res = []
    cur = None
    for yy in range(reg.shape[0]):
        row = reg[yy]
        # longest run of ink in this row
        best, s = 0, None
        for i, v in enumerate(row):
            if v:
                if s is None:
                    s = i
                if i - s + 1 > best:
                    best = i - s + 1
            else:
                s = None
        if best >= minrun:
            if cur is None:
                cur = [yy, yy]
            else:
                cur[1] = yy
        else:
            if cur:
                res.append(tuple(cur))
                cur = None
    if cur:
        res.append(tuple(cur))
    return [(round((y0 + a) / sc, 1), round((y0 + b) / sc, 1)) for a, b in res]


def xspan(m, box, ylo, yhi, sc=1.0, minrun=6):
    x0, y0, x1, y1 = box
    a = m[y0 + int(ylo):y0 + int(yhi), x0:x1]
    cols = np.where(a.sum(axis=0) >= minrun)[0]
    if len(cols) == 0:
        return None
    return (round((x0 + cols[0]) / sc, 1), round((x0 + cols[-1]) / sc, 1))


for nm, img, box, sc in [
    ("ORIG Box1", ORIG, (86, 103, 388, 220), 1.0),
    ("ORIG Box2", ORIG, (433, 103, 740, 220), 1.0),
    ("REND Box1", R, (86, 103, 388, 220), SC),
    ("REND Box2", R, (433, 103, 740, 220), SC),
]:
    m = ink(img)
    print("\n=== %s box(frame)=%s ===" % (nm, box))
    for a, b, n in tall_verticals(m, box):
        print("  tall vertical x %d..%d (avg %d rows)" % (a, b, n))
    for lo, hi in bands(m, box, sc):
        print("  band y %s..%s  xspan=%s" % (lo, hi, xspan(m, box, (lo * sc - box[1]), (hi * sc - box[1]), sc)))
