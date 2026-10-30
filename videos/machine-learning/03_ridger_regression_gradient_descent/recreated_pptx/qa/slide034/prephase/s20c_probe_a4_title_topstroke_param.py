from PIL import Image
im = Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg').convert('RGB')
W,H = im.size
px = im.load()
print('size', W, H)

def classify(r,g,b):
    if r>130 and g<95 and b<95: return 'RED'
    if g>110 and r<110 and b<140 and g-b>30: return 'GREEN'
    if b>120 and b-r>40 and b-g>40: return 'BLUE'
    if r<90 and g<90 and b<90: return 'DARK'
    return None

# A. Title band hue histogram
print('--- A title band y58..92 x180..450 (20px buckets)')
fam = {}
for x0 in range(180,450,20):
    c = {'RED':0,'GREEN':0,'BLUE':0,'DARK':0}
    for x in range(x0,min(x0+20,450)):
        for y in range(58,92):
            k = classify(*px[x,y])
            if k: c[k]+=1
    fam[x0]=c
for x0,c in fam.items():
    if sum(c.values()): print(f'x{x0}-{x0+20}: {c}')

# A2. per-run x spans: red pixels and any green/blue pixels
xs_red=[x for x in range(180,450) for y in range(58,92) if classify(*px[x,y])=='RED']
xs_green=[x for x in range(180,450) for y in range(58,92) if classify(*px[x,y])=='GREEN']
xs_blue=[x for x in range(180,450) for y in range(58,92) if classify(*px[x,y])=='BLUE']
def spans(xs):
    if not xs: return []
    xs=sorted(set(xs)); out=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x-p>6: out.append((s,p)); s=x
        p=x
    out.append((s,p)); return out
print('RED spans:', spans(xs_red))
print('GREEN spans:', spans(xs_green), 'BLUE spans:', spans(xs_blue))
from collections import Counter
samp = Counter(px[x,y] for x in range(180,450) for y in range(58,92) if classify(*px[x,y])=='RED')
print('top red samples:', samp.most_common(4))

# B. top stroke red count
n=0; where=[]
for x in range(50,910):
    for y in range(40,58):
        r,g,b=px[x,y]
        if r>150 and g<80 and b<80: n+=1; where.append((x,y))
print('--- B top-stroke red px (y40..58):', n, ('sample '+str(where[:6])) if where else '')

# C. param box row-1 value cell
print('--- C param row1 value cell x128..172 y250..264')
cnt=Counter(px[x,y] for x in range(128,172) for y in range(250,264))
print(cnt.most_common(5))
print('param row1 label cell x80..122 y250..264:', Counter(px[x,y] for x in range(80,122) for y in range(250,264)).most_common(3))
print('param border left x74..77 y260..300:', Counter(px[x,y] for x in range(73,78) for y in range(260,300)).most_common(3))

# D. slope row special cells
print('--- D slope row y460..477: yellow-cell runs')
ys=range(460,477)
def is_yellow(r,g,b): return r>225 and g>225 and 140<b<215
def is_salmon(r,g,b): return 170<r<245 and 110<g<190 and 70<b<160 and r-g>30
def is_red(r,g,b): return r>150 and g<80 and b<80
ycols=[x for x in range(140,875) if sum(1 for y in ys if is_yellow(*px[x,y]))>=8]
print('yellow col spans:', spans(ycols))
scols=[x for x in range(140,875) if sum(1 for y in ys if is_salmon(*px[x,y]))>=8]
print('salmon col span count:', len(scols), 'first/last:', (scols[0],scols[-1]) if scols else None)
rcols=[x for x in range(140,875) if sum(1 for y in ys if is_red(*px[x,y]))>=10]
print('red col spans (borders):', spans(rcols)[:12])
print('yellow samples:', Counter(px[x,y] for x in ycols[:40] for y in ys if is_yellow(*px[x,y])).most_common(3))
# label cell fill
print('slope label cell x82..136 fill:', Counter(px[x,y] for x in range(84,134) for y in range(462,476)).most_common(3))
