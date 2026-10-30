from PIL import Image
import numpy as np
f=float(2001/960.0)
O=np.asarray(Image.open('recreated_pptx/qa/slide031/render_9.png').convert('RGB')).astype(int)
def cls(p):
    r,g,b=int(p[0]),int(p[1]),int(p[2])
    if r>245 and g>245 and b>245: return ' '
    if r>120 and g<90 and b<90: return 'R'
    if g>r+15 and g>b+15: return 'G'
    if b>r+30 and b>g+30: return 'B'
    if r>110 and g>70 and b<110: return 'r'
    mx=max(p)
    if mx<80: return '#'
    if mx<140: return '%'
    if mx<190: return '*'
    if mx<225: return ':'
    if mx<245: return '.'
    return ','
print("render_9 same ASCII grid")
for y in range(0,540,6):
    def row():
        s=''
        for x in range(0,960,6):
            s+=cls(O[int(y*f),int(x*f)])
        return s
    print(f"{y:3d}|"+row())
