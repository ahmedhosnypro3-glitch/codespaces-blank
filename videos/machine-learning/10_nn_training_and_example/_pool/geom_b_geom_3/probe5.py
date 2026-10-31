import numpy as np
from PIL import Image
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
def dark(a,l=150):
    return (a[:,:,0]*299+a[:,:,1]*587+a[:,:,2]*114)/1000.0 < l
def bands(m,min_gap=6,min_ink=4):
    on=m.sum(1)>min_ink; out=[];s=None
    for y,v in enumerate(on):
        if v and s is None: s=y
        elif not v and s is not None: out.append((s,y-1)); s=None
    if s is not None: out.append((s,m.shape[0]-1))
    mg=[]
    for b in out:
        if mg and b[0]-mg[-1][1]-1<min_gap: mg[-1]=(mg[-1][0],b[1])
        else: mg.append(b)
    return mg
def bbox(m,y0,y1,ox=0,oy=0):
    s=m[y0:y1+1,:]; ys,xs=np.nonzero(s)
    if len(xs)==0: return None
    return int(xs.min())+ox,int(ys.min())+oy,int(xs.max())+ox,int(ys.max())+oy
FY=540/1125.0
for n in ["014","024","017","023","016"]:
    a=np.asarray(Image.open(f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{n}_150.png").convert("RGB")).astype(int)
    m=dark(a); m[0,:]=m[-1,:]=m[:,0]=m[:,-1]=False
    H,W=m.shape
    ex=np.zeros_like(m); inset,band=22,6
    for t in (inset,W-1-inset): ex[:,max(0,t-band):t+band+1]=True
    for t in (inset,H-1-inset): ex[max(0,t-band):t+band+1,:]=True
    ex[15:150,1830:1975]=True
    m=m&~ex
    bs=bands(m)
    print(f"== {n} render bands (render px -> frame px):")
    for b in bs[:6]:
        bb=bbox(m,b[0],b[1])
        print(f"   y{b[0]}..{b[1]} (frame {b[0]*FY:.0f}..{b[1]*FY:.0f}) x{bb[0]}..{bb[2]} (frame {bb[0]*960/2001:.0f}..{bb[2]*960/2001:.0f})")
    print(f"   ... total bands {len(bs)}")
