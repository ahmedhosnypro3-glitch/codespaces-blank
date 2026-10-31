#!/usr/bin/env python3
"""Slide025 fresh-FAIL adjudication probe 2: tight text bands + BR silhouette."""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
S = f"{RJ}/slide025"

render = Image.open(f"{S}/render.png").convert("RGB")
orig = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
W, H = render.size
sx, sy = W / 960.0, H / 540.0
R = np.asarray(render).astype(int)
O = np.asarray(orig.resize((W, H), Image.LANCZOS)).astype(int)

def crop(a, x0, y0, x1, y1):
    return a[int(y0*sy):int(y1*sy), int(x0*sx):int(x1*sx)]

def sim(a, b):
    if a.shape != b.shape:
        b = np.asarray(Image.fromarray(b.astype(np.uint8)).resize((a.shape[1], a.shape[0]), Image.LANCZOS)).astype(int)
    return float(np.abs(a - b).mean())

print("== A. BL tight text bands (slide px) ==")
# per build measurements of the ORIGINAL frame:
bands = {
    "GlobalMinima_LL": (143, 437, 203, 468),
    "LocalMinima_R":   (284, 384, 344, 407),
    "GlobalMaxima_T":  (240, 302, 270, 312),
    "LocalMaxima_M":   (280, 335, 318, 355),
}
for k, b in bands.items():
    co, cr = crop(O, *b), crop(R, *b)
    print(f"  {k}: orig-vs-render diff={sim(co, cr):.2f}  orig dark={int((co.sum(axis=2)<300).sum())} render dark={int((cr.sum(axis=2)<300).sum())}")
# cross-swap test on the two minima bands only
bLL, bLR = bands["GlobalMinima_LL"], bands["LocalMinima_R"]
coLL, coLR, crLL, crLR = crop(O,*bLL), crop(O,*bLR), crop(R,*bLL), crop(R,*bLR)
print(f"  swap test: rLL~oLL={sim(crLL,coLL):.2f} rLL~oLR={sim(crLL,coLR):.2f} rLR~oLR={sim(crLR,coLR):.2f} rLR~oLL={sim(crLR,coLL):.2f}")

print("== B. BR silhouette: per-column topmost colored row (surface profile) ==")
def profile(a, x0, y0, x1, y1):
    b = crop(a, x0, y0, x1, y1)
    sat = b.max(axis=2) - b.min(axis=2)
    col = sat > 60
    tops = []
    for j in range(b.shape[1]):
        ys = np.where(col[:, j])[0]
        tops.append(ys.min() if len(ys) else -1)
    return np.array(tops)
pO = profile(O, 618, 347, 877, 531)
pR = profile(R, 618, 347, 877, 531)
n = min(len(pO), len(pR))
pO, pR = pO[:n], pR[:n]
valid = (pO >= 0) & (pR >= 0)
print(f"  columns valid={int(valid.sum())}/{n}  mean|top diff|={float(np.abs(pO[valid]-pR[valid]).mean()):.2f} px "
      f" max={int(np.abs(pO[valid]-pR[valid]).max())}")
# valley count: local minima of the top profile (dips = valleys in surface silhouette)
def valleys(p):
    v = 0
    for i in range(2, len(p)-2):
        if p[i] > p[i-1] and p[i] > p[i+1] and p[i] > p[i-2] and p[i] > p[i+2]:
            v += 1
    return v
print(f"  silhouette peaks: orig={valleys(pO)} render={valleys(pR)}")

print("== C. BR black path ink by color class ==")
for label, a in [("orig", O), ("render", R)]:
    b = crop(a, 618, 347, 877, 531)
    g = b.sum(axis=2)
    print(f"  {label}: <80={int((g<80).sum())} 80-240={int(((g>=80)&(g<240)).sum())} 240-450={int(((g>=240)&(g<450)).sum())} 450-600={int(((g>=450)&(g<600)).sum())}")

print("== D. TR red-line orientation (claim: added diagonal red line) ==")
for label, a in [("orig", O), ("render", R)]:
    b = crop(a, 619, 118, 876, 314)
    red = (b[:,:,0] > 120) & (b[:,:,1] < 100) & (b[:,:,2] < 100)
    ys, xs = np.where(red)
    if len(ys) == 0:
        print(f"  {label}: no red"); continue
    # fit slope via covariance
    if len(ys) > 2:
        slope = float(np.cov(xs, ys)[0,1] / np.var(xs))
    else:
        slope = 0.0
    horiz = int((np.abs(np.diff(ys)) < 3).sum())
    print(f"  {label}: red px={int(red.sum())} slope(dy/dx)={slope:.3f} | horizontal-run px pairs={horiz}")
