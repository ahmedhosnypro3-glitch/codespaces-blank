#!/usr/bin/env python3
"""att27 pre-fix PIL measurements on unique_slides/slide_034.jpg (960x540, 1px=1pt).

Pins every value the slide_034 rebuild needs: plot calibration fitted on the
frame's teal ink, gridline extent, tick-label presence, curve core color,
param-box rows/fills/divider + the "7" ink color, callout box fill + f(x) ink
color, red down-arrow bbox, title/L1/L2 ink bboxes + L2 run split, eq-box
geometry/border, table frame/separators/band fills/insert/slope-cells.
"""
import numpy as np
from PIL import Image
from scipy.optimize import least_squares

FR = Image.open("unique_slides/slide_034.jpg").convert("RGB")
A = np.asarray(FR).astype(int)
H, W = A.shape[:2]
out = []
def P(*a):
    s = " ".join(str(x) for x in a)
    out.append(s); print(s)

P("### 1. plot calibration fit on teal ink (region x607..846 y58..314)")
R = A[58:314, 607:846]
r, g, b = R[..., 0], R[..., 1], R[..., 2]
teal = (g > 140) & (b > 140) & (g - r > 35) & (b - r > 20)
ys, xs = np.nonzero(teal)
P("teal px:", len(xs))
cols = np.unique(xs)
pts = []
for c in cols:
    yy = ys[xs == c]
    pts.append((c + 607, yy.mean() + 58, len(yy)))
P("teal columns:", len(pts), "x-extent:", int(min(p[0] for p in pts)), "..", int(max(p[0] for p in pts)))

def f(x):
    return (x * x * np.cos(x) - x) / 10.0

def resid(p):
    X0, SX, Y0, SY = p
    e = []
    for xpx, ypx, n in pts:
        xd = (xpx - X0) / SX
        e.append(ypx - (Y0 - SY * f(xd)))
    return np.array(e)

sol = least_squares(resid, [721.5, 9.5, 172.0, 9.5], method="lm")
X0, SX, Y0, SY = sol.x
e = np.abs(resid(sol.x))
P("fit: X0=%.3f SX=%.4f Y0=%.3f SY=%.4f" % (X0, SX, Y0, SY))
P("residual median %.3f p95 %.3f max %.3f" % (np.median(e), np.percentile(e, 95), e.max()))
# teal core color: darkest-teal mode
tl = R[teal]
dark = tl[tl.sum(axis=1) < np.percentile(tl.sum(axis=1), 30)]
P("teal core mean RGB:", dark.mean(axis=0).round(1), "| 033 used #2FA9AC, desc_plot #45C0CC")

