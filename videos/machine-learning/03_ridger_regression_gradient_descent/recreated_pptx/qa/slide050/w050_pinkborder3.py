#!/usr/bin/env python3
"""Pink-box border adjudication v3 — raw color scanlines across the box edges."""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide050"

o = np.asarray(Image.open(NS + "/unique_slides/slide_050.jpg").convert("RGB")).astype(int)
r = Image.open(QA + "/render_13.png").convert("RGB")
SC = r.size[1] / 540.0
r = np.asarray(r).astype(int)

print("ORIG scanline y=100 (x735..835):")
print("  " + " ".join("%d:%s" % (x, tuple(o[100, x])) for x in range(735, 836, 3)))
print("ORIG scanline y=170 (x735..835):")
print("  " + " ".join("%d:%s" % (x, tuple(o[170, x])) for x in range(735, 836, 3)))
print("ORIG vertical x=790 (y50..180):")
print("  " + " ".join("%d:%s" % (y, tuple(o[y, 790])) for y in range(50, 181, 3)))
print("\nORIG row means x750..820:")
for y in range(52, 62):
    print("  y%d %s" % (y, o[y, 750:820].mean(axis=0).round(0)))
print("ORIG bottom rows:")
for y in range(136, 150):
    print("  y%d %s" % (y, o[y, 750:820].mean(axis=0).round(0)))

print("\nRENDER13 scanline frame y=100 => row %d (x735..835 => cols %d..%d):" % (int(100*SC), int(735*SC), int(835*SC)))
row = int(100*SC)
print("  " + " ".join("%d(%s)" % (round(x/SC), tuple(r[row, x])) for x in range(int(735*SC), int(836*SC), 6)))
print("RENDER13 vertical frame x=790 => col %d (y50..180):" % int(790*SC))
col = int(790*SC)
print("  " + " ".join("%d(%s)" % (round(y/SC), tuple(r[y, col])) for y in range(int(50*SC), int(181*SC), 6)))
print("RENDER13 top rows (frame y52..62):")
for y in range(int(52*SC), int(62*SC)):
    print("  f%.1f %s" % (y/SC, r[y, int(750*SC):int(820*SC)].mean(axis=0).round(0)))
