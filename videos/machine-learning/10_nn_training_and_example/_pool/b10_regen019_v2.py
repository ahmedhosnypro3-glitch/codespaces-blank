#!/usr/bin/env python3
"""Regenerate slide_019 bottom-panel equations.
ea1: full chain-rule identity with brackets (was canvas-clipped by render_eq's
10in figure). Right panel: arrow style aligned with the frame; fs=12 so the
widest line fits inside the bottom-right panel (x 9.0..12.83).
"""
import json
import subprocess

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
OUT = f"{NS}/recreated_pptx/build/eq_slide_019"
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"

EQS = [
    ("eq1.png", 16,
     r"\frac{\partial E}{\partial w_{ji}} = \left[ \frac{\partial E}{\partial Net_{k_{1}}} \cdot "
     r"\frac{\partial Net_{k_{1}}}{\partial O_{j}} + \frac{\partial E}{\partial Net_{k_{2}}} \cdot "
     r"\frac{\partial Net_{k_{2}}}{\partial O_{j}} + \cdots + \frac{\partial E}{\partial Net_{k_{m}}} \cdot "
     r"\frac{\partial Net_{k_{m}}}{\partial O_{j}} \right] \cdot \frac{\partial O_{j}}{\partial Net_{j}} \cdot "
     r"\frac{\partial Net_{j}}{\partial w_{ji}}"),
    ("eq2.png", 12, r"\frac{\partial E}{\partial Net_{k}} \Rightarrow -\delta_{k}"),
    ("eq3.png", 12,
     r"\mathrm{Net}_{k}=\sum_{k} w_{kj}\,O_{j} \Rightarrow \frac{\partial \mathrm{Net}_{k}}{\partial O_{j}} = w_{kj}"),
    ("eq4.png", 12,
     r"O_{j} = \frac{1}{1+e^{-Net_{j}}} \Rightarrow \frac{\partial O_{j}}{\partial Net_{j}} = O_{j}(1-O_{j})"),
    ("eq5.png", 12,
     r"\mathrm{Net}_{j}=\sum_{j} w_{ji}\,O_{i} \Rightarrow \frac{\partial \mathrm{Net}_{j}}{\partial w_{ji}} = O_{i}"),
]

for name, fs, latex in EQS:
    r = subprocess.run(["python3", RENDER, latex, f"{OUT}/{name}", str(fs), "000000"],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout.strip().splitlines()[-1])
        print(f"{name}: {d['w_px']}x{d['h_px']}px w={d['w_in']:.4f}in h={d['h_in']:.4f}in")
    except Exception:
        print(name, "FAIL", r.stdout[-160:], r.stderr[-160:])
