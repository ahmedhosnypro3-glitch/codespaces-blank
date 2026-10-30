import numpy as np
from PIL import Image
FR="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
a=np.asarray(Image.open(FR).convert("RGB")).astype(int)
R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; lum=a.mean(axis=2)
red=(R-G>30)&(R-B>30); dark=lum<95; blue=(B-R>25)&(B-G>12)&(B>70)
print("BOX2 vector body x498..560 y112..209 (R=red B=blue K=dark):")
print("      "+''.join(str(x%10) for x in range(498,560)))
for x in range(498,560):
    r=red[112:209,x].sum(); d=dark[112:209,x].sum(); b=blue[112:209,x].sum()
    if r+d+b>0:
        tag = 'RED' if r>b and r>d else ('BLU' if b>d else 'DRK')
        print(f"  x{x}: r{r:3d} d{d:3d} b{b:3d} -> {tag}")
# also: where is BOX2 'Let Yhat =' ? dark pixels left of x497
print("BOX2 'Let Yhat' dark cols x427..496:")
xs=[x for x in range(427,497) if dark[120:208,x].sum()>0]
print("  ", xs if xs else "none")
print("BOX1 'Let Y' dark cols x86..152:")
xs=[x for x in range(86,153) if dark[126:158,x].sum()>0]
print("  ", xs if xs else "none")
