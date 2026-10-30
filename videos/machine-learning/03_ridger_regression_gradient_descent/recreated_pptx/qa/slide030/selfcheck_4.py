"""Self-check 4 — slide 030: remaining regions (red dot, param table, eq PNGs,
title colors, callout, arrow, iter-table fills) render vs original."""
import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540
def bbox(fx0,fy0,fx1,fy1): return int(round(fx0*SX)), int(round(fy0*SY)), int(round(fx1*SX)), int(round(fy1*SY))
def mode_rgb(img, box, name, note=""):
    x0,y0,x1,y1 = box
    sub = img[y0:y1, x0:x1].reshape(-1,3)
    cnt = {}
    for p in sub:
        k = tuple(p//10*10)
        cnt[k] = cnt.get(k,0)+1
    top = sorted(cnt.items(), key=lambda kv:-kv[1])[:4]
    print(f"   {name:28s} mode colors: " + ", ".join("#%02X%02X%02X(%d)" % (k[0],k[1],k[2],v) for k,v in top) + ("  " + note if note else ""))

print("== 1. RED DOT in plot (orig bbox x659..662 y180..186; build center 662,183 d8) ==")
def isred(s): return (s[:,:,0]>90)&((s[:,:,0]-s[:,:,1])>40)&((s[:,:,0]-s[:,:,2])>10)
for nm, img, sc in (("render", ren, 1), ("orig", orig, 1)):
    if nm == "render":
        x0,y0,x1,y1 = bbox(650,172,676,196)
    else:
        x0,y0,x1,y1 = 650,172,676,196
    sub = img[y0:y1, x0:x1]
    m = isred(sub)
    ys, xs = np.nonzero(m)
    if len(xs):
        if nm == "render":
            print(f"   {nm}: red bbox frame x{(x0+xs.min())/SX:.1f}..{(x0+xs.max())/SX:.1f} y{(y0+ys.min())/SY:.1f}..{(y0+ys.max())/SY:.1f} center=({(x0+(xs.min()+xs.max())/2)/SX:.1f},{(y0+(ys.min()+ys.max())/2)/SY:.1f})")
        else:
            print(f"   {nm}: red bbox frame x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} center=({x0+(xs.min()+xs.max())/2:.1f},{y0+(ys.min()+ys.max())/2:.1f})")

print("== 2. PARAM TABLE row fills (orig y199..281, rows 199-226 / 226-253 / 253-281) ==")
rows = [(200,225,"row1 step/0.2"), (228,251,"row2 initialX/3"), (256,280,"row3 delta/0.1")]
for nm, img in (("render", ren), ("orig", orig)):
    print(f" -- {nm}")
    for ny0, ny1, lab in rows:
        if nm == "render":
            x0,y0,x1,y1 = bbox(120,ny0,220,ny1)
        else:
            x0,y0,x1,y1 = 120,ny0,220,ny1
        mode_rgb(img, (x0,y0,x1,y1), lab)

print("== 3. EQUATION PNG ink presence (eq box A x399..530 y185..212; green box 'X=5' x348..554 y234..281) ==")
def darkish(s): return s.sum(axis=2) < 500
for nm, img in (("render", ren), ("orig", orig)):
    if nm == "render":
        bA = bbox(400,186,530,212); bX = bbox(350,236,552,280)
    else:
        bA = (400,186,530,212); bX = (350,236,552,280)
    for lab, b in (("eq-A ink", bA), ("greenbox ink", bX)):
        x0,y0,x1,y1 = b
        n = int(darkish(img[y0:y1, x0:x1]).sum())
        print(f"   {nm} {lab}: {n} ink px")

print("== 4. TITLE colors (orig: red C00000 + green 008000 + red; x58..556 y65..84) ==")
def sat_red(s): return (s[:,:,0]>120)&(s[:,:,1]<100)&(s[:,:,2]<100)
def sat_green(s): return (s[:,:,1]>s[:,:,0]+25)&(s[:,:,1]>s[:,:,2]+25)&(s[:,:,1]>60)&(s[:,:,1]<240)
for nm, img in (("render", ren), ("orig", orig)):
    if nm == "render":
        b = bbox(56,60,560,88)
    else:
        b = (56,60,560,88)
    x0,y0,x1,y1 = b
    sub = img[y0:y1, x0:x1]
    nr, ng = int(sat_red(sub).sum()), int(sat_green(sub).sum())
    print(f"   {nm}: red px={nr} green px={ng}")

print("== 5. CALLOUT box (orig x335..569 y292..320 fill F7C8FA border purple; text purple italic) ==")
for nm, img in (("render", ren), ("orig", orig)):
    if nm == "render":
        x0,y0,x1,y1 = bbox(340,296,560,318)
    else:
        x0,y0,x1,y1 = 340,296,560,318
    mode_rgb(img, (x0,y0,x1,y1), "callout core")

print("== 6. ITER TABLE row-fill colors (orig rows y334..523; build groups at 334/380/427/473/499) ==")
for nm, img in (("render", ren), ("orig", orig)):
    print(f" -- {nm}")
    for ymid, lab in ((345,"g1 x-row"), (391,"g2 x-delta"), (438,"g3 x+delta"), (482,"slope"), (508,"next-x")):
        if nm == "render":
            x0,y0,x1,y1 = bbox(300,ymid-6,500,ymid+6)
        else:
            x0,y0,x1,y1 = 300,ymid-6,500,ymid+6
        mode_rgb(img, (x0,y0,x1,y1), lab)
