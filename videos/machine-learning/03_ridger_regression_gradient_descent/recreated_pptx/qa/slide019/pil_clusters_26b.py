#!/usr/bin/env python3
"""Correct per-image indexing: orig 960x540 native (scale 1.0), render per-axis
(sx=W/960, sy=H/540). Cluster-dump of the outlier column x56..130 y175..515 for
both images. Replaces the void-orig-indexed want table in pil_probe_26.py."""
from PIL import Image
import numpy as np
from collections import deque
import sys

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide019"
REND = sys.argv[1] if len(sys.argv) > 1 else f"{Q}/render_26.png"


def classify(px):
    r, g, b = px
    if r > 200 and g > 200 and b < 190:
        return "YELBG"
    if b > r + 25 and b > g + 25 and b > 70:
        return "BLUE"
    if r > g + 40 and r > b + 40 and r > 90:
        return "REDD"
    if g > r + 30 and g > b + 30 and g > 80:
        return "GREEN"
    if r < 120 and g < 120 and b < 120:
        return "DARK"
    return None


def clusters(img, x0, y0, x1, y1, scale=(1.0, 1.0), min_n=6):
    H, W = y1 - y0, x1 - x0
    lab = np.zeros((H, W), dtype=bool)
    cls = {}
    px = img.load()
    for fy in range(y0, y1):
        for fx in range(x0, x1):
            sx, sy = int(fx * scale[0]), int(fy * scale[1])
            if sx >= img.size[0] or sy >= img.size[1]:
                continue
            c = classify(px[sx, sy])
            if c and c != "YELBG":
                lab[fy - y0, fx - x0] = True
                cls[(fx, fy)] = c
    seen = np.zeros_like(lab)
    out = []
    for i in range(H):
        for j in range(W):
            if lab[i, j] and not seen[i, j]:
                q = deque([(i, j)])
                seen[i, j] = 1
                pts = []
                while q:
                    y, x = q.popleft()
                    pts.append((x + x0, y + y0))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < H and 0 <= nx < W and lab[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = 1
                                q.append((ny, nx))
                if len(pts) >= min_n:
                    xs = [p[0] for p in pts]
                    ys = [p[1] for p in pts]
                    cc = {}
                    for p in pts:
                        cc[cls[p]] = cc.get(cls[p], 0) + 1
                    out.append((min(xs), min(ys), max(xs), max(ys), len(pts),
                                sorted(cc.items(), key=lambda kv: -kv[1])))
    out.sort(key=lambda c: (c[1], c[0]))
    return out


def yellow_bbox(img, x0, y0, x1, y1, scale=(1.0, 1.0)):
    px = img.load()
    xs, ys = [], []
    for fy in range(y0, y1):
        for fx in range(x0, x1):
            sx, sy = int(fx * scale[0]), int(fy * scale[1])
            if sx >= img.size[0] or sy >= img.size[1]:
                continue
            r, g, b = px[sx, sy]
            if r > 200 and g > 190 and b < 140:
                xs.append(fx)
                ys.append(fy)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


orig = Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")
rend = Image.open(REND).convert("RGB")
SX = rend.size[0] / orig.size[0]
SY = rend.size[1] / orig.size[1]
print(f"orig={orig.size} rend={rend.size} scale=({SX:.5f},{SY:.5f})")

print("\n== ORIG outlier col x56..130 y175..515 clusters (native indexing) ==")
for c in clusters(orig, 56, 175, 130, 515):
    print(f"  ({c[0]:3d},{c[1]:3d})-({c[2]:3d},{c[3]:3d}) w{c[2]-c[0]+1:3d} h{c[3]-c[1]+1:3d} n={c[4]:4d} {c[5]}")

print("\n== RENDER outlier col same frame zone (scaled indexing) ==")
for c in clusters(rend, 56, 175, 130, 515, (SX, SY)):
    print(f"  ({c[0]:3d},{c[1]:3d})-({c[2]:3d},{c[3]:3d}) w{c[2]-c[0]+1:3d} h{c[3]-c[1]+1:3d} n={c[4]:4d} {c[5]}")

print("\n== YELLOW patches x60..140 per band (orig native vs render scaled) ==")
for tag, y0, y1 in [("patch_g1", 264, 292), ("patch_g2", 371, 399), ("patch_g3", 475, 503)]:
    o = yellow_bbox(orig, 60, y0, 140, y1)
    r = yellow_bbox(rend, 60, y0, 140, y1, (SX, SY))
    print(f"  {tag}: orig={o} rend={r}")
