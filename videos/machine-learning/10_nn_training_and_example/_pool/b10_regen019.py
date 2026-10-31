import sys
import numpy as np
from PIL import Image

# Regenerate slide_019 bottom-right panel equations to match the ORIGINAL frame
# (ground truth per REJUDGE_PROTOCOL). Reads frame via doc-parse + judge agreement:
#   line2: Net_k = sum_k w_kj O_j  =>  dNet_k/dO_j = w_kj
#   line4: Net_j = sum_j w_ij O_i  =>  dNet_j/dw_ji = O_i   (frame prints w_ji-family)
import subprocess, json, os

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
OUT = f"{NS}/recreated_pptx/build/eq_slide_019"
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"

# color segments rendered in black; red arrow kept black for simplicity? keep black
EQS = {
    # line2 (eq3.png): Net_k = sum_k w_kj O_j => dNet_k/dO_j = w_kj
    "eq3.png": r"\mathrm{Net}_{k}=\sum_{k} w_{kj}\,O_{j} \Rightarrow \frac{\partial \mathrm{Net}_{k}}{\partial O_{j}} = w_{kj}",
    # line4 (eq5.png): Net_j = sum_j w_ij O_i => dNet_j/dw_ji = O_i
    "eq5.png": r"\mathrm{Net}_{j}=\sum_{j} w_{ij}\,O_{i} \Rightarrow \frac{\partial \mathrm{Net}_{j}}{\partial w_{ji}} = O_{i}",
}

for name, latex in EQS.items():
    out = f"{OUT}/{name}"
    r = subprocess.run(
        ["python3", RENDER, latex, out, "14", "000000"],
        capture_output=True, text=True)
    print(name, r.stdout.strip() or r.stderr.strip()[:200])
