import importlib.util, numpy as np
from PIL import Image
from scipy import ndimage
s=importlib.util.spec_from_file_location('g','_pool/bgeom2_geom.py')
g=importlib.util.module_from_spec(s); s.loader.exec_module(g)

def mask_with(path, kind, lum_t, chroma_t, dil):
    arr=np.asarray(Image.open(path).convert("RGB")); h,w=arr.shape[:2]
    a=arr.astype(int); mx,mn=a.max(2),a.min(2)
    lum=0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2]
    m=(lum<lum_t)|((mx-mn)>chroma_t)
    m=g.strip_frame_lines(m,arr)
    m=ndimage.binary_opening(m,structure=np.ones((3,3)))
    if dil: m=ndimage.binary_dilation(m,structure=np.ones((3,3)))
    mp=g.make_map(kind)
    yy,xx=np.mgrid[0:h,0:w]; sx,sy=mp["x"](xx),mp["y"](yy)
    ins=(sx>=0)&(sx<=13.3333)&(sy>=0)&(sy<=7.5)
    bg=((sx>=g.BADGE[0])&(sx<=g.BADGE[2])&(sy>=g.BADGE[1])&(sy<=g.BADGE[3]))
    return m&ins&~bg, mp

CFG=[("base",170,45,False),("sensitive",205,30,True)]
for sl in ("008","009","010","012","013"):
    print("="*72); print("SLIDE",sl)
    for cname,lt,ct,dil in CFG:
        rm,rmap=mask_with(f"_pool/tmp_geom_b_geom_2/{sl}/render-1.png","rend",lt,ct,dil)
        om,omap=mask_with(f"unique_slides/slide_{sl}.jpg","orig",lt,ct,dil)
        print(f"  [{cname}] ink rend={int(rm.sum())} orig={int(om.sum())}")
        for nm,(y0,y1) in g.REGIONS.items():
            a=g.region_box(rm,rmap,y0,y1); b=g.region_box(om,omap,y0,y1)
            if not (a and b):
                print(f"     {nm:7s} one-side-empty"); continue
            d=g.deltas_px150(a,b); w=max(abs(v) for v in d.values())
            print(f"     {nm:7s} worst={w:7.1f} {'PASS' if w<=4 else 'EXC'}  L/T/R/B={d['left']:+.0f}/{d['top']:+.0f}/{d['right']:+.0f}/{d['bottom']:+.0f}")
