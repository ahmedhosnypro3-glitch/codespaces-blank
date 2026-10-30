#!/usr/bin/env python3
"""Generate slide 025 graphs: Linear, Unipolar Unit Step, Bipolar Unit Step functions - SIMPLIFIED mathtext."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

outdir = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(outdir, exist_ok=True)

RED = "#e74c3c"
BLUE_BORDER = "#0000ff"
WHITE_BG = "#ffffff"

x_range = (-3, 3)
x = np.linspace(x_range[0], x_range[1], 400)

def save_with_arrows(fig, ax, filename):
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ax.annotate('', xy=(xmax, 0), xytext=(xmin, 0), arrowprops=dict(arrowstyle='->', color=RED, lw=2))
    ax.annotate('', xy=(0, ymax), xytext=(0, ymin), arrowprops=dict(arrowstyle='->', color=RED, lw=2))
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(BLUE_BORDER)
        spine.set_linewidth(1.5)
    ax.set_facecolor(WHITE_BG)
    fig.patch.set_facecolor(WHITE_BG)
    plt.tight_layout(pad=0.1)
    plt.savefig(filename, dpi=150, facecolor=WHITE_BG, edgecolor='none')

# Plot 1: Linear
fig, ax = plt.subplots(figsize=(3.0, 2.0), dpi=150)
ax.plot(x, x, color=RED, linewidth=2)
ax.set_xlim(x_range)
ax.set_ylim(-1, 3)
save_with_arrows(fig, ax, f"{outdir}/slide_025_linear.png")
plt.close()

# Plot 2: Unipolar
fig, ax = plt.subplots(figsize=(3.0, 2.0), dpi=150)
y_unipolar = np.where(x < 0, 0, 1)
ax.plot(x, y_unipolar, color=RED, linewidth=2)
ax.axvline(x=0, color=RED, linewidth=2, linestyle='-')
ax.set_xlim(x_range)
ax.set_ylim(-0.5, 1.5)
save_with_arrows(fig, ax, f"{outdir}/slide_025_unipolar_step.png")
plt.close()

# Plot 3: Bipolar
fig, ax = plt.subplots(figsize=(3.0, 2.0), dpi=150)
y_bipolar = np.where(x < 0, -1, 1)
ax.plot(x, y_bipolar, color=RED, linewidth=2)
ax.axvline(x=0, color=RED, linewidth=2, linestyle='-')
ax.set_xlim(x_range)
ax.set_ylim(-1.5, 1.5)
save_with_arrows(fig, ax, f"{outdir}/slide_025_bipolar_step.png")
plt.close()

# Equation images - use >= instead of \ge
# Unipolar equation
fig, ax = plt.subplots(figsize=(3.5, 0.8), dpi=600)
ax.text(0.5, 0.5, r'$F(x) = \mathrm{Uni\text{-}polar\ Unit\ Step} = \{ 0 \text{ for } x<0;\ 1 \text{ for } x>=0 \}$',
        ha='center', va='center', fontsize=14, color='black')
ax.axis('off')
fig.patch.set_facecolor('#FFE6CC')
plt.savefig(f"{outdir}/slide_025_unipolar_eq.png", dpi=600, facecolor='#FFE6CC', edgecolor='none', transparent=False, bbox_inches='tight', pad_inches=0.02)
plt.close()

# Bipolar equation
fig, ax = plt.subplots(figsize=(3.5, 0.8), dpi=600)
ax.text(0.5, 0.5, r'$F(x) = \mathrm{Bi\text{-}polar\ Unit\ Step} = \{-1 \text{ for } x<0;\ 1 \text{ for } x>=0 \}$',
        ha='center', va='center', fontsize=14, color='black')
ax.axis('off')
fig.patch.set_facecolor('#FFE6CC')
plt.savefig(f"{outdir}/slide_025_bipolar_eq.png", dpi=600, facecolor='#FFE6CC', edgecolor='none', transparent=False, bbox_inches='tight', pad_inches=0.02)
plt.close()

# Linear equation (inline)
fig, ax = plt.subplots(figsize=(3.5, 0.6), dpi=600)
ax.text(0.5, 0.5, r'$F(x) = x \quad \text{Linear (No Activation)}$',
        ha='center', va='center', fontsize=14, color='black')
ax.axis('off')
fig.patch.set_facecolor('#FFE6CC')
plt.savefig(f"{outdir}/slide_025_linear_eq.png", dpi=600, facecolor='#FFE6CC', edgecolor='none', transparent=False, bbox_inches='tight', pad_inches=0.02)
plt.close()

print("Generated all slide_025 graphs and equation images")