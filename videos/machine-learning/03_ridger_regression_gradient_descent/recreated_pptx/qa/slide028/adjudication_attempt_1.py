#!/usr/bin/env python3
"""PIL adjudication of slide 028 judge_attempt_1.txt findings.

Every judge finding is a HYPOTHESIS — adjudicate against the original frame
before changing geometry or colors.
"""
import numpy as np
from collections import Counter
from PIL import Image

QA = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide028/'
ORIG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_028.jpg'

o = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)
r = np.asarray(Image.open(QA + 'render_3.png').convert('RGB')).astype(int)
S = r.shape[0] / 540.0
def cv(v): return int(round(v * S))
O = 'orig'; R = 'rend'

def band_colors(a, x0, y0, x1, y1, n=6, sy=None):
    sub = a[(y0 if sy is None else sy):y1, x0:x1]
    c = Counter(tuple(p) for p in sub.reshape(-1, 3))
    return c.most_common(n)

print(f"scale {S:.4f}")

# ---- CLAIM A: "Loss" all-caps + red in render, neutral 'Loss' in original ----
print("\n=== CLAIM A: 'Loss' label color/case ===")
print("ORIG left y-label band (x95..142,y215..252):", band_colors(o, 95, 215, 142, 252))
print("REND left y-label band  (cv scale)         :", band_colors(r, cv(95), cv(215), cv(142), cv(252)))
print("ORIG right y-label band (x477..524,y210..247):", band_colors(o, 477, 210, 524, 247))
print("REND right y-label band                    :", band_colors(r, cv(477), cv(210), cv(524), cv(247)))

# ---- CLAIM B: axis line color (build uses SHAFT_BLUE 1B1263; judge says original red) ----
print("\n=== CLAIM B: axis shaft colors ===")
print("ORIG left  shaft x88..93 y230..300:", band_colors(o, 88, 230, 93, 300))
print("REND left  shaft x88..93 y230..300:", band_colors(r, cv(88), cv(230), cv(93), cv(300)))
print("ORIG left  h-shaft y506..512 x120..250:", band_colors(o, 120, 506, 250, 512))
print("REND left  h-shaft y506..512 x120..250:", band_colors(r, cv(120), cv(506), cv(250), cv(512)))
print("ORIG right shaft x472..477 y230..300:", band_colors(o, 472, 230, 477, 300))
print("REND right shaft x472..477 y230..300:", band_colors(r, cv(472), cv(230), cv(477), cv(300)))

# ---- CLAIM C: extra "red outer rectangle around the entire slide" ----
# the only red strokes are the house strokes (x58.5/x901/y538.5) = intentional chrome.
# Is there a red rect at, say, the panel boundary or a second frame?
print("\n=== CLAIM C: extra red outer rectangle ===")
def redmask(a):
    rr, gg, bb = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (rr > 140) & (gg < 110) & (bb < 110)
rm = redmask(r)
ys, xs = np.where(rm)
print(f"render red px={rm.sum():6d} bbox x{xs.min()/S:.0f}-{xs.max()/S:.0f} y{ys.min()/S:.0f}-{ys.max()/S:.0f}")
# rows dominated by red (horizontal red runs)
rowsum = rm.sum(axis=1)
print("render rows with red count > 300 (candidate long horizontal red strokes):")
for y in np.where(rowsum > 300)[0]:
    print(f"   y={y/S:.1f} count={rowsum[y]}")
colsum = rm.sum(axis=0)
print("render cols with red count > 300:")
for x in np.where(colsum > 300)[0]:
    print(f"   x={x/S:.1f} count={colsum[x]}")
# original red rows/cols
rmo = redmask(o)
ro_ = rmo.sum(axis=1); co_ = rmo.sum(axis=0)
print("ORIG rows with red count > 300:")
for y in np.where(ro_ > 300)[0]:
    print(f"   y={y} count={ro_[y]}")
print("ORIG cols with red count > 300:")
for x in np.where(co_ > 300)[0]:
    print(f"   x={x} count={co_[x]}")

# ---- CLAIM D: small black triangle + leader line near left valley (build line 108-109) ----
print("\n=== CLAIM D: black pointer at left valley ===")
print("build draws: line (267,443)-(-12,-15) [i.e. to 255,428] + arrow triangle at 255..258,428..436")
# original: dark ink near x240..275, y420..450?
dark_o = (o[:, :, 0] < 105) & (o[:, :, 1] < 105) & (o[:, :, 2] < 105)
for nm, a, sc in [('ORIG', dark_o, 1.0)]:
    sub = a[415:455, 235:285]
    ys2, xs2 = np.where(sub)
    if len(ys2):
        print(f"  {nm} dark ink x235..285 y415..455: n={sub.sum()} bbox "
              f"x{xs2.min()+235}-{xs2.max()+235} y{ys2.min()+415}-{ys2.max()+415}")
    else:
        print(f"  {nm} dark ink x235..285 y415..455: NONE")

# ---- CLAIM E: right panel oscillation geometry ----
print("\n=== CLAIM E: right panel dots + connecting segments ===")
blue_o = (np.abs(o[:, :, 0] - 46) < 85) & (np.abs(o[:, :, 1] - 117) < 85) & (np.abs(o[:, :, 2] - 182) < 85)
blue_r = (np.abs(r[:, :, 0] - 46) < 70) & (np.abs(r[:, :, 1] - 117) < 70) & (np.abs(r[:, :, 2] - 182) < 70)
for nm, bm in [('ORIG', blue_o), ('REND', blue_r)]:
    b = bm.copy()
    b[:, :int(478 * (1 if nm == 'ORIG' else S))] = False      # right panel only
    b[:, int((858 if nm == 'ORIG' else 858) * (1 if nm == 'ORIG' else S)):] = False
    # exclude axis shafts (dark blue) already excluded by color tolerance
    ys2, xs2 = np.where(b)
    if len(ys2):
        sc = 1.0 if nm == 'ORIG' else S
        print(f"  {nm} right-panel curve/dot px={len(ys2)} bbox x{xs2.min()/sc:.0f}-{xs2.max()/sc:.0f} "
              f"y{ys2.min()/sc:.0f}-{ys2.max()/sc:.0f}")
    else:
        print(f"  {nm} right-panel curve/dot px=0")

# right-panel dot markers: large filled circles d~7 => find blobs
print("\n  --- ORIG right panel: horizontal ink profile (blue, right panel) ---")
bo = blue_o.copy(); bo[:, :478] = False; bo[:, 860:] = False
colsum_o = bo.sum(axis=0)
runs = []
inrun = None
for x in range(478, 860):
    if colsum_o[x] >= 2 and inrun is None:
        inrun = x
    elif colsum_o[x] < 2 and inrun is not None:
        runs.append((inrun, x - 1)); inrun = None
if inrun is not None: runs.append((inrun, 859))
print("  ORIG blue column runs (x-ranges, width):", [(a, b, b - a + 1) for a, b in runs])
print("\n  --- REND right panel: horizontal ink profile ---")
br = blue_r.copy(); br[:, :cv(478)] = False; br[:, cv(860):] = False
colsum_r = br.sum(axis=0)
runs = []
inrun = None
for x in range(cv(478), cv(860)):
    if colsum_r[x] >= 2 and inrun is None:
        inrun = x
    elif colsum_r[x] < 2 and inrun is not None:
        runs.append((inrun, x - 1)); inrun = None
if inrun is not None: runs.append((inrun, cv(860) - 1))
print("  REND blue column runs:", [(round(a / S), round(b / S), round((b - a + 1) / S)) for a, b in runs])
