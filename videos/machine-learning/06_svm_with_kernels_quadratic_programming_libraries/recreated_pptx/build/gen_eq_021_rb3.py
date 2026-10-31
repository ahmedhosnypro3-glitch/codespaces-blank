#!/usr/bin/env python3
"""Fresh rb3 math assets for slide_021 (Quadratic Kernel), spec section 8 only."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_021")
os.makedirs(OUT, exist_ok=True)

AB = "#CC0000:a^{T}||#0000CC:b"
HDR = "#333333:[||" + AB + "||#333333:]^{2}"

ASSETS = [
    ("rb3_header", 18, 1.00, 0.40, [HDR]),
    ("rb3_chip", 14, 0.79, 0.36, [HDR]),
    ("rb3_ab", 12, 0.79, 0.46, [
        "#CC0000:a_{1}||#333333:\\ \\vert\\ ||#0000CC:b_{1}",
        "#CC0000:a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{2}",
    ]),
    ("rb3_normal", 12, 0.87, 0.45, [
        "#CC0000:a_{1}\\ a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{1}",
        "#CC0000:\\phantom{a_{1}\\ a_{2}}||#333333:\\ \\vert\\ ||#0000CC:b_{2}",
    ]),
    ("rb3_calc_ab", 12, 1.18, 0.22, [
        "#1A1A1A:\\mathrm{Calculate}\\ \\ ||#CC0000:a^{T}\\ ||#0000CC:b",
    ]),
    ("rb3_calc_uv", 12, 1.06, 0.22, [
        "#1A1A1A:\\mathrm{Calculate}\\ \\ ||#CC0000:u^{T}\\ ||#0000CC:v",
    ]),
    ("rb3_mapping", 13, 1.40, 0.21, [
        "#CC0000:a\\ ,\\ b\\ \\Rightarrow\\ u\\ ,\\ v",
    ]),
    ("rb3_pink", 12, 1.42, 0.92, [
        "#CC0000:\\left[\\overset{a_{1}^{2}}{\\overset{a_{2}^{2}}{\\sqrt{2}\\,a_{1}a_{2}}}\\right]"
        "||#333333:\\ ,\\ ||#0000CC:\\left[\\overset{b_{1}^{2}}{\\overset{b_{2}^{2}}{\\sqrt{2}\\,b_{1}b_{2}}}\\right]",
    ]),
    ("rb3_kernel", 12, 2.10, 1.00, [
        "#CC0000:[a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}||#333333:\\ \\vert\\ ||#0000CC:b_{1}^{2}]",
        "#CC0000:\\phantom{[a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}}||#333333:\\ \\vert\\ ||#0000CC:\\phantom{b_{1}^{2}]}b_{2}^{2}]",
        "#CC0000:\\phantom{[a_{1}^{2}\\ a_{2}^{2}\\ \\sqrt{2}\\,a_{1}a_{2}}||#333333:\\ \\vert\\ ||#0000CC:\\phantom{b_{1}^{2}]}\\sqrt{2}\\,b_{1}b_{2}]",
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
