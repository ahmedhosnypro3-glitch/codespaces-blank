#!/usr/bin/env python3
"""Probe: judge_full_fresh2.txt (06:38 FAIL, clean) claims vs the CURRENT k15 render
(render.png md5 52e190a4, 05:21). Claim-targeted PIL measurements."""
import numpy as np
from PIL import Image
import hashlib

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
rp = f"{RJ}/slide025/render.png"
print("render.png md5:", hashlib.md5(open(rp, "rb").read()).hexdigest())
r = Image.open(rp).convert("RGB").resize((960, 540), Image.LANCZOS)
o = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
R = np.asarray(r).astype(int); O = np.asarray(o).astype(int)

def dark(A): return A.sum(axis=2) < 330
def red(A): return (A[:, :, 0] > 120) & (A[:, :, 1] < 100) & (A[:, :, 2] < 100)
def grayish(A):  # mesh/grid walls: mid gray, not panel bg, not white
    g = A.sum(axis=2) / 3.0
    return (g > 120) & (g < 215) & (np.abs(A[:, :, 0] - A[:, :, 1]) < 18) & (np.abs(A[:, :, 1] - A[:, :, 2]) < 18)
def white(A): return (A[:, :, 0] > 245) & (A[:, :, 1] > 245) & (A[:, :, 2] > 245)

rd, od = dark(R), dark(O)
rg, og = grayish(R), grayish(O)
rw, ow = white(R), white(O)

# D1: TR x10^4 corner (top-left of TR plot box x616-879 y115-317)
for nm, d in (("render", rd), ("orig", od)):
    print(f"D1 TR x10^4 corner x618-680 y117-140: {nm} dark ink = {int(d[117:140, 618:680].sum())}")
# D1b: TR z-tick strip (left edge of TR box, x618-660, y140-300)
for nm, d in (("render", rd), ("orig", od)):
    print(f"D1b TR z-tick strip x618-662 y140-300: {nm} dark ink = {int(d[140:300, 618:662].sum())}")
# D2/D3: TR surface fill + white
for nm, (s, w) in (("render", (rd, rw)), ("orig", (od, ow))):
    pass
sl = (slice(115, 317), slice(616, 879))
print(f"TR panel: white render={int(rw[sl].sum())} orig={int(ow[sl].sum())}; graymesh render={int(rg[sl].sum())} orig={int(og[sl].sum())}; dark render={int(rd[sl].sum())} orig={int(od[sl].sum())}")

# D6: BR containment bottom rows
rgray_bg = (np.abs(R[:, :, 0] - 233) < 14) & (np.abs(R[:, :, 1] - 233) < 14) & (np.abs(R[:, :, 2] - 231) < 14)
ogray_bg = (np.abs(O[:, :, 0] - 233) < 14) & (np.abs(O[:, :, 1] - 233) < 14) & (np.abs(O[:, :, 2] - 231) < 14)
print("D6 BR bottom rows x615-880 non-bg(non-white,non-panel):")
for y0, y1 in [(510, 518), (518, 526), (526, 532), (532, 536), (536, 538), (538, 540)]:
    sl2 = (slice(y0, y1), slice(615, 880))
    rb = (~rw[sl2]) & (~rgray_bg[sl2]); ob = (~ow[sl2]) & (~ogray_bg[sl2])
    print(f"   y{y0}-{y1}: render={int(rb.sum())} orig={int(ob.sum())}")

# D4: BL gray 3D box/grid walls + surface extent
sl = (slice(290, 527), slice(83, 376))
print(f"BL panel: graymesh render={int(rg[sl].sum())} orig={int(og[sl].sum())}; dark render={int(rd[sl].sum())} orig={int(od[sl].sum())}; white render={int(rw[sl].sum())} orig={int(ow[sl].sum())}")
# BL surface x-extent (non-white non-bg columns in mid rows y380-500)
def xextent(A, w, bg):
    sl2 = (slice(380, 500), slice(83, 376))
    m = (~w[sl2]) & (~bg[sl2])
    cols = m.sum(axis=0)
    xs = np.where(cols > 3)[0]
    return (83 + xs.min(), 83 + xs.max()) if len(xs) else None
print("BL content x-extent y380-500: render", xextent(R, rw, rgray_bg), "orig", xextent(O, ow, ogray_bg))

# D8: TL tick values strip (left of TL box x85-265 y115-288: z ticks at x85-110)
for nm, d in (("render", rd), ("orig", od)):
    print(f"D8 TL z-tick strip x85-112 y115-288: {nm} dark ink = {int(d[115:288, 85:112].sum())}")
    print(f"   TL x-tick strip y255-288 x85-265: {nm} dark ink = {int(d[255:288, 85:265].sum())}")

# D5: BL callout positions — dark text clusters (approx) in BL
for nm, d in (("render", rd), ("orig", od)):
    sub = d[300:527, 83:376]
    rows = sub.sum(axis=1)
    bands, st = [], None
    for i, v in enumerate(rows):
        if v > 5 and st is None: st = i
        elif v <= 5 and st is not None:
            if i - st >= 3: bands.append((300 + st, 300 + i))
            st = None
    print(f"D5 {nm} BL text/ink bands y: {bands}")
