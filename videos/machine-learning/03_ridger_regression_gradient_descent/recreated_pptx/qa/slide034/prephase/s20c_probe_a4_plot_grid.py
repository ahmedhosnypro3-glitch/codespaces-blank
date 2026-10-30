from PIL import Image
im = Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg').convert('RGB')
px = im.load()
def is_gray(c): return all(180<=v<=225 for v in c) and max(c)-min(c)<12
def is_black(c): return all(v<70 for v in c)
# gridline columns: count gray rows per column in plot interior
cols=[(x,sum(1 for y in range(66,304) if is_gray(px[x,y]))) for x in range(612,842)]
gl=[x for x,n in cols if n>=120]
print('gridline cols:', gl)
if len(gl)>2:
    d=[b-a for a,b in zip(gl,gl[1:]) if b-a>1]
    print('spacings:', d)
rows=[(y,sum(1 for x in range(614,838) if is_gray(px[x,y]))) for y in range(66,304)]
grl=[y for y,n in rows if n>=160]
print('gridline rows:', grl[:20])
# axis lines: black column/row
bc=[(x,sum(1 for y in range(66,304) if is_black(px[x,y]))) for x in range(610,845)]
bcol=max(bc,key=lambda t:t[1]); print('blackest col (y-axis):', bcol)
br=[(y,sum(1 for x in range(614,838) if is_black(px[x,y]))) for y in range(60,308)]
brow=max(br,key=lambda t:t[1]); print('blackest row (x-axis):', brow)
from PIL import Image
from collections import Counter
im = Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg').convert('RGB')
px = im.load()
def is_dark(c): return sum(c)/3 < 120 and max(c)-min(c)<60
bc=Counter()
for x in range(610,845):
    n=sum(1 for y in range(66,304) if is_dark(px[x,y]))
    if n>=60: bc[x]=n
print('dark cols (y-axis candidates):', sorted(bc.items(), key=lambda t:-t[1])[:6])
def is_gray(c): return all(175<=v<=232 for v in c) and max(c)-min(c)<22
cols=[x for x in range(612,842) if sum(1 for y in range(66,304) if is_gray(px[x,y]))>=50]
print('gray cols>=50:', cols)
if len(cols)>2:
    print('spacings:', [b-a for a,b in zip(cols,cols[1:])])
from PIL import Image
im = Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg').convert('RGB')
px = im.load()
def is_grayish(c):
    r,g,b=c; m=(r+g+b)/3
    return 165<=m<=238 and max(c)-min(c)<38
cols=[(x,sum(1 for y in range(64,306) if is_grayish(px[x,y]))) for x in range(612,842)]
strong=[(x,n) for x,n in cols if n>=30]
print('grayish cols>=30:', strong)
if len(strong)>2:
    xs=[x for x,n in strong]
    print('spacings:', [b-a for a,b in zip(xs,xs[1:])])
rows=[(y,sum(1 for x in range(612,842) if is_grayish(px[x,y]))) for y in range(62,308)]
srow=[(y,n) for y,n in rows if n>=120]
print('grayish rows>=120:', srow[:24])
if len(srow)>2:
    ys=[y for y,n in srow]
    print('spacings:', [b-a for a,b in zip(ys,ys[1:])][:20])
