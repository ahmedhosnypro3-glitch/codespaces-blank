"""Region-specific measurements for slide 017."""
from PIL import Image
import numpy as np

P = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
     "09_introduction_to_neural_networks/unique_slides/slide_017.jpg")
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
blue = (b > 120) & (b - r > 40) & (b - g > 20)
blk = (r < 80) & (g < 80) & (b < 80)


def cols(mask, y0, y1, thr=40):
    s = mask[y0:y1].sum(axis=0)
    return [(int(i), int(s[i])) for i in range(len(s)) if s[i] > thr]


def rows(mask, x0, x1, thr=40):
    s = mask[:, x0:x1].sum(axis=1)
    return [(int(i), int(s[i])) for i in range(len(s)) if s[i] > thr]


print("TOP panel blue cols (y120..270):", cols(blue, 120, 270, 60))
print("TOP panel blue rows (x300..600):", rows(blue, 300, 600, 100))
print("LOWER blue cols (y285..440):", cols(blue, 285, 440, 60))
print("LOWER blue rows (x120..420):", rows(blue, 120, 420, 100))
print("LOWER blue rows (x450..740):", rows(blue, 450, 740, 100))
print("black rows in TOP panel (x310..600):", rows(blk, 310, 600, 60))
print("black cols in TOP panel (y120..270):", cols(blk, 120, 270, 30))
print("black rows left lower (x130..425):", rows(blk, 130, 425, 60))
print("black cols left lower (y288..440):", cols(blk, 288, 440, 30))
print("black rows right lower (x460..735):", rows(blk, 460, 735, 60))
print("black cols right lower (y288..440):", cols(blk, 288, 440, 30))

# red curve pixels (strong red)
red = (r > 120) & (r - g > 50) & (r - b > 40)
print("red pixels top panel cols:", cols(red, 120, 270, 3))
print("red pixels top panel rows:", rows(red, 300, 600, 3))
print("red left-lower rows:", rows(red, 130, 425, 3))
print("red left-lower cols:", cols(red, 288, 440, 2))
print("red right-lower rows:", rows(red, 460, 735, 3))
print("red right-lower cols:", cols(red, 288, 440, 2))

# callout boxes: warm pale fill (r>b>g-ish)
warm = (r > 230) & (r - b > 15) & (r - g > 5)
print("callout top-right warm rows (x565..845):", rows(warm, 565, 845, 60))
print("callout top-right warm cols (y160..205):", cols(warm, 160, 205, 10))
print("callout BL warm rows (x105..420):", rows(warm, 105, 420, 60))
print("callout BL warm cols (y440..495):", cols(warm, 440, 495, 10))
print("callout BR warm rows (x465..730):", rows(warm, 465, 730, 60))
print("callout BR warm cols (y440..495):", cols(warm, 465, 730, 10))
