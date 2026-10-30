from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
R9=np.asarray(Image.open('recreated_pptx/qa/slide031/render_9.png').convert('RGB')).astype(int)
f=2001/960.0
def feats(a,box,fx):
    x0,y0,x1,y1=[int(v*fx) for v in box]
    reg=a[y0:y1,x0:x1].astype(int)
    V=reg.max(axis=2)
    r,g,b=reg[:,:,0],reg[:,:,1],reg[:,:,2]
    return dict(ink=int((V<240).sum()), red=int(((r>110)&(g<95)&(b<95)).sum()),
                green=int(((g>r+15)&(g>b+15)).sum()), blue=int(((b>r+30)&(b>g+30)).sum()),
                dark=int((V<150).sum()))
for name,box in [("plot interior x574..808 y68..308",(574,68,808,308)),
                 ("plot lower y244..308",(574,244,808,308)),
                 ("plot upper y68..243",(574,68,808,243)),
                 ("annotation interior x245..808 y245..288",(245,245,808,288)),
                 ("x-label band x574..808 y267..292",(574,267,808,292))]:
    fo=feats(O,box,1.0); fr=feats(R9,box,f)
    print(name)
    print("   " + "  ".join(f"{k}: orig={fo[k]:>6d} r9={fr[k]:>6d}" for k in fo))
