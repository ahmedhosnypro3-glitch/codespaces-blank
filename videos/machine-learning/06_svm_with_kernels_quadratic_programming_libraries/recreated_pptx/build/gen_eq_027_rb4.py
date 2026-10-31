#!/usr/bin/env python3
"""Regenerate eq_027 assets (rb4): STIX mathtext (heavier, more legible than cm),
full spec-box max sizes, plus the =phi(a)^T phi(b) label the judges flagged missing."""
import os
import subprocess
import sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
OUT = BASE + "/eq_027"
RM = BASE + "/render_math.py"
MAROON = "#7B241C"
RED = "#C00000"

os.environ["MATHTEXT_FONTSET"] = "stix"

# name, size_pt, maxw_in, maxh_in, row
ASSETS = [
    ("eq_veca", 20, 0.55, 0.50, f"{MAROON}:\\left[\\substack{{a_{{1}}\\\\a_{{2}}}}\\right]"),
    ("eq_vecb", 20, 0.55, 0.50, f"{MAROON}:\\left[\\substack{{b_{{1}}\\\\b_{{2}}}}\\right]"),
    ("eq_remember", 17, 6.72, 0.30,
     f"{MAROON}:\\mathrm{{Remember:}}\\ [a^{{T}}b]^{{2}}=[a_{{1}}\\ a_{{2}}][b_{{1}}\\ b_{{2}}]"
     f"=(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})^{{2}}=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}"),
    ("eq_label", 15, 3.15, 0.22, f"{RED}:|a^{{T}}b|^{{2}}"),
    ("eq_tan1", 20, 1.60, 0.43, f"{MAROON}:[a^{{T}}b+1]^{{2}}"),
    ("eq_tan2", 18, 1.58, 0.42, f"{MAROON}:[a^{{T}}b+1]^{{2}}="),
    ("eq_exp1", 17, 10.75, 0.35,
     f"{MAROON}:[a^{{T}}b+1]^{{2}}=(a^{{T}}b)^{{2}}+2a^{{T}}b+1=(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})^{{2}}"
     f"=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}+2(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})+1"),
    ("eq_exp2", 17, 10.70, 0.31,
     f"{MAROON}:=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}+2a_{{1}}b_{{1}}+2a_{{2}}b_{{2}}+1"),
    ("eq_strip", 15, 4.05, 0.217,
     f"{RED}:a_{{1}}^{{2}}\\ \\ a_{{2}}^{{2}}\\ \\ \\sqrt{{2}}a_{{1}}a_{{2}}\\ \\ \\sqrt{{2}}a_{{1}}\\ \\ \\sqrt{{2}}a_{{2}}\\ \\ 1"),
    ("eq_phib", 16, 0.98, 1.32,
     f"{MAROON}:\\left[\\substack{{b_{{1}}^{{2}}\\\\b_{{2}}^{{2}}\\\\sqrt{{2}}b_{{1}}b_{{2}}\\\\sqrt{{2}}b_{{1}}\\\\sqrt{{2}}b_{{2}}\\\\1}}\\right]"),
    ("eq_phix", 16, 1.35, 1.32,
     f"{MAROON}:\\left[\\substack{{x_{{1}}^{{2}}\\\\x_{{2}}^{{2}}\\\\sqrt{{2}}x_{{1}}x_{{2}}\\\\sqrt{{2}}x_{{1}}\\\\sqrt{{2}}x_{{2}}\\\\1}}\\right]"),
    ("eq_where", 16, 2.39, 0.30,
     f"{MAROON}:\\mathrm{{Where:}}\\ \\phi(x)\\equiv\\left[\\substack{{x_{{1}}\\\\x_{{2}}}}\\right]\\ \\Rightarrow"),
    ("eq_phimap", 16, 2.10, 0.30, f"{MAROON}:=\\phi(a)^{{T}}\\phi(b)"),
    ("eq_2d6d", 20, 1.39, 0.25, f"{RED}:\\mathbf{{2D}}\\ \\Rightarrow\\ \\mathbf{{6D}}"),
]

for name, size, maxw, maxh, row in ASSETS:
    cmd = [sys.executable, RM, "--out", f"{OUT}/{name}.png", "--size", str(size),
           "--maxw", str(maxw), "--maxh", str(maxh), "--row", row,
           "--out-json", f"{OUT}/{name}.png.json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", name, r.stderr[-400:])
        sys.exit(1)
    print("OK", name, r.stdout.strip())
