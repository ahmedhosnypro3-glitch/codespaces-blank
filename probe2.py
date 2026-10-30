from PIL import Image
import numpy as np
im = Image.open('../../unique_slides/slide_025.jpg').convert('RGB')
a = np.asarray(im).astype(int)
h,w,_ = a.shape
def crop(y0,y1,x0,x1,name):
    Image.open('../../unique_slides/slide_025.jpg').crop((x0,y0,x1,y1)).save(name)
# finding 1: arrowheads on axes -> check top-left plot interior for black axis lines
# plot A interior: x 137..308, y 121..267
A = a[121:268, 137:308]
blackA = ((A[:,:,0]<100)&(A[:,:,1]<100)&(A[:,:,2]<100))
rows = blackA.sum(axis=1)
print('plot A black row-profile (rows with >25 px):')
for y in range(0,147,3):
    c=int(rows[y])
    bar='#'*(c//4)
    print(f'  y={y:3d} abs={y+121:3d} n={c:3d} {bar}')
cols = blackA.sum(axis=0)
print('plot A black col-profile (cols with >25 px):')
for x in range(0,171,4):
    c=int(cols[x])
    bar='#'*(c//4)
    print(f'  x={x:3d} abs={x+137:3d} n={c:3d} {bar}')
