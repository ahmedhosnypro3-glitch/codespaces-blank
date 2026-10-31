from PIL import Image
V="/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
orig=Image.open(f"{V}/unique_slides/slide_018.jpg").convert("RGB")
refs=[("W",(255,255,255)),("Y",(255,255,133)),("G",(208,161,48)),("P",(196,94,108)),
      ("S",(74,74,74)),("K",(26,26,26)),("D",(147,7,22))]
def cls(p):
    best=None;bd=1e9
    for c,r in refs:
        d=sum((a-b)**2 for a,b in zip(p,r))
        if d<bd: bd=d;best=c
    return best,bd
def runs(y,x0,x1,maxd=4000):
    out=[];cur=None;st=None
    for x in range(x0,x1):
        c,d=cls(orig.getpixel((x,y)))
        if d>maxd: c="?"
        if c!=cur:
            if cur is not None: out.append((cur,st,x-1))
            cur=c;st=x
    out.append((cur,st,x1-1))
    return [r for r in out if r[2]-r[1]>=0]
for label,(x0,x1) in (("UNIPOLAR",(80,330)),("BIPOLAR",(530,780))):
    print("=== ",label)
    for y in range(172,272,1):
        rr=runs(y,x0,x1)
        print(f" y{y}: "+" ".join(f"{c}[{a}-{b}]" for c,a,b in rr))
