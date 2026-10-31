#!/usr/bin/env python3
"""Targeted slide003 crop-FAIL checks: >>> color, In-General enclosure, y underline."""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"

o = Image.open(f"{NS}/unique_slides/slide_003.jpg").convert("RGB")
r = Image.open(f"{RJ}/slide003/render.png").convert("RGB")
rs = r.resize((960, 540), Image.LANCZOS)
O = np.asarray(o).astype(int)
R = np.asarray(rs).astype(int)

def red(A): return (A[:,:,0] > A[:,:,1]+60) & (A[:,:,0] > A[:,:,2]+60) & (A[:,:,0] > 100)
def blue(A): return (A[:,:,2] > A[:,:,0]+40) & (A[:,:,2] > A[:,:,1]+30) & (A[:,:,2] > 90)
def dark(A): return A.sum(axis=2) < 300

# ASCII map of region x568-872 y136-344, 2x2 slide-px per char
X0,Y0,X1,Y1 = 568,136,872,344
for name, A in (("ORIG",O),("RENDER",R)):
    print(f"\n===== {name} region map (R=red B=blue K=dark .=bg) x{X0}-{X1} y{Y0}-{Y1}")
    rm,bm,km = red(A),blue(A),dark(A)
    for y in range(Y0,Y1,2):
        line=""
        for x in range(X0,X1,2):
            cell_r = rm[y:y+2,x:x+2].sum(); cell_b = bm[y:y+2,x:x+2].sum(); cell_k = km[y:y+2,x:x+2].sum()
            if cell_r>=2: line+="R"
            elif cell_b>=2: line+="B"
            elif cell_k>=2: line+="K"
            else: line+="."
        print(f"{y:3d} {line}")

# >>> color: find the "In General" line. Look at band y268-295 in both, per-row red/blue x640-874
print("\n===== 'In General' band y268-300, x640-874 per-row counts")
for name, A in (("ORIG",O),("RENDER",R)):
    rm,bm = red(A),blue(A)
    for y in range(268,301):
        rr = rm[y,640:874].sum(); bb = bm[y,640:874].sum(); kk = dark(A)[y,640:874].sum()
        if rr+bb+kk >= 10:
            print(f"  {name} y={y} red={rr} blue={bb} dark={kk}")

# column profile of the >>> cluster within that band: x where red/blue ink sits y276-292
print("\n===== x-distribution of red vs blue ink, y274-292, x640-874")
for name, A in (("ORIG",O),("RENDER",R)):
    rm,bm = red(A),blue(A)
    band_r = rm[274:293,640:874].sum(axis=0)
    band_b = bm[274:293,640:874].sum(axis=0)
    xs_r = [640+i for i,v in enumerate(band_r) if v>=3]
    xs_b = [640+i for i,v in enumerate(band_b) if v>=3]
    print(f"  {name} red x-ranges: {xs_r}")
    print(f"  {name} blue x-ranges: {xs_b}")

# underline under first y in Remember eq: Remember box x650-874 y153-221; eq text inside.
# Find dark-ink rows inside box and horizontal bar runs below glyph bottoms, y160-218
print("\n===== Remember-box interior ink rows x652-872 (per-row dark/red/blue), y156-218")
for name, A in (("ORIG",O),("RENDER",R)):
    km,rm = dark(A),red(A)
    for y in range(156,219):
        kk = km[y,652:872].sum(); rr = rm[y,652:872].sum()
        if kk+rr >= 8:
            # longest dark run
            row = km[y,652:872]
            best=0; cur=0
            for v in row:
                cur = cur+1 if v else 0
                best = max(best,cur)
            print(f"  {name} y={y} dark={kk} red={rr} maxrun={best}")
