#!/usr/bin/env python3
"""Slide 020 attempt-2 assets: re-render the undersized equations/text to the
ORIGINAL's measured typography scale. Targets from closed-loop PIL:
  eq_where 11 -> 18pt (orig ink 7.94in vs render 4.94in = 1.61x)
  eq_delta 13 -> 15.6pt (orig 5.14 vs 4.28 = 1.20x)
  eq_r1..r4 11 -> 13pt (orig/rend line widths 1.18-1.24x)
Output dir eq_slide_020_v2 keeps the attempt-1 assets banked."""
import json
import os
import subprocess

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
OUT = f"{NS}/recreated_pptx/build/eq_slide_020_v2"
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"
os.makedirs(OUT, exist_ok=True)

EQS = [
    # name, fs, latex  (unchanged content — only the type scale moves)
    ("eq_r1.png", 13, r"\frac{\partial E}{\partial Net_k} \rightarrow -\delta_k"),
    ("eq_r2.png", 13,
     r"Net_k = \sum_{j} w_{kj} O_j \rightarrow \frac{\partial Net_k}{\partial O_j} = w_{kj}"),
    ("eq_r3.png", 13,
     r"O_j = \frac{1}{1+e^{-Net_j}} \rightarrow \frac{\partial O_j}{\partial Net_j} = O_j(1-O_j)"),
    ("eq_r4.png", 13,
     r"Net_j = \sum_{i} w_{ji} O_i \rightarrow \frac{\partial Net_j}{\partial w_{ji}} = O_i"),
    ("eq_delta.png", 15.6,
     r"\Delta_{ji} = -\eta \frac{\partial E}{\partial w_{ji}} = \sum_{k=1}^{m} \delta_k w_{kj} \cdot O_j(1-O_j) \cdot O_i = \eta \delta_j \cdot O_i"),
    ("eq_where.png", 18,
     r"\mathrm{Where}\ \delta_j = \sum_{k=1}^{m} \delta_k w_{kj} \cdot O_j(1-O_j) \quad (\mathrm{for\ each\ Node}\ j\ \mathrm{at\ hidden\ layer})"),
]

for name, fs, latex in EQS:
    r = subprocess.run(["python3", RENDER, latex, f"{OUT}/{name}", str(fs), "000000"],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout.strip().splitlines()[-1])
        print(f"{name}: {d['w_px']}x{d['h_px']}px w={d['w_in']:.4f}in h={d['h_in']:.4f}in")
    except Exception:
        print(name, "FAIL", r.stdout[-200:], r.stderr[-200:])
