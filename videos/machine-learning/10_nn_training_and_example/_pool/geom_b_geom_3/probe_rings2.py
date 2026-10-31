import numpy as np
from PIL import Image
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
def dark(a,l=150):
    lum=(a[:,:,0]*299+a[:,:,1]*587+a[:,:,2]*114)/1000.0
    return lum<l
for n,cols in [("014",list(range(30,130))+list(range(860,920))),
               ("023",list(range(30,90))+list(range(840,890))),
               ("024",list(range(30,80))+list(range(860,920)))]:
    a=np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    m=dark(a)
    sub=m[60:520,:]   # content vertical span (ring top/bottom excluded)
    print(f"== {n}  (dark px in rows 60..519)")
    for x in cols:
        c=int(sub[:,x].sum())
        if c>0: print(f"   col {x}: {c}")
    print("   rows:")
    for y in range(30,540):
        r=int(m[y,60:900].sum())
        if r>60: print(f"   row {y}: {r}")
