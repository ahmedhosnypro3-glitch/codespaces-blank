#!/usr/bin/env python3
"""Slide 032 — connected-component census of the original graph's label ink.

For every dark-ink connected component in the original graph area, print its
bounding box and an ASCII bitmap. Used to identify the right chord-endpoint
label glyph-by-glyph (the crop_9_graph FAIL: "(7, 7)" vs "(?, ?)").
"""
import os
from collections import deque
from PIL import Image

ROOT = "/worksp""aces/codespaces-blank/ai_llm_slides"
DECK = os.path.join(ROOT, "videos/machine-learning/03_ridger_regression_gradient_descent")
ORIG = os.path.join(DECK, "unique_slides/slide_032.jpg")
REND = os.path.join(DECK, "recreated_pptx/qa/slide032/render_10.png")

def components(im, x0, y0, x1, y1, thr, gap=1):
    px = im.load()
    pts = set()
    for y in range(y0, y1):
        for x in range(x0, x1):
            if px[x, y] < thr:
                pts.add((x, y))
    comps = []
    while pts:
        seed = pts.pop()
        q = deque([seed]); blob = [seed]
        while q:
            cx, cy = q.popleft()
            for dx in range(-gap, gap + 1):
                for dy in range(-gap, gap + 1):
                    p = (cx + dx, cy + dy)
                    if p in pts:
                        pts.remove(p); q.append(p); blob.append(p)
        comps.append(blob)
    comps.sort(key=lambda b: (min(p[0] for p in b), min(p[1] for p in b)))
    return comps

def art(blob, im, thr):
    xs = [p[0] for p in blob]; ys = [p[1] for p in blob]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    px = im.load()
    print(f"   blob bbox x{x0}..{x1} y{y0}..{y1} ({x1-x0+1}x{y1-y0+1}) n={len(blob)}")
    for y in range(y0, y1 + 1):
        print("     " + "".join("#" if px[x, y] < thr else "." for x in range(x0, x1 + 1)))
    return (x0, x1, y0, y1)

def report(path, label, x0, y0, x1, y1, thr, minpix=2):
    im = Image.open(path).convert("L")
    print(f"\n########## {label}  ({path}) thr<{thr} region x{x0}..{x1} y{y0}..{y1}")
    comps = components(im, x0, y0, x1, y1, thr)
    for b in comps:
        if len(b) < minpix:
            continue
        art(b, im, thr)
    return comps

# original: the whole right-hand label neighbourhood
report(ORIG, "ORIGINAL right-label neighbourhood", 700, 120, 790, 170, 170)
report(ORIG, "ORIGINAL left-label neighbourhood (control: known '(2, 10)')", 610, 120, 700, 170, 170)
