import numpy as np
from PIL import Image
FR="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
a=np.asarray(Image.open(FR).convert("RGB")).astype(int)
R,G,B=a[:,:,0],a[:,:,1],a[:,:,2]; lum=a.mean(axis=2)
redm=(R-G>30)&(R-B>30); bluem=(B-R>25)&(B-G>12)&(B>70); darkm=lum<95
def core(mask,name,region):
    x0,x1,y0,y1=region; sub=mask[y0:y1,x0:x1]; px=a[y0:y1,x0:x1][sub]
    if len(px)==0: print(name,"none"); return
    # darkest = strongest pigment (min luminance)
    l=px.mean(axis=1); order=np.argsort(l); n=max(1,len(px)//10)
    top=px[order[:n]]
    print(f"{name}: n={len(px)} darkest10% median RGB={tuple(int(v) for v in np.median(top,axis=0))} overall median={tuple(int(v) for v in np.median(px,axis=0))}")
core(redm,"RED vector BOX1",(160,215,140,202))
core(redm,"RED caption Original Labels",(245,375,136,155))
core(redm,"RED paren BOX1",(153,163,140,192))
core(bluem,"BLUE Predicted Labels caption",(587,723,136,152))
core(bluem,"BLUE Obj/Err/Formula border",(78,86,250,300))
core(darkm,"DARK text (title/body)",(280,650,70,100))
