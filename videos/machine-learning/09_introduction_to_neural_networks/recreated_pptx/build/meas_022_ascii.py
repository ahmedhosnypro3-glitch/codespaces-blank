"""ASCII structural map + per-box border/fill/ink analysis of slide_022 original."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(axis=2); mn = a.min(axis=2)
sat = mx - mn
dark = mx < 190          # any dark ink
redish = dark & (R - G > 55) & (R - B > 55)
bluish = dark & (B - R > 45) & (B - G > 45)
greenish = dark & (G - R > 40) & (G - B > 40)
blackish = dark & (sat < 60)
goldish = dark & (R > 90) & (G > 70) & (B < 130) & (R - B > 40) & (G - B > 20)

print("=== ASCII MAP (1 char = 8x8 px block), x 0..960 y 0..540 ===")
for by in range(0, H, 8):
    line = ""
    for bx in range(0, W, 8):
        sl = (slice(by, by + 8), slice(bx, bx + 8))
        rr = redish[sl].sum(); bb = bluish[sl].sum()
        gg = greenish[sl].sum(); kk = blackish[sl].sum()
        dl = goldish[sl].sum()
        if rr >= 6: line += "R"
        elif bb >= 6: line += "B"
        elif gg >= 4: line += "G"
        elif dl >= 6: line += "D"
        elif kk >= 8: line += "#"
        elif kk >= 3: line += "+"
        else: line += "."
    print("%3d %s" % (by, line))

print("\nlegend: R=red B=blue G=green D=gold #=black +=faintblack .=light")
