#!/usr/bin/env python3
"""Re-verify slide 050 measured facts (task-state recovery; summary is notes, not proof)."""
from PIL import Image
from collections import Counter

im = Image.open('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_050.jpg').convert('RGB')
W, H = im.size
px = im.load()

def band_colors(y0, y1, x0, x1, n=8):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[px[x, y]] += 1
    return c.most_common(n)

print("=== panel interior samples ===")
for (x, y) in [(700,500),(200,500),(880,300),(600,520),(50,300),(860,500)]:
    print((x,y), px[x,y])

print("\n=== table box: vertical profile at x=100 (rows 50..135) ===")
prev=None
for y in range(50,136):
    p = px[100,y]
    if p != prev:
        print(y, p)
        prev = p

print("\n=== table box: horizontal profile at y=70 (cols 60..260) ===")
prev=None
for x in range(60,262):
    p = px[x,70]
    if p != prev:
        print(x, p)
        prev = p

print("\n=== navy box region: find navy-ish px bbox (all frame, excl top-left table area) ===")
xs=[];ys=[]
for y in range(0,H):
    for x in range(0,W):
        r,g,b = px[x,y]
        if b>70 and b<160 and r<80 and g<70 and b-r>30:
            xs.append(x);ys.append(y)
print("count",len(xs), "bbox", (min(xs),min(ys),max(xs),max(ys)) if xs else None)

print("\n=== bottom of navy box vertical scan at x=430 ===")
prev=None
for y in range(50,140):
    p = px[430,y]
    if p != prev:
        print(y, p)
        prev = p

print("\n=== caption box vertical scan x=150 rows 130..250 ===")
prev=None
for y in range(128,252):
    p = px[150,y]
    if p != prev:
        print(y,p)
        prev=p

print("\n=== caption box horiz scan y=190 cols 60..250 ===")
prev=None
for x in range(60,250):
    p = px[x,190]
    if p != prev:
        print(x,p)
        prev=p

print("\n=== pink box: horiz scan y=120 cols 730..845 ===")
prev=None
for x in range(730,845):
    p = px[x,120]
    if p != prev:
        print(x,p)
        prev=p

print("\n=== pink box: vert scan x=786 rows 50..180 ===")
prev=None
for y in range(50,180):
    p = px[786,y]
    if p != prev:
        print(y,p)
        prev=p

print("\n=== red box 'Iteration 2': vert scan x=150 rows 270..310 ===")
prev=None
for y in range(270,312):
    p = px[150,y]
    if p != prev:
        print(y,p)
        prev=p

print("\n=== red box: horiz scan y=290 cols 78..222 ===")
prev=None
for x in range(78,222):
    p = px[x,290]
    if p != prev:
        print(x,p)
        prev=p

print("\n=== chart: horiz scan y=300 cols 305..830 ===")
prev=None
for x in range(305,830):
    p = px[x,300]
    if p != prev:
        print(x,p)
        prev=p
