from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def isred(a):
    return (a[:,:,0]>110)&(a[:,:,1]<90)&(a[:,:,2]<90)
R=isred(O)
print("== ORIG red in region x560..830, y40..340 ==")
reg=R[40:340,560:830]
ys,xs=np.nonzero(reg)
print("bbox x",xs.min()+560,xs.max()+560,"y",ys.min()+40,ys.max()+40)
# column red counts
for x in [572,573,574,575,808,809,810]:
    col=R[40:340,x]
    idx=np.nonzero(col)[0]
    if len(idx): print("col x=",x,"red rows",idx.min()+40,"..",idx.max()+40,"count",len(idx))
# row red counts in 560..830
print("-- row red counts (frame y) for x 560..830 --")
for y in range(60,320):
    c=R[y,560:830].sum()
    if c>50: print(" y",y,"redcount",c)
