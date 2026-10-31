"""Line/panel detection for slide 018 original via gradients."""
import numpy as np
from PIL import Image

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_018.jpg"
im = Image.open(IM).convert("L")
g = np.asarray(im).astype(int)
H, W = g.shape
gx = np.zeros_like(g)
gy = np.zeros_like(g)
gx[:, 1:] = np.abs(np.diff(g, axis=1))
gy[1:, :] = np.abs(np.diff(g, axis=0))
# strong vertical lines: columns with many adjacent-pixel differences
vscore = (gx > 60).sum(axis=0)
hscore = (gy > 60).sum(axis=1)
cols = [(x, int(vscore[x])) for x in range(W) if vscore[x] > 60]
rows = [(y, int(hscore[y])) for y in range(H) if hscore[y] > 60]
print("cols with >60 strong-vert pixels:", cols)
print("rows with >60 strong-horiz pixels:", rows)

# also: overall darkness profile to locate panel bands
dark = (g < 200).sum(axis=1)
print("row dark counts (every 5px):")
print([(y, int(dark[y])) for y in range(0, H, 5)])
