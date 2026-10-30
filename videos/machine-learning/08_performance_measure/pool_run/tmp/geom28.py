from PIL import Image
import numpy as np
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/unique_slides/slide_028-.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R - G > 45) & (R - B > 45) & (R > 90)
dark = (R < 120) & (G < 120) & (B < 120)

print("=== RED horizontal runs (>=40px long) ===")
for y in range(H):
    row = red[y]
    idx = np.where(row)[0]
    if len(idx) == 0: continue
    # find runs
    runs = []
    st = idx[0]; prev = idx[0]
    for v in idx[1:]:
        if v - prev > 3:
            runs.append((st, prev)); st = v
        prev = v
    runs.append((st, prev))
    for (s, e) in runs:
        if e - s >= 40:
            print(f"  y={y}: x {s}-{e} (len {e-s+1})")

print("=== RED vertical runs (>=20px long) ===")
for x in range(W):
    col = red[:, x]
    idx = np.where(col)[0]
    if len(idx) == 0: continue
    runs = []
    st = idx[0]; prev = idx[0]
    for v in idx[1:]:
        if v - prev > 3:
            runs.append((st, prev)); st = v
        prev = v
    runs.append((st, prev))
    for (s, e) in runs:
        if e - s >= 20:
            print(f"  x={x}: y {s}-{e} (len {e-s+1})")

print("=== DARK text lines inside def boxes ===")
def textlines(y0, y1, x0, x1, label):
    sub = dark[y0:y1, x0:x1]
    cnt = sub.sum(axis=1)
    rows = cnt >= 2
    raw = []; inb = False
    for i, v in enumerate(rows):
        if v and not inb: st = i; inb = True
        elif not v and inb: raw.append((st+y0, i-1+y0)); inb = False
    if inb: raw.append((st+y0, y1-1))
    merged = []
    for b in raw:
        if merged and b[0]-merged[-1][1] <= 4: merged[-1][1] = b[1]
        else: merged.append([b[0], b[1]])
    print(f"--- {label} ---")
    for (s,e) in merged:
        band = dark[s:e+1, x0:x1]
        idx = np.where(band.any(axis=0))[0]
        print(f"  y={s}-{e} (h={e-s+1}) x={idx.min()+x0}-{idx.max()+x0} (w={idx.max()-idx.min()+1})")

textlines(255, 312, 330, 860, "TPR def box interior")
textlines(365, 425, 335, 890, "FPR def box interior")
textlines(205, 255, 80, 800, "TPR leadin region")
textlines(330, 365, 80, 800, "FPR leadin region")
textlines(305, 345, 540, 760, "best value 1 region")
textlines(415, 450, 540, 760, "best value 0 region")
