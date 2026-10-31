#!/usr/bin/env python3
"""Re-render slide 012 equation PNGs (rb3) with bold math and region-fit sizes."""
import subprocess, os

BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
OUT = os.path.join(BUILD, "eq_012", "rb3")
os.makedirs(OUT, exist_ok=True)
B = lambda s: "\\boldsymbol{" + s + "}"

EQS = {
    "e1": (6.00, 0.25, ["#0000CC:" + B(r"[+1\alpha_{1}^{2}+2\alpha_{1}\alpha_{2}-5.5\alpha_{1}\alpha_{3}-6\alpha_{1}\alpha_{4}\;+2\alpha_{2}\alpha_{4}\text{[?]}+4\alpha_{2}^{2}-11\alpha_{2}\alpha_{3}-12\alpha_{2}\alpha_{4}")]),
    "e2": (8.80, 0.26, ["#0000CC:" + B(r"-5.5\alpha_{3}\alpha_{1}-11\alpha_{3}\alpha_{2}+32.5\alpha_{3}^{2}+36\alpha_{3}\alpha_{4}\;-6\alpha_{4}\alpha_{1}-12\alpha_{4}\alpha_{2}+36\alpha_{4}\alpha_{3}+40\alpha_{4}^{2}]-[\alpha_{1}+\alpha_{2}+\alpha_{3}+\alpha_{4}]")]),
    "e3": (0.50, 0.30, ["#CC0000:" + B(r"\sum\alpha_i y_i=0")]),
    "e4": (1.55, 0.20, ["#CC0000:" + B(r"\alpha_{1}+\alpha_{2}-\alpha_{3}-\alpha_{4}=0")]),
    "e5": (0.50, 0.27, ["#CC0000:" + B(r"\alpha_i\leq C")]),
    "e6": (2.75, 0.24, ["#CC0000:" + B(r"\alpha_{1}\leq1,\;\alpha_{2}\leq1,\;\alpha_{3}\leq1,\;\alpha_{4}\leq1")]),
    "e7": (0.50, 0.28, ["#CC0000:" + B(r"\alpha_i\geq 0")]),
    "e8": (2.80, 0.24, ["#CC0000:" + B(r"\alpha_{1}>0,\;\alpha_{2}>0,\;\alpha_{3}>0,\;\alpha_{4}>0")]),
    "e9": (1.82, 0.42, ["#008000:" + B(r"\frac{1}{2}"), "#0000CC:" + B(r"[X^{T}PX]+"), "#CC0000:" + B(r"q^{T}"), "#0000CC:" + B(r"X")]),
    "e10": (5.10, 0.27, ["#0000CC:" + B(r"[+2\alpha_{1}^{2}+4\alpha_{1}\alpha_{2}-11\alpha_{1}\alpha_{3}-12\alpha_{1}\alpha_{4}\;+4\alpha_{1}\alpha_{4}\text{[?]}+8\alpha_{2}^{2}-22\alpha_{2}\alpha_{3}-24\alpha_{2}\alpha_{4}")]),
    "e11": (8.60, 0.27, ["#0000CC:" + B(r"-11\alpha_{3}\alpha_{1}-22\alpha_{3}\alpha_{2}+65\alpha_{3}^{2}+72\alpha_{3}\alpha_{4}\;-12\alpha_{4}\alpha_{1}-24\alpha_{4}\alpha_{2}+72\alpha_{4}\alpha_{3}+80\alpha_{4}^{2}]-[\alpha_{1}+\alpha_{2}+\alpha_{3}+\alpha_{4}]")]),
    "e13": (2.80, 0.38, ["#CC0000:" + B(r"q^{T}="), "#0000CC:" + B(r"[-1\;-1\;-1\;-1]")]),
    "half": (0.21, 0.42, ["#008000:" + B(r"\frac{1}{2}")]),
    "pmat": (3.15, 1.26, ["#CC0000:" + B(r"P="), "#0000CC:" + B(r"\left[\overset{2\;\;\;4\;-11\;-12}{\overset{4\;\;\;8\;-22\;-24}{\overset{-11\;-22\;65\;72}{-12\;-24\;72\;80}}}\right]")]),
}

for name, (mw, mh, segs) in EQS.items():
    row = "||".join(segs)
    out = os.path.join(OUT, name + ".png")
    cmd = ["python3", os.path.join(BUILD, "render_math.py"), "--out", out,
           "--out-json", os.path.join(OUT, name + ".json"),
           "--size", "14", "--maxw", str(mw), "--maxh", str(mh), "--row", row]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(name, r.stdout.strip() or r.stderr.strip()[-200:])
