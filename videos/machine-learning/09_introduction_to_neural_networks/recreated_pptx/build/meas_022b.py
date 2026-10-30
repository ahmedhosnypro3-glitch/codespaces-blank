"""Find the actual dominant colors and edge lines in slide_022 original."""
from PIL import Image
import numpy as np
from collections import Counter

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

# Dominant colors (quantize to 16-level per channel)
q = (a // 16 * 16)
flat = q.reshape(-1, 3)
c = Counter(map(tuple, flat))
print("top 25 colors (RGB, count):")
for col, n in c.most_common(25):
    print("  #%02x%02x%02x" % col, n)
