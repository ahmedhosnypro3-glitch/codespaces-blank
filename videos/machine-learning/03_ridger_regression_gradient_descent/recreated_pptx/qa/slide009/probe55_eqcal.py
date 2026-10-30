#!/usr/bin/env python3
"""Probe 55: calibrate mathtext equation render size against the frame's ink."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

OUT = "/home/ahmed/Projects/ai_llm_slides/scratch/tmp/eq_cal"
os.makedirs(OUT, exist_ok=True)
RE = "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py"

# frame truth: ink box + glyph row structure (frame px == pt)
TARGETS = {
    "50.85^{2} = 2585": {"x": (226, 307), "y": (154, 166), "w": 82, "h": 13},
    "63.64^{2} = 4050": {"x": (643, 723), "y": (154, 166), "w": 81, "h": 13},
}

for latex, t in TARGETS.items():
    print(f"\n=== {latex}  target ink w={t['w']} h={t['h']} (frame pt) ===")
    for fs in (11, 12, 13, 14, 15, 16, 17, 18):
        p = f"{OUT}/cal_{fs}.png"
        out = subprocess.run([sys.executable, RE, latex, p, str(fs), "000000"],
                             capture_output=True, text=True)
        if out.returncode != 0:
            print(f"  fs={fs}: FAIL {out.stderr.strip()[:120]}")
            continue
        info = json.loads(out.stdout)
        im = Image.open(p)
        a = np.asarray(im)
        ink = a[:, :, 3] > 8
        rows = np.where(ink.any(axis=1))[0]
        cols = np.where(ink.any(axis=0))[0]
        PAD = 8
        iw = cols[-1] - cols[0] + 1 - 2 * PAD
        ih = rows[-1] - rows[0] + 1 - 2 * PAD
        w_pt = iw / 600 * 72
        h_pt = ih / 600 * 72
        print(f"  fs={fs:2d}: ink {iw}x{ih}px = {w_pt:.2f}x{h_pt:.2f} pt  "
              f"ratio w/h={w_pt/h_pt:.2f}  (target ratio {t['w']/t['h']:.2f})")
