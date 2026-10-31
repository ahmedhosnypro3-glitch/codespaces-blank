import numpy as np
from PIL import Image
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
def dark(a,l=150):
    return (a[:,:,0]*299+a[:,:,1]*587+a[:,:,2]*114)/1000.0 < l
FX,FY=960/2001.0,540/1125.0
# house frame @150dpi: 0.15in inset -> x,y in [22,1978]x[22,1103]
for n in ["014","016","017","023","024"]:
    a=np.asarray(Image.open(f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{n}_150.png").convert("RGB")).astype(int)
    m=dark(a); m[0,:]=m[-1,:]=m[:,0]=m[:,-1]=False
    H,W=m.shape
    out=np.zeros_like(m)
    out[:22,:]=True; out[1104:,:]=True; out[:,:22]=True; out[:,1979:]=True
    om=m&out
    ys,xs=np.nonzero(om)
    print(f"== {n}: ink outside house frame = {int(om.sum())} px", end=" ")
    if len(xs): print(f"bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} -> frame [{xs.min()*FX:.1f}..{xs.max()*FX:.1f}]x[{ys.min()*FY:.1f}..{ys.max()*FY:.1f}]")
    else: print("(none)")
    # characterize the dark pixel colors in that overflow
    if len(xs):
        pts=a[ys[:4000],xs[:4000]]
        uq,cnt=np.unique(pts//24*24,axis=0,return_counts=True)
        order=np.argsort(-cnt)
        print("   top colors:", [(tuple(uq[i]),int(cnt[i])) for i in order[:4]])
