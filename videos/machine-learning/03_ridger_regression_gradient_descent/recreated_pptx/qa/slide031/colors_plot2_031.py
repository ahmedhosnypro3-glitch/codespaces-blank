from PIL import Image
import numpy as np, collections
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def rep(name,x0,x1,y0,y1):
    reg=O[y0:y1,x0:x1].reshape(-1,3)
    V=reg.max(axis=1); mn=reg.min(axis=1); sat=V-mn
    print(f"-- {name}")
    for lab,sel in [("dark(V<150)",V<150),("sat>45",sat>45),("mid 150-225",(V>=150)&(V<225))]:
        sub=reg[sel]
        if len(sub)==0: print(f"   {lab}: none"); continue
        c=collections.Counter(map(tuple,(sub//12*12)))
        print(f"   {lab}: n={len(sub)} top={c.most_common(4)}")
rep("curve left arm",644,656,79,135)
rep("curve right arm",706,720,177,235)
rep("chord y146 x660..740",660,740,144,149)
rep("vert x687 y68..120",685,691,68,120)
rep("vert x687 y200..262",685,691,200,262)
rep("vert x745 y68..120",743,748,68,120)
rep("green marker",676,702,246,258)
rep("label (5,1)",492,561,248,262)
rep("xtick labels",578,806,268,291)
rep("red dot",655,667,177,190)
rep("plot bottom border",573,810,306,312)
