#!/usr/bin/env python3
"""Geometry probe of the ORIGINAL slide_003: bottom-strip boxes, diagram panel,
and the coloured summary boxes, measured in original pixels (960x540)."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def near(a, rgb, tol=26):
    return (abs(a[:, :, 0] - rgb[0]) < tol) & (abs(a[:, :, 1] - rgb[1]) < tol) & (abs(a[:, :, 2] - rgb[2]) < tol)


def runs(mask, axis, minlen=8):
    """Contiguous run lengths along `axis` of a boolean mask."""
    m = mask.any(axis=axis)
    out, start = [], None
    for i, v in enumerate(m):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= minlen:
                out.append((start, i - 1))
            start = None
    if start is not None and len(m) - start >= minlen:
        out.append((start, len(m) - 1))
    return out


def main():
    a = np.asarray(Image.open(f"{BASE}/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
    H, W = a.shape[:2]
    print(f"original {W}x{H}")
    for name, rgb in [
        ("cream FFFFE0", (255, 255, 224)),
        ("lightblue ADD8E6", (173, 216, 230)),
        ("lightgreen 90EE90", (144, 238, 144)),
        ("beige F5EFE0", (245, 239, 224)),
        ("darkred 8B0000", (139, 0, 0)),
        ("blue 0000FF", (0, 0, 255)),
        ("green 008000", (0, 128, 0)),
    ]:
        m = near(a, rgb, tol=30)
        print(f"\n## {name}: {m.sum()} px")
        cols = runs(m, 0, 12)
        rows = runs(m, 1, 12)
        print(f"   col bands: {cols[:14]}")
        print(f"   row bands: {rows[:14]}")


if __name__ == "__main__":
    main()
