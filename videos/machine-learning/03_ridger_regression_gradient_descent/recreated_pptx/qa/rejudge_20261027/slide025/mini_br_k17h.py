import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from scipy.interpolate import CubicSpline
from scipy import ndimage
from PIL import Image
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
DPI = 150; BW, BH = 265, 187
JET = plt.get_cmap("jet")
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
ORIG_PROF = np.array([82,82,82,82,82,83,83,85,85,85,82,81,79,76,76,76,76,75,74,74,
                      73,73,72,72,71,70,66,56,55,50,46,46,46,45,45,45,44,44,44,43,46,
                      46,45,45,42,41,41,41,43,44,41,41,41,39,37,36,36,30,26,22,18,17,
                      16,18,16,12,10,12,9,2,2], dtype=np.float64)
def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:,:,0]>170)&(a[:,:,1]<90)&(a[:,:,2]<90)
    return ((mx-mn)>60)&(mx>90)&~red
def br_surface(X, Y):
    return (3.2*np.exp(-(((X-0.5)**2+(Y+0.7)**2)/1.6))
            +2.0*np.exp(-(((X+1.8)**2+(Y-1.3)**2)/1.2))
            +1.3*np.exp(-(((X-2.3)**2+(Y-1.9)**2)/0.7))
            -2.3*np.exp(-(((X+0.9)**2+(Y+1.6)**2)/1.0))
            -1.8*np.exp(-(((X-2.0)**2+(Y+1.7)**2)/0.8))
            -1.7*np.exp(-(((X-0.9)**2+(Y-2.2)**2)/1.1))
            +0.38*np.sin(2.1*X)*np.cos(2.3*Y))
_X = np.linspace(-3,3,120); _XG,_YG = np.meshgrid(_X,_X); _ZG = br_surface(_XG,_YG)
_ZMIN,_ZMAX = float(_ZG.min()), float(_ZG.max()); _ZRNG = _ZMAX-_ZMIN
WP = np.array([(2.4,1.9),(1.7,1.1),(0.9,1.45),(0.2,0.6),(-0.5,0.95),(-1.0,0.3),(-0.6,-0.6),(-1.3,-0.9),(-0.8,-1.7),(-1.5,-2.2)])
def fit(fig, ax, capx, capy, zaspect, rounds=12):
    lo,hi = 0.02,40.0; zoom = 1.0
    for _ in range(rounds):
        ax.set_box_aspect(zaspect, zoom=zoom); fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[:,:,:3].astype(np.int32)
        m = colmask(buf); m[:2]=False; m[-2:]=False; m[:,:2]=False; m[:,-2:]=False
        ys,xs = np.nonzero(m)
        if not len(xs): break
        fx = (xs.max()-xs.min()+1)/buf.shape[1]; fy = (ys.max()-ys.min()+1)/buf.shape[0]
        if fx<=capx and fy<=capy: lo=zoom; zoom=min(hi,zoom*1.08)
        else: hi=zoom; zoom=0.5*(lo+hi)
    ax.set_box_aspect(zaspect, zoom=lo); fig.canvas.draw()
def proj_xy(ax,x,y,z):
    x2,y2,_ = proj3d.proj_transform(x,y,z,ax.get_proj())
    disp = ax.transData.transform([(x2,y2)])[0]
    W = ax.figure.get_size_inches()[0]*DPI; H = ax.figure.get_size_inches()[1]*DPI
    return (disp[0]/W, 1.0-disp[1]/H)
