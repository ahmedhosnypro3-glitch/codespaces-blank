#!/usr/bin/env python3
"""Slide 019 equations, attempt 3 build: frame-faithful index notation
(Net_{k=1}, not nested Net_{k_{1}}) and a 14pt bottom-right panel so the
indices w_kj / w_ji are legible at the 150dpi QA render.
"""
import json
import subprocess

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
OUT = f"{NS}/recreated_pptx/build/eq_slide_019"
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"

EQS = [
    ("eq1.png", 16,
     r"\frac{\partial E}{\partial w_{ji}} = \left[ \frac{\partial E}{\partial \mathrm{Net}_{k=1}} \cdot "
     r"\frac{\partial \mathrm{Net}_{k=1}}{\partial O_{j}} + \frac{\partial E}{\partial \mathrm{Net}_{k=2}} \cdot "
     r"\frac{\partial \mathrm{Net}_{k=2}}{\partial O_{j}} + \cdots + \frac{\partial E}{\partial \mathrm{Net}_{k=m}} \cdot "
     r"\frac{\partial \mathrm{Net}_{k=m}}{\partial O_{j}} \right] \cdot \frac{\partial O_{j}}{\partial Net_{j}} \cdot "
     r"\frac{\partial Net_{j}}{\partial w_{ji}}"),
    ("eq2.png", 14, r"\frac{\partial E}{\partial Net_{k}} \Rightarrow -\delta_{k}"),
    ("eq3.png", 14,
     r"\mathrm{Net}_{k}=\sum_{k} w_{kj}\,O_{j} \Rightarrow \frac{\partial \mathrm{Net}_{k}}{\partial O_{j}} = w_{kj}"),
    ("eq4.png", 14,
     r"O_{j} = \frac{1}{1+e^{-Net_{j}}} \Rightarrow \frac{\partial O_{j}}{\partial Net_{j}} = O_{j}(1-O_{j})"),
    ("eq5.png", 14,
     r"\mathrm{Net}_{j}=\sum_{j} w_{ji}\,O_{i} \Rightarrow \frac{\partial \mathrm{Net}_{j}}{\partial w_{ji}} = O_{i}"),
]

for name, fs, latex in EQS:
    r = subprocess.run(["python3", RENDER, latex, f"{OUT}/{name}", str(fs), "000000"],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout.strip().splitlines()[-1])
        print(f"{name}: {d['w_px']}x{d['h_px']}px w={d['w_in']:.5f} h={d['h_in']:.5f}")
    except Exception:
        print(name, "FAIL", r.stdout[-160:], r.stderr[-160:])
