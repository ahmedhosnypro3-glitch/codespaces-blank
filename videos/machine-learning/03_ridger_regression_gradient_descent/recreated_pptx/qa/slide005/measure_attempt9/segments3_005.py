import numpy as np
from PIL import Image
D = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(D + "/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
r6 = np.asarray(Image.open(D + "/recreated_pptx/qa/slide005/render_7.png").convert("RGB")).astype(int)
r8 = np.asarray(Image.open(D + "/recreated_pptx/qa/slide005/render_8.png").convert("RGB")).astype(int)
SX, SY = 2001/960.0, 1125/540.0

def groups(arr, x0, x1, y0, y1, sx, sy, gap=2.0, minink=3, thr=200):
    X0, X1, Y0, Y1 = int(x0*sx), int(x1*sx), int(y0*sy), int(y1*sy)
    sub = arr[Y0:Y1+1, X0:X1+1].mean(axis=2) < thr
    cs = sub.sum(axis=0)
    g = int(round(gap*sx)); out = []; s = None
    for i, v in enumerate(cs):
        if v >= minink and s is None: s = i
        elif v < minink and s is not None:
            nxt = i
            while nxt < len(cs) and cs[nxt] < minink: nxt += 1
            if nxt - i >= g or nxt >= len(cs):
                out.append(((X0+s)/sx, (X0+i-1)/sx)); s = None
    if s is not None: out.append(((X0+s)/sx, (X0+len(cs)-1)/sx))
    return out

go = groups(o, 90, 686, 456, 508, 1, 1)
for tag, arr in (("ORIG ", o), ("A6   ", r6), ("A8   ", r8)):
    sx, sy = (1, 1) if tag.startswith("ORIG") else (SX, SY)
    g = groups(arr, 90, 686, 456, 508, sx, sy)
    # exclude noise: groups narrower than 3 frame px
    real = [x for x in g if x[1]-x[0] >= 2.5]
    print("%s %2d real groups (x%.0f..x%.0f): %s" % (tag, len(real), real[0][0], real[-1][1],
          " ".join("[%d-%d]" % x for x in real)))
