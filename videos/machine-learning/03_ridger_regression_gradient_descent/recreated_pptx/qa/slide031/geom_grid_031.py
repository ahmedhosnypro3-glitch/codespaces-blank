from PIL import Image
import numpy as np, collections
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
R,G,B=O[:,:,0],O[:,:,1],O[:,:,2]
V=O.max(axis=2)
# light-gray gridline pixels: gray, 190..232
grid=(abs(R-G)<10)&(abs(G-B)<10)&(V>=190)&(V<=232)
print("== vertical gridline columns: count of grid px in y 70..262 ==")
for x in range(573,810):
    c=grid[70:262,x].sum()
    if c>100: print("  x",x,c)
print("== horizontal gridline rows: count of grid px in x 580..805 ==")
for y in range(67,310):
    c=grid[y,580:805].sum()
    if c>100: print("  y",y,c)
print()
print("== pinkish (light red) pixels in plot, per row x 573..808 ==")
pink=(R>G+12)&(R>B+8)&(R>120)
for y in range(67,310):
    c=pink[y,573:809].sum()
    if c>0: print("  y",y,c, "cols:", np.nonzero(pink[y,573:809])[0][:20]+573)
