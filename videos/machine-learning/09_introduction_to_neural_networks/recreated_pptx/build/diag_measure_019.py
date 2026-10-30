#!/usr/bin/env python3
"""Measure slide 019 geometry: original frame vs recreation render.

Both are mapped into the house-frame coordinate system (the crimson/red frame
region is the slide body in both images).
"""
import numpy as np
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_019.jpg"
REND = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_019_rejudge_rendered-1.png"


def bbox_of_mask(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def frame_box(img, kind):
    a = np.asarray(img.convert("RGB")).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    if kind == "orig":
        # muted crimson #B94350 frame
        m = (r > 140) & (r < 220) & (g > 40) & (g < 110) & (b > 50) & (b < 120)
        # keep only long thin runs: use row/col counts
        rows = m.sum(axis=1)
        cols = m.sum(axis=0)
        ys = np.nonzero(rows > img.width * 0.4)[0]
        xs = np.nonzero(cols > img.height * 0.4)[0]
        if len(ys) and len(xs):
            return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
        return bbox_of_mask(m)
    # render: house frame #C00000
    m = (r > 150) & (r < 210) & (g < 60) & (b < 60)
    return bbox_of_mask(m)


def blue_panels(img):
    a = np.asarray(img.convert("RGB")).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = (b > 140) & (r < 120) & (g < 120)
    # column profile to find vertical border lines
    cols = m.sum(axis=0)
    thr = img.height * 0.05
    cand = np.nonzero(cols > thr)[0]
    groups = []
    for c in cand:
        if groups and c - groups[-1][-1] <= 2:
            groups[-1].append(c)
        else:
            groups.append([c])
    return [(gp[0], gp[-1]) for gp in groups], m


def arrow_box(img, frame, kind):
    """Red-outlined hollow arrow between the bottom panels."""
    a = np.asarray(img.convert("RGB")).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    fx0, fy0, fx1, fy1 = frame
    # search band: vertical middle of lower row, horizontal gutter
    if kind == "orig":
        x0, x1 = int(0.40 * img.width), int(0.49 * img.width)
        y0, y1 = int(0.63 * img.height), int(0.77 * img.height)
    else:
        x0, x1 = int(0.42 * img.width), int(0.53 * img.width)
        y0, y1 = int(0.60 * img.height), int(0.78 * img.height)
    reg = np.zeros(a.shape[:2], bool)
    reg[y0:y1, x0:x1] = True
    # bright red pixels (stroke) - exclude dark red frame
    m = reg & (r > 170) & (g < 80) & (b < 80)
    return bbox_of_mask(m), (x0, y0, x1, y1)


for name, path, kind in (("ORIGINAL", ORIG, "orig"), ("RENDER", REND, "rend")):
    img = Image.open(path)
    print(f"=== {name} {img.size}")
    fr = frame_box(img, kind)
    print("frame bbox:", fr)
    groups, mask = blue_panels(img)
    print("blue vertical border groups (x):", groups)
    if len(groups) >= 2:
        # panel left/right edges from border groups
        edges = [g[0] for g in groups] + [groups[-1][1]]
        print("panel x edges (px):", edges)
    rows = mask.sum(axis=1)
    thr = img.width * 0.03
    cand = np.nonzero(rows > thr)[0]
    gs = []
    for c in cand:
        if gs and c - gs[-1][-1] <= 2:
            gs[-1].append(c)
        else:
            gs.append([c])
    print("blue horizontal border groups (y):", [(g[0], g[-1]) for g in gs])
    ab, sr = arrow_box(img, fr, kind)
    print("arrow red-stroke bbox:", ab, "search:", sr)
    if ab:
        print("  arrow px size:", ab[2] - ab[0], "x", ab[3] - ab[1])
