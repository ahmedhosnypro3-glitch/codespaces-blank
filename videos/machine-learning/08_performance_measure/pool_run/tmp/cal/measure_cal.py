from PIL import Image
import numpy as np
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/pool_run/tmp/cal/cal-1.png").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("render size", W, H, " px/in =", W / 13.3333)
S = W / 13.3333
mx = a.max(axis=2); mn = a.min(axis=2)
ink = (mx < 210) & ((mx - mn) > 25)
cnt = ink.sum(axis=1)
rows = cnt >= 3
raw = []; inb = False
for i, v in enumerate(rows):
    if v and not inb: st = i; inb = True
    elif not v and inb: raw.append((st, i-1)); inb = False
if inb: raw.append((st, len(rows)-1))
merged = []
for b in raw:
    if merged and b[0]-merged[-1][1] <= 6: merged[-1][1] = b[1]
    else: merged.append([b[0], b[1]])
labels = []
for size in (18, 19, 20):
    labels += [f"L1-{size}", f"L2-{size}", f"P2B-{size}", f"P2R-{size}", f"TL-{size}", f"DL-{size}", f"CL-{size}"]
print(f"{len(merged)} bands, {len(labels)} labels")
for lab, (s, e) in zip(labels, merged):
    band = ink[s:e+1]
    idx = np.where(band.any(axis=0))[0]
    wpx = (idx.max()-idx.min()+1)
    print(f"{lab:8s} y={s/S:.3f}in-{(e+1)/S:.3f}in  x={(idx.min()+0.5)/S:.3f}in-{(idx.max()+1)/S:.3f}in  width={wpx/S:.3f}in ({wpx}px)")
