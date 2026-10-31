"""Ink extraction for the BL equation box (subtract measured fill colour)."""
from PIL import Image
import numpy as np

P = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
     "09_introduction_to_neural_networks/unique_slides/slide_017.jpg")
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
FILL = np.array([248, 235, 218])


def inkmap(x0, x1, y0, y1, tol=28, label=""):
    sub = a[y0:y1, x0:x1]
    dev = np.abs(sub - FILL).max(axis=2)
    m = dev > tol
    print(f"--- {label} x{x0}-{x1} y{y0}-{y1} tol{tol} ---")
    for i, y in enumerate(range(y0, y1)):
        line = "".join("#" if v else "." for v in m[i])
        if "#" in line:
            print(f"{y:4d} {line}")
    print()


inkmap(108, 420, 455, 510, 30, "BL eq box all")
inkmap(108, 300, 465, 505, 45, "BL eq box left (prefix)")
inkmap(300, 420, 460, 508, 45, "BL eq box right (brace+rows)")
