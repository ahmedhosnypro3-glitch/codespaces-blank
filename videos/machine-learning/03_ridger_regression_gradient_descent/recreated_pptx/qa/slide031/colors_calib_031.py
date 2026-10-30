from PIL import Image
import numpy as np, collections
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def rep(name,x0,x1,y0,y1):
    reg=O[y0:y1,x0:x1].reshape(-1,3)
    V=reg.max(axis=1); mn=reg.min(axis=1); sat=V-mn
    print(f"-- {name}")
    for lab,sel in [("dark(V<150)",V<150),("sat>45",sat>45)]:
        sub=reg[sel]
        if len(sub)==0: print(f"   {lab}: none"); continue
        c=collections.Counter(map(tuple,(sub//12*12)))
        arr=np.asarray(sub); print(f"   {lab}: n={len(sub)} mean={arr.mean(0).round(1)} top={c.most_common(4)}")
rep("house left stroke x57..61 y100..500",56,62,100,500)
rep("house right stroke x899..903 y100..500",898,904,100,500)
rep("house bottom stroke y536..541 x60..900",60,900,536,541)
rep("plot top border x580..800 y65..68",580,800,64,69)
rep("plot left border x572..576 y80..300",571,577,80,300)
rep("annotation green top edge x250..560 y243..247",250,560,242,248)
rep("annotation green bottom edge x250..560 y286..292",250,560,285,293)
rep("annotation left edge x241..246 y250..285",240,247,250,286)
rep("annotation red right edge x806..812 y250..285",805,813,250,286)
rep("gray panel x100..140 y100..140",100,140,100,140)
rep("canvas top-left x5..40 y5..40",5,40,5,40)
