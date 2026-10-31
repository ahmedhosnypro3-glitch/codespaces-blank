#!/usr/bin/env python3
"""Generate eq_021/ math assets for slide_021 (Quadratic Kernel) via render_math.py."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_021")
os.makedirs(OUT, exist_ok=True)

ASSETS = [
    ("eq_header", 18, 0.93, 0.375, [
        "#333333:[||#CC0000:a^{T}||#0000CC:b||#333333:]^{2}",
    ]),
    ("eq_ab", 12, 0.80, 0.62, [
        "#CC0000:a_{1}||#333333:\\ \\vert\\ ||#0000CC:b_{1}",
        "#CC0000:a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{2}",
    ]),
    ("eq_normal_inner", 12, 0.88, 0.55, [
        "#CC0000:a_{1}\\ a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{1}",
        "#CC0000:\\phantom{a_{1}\\ a_{2}}||#333333:\\ \\vert\\ ||#0000CC:b_{2}",
    ]),
    ("eq_calc_ab", 12, 1.20, 0.24, [
        "#1A1A1A:\\mathrm{Calculate}\\ \\ ||#CC0000:a^{T}\\ ||#0000CC:b",
    ]),
    ("eq_calc_uv", 12, 1.08, 0.24, [
        "#1A1A1A:\\mathrm{Calculate}\\ \\ ||#CC0000:u^{T}\\ ||#0000CC:v",
    ]),
    ("eq_mapping", 13, 1.426, 0.2175, [
        "#CC0000:\\boldsymbol{a}\\ ,\\ \\boldsymbol{b}\\ \\Rightarrow\\ \\boldsymbol{u}\\ ,\\ \\boldsymbol{v}",
    ]),
    ("eq_pink", 12, 1.439, 0.93, [
        "#CC0000:\\left[\\overset{a_{1}^{2}}{\\overset{a_{2}^{2}}{\\sqrt{2}\\,a_{1}a_{2}}}\\right]"
        "||#333333:\\ ,\\ ||#0000CC:\\left[\\overset{b_{1}^{2}}{\\overset{b_{2}^{2}}{\\sqrt{2}\\,b_{1}b_{2}}}\\right]",
    ]),
    ("eq_kernel_inner", 12, 2.119, 1.005, [
        "#CC0000:[a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}]||#333333:\\ \\vert\\ ||#0000CC:b_{1}^{2}]",
        "#CC0000:\\phantom{[a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}]}||#333333:\\ \\vert\\ ||#0000CC:\\phantom{b_{1}^{2}]}b_{2}^{2}]",
        "#CC0000:\\phantom{[a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}]}||#333333:\\ \\vert\\ ||#0000CC:\\phantom{b_{1}^{2}]}\\sqrt{2}\\,b_{1}b_{2}]",
    ]),
]


def main():
    for name, size, maxw, maxh, rows in ASSETS:
        png = os.path.join(OUT, name + ".png")
        js = os.path.join(OUT, name + ".json")
        cmd = [sys.executable, os.path.join(HERE, "render_math.py"),
               "--out", png, "--size", str(size), "--maxw", str(maxw),
               "--maxh", str(maxh), "--out-json", js]
        for r in rows:
            cmd += ["--row", r]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print("FAIL", name, res.stderr[-500:])
            sys.exit(1)
        info = json.loads(res.stdout)
        print(name, info["w_in"], "x", info["h_in"], "in", info["w_px"], "x", info["h_px"], "px")


if __name__ == "__main__":
    main()
