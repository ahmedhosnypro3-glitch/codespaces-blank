#!/usr/bin/env python3
"""Pass 8 — vector content color, PredWhere line structure + colour runs,
and Arial-equivalent font sizing via Liberation Sans advance-width matching.
1px=1pt.
"""
import numpy as np
from PIL import Image, ImageFont

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 30)
dark = (r + g + b) < 330
text = dark | red | blue

# --- vector content dominant color (strict core pixels) ---
print("=== vector content color (BOX1 x165..208,y130..178 / BOX2 x480..552,y130..196) ===")
for lbl, x0,x1,y0,y1 in [("BOX1-vec",165,208,130,178), ("BOX2-vec",490,553,132,196)]:
    sub = im[y0:y1, x0:x1].reshape(-1,3)
    k = (sub[:,0]+sub[:,1]+sub[:,2]<330) | ((sub[:,0]>120)&((sub[:,0]-sub[:,1])>50))
    sub = sub[k]
    if len(sub):
        print(f"  {lbl}: median RGB {tuple(int(np.median(sub[:,c])) for c in range(3))} over {len(sub)} ink px")

def adv(txt, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    return f.getlength(txt)

REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
BD  = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
IT  = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
import os
has = {k:os.path.exists(p) for k,p in [("reg",REG),("bold",BD),("italic",IT)]}
print("fonts present:", has)

def size_for_width(txt, target_w, fontpath, lo=8, hi=40):
    best=None
    for s in range(lo,hi):
        w=adv(txt,fontpath,s)
        if best is None or abs(w-target_w)<abs(best[1]-target_w):
            best=(s,w)
    return best[0], round(best[1],1)

print("\n=== font size by advance-width match (Liberation Sans ~ Arial) ===")
# (label, string, measured ink width px, style)
cases = [
  ("TITLE",      "Concept of LOSS Function", 351, BD),
  ("OrigLabels", "Original Labels",          128, BD),
  ("FromTrain",  "from Training Samples",    162, REG),
  ("PredLabels", "Predicted Labels",         136, BD),
  ("Predicted",  "Predicted",                80,  REG),
  ("FromModel",  "from Model \u0176=XW",     169, REG),
  ("Remember",   "Remember",                 74,  BD),
  ("Objective",  "Objective is \u0176=Y",     161, REG),
  ("If..Y",      "If",                       20,  REG),
]
for lbl, txt, w, fp in cases:
    s, mw = size_for_width(txt, w, fp)
    print(f"  {lbl:11s} '{txt}' target_w={w} -> size~{s}pt (adv {mw})")

# Error line breakdown
def color_runs(x0,x1,y0,y1):
    rb = (text[y0:y1, x0:x1]).sum(axis=0) > 0
    out=[]
    for x in range(x1-x0):
        colred = int(red[y0:y1, x0+x].sum())
        colblue = int(blue[y0:y1, x0+x].sum())
        coldark = int(dark[y0:y1, x0+x].sum())
        if colred+colblue+coldark==0:
            c='.'
        elif colred>=colblue and colred>=coldark: c='R'
        elif colblue>=coldark: c='B'
        else: c='K'
        out.append(c)
    return "".join(out)

print("\n=== PredWhere fine line structure (x495..884) ===")
ti = text[237:366, 495:884]
rows = ti.sum(axis=1)
# row bands min_len 3
d1 = np.diff(np.concatenate(([0], (rows>0).astype(int), [0])))
starts=np.where(d1==1)[0]; ends=np.where(d1==-1)[0]-1
for s,e in zip(starts,ends):
    if e-s+1>=3:
        cols=np.where(ti[s:e+1].sum(axis=0)>0)[0]
        print(f"  line y{237+s}..{237+e} (h{e-s+1}) x{495+cols.min()}..{495+cols.max()}")
        print("     color:", color_runs(495, 884, 237+s-1, 237+e+2))

print("\n=== Error line color run (x82..486, y322..345) ===")
print("  ", color_runs(82, 486, 321, 346))
print("\n=== Define line color run (x82..650, y405..429) ===")
print("  ", color_runs(82, 650, 405, 430))
print("\n=== Objective color run (x82..302,y258..286) ===")
print("  ", color_runs(82, 302, 257, 287))
