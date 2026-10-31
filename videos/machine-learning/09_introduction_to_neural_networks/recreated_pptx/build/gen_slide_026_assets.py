#!/usr/bin/env python3
"""Regenerate slide_026 assets from PIL-measured geometry of the original frame.

All measurements from unique_slides/slide_026.jpg (960x540 px, 1px = 1pt = 1/72in):

- cream equation panel: rows 94..222, cols 69..889, fill #feffe8 (drawn by the build)
- eq row 1 ink rows 107..151: definition cols 76..299 BLACK bold,
  derivative cols 316..539 RED bold; cream value box cols 560..871, rows 107..149
- eq row 2 ink rows 176..214: definition cols 78..265, derivative cols 316..468;
  value box cols 560..871, rows 175..216
- value box fill #f6e4cc, border #d1c7ac; "at x=0" ink cols 574..627, values cols 664..870
- chart figure: blue border outer rows 231..432 cols 139..823, mint fill rows 235..427
  cols 144..820; left axes box cols 167..462 rows 254..420, right axes box
  cols 521..816 rows 265..408; zero crosshair row 337 / col 314 (left) and col 668 (right)
- red annotations (right chart): "1.0" text cols 549..570 rows 263..272 with guide
  line rows 266..267 cols ~575..708; "0.25" text cols 549..571 rows 336..345 with
  guide line row 342 cols ~588..716
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

OUT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "09_introduction_to_neural_networks/recreated_pptx/build")
DPI = 600
FS = 20

BLACK = "#1a1a1a"
RED = "#a02020"   # measured derivative / value ink

TANH_RED = "#e74c3c"
SIG_BLUE = "#3498db"
DER_GREEN = "#27ae60"
DER_PURPLE = "#9b59b6"
GRID = "#c8c8c8"
AXIS = "#333333"
MINT = "#e5ffef"
BLUE_EDGE = "#00004c"
ANNOT_RED = "#c00000"


def _ink_box(buf):
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    return rows, cols


def render_eq(mathtext, name, color, target_w_px_960, rescaled=True):
    """Render one equation; re-render at a size that matches the measured ink width."""
    def once(fs):
        fig = plt.figure(figsize=(16, 8), dpi=DPI)
        fig.patch.set_alpha(0.0)
        fig.text(0.5, 0.5, f"${mathtext}$", fontsize=fs, color=color,
                 ha="center", va="center", fontweight="bold")
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())
        rows, cols = _ink_box(buf)
        plt.close(fig)
        return buf, rows, cols

    buf, rows, cols = once(FS)
    w_px = cols[-1] - cols[0] + 1
    want_px = target_w_px_960 * DPI / 72.0
    fs2 = FS * want_px / w_px if rescaled else FS
    buf, rows, cols = once(fs2)

    pad = 6
    y0, y1 = max(rows[0] - pad, 0), min(rows[-1] + pad, buf.shape[0])
    x0, x1 = max(cols[0] - pad, 0), min(cols[-1] + pad, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(f"{OUT}/{name}.png")
    return {"image": f"{name}.png",
            "w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "w_in": round((x1 - x0) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5),
            "dpi": DPI, "font_size_pt": fs2, "color": color, "mathtext": mathtext,
            "name": name}


# measured ink widths (960-scale px) per equation part
eqs = [
    # row 1: definition (black) + derivative clause (red) + value label/values
    (r"f(x) = \mathrm{Sigmoid}(x) = \frac{1}{1+e^{-x}}", "eq_s026_def1",
     BLACK, 224),
    (r"\Rightarrow\ f'(x) = f(x)(1-f(x))", "eq_s026_der1", RED, 224),
    (r"\mathrm{at}\ x=0", "eq_s026_v1a", BLACK, 54),
    (r"f(0)=0.5\quad f'(0)=0.25", "eq_s026_v1b", RED, 207),
    # row 2
    (r"f(x) = \tanh(x) = \frac{\sinh x}{\cosh x}", "eq_s026_def2",
     BLACK, 188),
    (r"\Rightarrow\ f'(x) = 1-f(x)^{2}", "eq_s026_der2", RED, 153),
    (r"\mathrm{at}\ x=0", "eq_s026_v2a", BLACK, 54),
    (r"f(0)=0\quad f'(0)=1", "eq_s026_v2b", RED, 173),
]
results = [render_eq(mt, nm, col, tw) for mt, nm, col, tw in eqs]
with open(f"{OUT}/slide_026_equations.json", "w") as f:
    json.dump({"slide": "026", "equations": results}, f, indent=2)
for e in results:
    print(f"{e['name']}: fs={e['font_size_pt']:.2f} w={e['w_in']}in "
          f"h={e['h_in']}in")

# ---------------------------------------------------------------- chart figure
x = np.linspace(-4, 4, 500)
sigmoid = 1 / (1 + np.exp(-x))
tanh = np.tanh(x)
sig_d = sigmoid * (1 - sigmoid)
tanh_d = 1 - tanh ** 2

FW, FH = 9.47222, 2.75694      # measured chart region 140..822 x 232..431 px
fig = plt.figure(figsize=(FW, FH), dpi=200)
fig.patch.set_facecolor(MINT)
fig.patch.set_edgecolor(BLUE_EDGE)
fig.patch.set_linewidth(2.0)   # ~2 px at 960 scale


def rect(c0, c1, r0, r1):
    """original-pixel box -> figure-fractions rect (figure spans cols 140..822,
    rows 232..431, figure y measured from the bottom)."""
    return [(c0 - 140) / 682.0, 1 - (r1 - 232) / 199.0,
            (c1 - c0) / 682.0, (r1 - r0) / 199.0]


# ---- left subplot: functions ----
ax1 = fig.add_axes(rect(167, 462, 254, 420))
ax1.set_facecolor("white")
ax1.plot(x, tanh, color=TANH_RED, lw=2.0, label="Tanh", zorder=3)
ax1.plot(x, sigmoid, color=SIG_BLUE, lw=2.0, label="Sigmoid", zorder=3)
ax1.set_xlim(-4, 4)
ax1.set_ylim(-1, 1)
ax1.set_yticks(np.arange(-1.0, 1.01, 0.25))
ax1.set_yticklabels([f"{v:.2f}" for v in np.arange(1.0, -1.01, -0.25)])
ax1.set_xticks([-4, -2, 0, 2, 4])
ax1.grid(True, color=GRID, lw=0.6, zorder=1)
# dark zero crosshair, under the curves
ax1.axhline(0, color="#555555", lw=1.1, zorder=2)
ax1.axvline(0, color="#555555", lw=1.1, zorder=2)
ax1.set_axisbelow(True)
ax1.legend(loc="upper left", fontsize=8, frameon=True, facecolor="white",
           edgecolor="#bbbbbb", handlelength=1.6)
ax1.tick_params(axis="y", labelleft=True, labelright=True, labelsize=8, colors=AXIS)
ax1.tick_params(axis="x", labelsize=8, colors=AXIS)
for sp in ax1.spines.values():
    sp.set_color(AXIS)
    sp.set_linewidth(0.8)

# ---- right subplot: derivatives ----
ax2 = fig.add_axes(rect(521, 816, 265, 408))
ax2.set_facecolor("white")
ax2.plot(x, tanh_d, color=DER_GREEN, lw=2.0, label="Tanh Derivative", zorder=3)
ax2.plot(x, sig_d, color=DER_PURPLE, lw=2.0, label="Sigmoid Derivative", zorder=3)
ax2.set_xlim(-4, 4)
ax2.set_ylim(0, 1)
ax2.set_yticks(np.arange(0.0, 1.01, 0.2))
ax2.set_yticklabels([f"{v:.1f}" for v in np.arange(1.0, -0.01, -0.2)])
ax2.set_xticks([-4, -2, 0, 2, 4])
ax2.grid(True, color=GRID, lw=0.6, zorder=1)
ax2.axvline(0, color="#555555", lw=1.1, zorder=2)
ax2.set_axisbelow(True)
ax2.legend(loc="upper right", fontsize=8, frameon=True, facecolor="white",
           edgecolor="#bbbbbb", handlelength=1.6)
# red peak-reference labels + horizontal guide lines (original: label left of the
# peaks, line from just right of the label across the peaks)
for txt, yv in (("1.0", 1.0), ("0.25", 0.25)):
    ax2.plot([-2.4, 1.2], [yv, yv], color=ANNOT_RED, lw=1.4, zorder=4,
             solid_capstyle="butt")
    ax2.text(-3.3, yv, txt, color=ANNOT_RED, fontsize=10,
             fontweight="bold", ha="left", va="center", zorder=6)
ax2.tick_params(axis="y", labelsize=8, colors=AXIS)
ax2.tick_params(axis="x", labelsize=8, colors=AXIS)
for sp in ax2.spines.values():
    sp.set_color(AXIS)
    sp.set_linewidth(0.8)

fig.suptitle("Sigmoid vs Tanh", fontsize=13, fontweight="bold",
             color="#1a1a1a", y=0.955)
fig.savefig(f"{OUT}/slide_026_charts.png", dpi=200, facecolor=MINT,
            edgecolor=BLUE_EDGE)
plt.close(fig)
print("wrote slide_026_charts.png:",
      Image.open(f"{OUT}/slide_026_charts.png").size)
