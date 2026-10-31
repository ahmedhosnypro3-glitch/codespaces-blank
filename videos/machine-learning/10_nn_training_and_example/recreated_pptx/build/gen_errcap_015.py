#!/usr/bin/env python3
"""Slide 15 error-bar caption: "Error Error Error" as a 600dpi transparent PNG.

The original frame's dark-red bar (x 10.96..11.26 in, y 2.08..5.04 in) carries a
rotated white caption reading "Error Error Error". PIL on unique_slides/slide_015.jpg
found three discrete word clusters inside the bar:
    word 1  y 185..222 orig-px  (2.569..3.083 in)
    word 2  y 241..278 orig-px  (3.347..3.861 in)
    word 3  y 290..329 orig-px  (4.028..4.569 in)
each ~48 orig-px tall = one word of 5 letters at ~9pt Arial bold.

Rendering each word as its own rotated PNG (rather than one rotated text box) gives
per-word placement control and avoids LibreOffice's narrow-box rotated-text quirks.
Canvas == placed area, so no rescale: fig size == placement size, dpi 600.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# bar geometry, inches (measured from unique_slides/slide_015.jpg)
BAR_X, BAR_Y, BAR_W, BAR_H = 10.96, 2.08, 0.31, 2.96
# each word: (top y in inches, height in inches) from the measured clusters
WORDS = [
    (185 / 72.0, (222 - 185 + 1) / 72.0),
    (241 / 72.0, (278 - 241 + 1) / 72.0),
    (290 / 72.0, (329 - 290 + 1) / 72.0),
]
FS = 9.0  # pt, matches the measured ~9pt glyph run height

# canvas spans the full bar; each word is drawn at its measured y offset
fig = plt.figure(figsize=(BAR_W, BAR_H), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, BAR_W)
ax.set_ylim(0, BAR_H)
ax.axis("off")
fig.patch.set_alpha(0.0)

for top_in, h_in in WORDS:
    # image y runs bottom-up; word center measured from the top of the bar
    y_center_in = BAR_H - (top_in - BAR_Y) - h_in / 2.0
    ax.text(BAR_W / 2.0, y_center_in, "Error", fontsize=FS, fontweight="bold",
            color="white", ha="center", va="center", rotation=90, zorder=2)

fig.savefig("errcap_015.png", dpi=600, transparent=True)
plt.close(fig)
print("ok errcap_015.png", int(BAR_W * 600), int(BAR_H * 600))
