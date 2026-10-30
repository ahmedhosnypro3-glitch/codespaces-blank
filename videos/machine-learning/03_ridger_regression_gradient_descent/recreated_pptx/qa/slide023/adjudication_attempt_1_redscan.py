#!/usr/bin/env python3
"""Per-row red-ink scan under the two red numbers, both images (A3c)."""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg"
RENDER = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide023/render_1.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
a = np.array(Image.open(RENDER).convert("RGB")).astype(int)
S = a.shape[1] / 960.0

def redp(sub):
    return (sub[:, :, 0] - sub[:, :, 1] > 55) & (sub.mean(axis=2) < 210)

def scan(img, x0, x1, y0, y1, sc, pred, label):
    sub = img[int(round(y0 * sc)):int(round(y1 * sc)), int(round(x0 * sc)):int(round(x1 * sc))]
    m = pred(sub)
    print(f"--- {label} (x{x0}..{x1} y{y0}..{y1}) ---")
    for i in range(m.shape[0]):
        n = int(m[i].sum())
        if n:
            xs = np.where(m[i])[0]
            print(f"  y{y0 + i / sc:.1f}: n={n:4d} x{x0 + xs.min() / sc:.0f}..{x0 + xs.max() / sc:.0f}")

# The blue-box bottom stroke is at y425.5 and EX2's baseline is y416 with 'p' descender
# to ~421; the digits sit y399..418. A TRUE underline would be a 2px bar at y420..422
# spanning the full run width with a GAP from the glyph bottoms.
scan(o, 180, 340, 415, 428, 1.0, redp, "ORIGINAL under red 1,000,000,000")
scan(a, 180, 340, 415, 428, S, redp, "RENDER   under red 1,000,000,000")
print()
scan(o, 520, 585, 380, 388, 1.0, redp, "ORIGINAL under red 1000")
scan(a, 520, 585, 380, 388, S, redp, "RENDER   under red 1000")

print()
print("=== ALL-ink (non-red too) rows just below each red run, to catch a") 
print("    NON-red underline if the original used black/gray for it ===")
dark = lambda s: s.mean(axis=2) < 180
scan(o, 180, 340, 415, 428, 1.0, dark, "ORIGINAL all-ink under red 1e9")
scan(a, 180, 340, 415, 428, S, dark, "RENDER   all-ink under red 1e9")
