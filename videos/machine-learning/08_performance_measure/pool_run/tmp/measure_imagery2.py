#!/usr/bin/env python3
"""Scan whole frames for airplane-sketch-sized dark clusters (ground-truth imagery scale)."""
from PIL import Image
import numpy as np
from scipy import ndimage

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/unique_slides/"

def scan(path, name, wmin=40, wmax=260, hmin=25, hmax=200, minpx=200):
    im = Image.open(BASE + path).convert("L")
    a = np.array(im); H, W = a.shape
    ink = a < 150
    ndimage.binary_closing(ink, np.ones((3,3)), output=ink)   # fuse sketch strokes
    lab, n = ndimage.label(ink)
    out=[]
    for i, sl in enumerate(ndimage.find_objects(lab)):
        m = (lab[sl] == i+1); px = int(m.sum())
        if px < minpx: continue
        w = sl[1].stop-sl[1].start; h = sl[0].stop-sl[0].start
        if wmin <= w <= wmax and hmin <= h <= hmax:
            out.append((sl[1].start, sl[0].start, w, h, px))
    out.sort(key=lambda t: -t[4])
    print(f"\n### {name}  frame={W}x{H}  1px={13.33/W:.4f}in")
    print(f"  sketch-sized clusters (w {wmin}-{wmax}, h {hmin}-{hmax}, ink>={minpx}): {len(out)}")
    for x,y,w,h,px in out[:16]:
        print(f"    at x={x:4d} y={y:4d}  size {w:4d}x{h:4d}px = {w*13.33/W:.2f}x{h*13.33/W:.2f}in  ink={px}")

scan("slide_011.jpg", "s011")
scan("slide_010.jpg", "s010")
scan("slide_025.jpg", "s025")
scan("slide_019.jpg", "s019")
