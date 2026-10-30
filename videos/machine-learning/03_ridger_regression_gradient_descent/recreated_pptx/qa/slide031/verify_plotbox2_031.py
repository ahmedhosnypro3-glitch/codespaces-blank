from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def nw(a,t=235):
    return (a.min(axis=2)<t).astype(int)
def isred(a):
    return (a[:,:,0]>110)&(a[:,:,1]<90)&(a[:,:,2]<90)
def isblack(a):
    return (a.max(axis=2)<110)
def isgreen(a):
    return (a[:,:,1]>a[:,:,0]+15)&(a[:,:,1]>a[:,:,2]+15)&(a[:,:,1]<230)
def isblue(a):
    return (a[:,:,2]>a[:,:,0]+40)&(a[:,:,2]>a[:,:,1]+40)
print("== full red bbox in x200..960,y0..540 ==")
R=isred(O); ys,xs=np.nonzero(R)
m=(xs>=200)&(xs<=960)
print("red x",xs[m].min(),xs[m].max(),"y",ys[m].min(),ys[m].max())
print("== red pixel count per row, x 570..820 ==")
for y in range(220,320):
    c=R[y,570:820].sum()
    if c: print(" y",y,c)
