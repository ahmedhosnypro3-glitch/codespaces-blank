from PIL import Image
import numpy as np
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ren = np.array(Image.open(f"{NS}/recreated_pptx/renders/slide_040_recreated-1.png").convert("RGB")).astype(int)
org = np.array(Image.open(f"{NS}/qa/rejudge2/orig_png/slide_040.png").convert("RGB").resize((ren.shape[1], ren.shape[0]), Image.LANCZOS)).astype(int)
H, W = ren.shape[:2]
def reg(a, r):
    x0,y0,x1,y1 = int(r[0]*W), int(r[1]*H), int(r[2]*W), int(r[3]*H)
    return a[y0:y1, x0:x1]
def ink(a):  # non-background (bg is near-white in orig, E8E8E8 in render)
    return float((np.abs(a - np.array([255,255,255])).sum(axis=2) > 60).mean()) if a.mean() > 200 else float((np.abs(a - np.array([232,232,232])).sum(axis=2) > 60).mean())
panels = {"Aggregation":[0.11,0.26,0.31,0.52],"Compound":[0.39,0.26,0.58,0.52],"Spiral":[0.67,0.26,0.86,0.52],
          "Pathbased":[0.11,0.62,0.31,0.88],"Flame":[0.39,0.62,0.58,0.88],"Jain":[0.67,0.62,0.86,0.88]}
for name, r in panels.items():
    rr, oo = reg(ren, r), reg(org, r)
    def colfrac(a):
        m = np.abs(a - np.array([232,232,232])).sum(axis=2) > 60
        px = a[m]
        colored = px[(px.max(axis=1) - px.min(axis=1)) > 60]
        return float(len(colored)) / max(1, a.shape[0]*a.shape[1])
    print(f"{name:12s} ink render={ink(rr):.3f} orig={ink(oo):.3f} colored_frac render={colfrac(rr):.3f} orig={colfrac(oo):.3f}")
labels = {"Aggregation":[0.15,0.21,0.27,0.25],"Compound":[0.42,0.21,0.55,0.25],"Spiral":[0.70,0.21,0.83,0.25],
          "Pathbased":[0.15,0.57,0.27,0.61],"Flame":[0.42,0.57,0.55,0.61],"Jain":[0.70,0.57,0.83,0.61]}
for name, r in labels.items():
    for tag, a in (("ren", ren), ("org", org)):
        rr = reg(a, r)
        blue = ((rr[:,:,2] > 150) & (rr[:,:,0] < 120) & (rr[:,:,1] < 120)).mean()
        dark = (rr.sum(axis=2) < 300).mean()
        print(f"label {name:12s} {tag} blue={blue:.3f} dark={dark:.4f}", end="  ")
    print()
tr_r, tr_o = reg(ren,[0.28,0.10,0.72,0.20]), reg(org,[0.28,0.10,0.72,0.20])
red = lambda a: float(((a[:,:,0]>130)&(a[:,:,1]<110)&(a[:,:,2]<110)).mean())
print(f"title red_frac render={red(tr_r):.4f} orig={red(tr_o):.4f}")
bd_r, bd_o = reg(ren,[0.88,0.08,0.96,0.18]), reg(org,[0.88,0.08,0.96,0.18])
y = lambda a: float(((a[:,:,0]>200)&(a[:,:,1]>200)&(a[:,:,2]<220)).mean())
d = lambda a: float((a.sum(axis=2)<300).mean())
print(f"badge yellow render={y(bd_r):.3f} orig={y(bd_o):.3f}; numeral dark render={d(bd_r):.4f} orig={d(bd_o):.4f}")
# frame: red pixels along the 0.15in inset rectangle
def framefrac(a):
    tot, hit = 0, 0
    for (yy, xx0, xx1) in [(0.15, 0.15, 0.985), (0.975, 0.15, 0.985)]:
        row = a[int(yy*H)-2:int(yy*H)+3, int(xx0*W):int(xx1*W)]
        hit += int(((row[:,:,0]>130)&(row[:,:,1]<110)&(row[:,:,2]<110)).sum()); tot += row.shape[0]*row.shape[1]
    for (xx, yy0, yy1) in [(0.15, 0.15, 0.975), (0.985, 0.15, 0.975)]:
        col = a[int(yy0*H):int(yy1*H), int(xx*W)-2:int(xx*W)+3]
        hit += int(((col[:,:,0]>130)&(col[:,:,1]<110)&(col[:,:,2]<110)).sum()); tot += col.shape[0]*col.shape[1]
    return hit/tot
print(f"frame red_frac render={framefrac(ren):.3f} orig={framefrac(org):.3f}")
# cursor arrow region dark ink
ar_r, ar_o = reg(ren,[0.55,0.55,0.59,0.59]), reg(org,[0.55,0.55,0.59,0.59])
print(f"arrow dark render={float((ar_r.sum(axis=2)<300).mean()):.4f} orig={float((ar_o.sum(axis=2)<300).mean()):.4f}")
