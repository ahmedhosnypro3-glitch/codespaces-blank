#!/usr/bin/env python3
"""b15 PIL self-check: slide 030 recreation render vs original frame.
Matched-scale ink-band comparison at the 960x540 frame scale (render is 2001x1125,
so scale factor = 540/1125 = 0.48 of render px)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
FRAME = 960.0 / 2001.0  # render px -> frame px


def load(p, scale):
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    if scale != 1.0:
        im = Image.fromarray(a.astype("uint8"))
        im = im.resize((int(a.shape[1] * scale), int(a.shape[0] * scale)), Image.LANCZOS)
        a = np.asarray(im).astype(int)
    return a


def ink(a):
    bg = a[2, 2]
    return np.abs(a - bg).sum(axis=2) > 40


def bands(m, axis, thresh=3):
    cnt = m.sum(axis=axis)
    out, st = [], None
    for i, c in enumerate(cnt):
        if c >= thresh and st is None: st = i
        elif c < thresh and st is not None: out.append((st, i - 1)); st = None
    if st is not None: out.append((st, len(cnt) - 1))
    merged = []
    for s, e in out:
        if merged and s - merged[-1][1] <= 2: merged[-1] = (merged[-1][0], e)
        else: merged.append((s, e))
    return merged


def main():
    orig = load(f"{NS}/unique_slides/slide_030.jpg", 1.0)
    ren = load(f"{NS}/qa/slide030/b15/render-1.png", FRAME)
    print(f"orig {orig.shape[1]}x{orig.shape[0]}  render {ren.shape[1]}x{ren.shape[0]}")
    print(f"orig bg {orig[2,2]}  render bg {ren[2,2]}")
    o, r = ink(orig), ink(ren)
    print(f"orig ink px {int(o.sum())}  render ink px {int(r.sum())}")
    print("--- row bands (y, count) orig vs render ---")
    for name, (y0, y1) in {"title": (15, 60), "eq1": (95, 130), "eq2": (125, 160),
                           "eq3": (160, 200), "bwd": (205, 240), "eq4": (235, 265),
                           "eq5": (265, 290), "eq6": (295, 320), "grid": (320, 500),
                           "badge": (20, 45)}.items():
        print(f" {name:6s} orig {int(o[y0:y1].sum()):6d} | rend {int(r[y0:y1].sum()):6d}")
    print("--- orig text rows ---", [(s, e) for s, e in bands(o, 1)][:14])
    print("--- rend text rows ---", [(s, e) for s, e in bands(r, 1)][:14])
    print("--- orig cols ---", [(s, e) for s, e in bands(o, 0)][:14])
    print("--- rend cols ---", [(s, e) for s, e in bands(r, 0)][:14])


main()