P("### 2. gridline extent (light-gray rows/cols inside plot)")
gray = (np.abs(r - g) < 12) & (np.abs(g - b) < 12) & (r > 170) & (r < 225)
rowcounts = gray.sum(axis=1)
gridrows = [int(y) for y in np.nonzero(rowcounts > 120)[0]]
P("gray gridline rows (region-y, +58 = frame-y):", [y + 58 for y in gridrows])
if gridrows:
    y0 = gridrows[len(gridrows) // 2]
    xs_g = np.nonzero(gray[y0])[0]
    P("gridline row extent frame-x:", int(xs_g.min() + 607), "..", int(xs_g.max() + 607))
colcounts = gray.sum(axis=0)
gridcols = [int(x) for x in np.nonzero(colcounts > 120)[0]]
P("gray gridline cols (frame-x):", [x + 607 for x in gridcols])
if gridcols:
    x0 = gridcols[len(gridcols) // 2]
    ys_g = np.nonzero(gray[:, x0])[0]
    P("gridline col extent frame-y:", int(ys_g.min() + 58), "..", int(ys_g.max() + 58))

P("### 3. x tick labels -2 / 4 presence (dark ink at label spots)")
for name, lx in [("-2", 702), ("4", 759)]:
    zone = A[176:191, lx - 7:lx + 7]
    dk = (zone.max(axis=2) < 120).sum()
    P("label", name, "zone dark px:", int(dk))
# y tick labels 0 / -2 presence
for name, ly in [("0", 172), ("-2", 191)]:
    zone = A[ly - 7:ly + 8, 700:716]
    dk = (zone.max(axis=2) < 120).sum()
    P("ylabel", name, "zone dark px:", int(dk))

P("### 4. param box (x74..175 y245..307)")
B = A[245:308, 74:176]
rr, gg, bb = B[..., 0], B[..., 1], B[..., 2]
navy = (bb > 60) & (bb - gg > 30) & (rr < 90) & (gg < 90)
P("navy border px:", int(navy.sum()))
ysN, xsN = np.nonzero(navy)
if len(xsN):
    P("navy bbox frame: x%d..%d y%d..%d" % (xsN.min() + 74, xsN.max() + 74, ysN.min() + 245, ysN.max() + 245))
    P("navy core mean:", B[navy].mean(axis=0).round(1))
# row bands: classify each row y inside x80..168 by dominant fill
for yy in range(246, 307):
    row = A[yy, 82:126]
    m = row.mean(axis=0)
    if not (m[0] > 235 and m[1] > 235 and m[2] > 235):
        pass
fills = {}
for yy in range(247, 307):
    row = A[yy, 82:126]
    m = row.mean(axis=0).round(0).astype(int)
    fills[yy] = tuple(m)
runs = []
prev = None
for yy in range(247, 307):
    cur = fills[yy]
    if prev is None or max(abs(cur[i] - prev[i]) for i in range(3)) > 25:
        runs.append([yy, yy, cur])
        prev = cur
    else:
        runs[-1][1] = yy
P("label-cell fill runs (y0..y1 mean RGB):", [(a, b2, tuple(c)) for a, b2, c in runs if b2 - a >= 3])
# divider x: column with dark/navy ink across rows 255..300 in x120..140
div = []
for xx in range(115, 145):
    col = A[255:301, xx]
    dk = (col.max(axis=1) < 150).sum()
    if dk > 20:
        div.append(xx)
P("divider columns (x, dark rows>20):", div)
# the '7' ink color (value cell row2 y271..289 x130..170)
V = A[273:288, 132:168]
ink = V.max(axis=2) < 160
P("'7' ink px:", int(ink.sum()), "mean RGB:", V[ink].mean(axis=0).round(1) if ink.sum() else None)
reddish = ((V[..., 0] - V[..., 1] > 40) & (V[..., 0] - V[..., 2] > 40)).sum()
P("'7' reddish px:", int(reddish))
# '0.2' ink (row1) for comparison
V1 = A[256:270, 132:168]
ink1 = V1.max(axis=2) < 160
P("'0.2' ink px:", int(ink1.sum()), "mean RGB:", V1[ink1].mean(axis=0).round(1) if ink1.sum() else None)
# text ink height in the param label cell ('step' row1 x80..128)
T = A[250:275, 80:128]
tink = (T.max(axis=2) < 120)
rows_t = np.nonzero(tink.any(axis=1))[0]
P("'step' ink rows (frame-y):", int(rows_t.min() + 250), "..", int(rows_t.max() + 250), "-> glyph height", int(rows_t.max() - rows_t.min() + 1))

P("### 5. red down-arrow (search x140..220 y292..340)")
Z = A[292:340, 140:220]
red = (Z[..., 0] > 120) & (Z[..., 0] - Z[..., 1] > 50) & (Z[..., 0] - Z[..., 2] > 40)
ysA, xsA = np.nonzero(red)
P("red px:", int(red.sum()))
if len(xsA):
    P("arrow bbox frame: x%d..%d y%d..%d" % (xsA.min() + 140, xsA.max() + 140, ysA.min() + 292, ysA.max() + 292))
    P("arrow core mean RGB:", Z[red].mean(axis=0).round(1))
    # hollow or filled? sample the bbox center
    cx, cy = (xsA.min() + xsA.max()) // 2, (ysA.min() + ysA.max()) // 2
    P("bbox center RGB:", Z[cy, cx].tolist())

P("### 6. callout box (x270..597 y252..300)")
C = A[252:301, 270:598]
green_border = (C[..., 1] > 90) & (C[..., 1] - C[..., 0] > 40) & (C[..., 1] - C[..., 2] > 30)
ysC, xsC = np.nonzero(green_border)
P("green px:", int(green_border.sum()))
if len(xsC):
    P("green bbox frame: x%d..%d y%d..%d" % (xsC.min() + 270, xsC.max() + 270, ysC.min() + 252, ysC.max() + 252))
    P("green core mean:", C[green_border].mean(axis=0).round(1))
inner = A[256:297, 290:580]
# fill = modal light color
flat = inner.reshape(-1, 3)
light = flat[flat.sum(axis=1) > 600]
P("callout interior light mean RGB:", light.mean(axis=0).round(1) if len(light) else None)
# f(x) ink color line2 (y280..300 x268..330)
L2 = A[280:300, 268:335]
ink2 = L2.max(axis=2) < 170
P("line2 'f(x)' ink px:", int(ink2.sum()), "mean RGB:", L2[ink2].mean(axis=0).round(1) if ink2.sum() else None)
blueish = ((L2[..., 2] - L2[..., 0] > 40) & (L2[..., 2] - L2[..., 1] > 20)).sum()
reddish2 = ((L2[..., 0] - L2[..., 1] > 40) & (L2[..., 0] - L2[..., 2] > 30)).sum()
P("line2 f(x) blueish/reddish px:", int(blueish), int(reddish2))
# line1 ink run colors: X + 9.6 red? (y256..276 x268..597)
L1z = A[256:277, 268:598]
ink1z = L1z.max(axis=2) < 170
redm = (L1z[..., 0] - L1z[..., 1] > 40) & (L1z[..., 0] - L1z[..., 2] > 30)
# red x-clusters
redcols = np.nonzero(redm.any(axis=0))[0]
def clusters(idx):
    if len(idx) == 0:
        return []
    br = np.nonzero(np.diff(idx) > 4)[0]
    return [(int(idx[0]), int(idx[-1]))] if len(br) == 0 else [
        (int(s[0]), int(s[-1])) for s in np.split(idx, br + 1)]
P("line1 red x-clusters (frame-x):", [(a + 268, b2 + 268) for a, b2 in clusters(redcols)])
# line2 blue x-clusters
bluem = (L2[..., 2] - L2[..., 0] > 40) & (L2[..., 2] - L2[..., 1] > 20)
bluecols = np.nonzero(bluem.any(axis=0))[0]
P("line2 blue x-clusters (frame-x):", [(a + 268, b2 + 268) for a, b2 in clusters(bluecols)])

P("### 7. title block inks")
for name, (ya, yb) in [("title", (60, 90)), ("L1", (90, 116)), ("L2", (116, 144))]:
    Z = A[ya:yb, 60:610]
    ink = Z.max(axis=2) < 170
    ysT, xsT = np.nonzero(ink)
    if len(xsT):
        P(name, "ink bbox frame: x%d..%d y%d..%d  n=%d" % (xsT.min() + 60, xsT.max() + 60, ysT.min() + ya, ysT.max() + ya, len(xsT)))
# L2 run split: blue vs red columns
Z = A[117:141, 60:610]
bluem = (Z[..., 2] - Z[..., 0] > 40) & (Z[..., 2] - Z[..., 1] > 20)
redm = (Z[..., 0] - Z[..., 1] > 40) & (Z[..., 0] - Z[..., 2] > 30)
P("L2 blue x-clusters:", [(a + 60, b2 + 60) for a, b2 in clusters(np.nonzero(bluem.any(axis=0))[0])])
P("L2 red x-clusters:", [(a + 60, b2 + 60) for a, b2 in clusters(np.nonzero(redm.any(axis=0))[0])])

P("### 8. eq box (x455..615 y160..230)")
E = A[160:230, 455:615]
redE = (E[..., 0] > 110) & (E[..., 0] - E[..., 1] > 45) & (E[..., 0] - E[..., 2] > 35)
ysE, xsE = np.nonzero(redE)
P("red px:", int(redE.sum()))
if len(xsE):
    P("red bbox frame: x%d..%d y%d..%d" % (xsE.min() + 455, xsE.max() + 455, ysE.min() + 160, ysE.max() + 160))
# border rows/cols: red pixel counts per column/row
colcnt = redE.sum(axis=0); rowcnt = redE.sum(axis=1)
P("red columns n>40 (frame-x):", [int(x) + 455 for x in np.nonzero(colcnt > 40)[0]])
P("red rows n>40 (frame-y):", [int(y) + 160 for y in np.nonzero(rowcnt > 40)[0]])
bluE = (E[..., 2] - E[..., 0] > 40)
P("blue px in eq zone:", int(bluE.sum()))
# interior fill
ic = A[175:210, 480:590]
lighti = ic.reshape(-1, 3)[ic.reshape(-1, 3).sum(axis=1) > 640]
P("eq interior light mean RGB:", lighti.mean(axis=0).round(1) if len(lighti) else None)

P("### 9. table frame + separators + fills (y315..522 x60..900)")
Tb = A[315:522, 60:900]
dark = Tb.max(axis=2) < 150
colprof = dark.sum(axis=0)
vcols = [int(x) + 60 for x in np.nonzero(colprof > 100)[0]]
P("table dark vertical cols (frame-x, n>100):", vcols)
rowprof = dark.sum(axis=1)
hrows = [int(y) + 315 for y in np.nonzero(rowprof > 400)[0]]
P("table dark horizontal rows (frame-y, n>400):", hrows)
# top rule color
P("top-rule sample y320/321 @x300:", A[320, 300].tolist(), A[321, 300].tolist())
P("bottom rule y516/517 @x300:", A[516, 300].tolist(), A[517, 300].tolist())
# band fills at column x300 (clear of text? use x400 too)
for yy in [335, 345, 355, 365, 380, 390, 400, 410, 425, 435, 445, 452, 465, 470, 475, 488, 495, 510]:
    P("row y%d @x400:" % yy, A[yy, 400].tolist(), "@x200:", A[yy, 200].tolist())
# insert extent: green-cyan fill
G = A[315:380, 600:850]
gc = (G[..., 1] > 200) & (G[..., 0] > 100) & (G[..., 0] < 190) & (G[..., 2] > 140) & (G[..., 2] < 210)
ysG, xsG = np.nonzero(gc)
P("insert green px:", int(gc.sum()))
if len(xsG):
    P("insert bbox frame: x%d..%d y%d..%d" % (xsG.min() + 600, xsG.max() + 600, ysG.min() + 315, ysG.max() + 315))
    P("insert core mean RGB:", G[gc].mean(axis=0).round(1))
# dashed border color of insert: darker px adjacent to the insert edge
# slope yellow cells: bright yellow census y460..478
SY = A[458:480, 140:880]
yel = (SY[..., 0] > 230) & (SY[..., 1] > 230) & (SY[..., 2] < 210)
ysY, xsY = np.nonzero(yel)
P("slope yellow px:", int(yel.sum()))
if len(xsY):
    P("slope yellow bbox frame: x%d..%d y%d..%d" % (xsY.min() + 140, xsY.max() + 140, ysY.min() + 458, ysY.max() + 458))
    ycols = clusters(np.nonzero(yel.any(axis=0))[0])
    P("slope yellow col clusters (frame-x):", [(a + 140, b2 + 140) for a, b2 in ycols])
    P("slope yellow core mean RGB:", SY[yel].mean(axis=0).round(1))
# slope data fill + label fill
P("slope data fill @ (x300,y470):", A[470, 300].tolist(), "label @ (x100,y470):", A[470, 100].tolist())
P("next-x fill @ (x300,y493):", A[493, 300].tolist())
# label column ink extent (x row y336..350)
LX = A[336:352, 60:145]
inkL = LX.max(axis=2) < 150
ysL, xsL = np.nonzero(inkL)
if len(xsL):
    P("x-row label ink frame-x:", int(xsL.min() + 60), "..", int(xsL.max() + 60))
# column separator positions inside band1: darker-than-fill columns x140..881 y333..368
BB = A[333:368, 140:882]
fill_ref = np.median(BB.reshape(-1, 3), axis=0)
dkc = (BB.max(axis=2) < (fill_ref.max() - 60)).sum(axis=0)
seps = [int(x) + 140 for x in np.nonzero(dkc > 20)[0]]
P("band1 separator cols (n>20):", clusters(seps) if seps else "none")

with open("att27_frame_measure.txt", "w") as fh:
    fh.write("\n".join(out) + "\n")
print("WROTE att27_frame_measure.txt")
