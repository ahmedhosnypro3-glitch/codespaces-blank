#!/usr/bin/env python3
"""Slide 020 attempt-2 assets v3: iterate font size so each re-rendered equation
lands on the ORIGINAL's measured ink width (closed-loop PIL targets).
Targets (inches, from the 960x540 frame):
  cream r1 2.19 | r2 2.875 | r3 3.417 | r4 2.792
  delta 5.14 | where 7.94
Panel fit caps: cream lines <3.45in from x 9.22; delta <5.18in; where <8.26in."""
import json
import subprocess

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
OUT = f"{NS}/recreated_pptx/build/eq_slide_020_v2"
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"

SPEC = [
    ("eq_r1.png", 2.19, 3.45, r"\frac{\partial E}{\partial Net_k} \Rightarrow -\delta_k"),
    ("eq_r2.png", 2.875, 3.45,
     r"Net_k = \sum_{k} w_{kj} O_j \Rightarrow \frac{\partial Net_k}{\partial O_j} = w_{kj}"),
    ("eq_r3.png", 3.417, 3.45,
     r"O_j = \frac{1}{1+e^{-Net_j}} \Rightarrow \frac{\partial O_j}{\partial Net_j} = O_j(1-O_j)"),
    ("eq_r4.png", 2.792, 3.45,
     r"Net_j = \sum_{j} w_{ji} O_i \Rightarrow \frac{\partial Net_j}{\partial w_{ji}} = O_i"),
    ("eq_delta.png", 5.14, 5.18,
     r"\Delta_{ji} = -\eta \frac{\partial E}{\partial w_{ji}} = \sum_{k=1}^{m} \delta_k w_{kj} \cdot O_j(1-O_j) \cdot O_i = \eta \delta_j \cdot O_i"),
    ("eq_where.png", 7.94, 8.26,
     r"\mathrm{Where}\ \delta_j = \sum_{k=1}^{m} \delta_k w_{kj} \cdot O_j(1-O_j) \quad (\mathrm{for\ each\ Node}\ j\ \mathrm{at\ hidden\ layer})"),
]


def render(latex, out, fs):
    r = subprocess.run(["python3", RENDER, latex, out, str(fs), "000000"],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        print("  render fail:", r.stderr[-200:])
        return None


for name, target, cap, latex in SPEC:
    fs, best = 11.0, None
    for _ in range(14):
        d = render(latex, f"{OUT}/{name}", fs)
        if not d:
            break
        best = (fs, d)
        if abs(d["w_in"] - target) <= 0.03:
            break
        fs = round(fs * target / d["w_in"], 3)
        if fs > 60:
            break
    if not best:
        print(name, "FAILED")
        continue
    fs, d = best
    clipped = "  !! OVER CAP" if d["w_in"] > cap else ""
    print(f"{name}: fs={fs} -> {d['w_px']}x{d['h_px']}px w={d['w_in']:.4f}in "
          f"(target {target}){clipped}")
