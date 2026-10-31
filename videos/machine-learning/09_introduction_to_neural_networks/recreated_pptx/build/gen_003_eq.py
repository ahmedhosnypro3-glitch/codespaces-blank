#!/usr/bin/env python3
r"""Render the panel-3 Error-function equation as one 2D mathtext PNG at 600 dpi.

mathtext has no inline \color (a parse error, measured), so each colored span is
rendered independently and laid out by measured extents: the summation limits sit
directly beneath the big sigma, with "misclassified" in the original's red and
the rest of the limits in black.

Geometry is measured off videos/machine-learning/09_introduction_to_neural_networks/
unique_slides/slide_003.jpg (960x540 frame): the sigma glyph at x 212-232 with its
limit band at x 162-274 on y 386-393, the rest of the equation line on y 352-380.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

DPI = 600
FS = 22.0
SUB_FS = 14.0

SIGMA = r"\sum"
LIMITS = [
    (r"\mathit{all}", "black"),
    (r"\mathit{misclassified}", "red"),
    (r"\mathit{vectors}\,(i)", "black"),
]
# (mathtext, color, size, x-gap-before in 600dpi px)
SPANS = [
    (r"\mathbf{Error=}", "black", FS, 0),
    (SIGMA, "black", FS, 220),
    (r"\boldsymbol{W}^{T}\underline{X}_{i}", "green", FS, 250),
    (r"\mathbf{\Rightarrow}", "black", FS, 300),
    (r"\left(\boldsymbol{W}^{T}\underline{X}_{i}\right)", "green", FS, 250),
    (r"\mathit{take\ positive\ and\ negative\ values}", "green", FS, 180),
]


def measure(mathtext, fs):
    fig = plt.figure(figsize=(0.01, 0.01), dpi=DPI)
    t = fig.text(0, 0, f"${mathtext}$", fontsize=fs)
    fig.canvas.draw()
    bb = t.get_window_extent()
    plt.close(fig)
    return bb.width, bb.height


def limits_layout():
    parts = []
    for mathtext, color in LIMITS:
        w, h = measure(mathtext, SUB_FS)
        parts.append({"text": mathtext, "color": color, "w": w, "h": h})
    space = 0.28 * SUB_FS * DPI / 72.0
    width = sum(p["w"] for p in parts) + space * (len(parts) - 1)
    x = 0.0
    for p in parts:
        p["x"] = x
        x += p["w"] + space
    return parts, width, max(p["h"] for p in parts)


sigma_w, sigma_h = measure(SIGMA, FS)
limits, limits_w, limits_h = limits_layout()
span_w = max(sigma_w, limits_w)

widths = []
for mathtext, color, fs, gap in SPANS:
    widths.append(span_w if mathtext == SIGMA else measure(mathtext, fs)[0])
total_w = sum(widths) + sum(s[3] for s in SPANS)

line_half = max(measure(s[0], s[2])[1] for s in SPANS) / 2.0
top = max(line_half, sigma_h / 2.0)
below = sigma_h / 2.0 + limits_h + 4
content_h = top + below

pad = 8
canvas_w = total_w + 2 * pad
canvas_h = content_h + 2 * pad
w_in = canvas_w / DPI
h_in = canvas_h / DPI

fig = plt.figure(figsize=(w_in, h_in))
fig.patch.set_alpha(0.0)


def fx(x_px):
    return (pad + x_px) / canvas_w


def fy(content_row):
    return (canvas_h - pad - content_row) / canvas_h


def place(mathtext, color, fs, x_px, content_row):
    fig.text(fx(x_px), fy(content_row), f"${mathtext}$",
             fontsize=fs, color=color, va="center", ha="left")


x = 0.0
sigma_left = 0.0
for (mathtext, color, fs, gap), w in zip(SPANS, widths):
    x += gap
    place(mathtext, color, fs, x, top)
    if mathtext == SIGMA:
        sigma_left = x + (span_w - sigma_w) / 2.0
    x += w

limit_row = top + sigma_h / 2.0 + limits_h / 2.0 + 4
limit_left = sigma_left + sigma_w / 2.0 - limits_w / 2.0
for p in limits:
    place(p["text"], p["color"], SUB_FS, limit_left + p["x"], limit_row)

out = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/recreated_pptx/build/assets/eq_error.png")
fig.savefig(out, dpi=DPI, transparent=True)
plt.close(fig)

im = Image.open(out)
print("wrote", out, im.size, "w_in=%.4f h_in=%.4f" % (w_in, h_in))
print("aspect=%.4f" % (w_in / h_in))
