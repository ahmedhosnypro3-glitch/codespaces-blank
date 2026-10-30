#!/usr/bin/env python3
"""Find saturated colors (accents) in the original frame, regardless of exact hex."""
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
mx = a.max(axis=2); mn = a.min(axis=2)
sat = mx - mn
print(f"image {W}x{H}")

# saturated (non-gray) pixels
mask = sat > 40
print(f"saturated pixels: {mask.sum()}")
census = {}
ys, xs = np.where(mask)
# quantize to 32-step buckets
q = (a[mask] // 32) * 32
keys, counts = np.unique(q, axis=0, return_counts=True)
order = np.argsort(counts)[::-1]
print("\ntop saturated colors (quantized):")
shown = 0
for i in order:
    c = keys[i]
    n = counts[i]
    if n < 60:
        break
    print(f"  ~#{c[0]:02X}{c[1]:02X}{c[2]:02X}  n={n}")
    shown += 1
    if shown >= 25:
        break

def blobs(m, label, minpx=60):
    lab, n = ndimage.label(m)
    if n == 0:
        print(f"  {label}: NONE"); return
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    print(f"  {label}: {n} blobs, total {int(sizes.sum())}")
    for i in np.argsort(sizes)[::-1][:12]:
        if sizes[i] < minpx:
            break
        ys2, xs2 = np.where(lab == i + 1)
        print(f"     x[{xs2.min()}..{xs2.max()}] y[{ys2.min()}..{ys2.max()}] px={int(sizes[i])}")

print("\n=== green-dominant blobs (g > r+25 and g > b+25) ===")
blobs((a[:,:,1] > a[:,:,0] + 25) & (a[:,:,1] > a[:,:,2] + 25), "green")
print("\n=== blue-dominant blobs (b > r+25 and b > g+18) ===")
blobs((a[:,:,2] > a[:,:,0] + 25) & (a[:,:,2] > a[:,:,1] + 18), "blue")
print("\n=== red-dominant blobs (r > g+40 and r > b+40) ===")
blobs((a[:,:,0] > a[:,:,1] + 40) & (a[:,:,0] > a[:,:,2] + 40), "red")
print("\n=== purple-ish (r>g and b>g, r~=b) ===")
blobs((a[:,:,0] > a[:,:,1] + 15) & (a[:,:,2] > a[:,:,1] + 15), "purple")
print("\n=== yellow (r>150,g>150,b<130) ===")
blobs((a[:,:,0] > 150) & (a[:,:,1] > 150) & (a[:,:,2] < 130), "yellow")
