#!/usr/bin/env python3
"""Render all slide_011 equations with sidecar JSON output."""
import json, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = "/home/codespace/.agents/skills/slide-recreation/scripts/render_eq.py"

EQS = [
    ("eq1", r'\Delta_{ji} = -\eta \frac{\partial E}{\partial w_{ji}} = -\frac{\partial E}{\partial Net_j} \frac{\partial Net_j}{\partial w_{ji}} = \eta \delta_j \cdot O_i'),
    ("eq2", r'\delta_j = -\frac{\partial E}{\partial Net_j} \text{ (one } \delta \text{ for each Node } j \text{)}'),
    ("eq3", r'\text{For Output Layer, Sigmoid Activation } \Rightarrow \delta_j = (t_j-O_j) \cdot O_j(1-O_j) \Rightarrow \Delta_{ji} = \eta (t_j-O_j) \cdot O_j(1-O_j) \cdot O_i'),
]

for name, latex in EQS:
    png = os.path.join(HERE, name + ".png")
    side = os.path.join(HERE, name + ".json")
    r = subprocess.run(["python3", RENDER, latex, png, "14", "000000"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"{name}: FAILED {r.stderr.strip()[:120]}")
        continue
    info = json.loads(r.stdout)
    info["latex"] = latex
    info["rel_path"] = f"./eq_slide_011/{name}.png"
    with open(side, "w") as f:
        json.dump(info, f, indent=2)
    print(f"{name}: {info['w_in']}x{info['h_in']}in baseline_frac={info['baseline_frac']}")