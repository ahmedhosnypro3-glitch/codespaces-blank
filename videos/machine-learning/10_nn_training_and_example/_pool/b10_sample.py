import sys
import numpy as np
from PIL import Image

def sample(path, pts):
    a = np.array(Image.open(path).convert("RGB"))
    print(f"# {path} {a.shape[1]}x{a.shape[0]}")
    for label, fx, fy in pts:
        x = int(fx * a.shape[1]); y = int(fy * a.shape[0])
        patch = a[max(0, y-2):y+3, max(0, x-2):x+3].reshape(-1, 3)
        med = np.median(patch, axis=0).astype(int)
        print(f"  {label:26s} ({fx:.3f},{fy:.3f}) px=({x},{y}) rgb=#{med[0]:02X}{med[1]:02X}{med[2]:02X}")

if __name__ == "__main__":
    pts = [
        ("bg top-center", 0.50, 0.05),
        ("bg far-left-mid", 0.02, 0.50),
        ("bg bottom-center", 0.50, 0.97),
        ("cyanbox interior", 0.06, 0.12),
        ("tan canvas", 0.42, 0.15),
        ("outer frame edge", 0.015, 0.50),
        ("just inside frame", 0.035, 0.50),
        ("badge area", 0.94, 0.07),
        ("bottom-left panel", 0.30, 0.70),
        ("bottom-right panel", 0.80, 0.75),
        ("lower-left white", 0.20, 0.55),
    ]
    sample(sys.argv[1], pts)
