import numpy as np
from PIL import Image
p='videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg'
a = np.asarray(Image.open(p).convert('RGB')).astype(int)
r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
lum=(r+g+b)/3
INK = lum<228
import sys
x0,x1,y0,y1 = (int(v) for v in sys.argv[1:5])
out=[]
for yy in range(y0,y1+1):
    out.append(f"{yy:4d}|"+"".join("#" if INK[yy,xx] else "." for xx in range(x0,x1+1))+"|")
open(sys.argv[5],"w").write("\n".join(out))
