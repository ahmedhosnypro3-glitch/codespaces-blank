#!/usr/bin/env python3
"""Slide 011 assets v4: curly green underbrace PNG for the TP+FN bracket."""
import json, subprocess, sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
A = NS + "/recreated_pptx/build/assets"
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"


def render_eq(latex, out, fs, color="000000"):
    res = subprocess.run([sys.executable, RENDER, latex, out, str(fs), color],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr)
    return json.loads(res.stdout.strip().splitlines()[-1])


def render_eq_to_width(latex, out, target_w_in, fs0=20.0, color="000000"):
    info = render_eq(latex, out, fs0, color)
    fs = fs0 * target_w_in / info["w_in"]
    info = render_eq(latex, out, round(fs, 2), color)
    return info


i = render_eq_to_width(r"\underbrace{\;\;\;\;\;\;\;\;\;\;\;\;\;\;}",
                       A + "/brace_011_v4.png", 3.15, 20.0, color="#00B050")
print("brace:", i["w_px"], "x", i["h_px"], "=", i["w_in"], "x", i["h_in"], "in")
