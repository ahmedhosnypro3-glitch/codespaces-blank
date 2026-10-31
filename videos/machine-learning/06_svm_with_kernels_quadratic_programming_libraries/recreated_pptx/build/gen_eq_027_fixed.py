#!/usr/bin/env python3
"""Fixed-point equation renders for slide 027 (ink-tight, no fit shrink)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_math as rm
from PIL import Image

EQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eq_027")
INK = "#7B241C"; RED = "#C00000"
JOBS = [
    ("eq_remember.png", 16, f"{INK}:\\mathrm{{Remember:\\ }}||{INK}:[a^{{T}}b]^{{2}}=[a_{{1}}\\ a_{{2}}][b_{{1}}\\ b_{{2}}]=(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})^{{2}}=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{1}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}"),
    ("eq_strip.png", 14, f"{RED}:a_{{1}}^{{2}}\\ \\ a_{{2}}^{{2}}\\ \\ \\sqrt{{2}}a_{{1}}a_{{2}}\\ \\ \\sqrt{{2}}a_{{1}}\\ \\ \\sqrt{{2}}a_{{2}}\\ \\ 1"),
    ("eq_phib.png", 14, f"{INK}:\\left\\{{\\substack{{b_{{1}}^{{2}}}\\\\b_{{2}}^{{2}}\\\\sqrt{{2}}b_{{1}}b_{{2}}\\\\sqrt{{2}}b_{{1}}\\\\sqrt{{2}}b_{{2}}\\\\1}}\\right."),
    ("eq_phix.png", 14, f"{INK}:\\left\\{\\substack{{x_{{1}}^{{2}}}\\\\x_{{2}}^{{2}}\\\\sqrt{{2}}x_{{1}}x_{{2}}\\\\sqrt{{2}}x_{{1}}\\\\sqrt{{2}}x_{{2}}\\\\1}}\\right."),
    ("eq_where.png", 15, f"{INK}:\\mathrm{{Where:}}\\ \\phi(x)\\equiv x_{{1}}\\ \\Rightarrow"),
    ("eq_label.png", 14, f"{RED}:|a^{{T}}b|^{{2}}"),
    ("eq_exp1.png", 17, f"{INK}:[a^{{T}}b+1]^{{2}}=(a^{{T}}b)^{{2}}+2a^{{T}}b+1=(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})^{{2}}=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}+2(a_{{1}}b_{{1}}+a_{{2}}b_{{2}})+1"),
    ("eq_exp2.png", 16, f"{INK}:=a_{{1}}^{{2}}b_{{1}}^{{2}}+a_{{2}}^{{2}}b_{{2}}^{{2}}+2a_{{1}}b_{{1}}a_{{2}}b_{{2}}+2a_{{1}}b_{{1}}+2a_{{2}}b_{{2}}+1"),
]
for name, pt, row in JOBS:
    canvas = rm.render_row(row, pt)
    out = os.path.join(EQ, name)
    Image.fromarray(canvas).save(out)
    info = {"path": out, "w_px": int(canvas.shape[1]), "h_px": int(canvas.shape[0]),
            "w_in": round(canvas.shape[1] / rm.DPI, 5), "h_in": round(canvas.shape[0] / rm.DPI, 5),
            "dpi": rm.DPI, "fontsize_pt": [pt], "rows": [row]}
    with open(out + ".json", "w") as fh:
        json.dump(info, fh, indent=2)
    print(name, info["w_in"], "x", info["h_in"], "@", pt, "pt")
