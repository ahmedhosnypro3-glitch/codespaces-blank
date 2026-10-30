import numpy as np
from PIL import Image
FR = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
a = np.asarray(Image.open(FR).convert("RGB")).astype(int)
R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]; lum=a.mean(axis=2)
red=(R-G>30)&(R-B>30); dark=lum<95
def dump(tag,x0,x1,y0,y1,step=1):
    print(f"=== {tag}  x{x0}..{x1} y{y0}..{y1}  R=red K=dark . =light/white ===")
    xs=range(x0,x1); hdr='      '+''.join(str((x//10)%10) for x in xs); print(hdr)
    hdr2='      '+''.join(str(x%10) for x in xs); print(hdr2)
    for y in range(y0,y1,step):
        row=''
        for x in range(x0,x1):
            row += 'R' if red[y,x] else ('K' if dark[y,x] else '.')
        print(f"{y:4d}  {row}")
dump("BOX1 eq Let Y=(vec)_{nx1}", 86,238,112,206,step=1)
dump("BOX2 eq Let Yhat=(vec)_{nx1}", 424,586,100,220,step=1)
