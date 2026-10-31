#!/usr/bin/env python3
"""Slide 018 mapping equation PNGs, rb5: 3-row column vectors via \\substack
(verified to render in matplotlib 3.11 mathtext, unlike nested \\overset)."""
import subprocess
import sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"

subprocess.run([
    sys.executable, BASE + "/render_math.py",
    "--out", BASE + "/eq_018/eq18_map_rb5.png",
    "--size", "24", "--maxw", "1.15", "--maxh", "0.30",
    "--row", "#000000:\\boldsymbol{Z}||#CC0000:\\ \\Rightarrow\\ ||#0000CC:\\phi||#000000:(\\boldsymbol{Z})",
    "--out-json", BASE + "/eq_018/eq18_map_rb5.png.json",
], check=True)

subprocess.run([
    sys.executable, BASE + "/render_math.py",
    "--out", BASE + "/eq_018/eq18_colvec_rb5.png",
    "--size", "28", "--maxw", "2.38", "--maxh", "0.86",
    "--row", "#000000:\\boldsymbol{Z}=\\left(\\substack{x\\\\y}\\right)||#CC0000:\\ \\Rightarrow\\ ||#000000:\\left(\\substack{x^{2}\\\\y^{2}\\\\ \\sqrt{2}\\,xy}\\right)",
    "--out-json", BASE + "/eq_018/eq18_colvec_rb5.png.json",
], check=True)

from PIL import Image
for n in ("eq18_map_rb5", "eq18_colvec_rb5"):
    im = Image.open(f"{BASE}/eq_018/{n}.png")
    print(n, im.size, round(im.size[0] / 600, 4), "x", round(im.size[1] / 600, 4), "in")
