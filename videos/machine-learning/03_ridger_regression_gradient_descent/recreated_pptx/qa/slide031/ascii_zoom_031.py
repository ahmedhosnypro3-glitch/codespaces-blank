from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def cls(p):
    r,g,b=int(p[0]),int(p[1]),int(p[2])
    if r>245 and g>245 and b>245: return ' '
    if r>120 and g<90 and b<90: return 'R'
    if g>r+15 and g>b+15: return 'G'
    if b>r+30 and b>g+30: return 'B'
    mx=max(p)
    if mx<80: return '#'
    if mx<140: return '%'
    if mx<190: return '*'
    if mx<225: return ':'
    if mx<245: return '.'
    return ','
def dump(x0,x1,y0,y1,title):
    print(f"--- {title}  x{x0}..{x1} y{y0}..{y1} ---")
    print("     "+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1):
        print(f"{y:4d} "+''.join(cls(O[y,x]) for x in range(x0,x1)))
dump(655,700,262,292,"x-axis label region 655..700")
dump(560,615,240,312,"vertical line at 611")
dump(484,570,244,264,"(5,1) label")
