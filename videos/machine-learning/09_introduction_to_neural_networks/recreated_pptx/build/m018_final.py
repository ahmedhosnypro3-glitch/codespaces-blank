"""Final geometry confirmation for slide 018 original."""
import numpy as np
from PIL import Image

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_018.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
bgc = np.array([231, 233, 230])
dev = (np.abs(a - bgc).sum(axis=2) > 40)

print("=== bottom chart y-extent (row 74..336 and 390..635) ===")
for (x0, x1) in [(74, 336), (390, 635), (655, 890)]:
    sub = dev[:, x0:x1 + 1]
    rs = sub.sum(axis=1)
    rows = [y for y in range(a.shape[0]) if rs[y] > 200]
    print(f" x {x0}..{x1}: y {rows[0]}..{rows[-1]}" if rows else " none")

print("=== caption band y480..515 ink runs ===")
sub = dev[478:516, 60:900]
cs = sub.sum(axis=0)
runs = []
cur = None
for j in range(len(cs)):
    if cs[j] > 0:
        if cur is None:
            cur = [j, j]
        else:
            cur[1] = j
    elif cur is not None:
        if cur[1] - cur[0] > 3:
            runs.append((60 + cur[0], 60 + cur[1]))
        cur = None
if cur and cur[1] - cur[0] > 3:
    runs.append((60 + cur[0], 60 + cur[1]))
# merge runs closer than 12px
merged = []
for r in runs:
    if merged and r[0] - merged[-1][1] < 12:
        merged[-1] = (merged[-1][0], r[1])
    else:
        merged.append(r)
print(" caption runs:", merged)
rs = dev[478:516, 60:900].sum(axis=1)
print(" caption rows:", [(478 + i, int(rs[i])) for i in range(len(rs)) if rs[i] > 0])

print("=== eq card fill (cream/tan) regions ===")
# fill colors ~ (245,226,209) left card, (244,225,208) right card
fill = (a[:, :, 0] > 235) & (a[:, :, 0] - a[:, :, 2] > 25) & (a[:, :, 1] > 200)
for y in [120, 130, 150]:
    row = fill[y]
    runs = []
    cur = None
    for x in range(960):
        if row[x]:
            if cur is None:
                cur = [x, x]
            else:
                cur[1] = x
        elif cur is not None:
            if cur[1] - cur[0] > 5:
                runs.append((cur[0], cur[1]))
            cur = None
    if cur and cur[1] - cur[0] > 5:
        runs.append((cur[0], cur[1]))
    print(f" fill rows at y={y}:", runs)
fs = fill.sum(axis=1)
rows = [y for y in range(60, 500) if fs[y] > 30] if False else [y for y in range(60, min(500, a.shape[0])) if fs[y] > 30]
print(" fill row extent:", rows[0] if rows else None, rows[-1] if rows else None)
