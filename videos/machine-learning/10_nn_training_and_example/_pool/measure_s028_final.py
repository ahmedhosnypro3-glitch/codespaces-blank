import numpy as np
from PIL import Image
a = np.asarray(Image.open('unique_slides/slide_028.jpg').convert('RGB')).astype(int)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
RED=(r>120)&(r-g>45)&(r-b>45)
def rowgroups(y0,y1,x0,x1,mask,minpx=3,gap=3,vgap=14,label=""):
    sub=mask[y0:y1+1,x0:x1+1]
    cnt=sub.sum(axis=1); bands=[]; st=None
    for i,c in enumerate(cnt):
        if c>=minpx and st is None: st=i
        elif c<minpx and st is not None: bands.append((st,i-1)); st=None
    if st is not None: bands.append((st,len(cnt)-1))
    m=[]
    for (s,e) in bands:
        if m and s-m[-1][1]<=gap: m[-1]=(m[-1][0],e)
        else: m.append((s,e))
    print(f"-- {label} x[{x0}-{x1}] y[{y0}-{y1}]")
    for (s,e) in m:
        if e-s<3: continue
        band=sub[s:e+1]; ci=band.any(axis=0)
        runs=[]; i=0
        while i<len(ci):
            if ci[i]:
                j=i
                while j+1<len(ci) and ci[j+1]: j+=1
                runs.append([i,j]); i=j+1
            else: i+=1
        gr=[]
        for (rs,re) in runs:
            if gr and rs-gr[-1][1]-1<=vgap: gr[-1][1]=re
            else: gr.append([rs,re])
        gs=" | ".join(f"x[{x0+s}-{x0+e2}]({e2-s+1})" for s,e2 in gr)
        print(f"   y[{y0+s}-{y0+e}] h={e-s+1}  {gs}")

rowgroups(180,400,695,915,RED,label="FAR-RIGHT RED")
rowgroups(180,400,695,915,(a.mean(axis=2)<130),label="FAR-RIGHT DARK")
rowgroups(200,540,393,441,RED,label="GAP-COLUMN RED")
rowgroups(190,205,390,445,(a.mean(axis=2)<130),label="HEADER RIGHT EDGE")
rowgroups(526,540,45,915,RED,label="BOTTOM RED")
print("=== red pixel row histogram x[394-441] ===")
sub=RED[200:540,394:441]
for i,c in enumerate(sub.sum(axis=1)):
    if c>2: print(f"  y[{200+i}] cnt={c}")
