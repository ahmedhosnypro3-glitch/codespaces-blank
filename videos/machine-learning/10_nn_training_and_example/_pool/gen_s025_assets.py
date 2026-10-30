"""Generate slide-25 assets: 2D ReLU equations (mathtext->600dpi PNG) + charts."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/assets025"
DPI = 600
plt.rcParams["mathtext.fontset"] = "dejavusans"

def render_eq(mt, color, fname, fs=20):
    fig = plt.figure(figsize=(6, 1.2))
    t = fig.text(0.01, 0.5, mt, fontsize=fs, color=color, va="center", ha="left")
    fig.canvas.draw()
    bb = t.get_window_extent()
    fig.set_size_inches(bb.width / fig.dpi + 0.08, bb.height / fig.dpi + 0.08)
    fig.patch.set_alpha(0)
    fig.savefig(f"{OUT}/{fname}", dpi=DPI, transparent=True,
                bbox_inches=tight_pad if False else None, pad_inches=0.02)
    plt.close(fig)

tight_pad = None

# --- Eq 1: f(x) = ReLU = {0 for x<0, x for x>=0}  (piecewise 2D)
def eq_piecewise(lhs, rows, fname, color="#000000", fs=20):
    """Build a stacked piecewise block: lhs  then  {  row1 / row2 }."""
    fig = plt.figure(figsize=(4.2, 1.4))
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    ax.set_xlim(0, 4.2); ax.set_ylim(0, 1.4)
    ax.text(0.05, 0.70, lhs, fontsize=fs, color=color, va="center", ha="left")
    # brace height spans both rows
    ax.text(1.72, 0.70, r"$\{$", fontsize=fs * 3.4, color=color,
            va="center", ha="left")
    ax.text(2.15, 1.02, rows[0], fontsize=fs, color=color, va="center", ha="left")
    ax.text(2.15, 0.38, rows[1], fontsize=fs, color=color, va="center", ha="left")
    fig.canvas.draw()
    fig.savefig(f"{OUT}/{fname}", dpi=DPI, transparent=True)
    plt.close(fig)
    from PIL import Image
    im = Image.open(f"{OUT}/{fname}")
    return {"path": f"{OUT}/{fname}", "px": im.size, "in": (im.size[0] / DPI, im.size[1] / DPI)}

eq_piecewise(r"$f(x)\ =\ \mathrm{ReLU}\ =\ $",
             (r"$0$   for $x<0$", r"$x$   for $x\geq 0$"), "eq25_1.png")
eq_piecewise(r"$f'(x)\ =\ $",
             (r"$0$   for $x<0$", r"$1$   for $x\geq 0$"), "eq25_2.png")

# --- Chart 1: ReLU (bottom-left)
x = np.linspace(-10, 10, 800)
fig, ax = plt.subplots(figsize=(4.0, 2.4))
ax.plot(x, np.maximum(0, x), color="#C00000", lw=2.4)
ax.set_xlabel("$x$", fontsize=13)
ax.set_ylabel("$f$", fontsize=13, rotation=0)
ax.set_xticks([-10, -5, 0, 5, 10]); ax.set_yticks([0, 5, 10])
ax.tick_params(labelsize=11)
for sp in ax.spines.values():
    sp.set_color("#CCCCCC")
ax.grid(False)
fig.tight_layout()
fig.savefig(f"{OUT}/chart25_relu.png", dpi=200, facecolor="white")
plt.close(fig)

# --- Chart 2: Sigmoid vs Tanh (left sub) + derivatives (right sub)
fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.5))
sig = lambda t: 1 / (1 + np.exp(-t))
tt = np.linspace(-4, 4, 600)
axes[0].plot(tt, sig(tt), color="#0000FF", lw=2.0, label="Sigmoid")
axes[0].plot(tt, np.tanh(tt), color="#C00000", lw=2.0, label="Tanh")
axes[0].set_title("Sigmoid vs Tanh", fontsize=12)
axes[0].set_xticks([-4, 4]); axes[0].set_yticks(np.arange(-1, 1.01, 0.25))
axes[0].tick_params(labelsize=9); axes[0].legend(fontsize=9, loc="upper left", framealpha=0.9)
dsig = lambda t: sig(t) * (1 - sig(t))
axes[1].plot(tt, 1 - np.tanh(tt) ** 2, color="#00AA00", lw=2.0, label="Tanh Derivative")
axes[1].plot(tt, dsig(tt), color="#800080", lw=2.0, label="Sigmoid Derivative")
axes[1].set_xticks([-4, 4]); axes[1].set_yticks(np.arange(0, 1.01, 0.2))
axes[1].tick_params(labelsize=9); axes[1].legend(fontsize=9, loc="upper right", framealpha=0.9)
axes[1].annotate("1.0", xy=(0, 1.0), xytext=(0.4, 1.0), color="#C00000", fontsize=11)
axes[1].annotate("0.25", xy=(0, 0.25), xytext=(0.4, 0.25), color="#C00000", fontsize=11)
for ax in axes:
    for sp in ax.spines.values():
        sp.set_color("#CCCCCC")
fig.tight_layout()
fig.savefig(f"{OUT}/chart25_sigtanh.png", dpi=200, facecolor="white")
plt.close(fig)
print("assets written")
