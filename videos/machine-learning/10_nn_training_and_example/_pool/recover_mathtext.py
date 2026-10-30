#!/usr/bin/env python3
"""Recover the mathtext source of each equation PNG.

Re-renders candidate mathtext with scripts/render_eq.py and compares ink bbox
and pixel signature against the existing asset, so the OMML manifest's mathtext
matches the PNG the judge certified.
"""
import json
import subprocess
import sys

import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
VID = f"{ROOT}/videos/machine-learning/10_nn_training_and_example"
ASSETS = f"{VID}/recreated_pptx/build/assets"
RENDER = f"{ROOT}/scripts/render_eq.py"

CANDIDATES = {
    "slide_003/net_eq.png": [
        r"Net_j = \sum_{i} (w_{ji} \cdot O_i)",
        r"Net_j = \sum_{i} (w_{ji} O_i)",
        r"Net_j=\sum_{i}\left(w_{ji}O_i\right)",
    ],
    "slide_003/o_eq.png": [
        r"O_j = f(Net_j) = \frac{1}{(1+e^{-Net_j})}",
        r"O_j = f(Net_j) = 1/(1+e^{-Net_j})",
        r"O_j=f(Net_j)=\frac{1}{1+e^{-Net_j}}",
    ],
    "slide_003/e_eq.png": [
        r"E = \frac{1}{2} \sum_{j} (t_j - O_j)^2",
        r"E = \frac{1}{2}\sum{}_{j}\left(t_j - O_j\right)^2",
        r"E = \frac{1}{2}\sum_{j}(t_j - O_j)^{2}",
    ],
    "slide_004/eq1.png": [
        r"O_j = f(Net_j) = \frac{1}{1+e^{-Net_j}}",
        r"O_j = f(Net_j) = \frac{1}{(1+e^{-Net_j})}",
        r"f(Net_j) = \frac{1}{1+e^{-Net_j}}",
    ],
    "slide_004/eq2.png": [
        r"f(x) = \frac{1}{1+e^{-x}}",
        r"f(x) = \frac{1}{(1+e^{-x})}",
        r"f(x)=\frac{1}{1+e^{-x}}",
    ],
    "slide_004/eq3.png": [
        r"f'(Net_j) = \frac{e^{-Net_j}}{(1+e^{-Net_j})(1+e^{-Net_j})}",
        r"f'(Net_j) = \frac{e^{-Net_j}}{(1+e^{-Net_j})^{2}}",
        r"f'(Net_j)=\frac{\bullet e^{-Net_j}}{(1+e^{-Net_j})(1+e^{-Net_j})}",
    ],
    "slide_004/eq6.png": [
        r"f'(Net_j) = O_j(1 - O_j)",
        r"f'(Net_j) = O_j (1 - O_j)",
        r"f'(Net_j)=O_j(1-O_j)",
    ],
}


def ink_sig(path):
    a = np.asarray(Image.open(path).convert("RGBA")).astype(int)
    alpha = a[:, :, 3]
    ink = alpha > 10
    rows = np.nonzero(ink.any(axis=1))[0]
    cols = np.nonzero(ink.any(axis=0))[0]
    return a.shape[:2], tuple(int(v) for v in (cols.min(), cols.max(), rows.min(), rows.max())), int(ink.sum())


def main():
    for rel, cands in CANDIDATES.items():
        dst = f"{ASSETS}/{rel}"
        target_size, target_bb, target_n = ink_sig(dst)
        meta = json.load(open(dst + ".meta.json"))
        print(f"\n{rel}: existing {target_size} bbox={target_bb} ink={target_n} "
              f"fs={meta['fontsize_pt']} color={meta['color']}")
        for c in cands:
            out = f"/tmp/probe_{rel.split('/')[-1]}"
            try:
                r = subprocess.run(
                    [sys.executable, RENDER, c, out, str(meta["fontsize_pt"]), meta["color"]],
                    capture_output=True, text=True, timeout=180, cwd=ROOT)
                if r.returncode != 0:
                    print(f"  MISS {c[:60]} -> {r.stderr.strip()[:80]}")
                    continue
                s, bb, n = ink_sig(out)
                match = "MATCH" if (s == target_size and bb == target_bb and abs(n - target_n) < 400) else "diff "
                print(f"  {match} {c[:66]} -> {s} bbox={bb} ink={n}")
            except subprocess.TimeoutExpired:
                print(f"  TIMEOUT {c[:60]}")


if __name__ == "__main__":
    main()
