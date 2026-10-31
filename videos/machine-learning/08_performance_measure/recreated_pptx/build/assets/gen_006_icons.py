#!/usr/bin/env python3
"""Crop the Positive/Negative class illustrations from the original frame.

PIL ink measurement of unique_slides/slide_006.jpg (960x540, 1px = 1pt):
  positive icon ink bbox (590,324)-(671,371), negative icon ink (766,326)-(850,371).
Crops include a small margin; near-white pixels become transparent so the crop
sits seamlessly on the white tree panel.
"""
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ORIG = os.path.join(ROOT, "unique_slides", "slide_006.jpg")

CROPS = {
    "icon_006_pos.png": (584, 321, 678, 375),
    "icon_006_neg.png": (760, 321, 857, 375),
}


def main():
    im = Image.open(ORIG).convert("RGBA")
    a = np.asarray(im).copy()
    white = (a[:, :, 0] > 225) & (a[:, :, 1] > 225) & (a[:, :, 2] > 225)
    a[:, :, 3] = np.where(white, 0, 255)
    im = Image.fromarray(a)
    for name, box in CROPS.items():
        crop = im.crop(box)
        crop.save(os.path.join(HERE, name))
        print(name, crop.size)


if __name__ == "__main__":
    main()
