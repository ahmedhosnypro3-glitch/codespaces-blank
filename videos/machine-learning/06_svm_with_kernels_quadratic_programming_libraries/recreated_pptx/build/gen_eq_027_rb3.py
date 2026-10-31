#!/usr/bin/env python3
"""Regenerate eq_027 assets (rb3 fix2): multi-row --row stacking (reliable), bigger fonts."""
import subprocess
import sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"
OUT = BASE + "/eq_027"
RM = BASE + "/render_math.py"
MAROON = "#7B241C"
RED = "#C00000"

# name, size_pt, maxw_in, maxh_in, rows
ASSETS = [
    ("eq_veca", 30, 0.55, 0.50, [f"{MAROON}:a_{{1}}", f"{MAROON}:a_{{2}}"]),
    ("eq_vecb", 30, 0.55, 0.50, [f"{MAROON}:b_{{1}}", f"{MAROON}:b_{{2}}"]),
    ("eq_remember", 18, 6.70, 0.42, [
     f"{MAROON}:\\mathrm{{Remember:}}\\ [a^{{T}}b]^{{2}}=[a_{{1}}\\ a_{{2}}][b_{{1}}\\ b_{{2}}]"
     f"=(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})^{{2}}=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}"]),
    ("eq_label", 17, 3.10, 0.30, [f"{RED}:|a^{{T}}b|^{{2}}"]),
    ("eq_tan1", 22, 1.50, 0.38, [f"{MAROON}:[a^{{T}}b+1]^{{2}}"]),
    ("eq_tan2", 20, 1.50, 0.38, [f"{MAROON}:[a^{{T}}b+1]^{{2}}"]),
    ("eq_exp1", 17, 10.75, 0.34, [
     f"{MAROON}:[a^{{T}}b+1]^{{2}}=(a^{{T}}b)^{{2}}+2a^{{T}}b+1=(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})^{{2}}"
     f"=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}+2(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})+1"]),
    ("eq_exp2", 17, 10.70, 0.30, [
     f"{MAROON}:=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}+2a_{{1}}b_{{1}}+2a_{{2}}b_{{2}}+1"]),
    ("eq_strip", 17, 4.00, 0.34, [
     f"{RED}:a_{{1}}^{{2}}\\ \\ a_{{2}}^{{2}}\\ \\ \\sqrt{{2}}a_{{1}}a_{{2}}\\ \\ \\sqrt{{2}}a_{{1}}\\ \\ \\sqrt{{2}}a_{{2}}\\ \\ 1"]),
    ("eq_phib", 15, 1.30, 1.30, [
     f"{MAROON}:b_{{1}}^{{2}}", f"{MAROON}:b_{{2}}^{{2}}", f"{MAROON}:\\sqrt{{2}}b_{{1}}b_{{2}}",
     f"{MAROON}:\\sqrt{{2}}b_{{1}}", f"{MAROON}:\\sqrt{{2}}b_{{2}}", f"{MAROON}:1"]),
    ("eq_phix", 15, 1.45, 1.30, [
     f"{MAROON}:x_{{1}}^{{2}}", f"{MAROON}:x_{{2}}^{{2}}", f"{MAROON}:\\sqrt{{2}}x_{{1}}x_{{2}}",
     f"{MAROON}:\\sqrt{{2}}x_{{1}}", f"{MAROON}:\\sqrt{{2}}x_{{2}}", f"{MAROON}:1"]),
    ("eq_where", 18, 2.35, 0.36, [
     f"{MAROON}:\\mathrm{{Where:}}\\ \\phi(x)\\equiv(x_{{1}}\\ x_{{2}})^{{T}}\\ \\Rightarrow"]),
    ("eq_2d6d", 24, 1.35, 0.30, [f"{RED}:\\mathbf{{2D}}\\ \\Rightarrow\\ \\mathbf{{6D}}"]),
]

for name, size, maxw, maxh, rows in ASSETS:
    # render_math fits EACH --row to maxh independently, so divide by row count
    cmd = [sys.executable, RM, "--out", f"{OUT}/{name}.png", "--size", str(size),
           "--maxw", str(maxw), "--maxh", str(maxh / len(rows))]
    for r in rows:
        cmd += ["--row", r]
    cmd += ["--out-json", f"{OUT}/{name}.png.json"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", name, r.stderr[-300:])
        sys.exit(1)
    print("OK", name, r.stdout.strip()[:130])
