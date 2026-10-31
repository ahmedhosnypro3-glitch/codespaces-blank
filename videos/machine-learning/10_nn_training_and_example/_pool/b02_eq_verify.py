#!/usr/bin/env python3
"""Verify eq4/eq5 mathtext candidates reproduce the existing PNGs exactly."""
import json, subprocess, sys
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
ASSETS = f"{ROOT}/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets"
RENDER = f"{ROOT}/scripts/render_eq.py"
CANDS = {
    "slide_004/eq4.png": [
        r"f'(Net_j) = \frac{1}{1+e^{-Net_j}} \cdot \frac{(1+e^{-Net_j}) - 1}{1+e^{-Net_j}}",
        r"f'(Net_j) = \frac{1}{1+e^{-Net_j}} \cdot \frac{(1+e^{-Net_j}) - 1}{1 + e^{-Net_j}}",
    ],
    "slide_004/eq5.png": [
        r"f'(Net_j) = \frac{1}{1+e^{-Net_j}} \left( 1 - \frac{1}{1+e^{-Net_j}} \right)",
    ],
}

def sig(path):
    a = np.asarray(Image.open(path).convert("RGBA")).astype(int)
    ink = a[:, :, 3] > 10
    rows = np.nonzero(ink.any(axis=1))[0]
    cols = np.nonzero(ink.any(axis=0))[0]
    return a.shape[:2], (int(cols.min()), int(cols.max()), int(rows.min()), int(rows.max())), int(ink.sum())

for rel, cands in CANDS.items():
    dst = f"{ASSETS}/{rel}"
    ts, tb, tn = sig(dst)
    meta = json.load(open(dst + ".meta.json"))
    print(f"\n{rel}: existing {ts} bbox={tb} ink={tn} fs={meta['fontsize_pt']} color={meta['color']}")
    for c in cands:
        out = f"/tmp/b02v_{rel.split('/')[-1]}"
        r = subprocess.run([sys.executable, RENDER, c, out, str(meta["fontsize_pt"]), meta["color"]],
                           capture_output=True, text=True, timeout=180, cwd=ROOT)
        if r.returncode != 0:
            print(f"  MISS {c[:70]} -> {r.stderr.strip()[:100]}")
            continue
        s, b, n = sig(out)
        ok = s == ts and b == tb and abs(n - tn) < 400
        print(f"  {'MATCH' if ok else 'diff '} {c[:76]} -> {s} bbox={b} ink={n}")
