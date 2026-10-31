#!/usr/bin/env python3
"""Render the panel-3 Error-function equation as one 2D mathtext PNG at 600 dpi.

Each colored span is rendered independently (matplotlib mathtext has no inline
\color) and laid out left-to-right by measured extents, so the final strip keeps
the original's semantic colors: red "all misclassified ... (i)", green X_i /
"take positive and negative values", black W^T and punctuation.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

DPI = 600
FS = 22.0
CAP_FS = 14.0

# (mathtext, color, size, x-gap-before-in-points)
SPANS = [
    (r"\mathbf{Error=}", "black", FS, 0),
    (r"\sum_{\mathit{all\ misclassified\ vectors}\,(i)}", "black", FS, 40),
    (r"\boldsymbol{W}^{T}\underline{X}_{i}", "green", FS, 40),
    (r"\mathbf{\Rightarrow}", "black", FS, 60),
    (r"\left(\boldsymbol{W}^{T}\underline{X}_{i}\right)", "green", FS, 40),
    (r"\mathit{take\ positive\ and\ negative\ values}", "green", FS, 30),
]


def measure(mathtext, fs):
    fig = plt.figure(figsize=(0.01, 0.01), dpi=DPI)
    t = fig.text(0, 0, f"${mathtext}$", fontsize=fs)
    fig.canvas.draw()
    bb = t.get_window_extent()
    plt.close(fig)
    return bb.width, bb.height


widths = [measure(*[s[0], s[2]])[0] for s in SPANS]
gaps = [s[3] for s in SPANS]
total_w = sum(widths) + sum(gaps)
max_h = max(measure(s[0], s[2])[1] for s in SPANS)

pad = 8
w_in = (total_w + 2 * pad) / DPI
h_in = (max_h + 2 * pad) / DPI

fig = plt.figure(figsize=(w_in, h_in))
fig.patch.set_alpha(0.0)
renderer = fig.canvas.get_renderer()

x = pad
for mathtext, color, fs, gap in SPANS:
    if gap:
        x += gap
    fig.text(x / DPI / w_in, 0.5, f"${mathtext}$",
             fontsize=fs, color=color, va="center", ha="left")
    x += measure(mathtext, fs)[0]

out = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/recreated_pptx/build/assets/eq_error.png")
fig.savefig(out, dpi=DPI, transparent=True)
plt.close(fig)

im = Image.open(out)
print("wrote", out, im.size, "w_in=%.4f h_in=%.4f" % (w_in, h_in))
print("aspect=%.4f" % (w_in / h_in))