def render_br(azim, elev, bm, capx, capy, zfac):
    fig = plt.figure(figsize=(BW/72.0, BH/72.0), dpi=DPI)
    ax = fig.add_axes([0.02, bm, 0.96, 0.98-bm], projection="3d")
    ax.view_init(elev=elev, azim=azim)
    norm = Normalize(_ZMIN-0.40*_ZRNG, _ZMAX)
    ax.plot_surface(_XG,_YG,_ZG, cmap=JET, norm=norm, shade=False, antialiased=True,
                    rstride=3, cstride=3, linewidth=0.22, edgecolor=(0.05,0.05,0.05,0.35))
    t = np.linspace(0,1,len(WP)); ts = np.linspace(0,1,240)
    sx = CubicSpline(t,WP[:,0])(ts); sy = CubicSpline(t,WP[:,1])(ts)
    sz = np.array([float(br_surface(np.array(a),np.array(b))) for a,b in zip(sx,sy)])+0.12
    ax.plot(sx,sy,sz, color="black", lw=1.8, zorder=100, solid_capstyle="round")
    (ex,ey),(ex2,ey2) = proj_xy(ax,sx[-1],sy[-1],sz[-1]), proj_xy(ax,sx[-12],sy[-12],sz[-12])
    fig.add_artist(FancyArrowPatch(posA=(ex2,ey2), posB=(ex,ey), transform=fig.transFigure,
                                   arrowstyle="-|>", mutation_scale=9, color="black", lw=0.8, zorder=101))
    ax.set_xlim(-3,3); ax.set_ylim(-3,3); ax.set_zlim(_ZMIN-0.5,_ZMAX+0.5)
    ax.set_axis_off()
    fit(fig, ax, capx, capy, (6,6,_ZRNG*zfac))
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[:,:,:3].astype(np.int32)
    plt.close(fig)
    return buf
def score(buf):
    img = np.array(Image.fromarray(buf.astype(np.uint8)).resize((BW,BH), Image.BILINEAR)).astype(np.int32)
    m = colmask(img)
    prof = 100.0*m[455-344:526-344].mean(1)
    pe = np.abs(prof-ORIG_PROF).mean()
    ys,xs = np.nonzero(m)
    bbox = (615+xs.min(), 344+ys.min(), 615+xs.max(), 344+ys.max())
    dm = (img.max(2)<100)&((img.max(2)-img.min(2))<80)
    dm[:8]=False; dm[-8:]=False; dm[:,:8]=False; dm[:,-8:]=False
    lab,n = ndimage.label(dm, structure=np.ones((3,3)))
    best=None
    for i in range(1,n+1):
        yy,xx = np.nonzero(lab==i)
        if len(xx)>=20 and (best is None or len(xx)>best[0]): best=(len(xx),xx,yy)
    wind=0.0
    if best:
        _,xs2,ys2 = best
        rem=list(zip(xs2,ys2)); chain=[rem.pop(0)]
        while rem:
            c=chain[-1]; j=min(range(len(rem)), key=lambda i:(rem[i][0]-c[0])**2+(rem[i][1]-c[1])**2)
            chain.append(rem.pop(j))
        length=sum(np.hypot(chain[i+1][0]-chain[i][0],chain[i+1][1]-chain[i][1]) for i in range(len(chain)-1))
        straight=np.hypot(xs2.max()-xs2.min(), ys2.max()-ys2.min())
        wind=length/max(straight,1e-9)
    return pe, bbox, wind, prof
combos = [(-55,30,0.02,0.95,1.00,0.7), (-55,30,0.02,0.95,1.00,0.5), (-55,30,0.06,0.95,0.99,0.7),
          (-55,26,0.02,0.95,1.00,0.7), (-55,30,0.02,0.98,1.00,0.7), (-55,30,0.02,0.95,1.00,0.9)]
res=[]
for c in combos:
    buf = render_br(*c)
    pe,bbox,wind,prof = score(buf)
    res.append((pe+2*abs(wind-6.02), pe, wind, c, bbox, prof))
    print("c=%s prof=%.2f wind=%.2f bbox=%s" % (c, pe, wind, bbox), flush=True)
res.sort(key=lambda r:r[0])
print("BEST", res[0][3], "prof=%.2f wind=%.2f" % (res[0][1], res[0][2]))
print("prof:", " ".join("%.0f"%v for v in res[0][5]))
