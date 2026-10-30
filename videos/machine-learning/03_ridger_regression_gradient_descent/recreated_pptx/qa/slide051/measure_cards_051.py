#!/usr/bin/env python3
"""Find the horizontal card-border rows of the DEC cards in the original frame."""
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_051.jpg"
img = Image.open(ORIG).convert("RGB")
px = img.load()

print("### column x=280 (inside card, left of the d() label) — rows 130..340")
for y in range(130, 340):
    r, g, b = px[280, y]
    lum = int(0.299 * r + 0.587 * g + 0.114 * b)
    if lum < 245:
        print("  y=%3d  %3d/%3d/%3d  L=%3d" % (y, r, g, b, lum))

print("\n### column x=460 (empty span inside cards) — rows 130..340")
for y in range(130, 340):
    r, g, b = px[460, y]
    lum = int(0.299 * r + 0.587 * g + 0.114 * b)
    if lum < 245:
        print("  y=%3d  %3d/%3d/%3d  L=%3d" % (y, r, g, b, lum))

print("\n### row y=180 (inside card 1) — x 260..300 and 840..870")
for x in list(range(260, 300)) + list(range(840, 870)):
    r, g, b = px[x, 180]
    lum = int(0.299 * r + 0.587 * g + 0.114 * b)
    if lum < 245:
        print("  x=%3d  %3d/%3d/%3d  L=%3d" % (x, r, g, b, lum))
