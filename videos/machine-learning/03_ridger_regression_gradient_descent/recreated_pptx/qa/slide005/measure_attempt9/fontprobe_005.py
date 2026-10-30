from PIL import Image, ImageDraw, ImageFont
import numpy as np
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
S = "Get Best W that minimizes the loss"
# target from the ORIGINAL (frame px)
TGT_W, TGT_H = 305.0, 17.0
print(f"target (original ink): w={TGT_W} h={TGT_H}")
print(f"{'pt':>5} {'adv':>8} {'inkW':>7} {'inkH':>6}  note")
for pt in [18, 19, 20, 20.5, 21, 22]:
    f = ImageFont.truetype(F, int(round(pt*4)))   # 4x oversample, px = pt*4
    adv = f.getlength(S) / 4.0
    im = Image.new("L", (int(adv*4)+40, 160), 255)
    d = ImageDraw.Draw(im)
    d.text((20, 20), S, font=f, fill=0)
    a = np.asarray(im) < 200
    ys, xs = np.nonzero(a)
    iw, ih = (xs.max()-xs.min()+1)/4.0, (ys.max()-ys.min()+1)/4.0
    print(f"{pt:5} {adv:8.1f} {iw:7.1f} {ih:6.1f}")
print()
print("=== BOLD title probe: 'Minimization of Loss function to obtain BEST model parameters' ===")
T = "Minimization of Loss function to obtain BEST model parameters"
print("target (original ink): w=647 h=22")
for pt in [18, 19, 20, 21]:
    f = ImageFont.truetype(FB, int(round(pt*4)))
    adv = f.getlength(T) / 4.0
    im = Image.new("L", (int(adv*4)+40, 200), 255)
    d = ImageDraw.Draw(im); d.text((20, 30), T, font=f, fill=0)
    a = np.asarray(im) < 200
    ys, xs = np.nonzero(a)
    print(f"  pt={pt:3} adv={adv:7.1f} inkW={(xs.max()-xs.min()+1)/4.0:6.1f} inkH={(ys.max()-ys.min()+1)/4.0:6.1f}")
