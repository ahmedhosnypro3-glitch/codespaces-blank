#!/usr/bin/env python3
"""Find exact box-border colors + long edges in original slide_031."""
from PIL import Image
import numpy as np
from collections import Counter

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
orig = Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")
O = np.array(orig)
H, W = O.shape[:2]

# Most common non-white colors
flat = O.reshape(-1,3)
mask = ~(flat.min(axis=1) > 250)
c = Counter(map(tuple, flat[mask]))
print("top 25 non-white colors:")
for col, n in c.most_common(25):
    print("  ", col, n)
