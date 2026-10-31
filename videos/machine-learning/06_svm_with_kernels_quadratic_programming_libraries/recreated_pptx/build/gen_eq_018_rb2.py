#!/usr/bin/env python3
"""Re-render slide 018 mapping equation PNGs bigger/cleaner (rb2):
eq18_map_rb2.png  'Z ⇒ ϕ(Z)'   (black Z, red arrow, blue phi)
eq18_colvec_rb2.png 'Z = (x;y) ⇒ (x²;y²;√2xy)' stacked column vectors."""
import subprocess
import sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"

subprocess.run([
    sys.executable, BASE + "/render_math.py",
    "--out", BASE + "/eq_018/eq18_map_rb2.png",
    "--size", "24", "--maxw", "1.15", "--maxh", "0.30",
    "--row", "#000000:\\boldsymbol{Z}||#CC0000:\\ \\Rightarrow\\ ||#0000CC:\\phi||#000000:(\\boldsymbol{Z})",
    "--out-json", BASE + "/eq_018/eq18_map_rb2.png.json",
], check=True)

subprocess.run([
    sys.executable, BASE + "/render_math.py",
    "--out", BASE + "/eq_018/eq18_colvec_rb2.png",
    "--size", "28", "--maxw", "2.38", "--maxh", "0.86",
    "--row", "#000000:\\boldsymbol{Z}=\\left(\\overset{x}{y}\\right)||#CC0000:\\ \\Rightarrow\\ ||#000000:\\left(\\overset{x^{2}}{\\overset{y^{2}}{\\sqrt{2}\\,xy}}\\right)",
    "--out-json", BASE + "/eq_018/eq18_colvec_rb2.png.json",
], check=True)

from PIL import Image
for n in ("eq18_map_rb2", "eq18_colvec_rb2"):
    im = Image.open(f"{BASE}/eq_018/{n}.png")
    print(n, im.size, round(im.size[0] / 600, 4), "x", round(im.size[1] / 600, 4), "in")
