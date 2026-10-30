# Per-row ink-run dump of the two top "Let" boxes, ORIGINAL vs RENDER_4.
# Render pixels are reported back in frame px (divide by SC = 2001/960... /1125/540).
import numpy as np
from PIL import Image

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)
RIM = Image.open("recreated_pptx/qa/slide004/render_4.png").convert("RGB")
SC = RIM.size[1] / 540.0
R = np.asarray(RIM).astype(int)


def rowruns(row, x0, minrun=4):
    out, s = [], None
    for i, v in enumerate(row):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= minrun:
                out.append((s, i - 1))
            s = None
    if s is not None and len(row) - s >= minrun:
        out.append((s, len(row) - 1))
    return out


def dump(name, img, box, sc=1.0, thresh=700, minrun=4):
    x0, y0, x1, y1 = [int(round(v * sc)) for v in box]
    reg = img[y0:y1, x0:x1]
    m = reg.sum(axis=2) < thresh
    print("\n===== %s frame-box %s (img px %s) =====" % (name, box, (x0, y0, x1, y1)))
    for yy in range(m.shape[0]):
        rr = rowruns(m[yy], None, minrun * sc)
        rr = [(round((x0 + a) / sc, 1), round((x0 + b) / sc, 1)) for a, b in rr]
        if rr:
            print("  y%5.1f %s" % ((y0 + yy) / sc, rr))


dump("ORIG Box1 (Original Labels)", ORIG, (86, 100, 389, 222))
dump("ORIG Box2 (Predicted Labels)", ORIG, (431, 100, 741, 222))
dump("REND Box1", R, (86, 100, 389, 222), sc=SC)
dump("REND Box2", R, (431, 100, 741, 222), sc=SC)
