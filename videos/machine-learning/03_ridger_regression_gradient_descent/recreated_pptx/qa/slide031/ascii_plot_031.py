from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
def cls(p):
    r,g,b=p
    if r>225 and g>225 and b>225: return ' '
    mx=max(p); mn=min(p)
    if r>120 and g<90 and b<90: return 'R'   # red
    if g>r+15 and g>b+15 and g<235: return 'G' # green
    if b>r+40 and b>g+40: return 'B'         # blue
    if mx<90: return '#'                     # black
    if mx<150: return '@'
    if mx<200: return '+'
    if mx<235: return ':'
    return '.'
for y in range(60,316,2):
    row=''.join(cls(O[y,x]) for x in range(568,815,2))
    print(f"{y:3d}|{row}")
