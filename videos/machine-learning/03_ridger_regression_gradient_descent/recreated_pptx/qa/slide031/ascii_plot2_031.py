from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def cls(p):
    r,g,b=int(p[0]),int(p[1]),int(p[2])
    if abs(g-b)<12 and abs(r-g)<12 and r>248 and g>248 and b>248: return ' '   # white
    if r>120 and g<90 and b<90: return 'R'
    if g>r+15 and g>b+15 and g<240: return 'G'
    if b>r+30 and b>g+30: return 'B'
    if r>110 and g>70 and b<110 and g<r: return 'r'
    mx=max(p); mn=min(p)
    if mx-mn>35: return '?'
    if mx<70: return '#'      # dark black
    if mx<130: return '%'     # mid-dark
    if mx<175: return '*'
    if mx<215: return ':'     # 224 gridline family
    if mx<240: return '.'     # 240 plot bg
    return ','
print("legend: ' '=white '#'=dark '%'=mid '*'=midlt ':'=~224 ' .'=plot-bg ','=gray panel R=red G=green B=blue r=darkred ?=chromatic")
hdr='    '+''.join(str((568+i)//10%10) for i in range(0,246,2))
print(hdr)
for y in range(60,314,2):
    row=''.join(cls(O[y,x]) for x in range(567,813,2))
    print(f"{y:3d} {row}")
print("     "+''.join(str((567+i)%10) for i in range(0,246,2)))
