import numpy as np
from PIL import Image
FR="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
a=np.asarray(Image.open(FR).convert("RGB")).astype(int)
R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; lum=a.mean(axis=2)
red=(R-G>30)&(R-B>30); dark=lum<95
# BOX1 content band between the two paren verticals (x164..214, exclude box border x<90)
def analyze(tag,xc0,xc1,y0,y1):
    print(f"--- {tag}: ink columns x{xc0}..{xc1} y{y0}..{y1} ---")
    for x in range(xc0,xc1):
        rpx=red[y0:y1,x].sum(); dpx=dark[y0:y1,x].sum()
        if rpx+dpx>0:
            tot=rpx+dpx
            print(f"  x{x}: red={rpx:3d} dark={dpx:3d} -> {'RED' if rpx>dpx else 'DARK'}")
analyze("BOX1 vector body (parens+content)",164,216,112,206)
