#!/usr/bin/env python3
"""Measure ground-truth imagery (pencil airplane sketches) scale in original frames."""
from PIL import Image
import numpy as np
from scipy import ndimage

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/unique_slides/"

def clusters(path, name, region=None, thresh=150, min_px=25):
    im = Image.open(BASE + path).convert("L")
    a = np.array(im)
    H, W = a.shape
    if region:
        x0,y0,x1,y1 = region
        sub = a[y0:y1, x0:x1]
        ox, oy = x0, y0
    else:
        sub = a; ox, oy = 0, 0
    ink = sub < thresh
    lab, n = ndimage.label(ink)
    objs = ndimage.find_objects(lab)
    out=[]
    for i,sl in enumerate(objs):
        m = (lab[sl] == i+1)
        if m.sum() < min_px: continue
        h = sl[0].stop-sl[0].start; w = sl[1].stop-sl[1].start
        out.append((w,h,int(m.sum())))
    out.sort(key=lambda t:-t[2])
    print(f"\n### {name} ({path}) frame={W}x{H} 1px={13.33/W:.4f}in  region={region}")
    print(f"  dark clusters (>= {min_px}px): {len(out)}")
    for w,h,px in out[:14]:
        print(f"    {w:4d}x{h:4d}px  = {w*13.33/W:.3f}x{h*13.33/W:.3f}in   ink={px}")
    return out

# slide_011: right-hand tree panel, upper region (above tree roots) = airplane sketches
clusters("slide_011.jpg", "s011 tree panel upper (airplanes)", region=(560, 250, 900, 330))
# slide_025: bottom plot area full of airplane sketches
clusters("slide_025.jpg", "s025 bottom plot (airplanes)", region=(60, 300, 900, 580))
# slide_010: tree panel upper
clusters("slide_010.jpg", "s010 tree panel upper (airplanes)", region=(620, 250, 960, 330))
