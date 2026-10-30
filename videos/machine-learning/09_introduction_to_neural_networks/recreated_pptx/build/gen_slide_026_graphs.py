#!/usr/bin/env python3
"""Generate slide 026 graphs: Sigmoid vs Tanh and their derivatives."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

outdir = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(outdir, exist_ok=True)

# Colors from vision analysis
TANH_RED = "#e74c3c"
SIGMOID_BLUE = "#3498db"
TANH_DERIV_GREEN = "#27ae60"
SIGMOID_DERIV_PURPLE = "#9b59b6"
AXIS_GRAY = "#7f8c8d"
WHITE_BG = "#ffffff"

# Define functions
x = np.linspace(-4, 4, 400)
sigmoid = 1 / (1 + np.exp(-x))
tanh = np.tanh(x)
sigmoid_deriv = sigmoid * (1 - sigmoid)
tanh_deriv = 1 - tanh**2

# ---- Panel 1: Sigmoid vs Tanh ----
# Y-axis: -1.00 to 1.00, ticks at 0.25 increments
fig, ax = plt.subplots(figsize=(5.5, 4.0), dpi=150)
ax.plot(x, tanh, color=TANH_RED, linewidth=2, label='Tanh')
ax.plot(x, sigmoid, color=SIGMOID_BLUE, linewidth=2, label='Sigmoid')
ax.set_xlim(-4, 4)
ax.set_ylim(-1, 1)
ax.set_yticks([-1.00, -0.75, -0.50, -0.25, 0.00, 0.25, 0.50, 0.75, 1.00])
ax.set_xticks([-4, -2, 0, 2, 4])
ax.legend(loc='upper left', fontsize=8, frameon=True, facecolor='white', edgecolor='#cccccc')
ax.grid(True, alpha=0.3)
ax.set_facecolor(WHITE_BG)
fig.patch.set_facecolor(WHITE_BG)
plt.tight_layout(pad=0.1)
plt.savefig(f"{outdir}/slide_026_sigmoid_tanh.png", dpi=150, facecolor=WHITE_BG, edgecolor='none')
plt.close()

# ---- Panel 2: Sigmoid Derivative vs Tanh Derivative ----
# Y-axis: 0.0 to 1.0, ticks at 0.2 increments
fig, ax = plt.subplots(figsize=(5.5, 4.0), dpi=150)
ax.plot(x, tanh_deriv, color=TANH_DERIV_GREEN, linewidth=2, label='Tanh Derivative')
ax.plot(x, sigmoid_deriv, color=SIGMOID_DERIV_PURPLE, linewidth=2, label='Sigmoid Derivative')
ax.set_xlim(-4, 4)
ax.set_ylim(0, 1)
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xticks([-4, -2, 0, 2, 4])
ax.legend(loc='upper right', fontsize=8, frameon=True, facecolor='white', edgecolor='#cccccc')
ax.grid(True, alpha=0.3)
ax.set_facecolor(WHITE_BG)
fig.patch.set_facecolor(WHITE_BG)
plt.tight_layout(pad=0.1)
plt.savefig(f"{outdir}/slide_026_derivatives.png", dpi=150, facecolor=WHITE_BG, edgecolor='none')
plt.close()

print("Generated slide_026 graphs")