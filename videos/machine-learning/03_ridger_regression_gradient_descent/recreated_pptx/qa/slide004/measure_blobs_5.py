# Connected-component segmentation of the top boxes: bbox + dominant colour per blob.
import numpy as np
from PIL import Image

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)
RIM = Image.open("recreated_pptx/qa/slide004/render_4.png").convert("RGB")
SC = RIM.size[1] / 540.0
R = np.asarray(RIM.resize((int(round(RIM.size[0] / SC)), int(round(RIM.size[1] / SC))), Image.LANCZOS)).astype(int)


def components(mask, box):
    x0, y0, x1, y1 = box
    lab = np.zeros(mask.shape, dtype=int)
    cur = 0
    out = []
    from collections import deque
    for yy in range(mask.shape[0]):
        for xx in range(mask.shape[1]):
            if mask[yy, xx] and lab[yy, xx] == 0:
                cur += 1
                q = deque([(yy, xx)])
                lab[yy, xx] = cur
                px = []
                while q:
                    cy, cx = q.popleft()
                    px.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx] and lab[ny, nx] == 0:
                                lab[ny, nx] = cur
                                q.append((ny, nx))
                out.append(px)
    res = []
    for px in out:
        ys = [p[0] for p in px]
        xs = [p[1] for p in px]
        res.append(dict(x=min(xs), X=max(xs), y=min(ys), Y=max(ys), n=len(px)))
    return res


def classify(img, comp, box):
    x0, y0 = box[0], box[1]
    x, X, y, Y = comp["x"], comp["X"], comp["y"], comp["Y"]
    reg = img[y:Y + 1, x:X + 1]
    px = reg.reshape(-1, 3)
    ink = px[px.sum(axis=1) < 700]
    if len(ink) == 0:
        return "?"
    r, g, b = ink[:, 0].mean(), ink[:, 1].mean(), ink[:, 2].mean()
    if r > 140 and g < 120 and b < 120:
        return "RED"
    if b > 120 and r < 140:
        return "BLUE"
    if r < 120 and g < 120 and b < 120:
        return "BLACK"
    return "other(%d,%d,%d)" % (r, g, b)


BOX1 = (88, 104, 384, 218)
BOX2 = (433, 104, 736, 218)
for nm, box, img in [("ORIG Box1", BOX1, ORIG), ("ORIG Box2", BOX2, ORIG),
                     ("REND Box1", BOX1, R), ("REND Box2", BOX2, R)]:
    x0, y0, x1, y1 = box
    reg = img[y0:y1, x0:x1]
    m = reg.sum(axis=2) < 690
    comps = components(m, box)
    comps = [c for c in comps if c["n"] >= 12]
    comps.sort(key=lambda c: (c["y"], c["x"]))
    print("\n=== %s  box=%s  (%d blobs >=12px) ===" % (nm, box, len(comps)))
    for c in comps:
        print("  %-16s x %3d..%-3d  y %3d..%-3d  w %2d h %2d  n=%d" % (
            classify(img, c, box), x0 + c["x"], x0 + c["X"], y0 + c["y"], y0 + c["Y"],
            c["X"] - c["x"] + 1, c["Y"] - c["y"] + 1, c["n"]))
