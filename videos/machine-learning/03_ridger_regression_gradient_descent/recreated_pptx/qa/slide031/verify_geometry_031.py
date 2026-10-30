from PIL import Image
im = Image.open("render_1.png").convert("RGB")
W,H = im.size
s = W/960.0  # frame->render scale (150dpi: 2001/960 = 2.0844)
px = im.load()
def F(v): return int(round(v*s))

x0,y0,x1,y1 = 573,66,809,267   # plot box (frame px)
X0,Y0,X1,Y1 = F(x0),F(y0),F(x1),F(y1)

# strict blue escaped-ink count
esc = 0; bbox=None
minx=miny=10**9; maxx=maxy=-10**9
for Y in range(H):
    for X in range(W):
        r,g,b = px[X,Y][0],px[X,Y][1],px[X,Y][2]
        if b>150 and r<90 and g<90:
            if not (X0-2<=X<=X1+2 and Y0-2<=Y<=Y1+2):
                esc += 1
                minx=min(minx,X);miny=min(miny,Y);maxx=max(maxx,X);maxy=max(maxy,Y)
print("FAST1513: 04526203235")
print("INFO: esc_out=%d bbox=%s" % (esc, (minx,miny,maxx,maxy) if esc else None))
