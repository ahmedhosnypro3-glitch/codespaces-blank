"""Colour probes for eq-box ink and top-right callout."""
from PIL import Image
import numpy as np

P = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
     "09_introduction_to_neural_networks/unique_slides/slide_017.jpg")
a = np.asarray(Image.open(P).convert("RGB")).astype(int)


def darkest(x0, x1, y0, y1, n=3):
    region = a[y0:y1, x0:x1].reshape(-1, 3)
    lum = region.sum(axis=1)
    idx = np.argsort(lum)[-n:]
    return [tuple(int(v) for v in region[i]) for i in idx]


print("BL prefix red zone x144-152:", darkest(144, 152, 476, 486))
print("BL prefix mid x160-240:", darkest(160, 240, 476, 486))
print("BL prefix right x240-300:", darkest(240, 300, 476, 486))
print("BL digit 0 x330-340:", darkest(330, 340, 470, 481))
print("BL digit 1 x330-340:", darkest(330, 340, 488, 499))
print("BL cond row1 x355-405:", darkest(355, 405, 472, 482))
print("BL cond row2 x355-405:", darkest(355, 405, 489, 499))
print("BL bar x322-327:", darkest(322, 327, 465, 504))

print()
print("top-right box text"):
print(" F(x)=x x635-650:", darkest(635, 650, 182, 196))
print(" Linear x690-735:", darkest(690, 735, 182, 196))
print(" (NoAct) x738-830:", darkest(738, 830, 182, 196))
print()
print("graph ink samples:")
print(" top panel y-axis x443-448:", darkest(443, 448, 125, 195))
print(" top panel x-axis row197-201:", darkest(310, 595, 197, 201))
print(" top diagonal:", darkest(392, 486, 130, 195))
print(" left-lower zero level:", darkest(180, 265, 360, 375))
print(" left-lower +1 level:", darkest(280, 340, 320, 330))
print(" left-lower jump:", darkest(268, 278, 315, 370))
print(" right-lower -1 level:", darkest(540, 595, 400, 412))
print(" right-lower +1 level:", darkest(640, 690, 320, 330))
print(" right-lower jump:", darkest(625, 635, 330, 405))
print()
print("axis label colour f(x)/x:")
print(" BL f(x) x230-250 y300-316:", darkest(228, 250, 300, 316))
print(" BL x x360-385 y370-390:", darkest(360, 385, 370, 390))
print(" top f(x) x380-405 y135-150:", darkest(378, 405, 135, 150))
print(" top x x515-540 y200-218:", darkest(515, 540, 200, 218))
