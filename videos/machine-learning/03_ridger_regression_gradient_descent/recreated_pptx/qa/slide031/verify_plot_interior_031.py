from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def blue(a): return (a[:,:,2]>a[:,:,0]+40)&(a[:,:,2]>a[:,:,1]+40)
def green(a): return (a[:,:,1]>a[:,:,0]+15)&(a[:,:,1]>a[:,:,2]+15)&(a[:,:,1]<230)
def black(a): return (a.max(axis=2)<110)
def nw(a,t=235): return (a.min(axis=2)<t)
for name,m in [('BLUE',blue(O)),('GREEN',green(O)),('BLACK',black(O))]:
    reg=m[60:320,570:815]
    ys,xs=np.nonzero(reg)
    if len(xs)==0: print(name,'none'); continue
    print(name,'bbox x',xs.min()+570,xs.max()+570,'y',ys.min()+60,ys.max()+60,'n',len(xs))
print()
print("== per-column BLUE y-range (x 640..745) ==")
B=blue(O)
for x in range(640,746,3):
    idx=np.nonzero(B[60:320,x])[0]
    print(" x",x, (idx.min()+60,idx.max()+60,len(idx)) if len(idx) else None)
print()
print("== GREEN pixels in plot region x 573..815, y 60..320 ==")
G=green(O)
ys,xs=np.nonzero(G[60:320,573:815])
print("green bbox x",xs.min()+573,xs.max()+573,"y",ys.min()+60,ys.max()+60,"n",len(xs))
import collections
print("cols:",sorted(collections.Counter(xs+573).items()))
print("rows:",sorted(collections.Counter(ys+60).items()))
