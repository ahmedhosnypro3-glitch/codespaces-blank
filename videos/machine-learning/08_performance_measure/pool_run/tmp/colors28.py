from PIL import Image
import numpy as np
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/unique_slides/slide_028-.jpg").convert("RGB")
a = np.asarray(im).astype(int)

def dom(x0, y0, x1, y1, label):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    # keep saturated/dark pixels only
    mx = reg.max(axis=1); mn = reg.min(axis=1)
    ink = reg[(mx < 210)]
    if len(ink) == 0:
        print(f"{label}: no ink"); return
    # classify
    blue = ((ink[:,2] - ink[:,0] > 40)).sum()
    red = ((ink[:,0] - ink[:,2] > 40) & (ink[:,0] - ink[:,1] > 30)).sum()
    dark = ((ink.max(axis=1) < 130)).sum()
    print(f"{label}: n={len(ink)} blue={blue} red={red} dark={dark}  mean={ink.mean(axis=0).round(0)}  darkest={ink[ink.sum(axis=1).argmin()]}")

# para2 row y180-199
dom(80, 178, 360, 201, "para2-left(x80-360)")
dom(360, 178, 760, 201, "para2-right(x360-760)")
# para1 line1
dom(80, 112, 805, 130, "para1-line1")
# para1 line2
dom(80, 134, 175, 151, "para1-line2")
# tpr leadin
dom(80, 225, 745, 246, "tpr-leadin")
# tpr def text region (inside white box)
dom(330, 258, 855, 310, "tpr-def")
# fpr def text
dom(338, 368, 885, 420, "fpr-def")
# best value 1
dom(558, 312, 695, 336, "best1")
# best value 0
dom(558, 420, 695, 445, "best0")
# conclusion
dom(80, 455, 680, 480, "conclusion")
# title
dom(170, 60, 760, 100, "title")
# background sample
print("bg corner", a[520, 20], a[100, 880])
