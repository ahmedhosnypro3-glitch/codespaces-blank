#!/usr/bin/env python3
"""Report faint-ink x runs per row inside the fan zone."""
from PIL import Image
import numpy as np
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)


def groups_of(xs, gap=2):
    out = []
    if not xs:
        return out
    st = prev = xs[0]
    for v in xs[1:]:
        if v - prev > gap:
            out.append((st, prev)); st = v
        prev = v
    out.append((st, prev))
    return out


print("=== faint ink runs (diff from local white > 12), fan zone x430-700 ===")
for y in list(range(230, 272, 2)) + list(range(292, 330, 2)) + list(range(378, 420, 2)):
    xs = [x for x in range(430, 700) if abs(a[y, x] - np.array([254, 254, 254])).sum() > 12]
    g = groups_of(xs)
    if g:
        print(f"  y={y}: " + " ".join(f"{g0}-{g1}" for g0, g1 in g[:8]))
