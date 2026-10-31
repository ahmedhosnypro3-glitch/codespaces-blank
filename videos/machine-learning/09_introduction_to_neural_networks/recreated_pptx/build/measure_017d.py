"""ASCII map of the two bottom equation boxes (classify ink vs fill)."""
from PIL import Image
import numpy as np

P = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
     "09_introduction_to_neural_networks/unique_slides/slide_017.jpg")
a = np.asarray(Image.open(P).convert("RGB")).astype(int)


def classify(c):
    r, g, b = c
    if r > g + 25 and r > b + 25:
        return "R" if r < 210 else "r"
    if r < 110 and g < 110 and b < 110:
        return "#"
    if r > 235 and r - b > 10:
        return "."
    return " "


def amap(x0, x1, y0, y1, step=2, label=""):
    print(f"--- {label} x{x0}-{x1} y{y0}-{y1} (step {step}) ---")
    hdr = "     " + "".join(str((x // 10) % 10) if x % 20 == 0 else " "
                             for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1, step):
        line = "".join(classify(tuple(a[y, x])) for x in range(x0, x1, step))
        print(f"{y:4d} {line}")


amap(105, 425, 452, 512, 2, "bottom-left eq box")
amap(460, 800, 452, 512, 2, "bottom-right eq box")
amap(590, 900, 160, 215, 2, "top-right eq box")
