#!/usr/bin/env python3
"""Regenerate eq_027 assets: each equation fitted to its spec box (inches)."""
import subprocess
import sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
OUT = BASE + "/eq_027"
RM = BASE + "/render_math.py"
MAROON = "#7B241C"
RED = "#C00000"

# name, size_pt, maxw_in, maxh_in, row
ASSETS = [
    ("eq_veca", 20, 0.50, 0.46, f"{MAROON}:\\left[\\substack{{a_{{1}}\\\\a_{{2}}}}\\right]"),
    ("eq_vecb", 20, 0.50, 0.46, f"{MAROON}:\\left[\\substack{{b_{{1}}\\\\b_{{2}}}}\\right]"),
    ("eq_remember", 17, 6.70, 0.28,
     f"{MAROON}:\\mathrm{{Remember:}}\\ [a^{{T}}b]^{{2}}=[a_{{1}}\\ a_{{2}}][b_{{1}}\\ b_{{2}}]"
     f"=(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})^{{2}}=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}"),
    ("eq_label", 15, 3.10, 0.21, f"{RED}:|a^{{T}}b|^{{2}}"),
    ("eq_tan1", 20, 1.50, 0.38, f"{MAROON}:[a^{{T}}b+1]^{{2}}"),
    ("eq_tan2", 18, 1.50, 0.38, f"{MAROON}:[a^{{T}}b+1]^{{2}}="),
    ("eq_exp1", 17, 10.75, 0.34,
     f"{MAROON}:[a^{{T}}b+1]^{{2}}=(a^{{T}}b)^{{2}}+2a^{{T}}b+1=(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})^{{2}}"
     f"=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}+2(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})+1"),
    ("eq_exp2", 17, 10.70, 0.30,
     f"{MAROON}:=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}+2a_{{1}}b_{{1}}+2a_{{2}}b_{{2}}+1"),
    ("eq_strip", 15, 4.00, 0.21,
     f"{RED}:a_{{1}}^{{2}}\\ \\ a_{{2}}^{{2}}\\ \\ \\sqrt{{2}}a_{{1}}a_{{2}}\\ \\ \\sqrt{{2}}a_{{1}}\\ \\ \\sqrt{{2}}a_{{2}}\\ \\ 1"),
    ("eq_phib", 15, 0.95, 1.28,
     f"{MAROON}:\\left[\\substack{{b_{{1}}^{{2}}\\\\b_{{2}}^{{2}}\\\\sqrt{{2}}b_{{1}}b_{{2}}\\\\sqrt{{2}}b_{{1}}\\\\sqrt{{2}}b_{{2}}\\\\1}}\\right]"),
    ("eq_phix", 15, 1.30, 1.28,
     f"{MAROON}:\\left[\\substack{{x_{{1}}^{{2}}\\\\x_{{2}}^{{2}}\\\\sqrt{{2}}x_{{1}}x_{{2}}\\\\sqrt{{2}}x_{{1}}\\\\sqrt{{2}}x_{{2}}\\\\1}}\\right]"),
    ("eq_where", 16, 2.35, 0.28, f"{MAROON}:\\mathrm{{Where:}}\\ \\phi(x)\\equiv x_{{1}}\\ \\Rightarrow"),
    ("eq_2d6d", 16, 1.35, 0.24, f"{RED}:\\mathbf{{2D}}\\ \\Rightarrow\\ \\mathbf{{6D}}"),
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
