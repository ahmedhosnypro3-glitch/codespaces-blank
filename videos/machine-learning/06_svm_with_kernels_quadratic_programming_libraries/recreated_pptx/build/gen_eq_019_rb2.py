#!/usr/bin/env python3
"""Re-render slide 019 kernel-chain equation with crisp upright 'map to'/'and'
and a clear superscript T on phi(a)^T. Output eq_019/eq19_kernel_rb2.png."""
import json
import subprocess
import sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
OUT = BASE + "/eq_019/eq19_kernel_rb2.png"

row = (
    "#CC0000:\\boldsymbol{a}^{T}\\boldsymbol{b}"
    "||#0000CC:\\ \\Rightarrow\\ "
    "||#000000:\\mathrm{map\\ to}\\ "
    "||#009900:\\boldsymbol{\\phi(a)}\\ "
    "||#000000:\\mathrm{and}\\ "
    "||#009900:\\boldsymbol{\\phi(b)}"
    "||#0000CC:\\ \\Rightarrow\\ "
    "||#009900:\\boldsymbol{\\phi(a)}^{T}\\boldsymbol{\\phi(b)}"
    "||#000000:\\ \\equiv\\ "
    "||#009900:\\boldsymbol{K}"
    "||#CC0000:\\boldsymbol{(a,\\ b)}"
)

subprocess.run([
    sys.executable, BASE + "/render_math.py",
    "--out", OUT, "--size", "30", "--maxw", "8.4", "--maxh", "0.42",
    "--row", row, "--out-json", OUT + ".json",
], check=True)

from PIL import Image
im = Image.open(OUT)
print(OUT, im.size, im.size[0] / 600.0, "x", im.size[1] / 600.0, "in")
