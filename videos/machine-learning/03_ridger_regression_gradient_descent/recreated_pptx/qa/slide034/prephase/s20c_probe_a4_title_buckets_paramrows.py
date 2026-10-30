from PIL import Image
im = Image.open('videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg').convert('RGB')
px = im.load()

# Title brightness buckets
print('--- title mean RGB per 25px bucket (y60..90)')
for x0 in range(195,435,25):
    n=rs=gs=bs=0
    for x in range(x0,min(x0+25,435)):
        for y in range(60,90):
            r,g,b=px[x,y]
            if r>110 and g<95 and b<95: rs+=r; gs+=g; bs+=b; n+=1
    if n: print(f'x{x0}-{x0+25}: n={n} mean=({rs//n},{gs//n},{bs//n})')

# Param box rows: classify pixels near pin fills vs white
targets = {'GREEN':(232,251,209), 'PINK':(244,190,193), 'YELLOW':(249,253,15), 'PALEYEL':(237,255,151)}
def near(c,t,tol=28): return all(abs(a-b)<=tol for a,b in zip(c,t))
def is_white(c): return all(v>235 for v in c)
print('--- param box y246..310, label col x80..122 vs value col x128..172: % per y-row')
for y in range(246,310,4):
    row=[]
    for name,(x0,x1) in (('L',(80,122)),('V',(128,172))):
        cnt={'G':0,'P':0,'Y':0,'W':0,'o':0}; tot=0
        for x in range(x0,x1):
            for yy in range(y,min(y+4,310)):
                c=px[x,yy]; tot+=1
                if near(c,targets['GREEN']): cnt['G']+=1
                elif near(c,targets['PINK']): cnt['P']+=1
                elif near(c,targets['YELLOW']) or near(c,targets['PALEYEL']): cnt['Y']+=1
                elif is_white(c): cnt['W']+=1
                else: cnt['o']+=1
        row.append(f"{name} y{y}: " + ' '.join(f"{k}{100*v//tot}%" for k,v in cnt.items()))
    print(' | '.join(row))
