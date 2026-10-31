#!/usr/bin/env python3
"""Render slide-31 equation PNGs (600dpi, transparent) + sidecars into build/assets/s31/."""
import json, os, sys
sys.path.insert(0, "/home/codespace/ai_llm_slides/scripts")
from render_eq import render

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets/s31"
os.makedirs(OUT, exist_ok=True)

TOP = [
    ("t1", r"\delta_j = O_j(1-O_j)\left[\sum_k (\delta_k w_{kj})\right]", "FF0000"),
    ("t2", r"\Delta_j = \eta\, O_j(1-O_j)\left[\sum_k (\delta_k w_{kj})\right] = \eta\, O_j\, \delta_j", "0000FF"),
    ("t3", r"\delta_6 = 0.791(1-0.791)(0-0.791) = -0.131", "FF0000"),
    ("t4", r"\delta_7 = 0.791(1-0.791)(1-0.791) = 0.035", "0000FF"),
]
DELTAS = [
    ("d1", r"\delta_3 = O_3(1-O_3)\left[\delta_6 w_{63} + \delta_7 w_{73}\right]", "000000"),
    ("d2", r"\delta_3 = 0.9(1-0.9)\left[-0.131{\times}(-0.29) + 0.035{\times}0.458\right] = 0.005", "000000"),
    ("d3", r"\delta_4 = 0.943(1-0.943)\left[-0.131{\times}(-0.218) + 0.035{\times}0.565\right] = 0.003", "000000"),
    ("d4", r"\delta_5 = 0.968(1-0.968)\left[-0.131{\times}(-0.134) + 0.035{\times}0.669\right] = 0.001", "000000"),
]
SIG = [
    ("s1", r"O_3 = \dfrac{1}{1+e^{-2.2}} = 0.9", "000000"),
    ("s2", r"O_4 = \dfrac{1}{1+e^{-2.8}} = 0.943", "000000"),
    ("s3", r"O_5 = \dfrac{1}{1+e^{-3.4}} = 0.968", "000000"),
    ("s4", r"O_6 = \dfrac{1}{1+e^{-1.3312}} = 0.791", "000000"),
    ("s5", r"O_7 = \dfrac{1}{1+e^{-1.3312}} = 0.791", "000000"),
]
DW = [
    ("31", "5{\\times}0.005{\\times}1", "0.025"),
    ("32", "5{\\times}0.005{\\times}1", "0.125"),
    ("3b", "5{\\times}0.005{\\times}1", "0.025"),
    ("41", "5{\\times}0.003{\\times}1", "0.015"),
    ("42", "5{\\times}0.003{\\times}5", "0.075"),
    ("4b", "5{\\times}0.003{\\times}1", "0.015"),
    ("51", "5{\\times}0.001{\\times}1", "0.005"),
    ("52", "5{\\times}0.001{\\times}5", "0.025"),
    ("5b", "5{\\times}0.001{\\times}1", "0.005"),
]
W = [
    ("31", "0.1 + 0.025", "0.125"),
    ("32", "0.4 + 0.125", "0.525"),
    ("3b", "0.1 + 0.025", "0.125"),
    ("41", "0.2 + 0.015", "0.215"),
    ("42", "0.075 + 0.075", "0.15"),
    ("4b", "0.1 + 0.015", "0.115"),
    ("51", "0.3 + 0.005", "0.305"),
    ("52", "0.6 + 0.025", "0.625"),
    ("5b", "0.1 + 0.005", "0.105"),
]

manifest = {}
def emit(key, latex, color, fs=12):
    png = f"{OUT}/{key}.png"
    info = render(latex, png, fs, "#" + color)
    manifest[key] = {"png": png, "latex": latex, **info}
    return info

for k, l, c in TOP:
    emit(k, l, c)
for k, l, c in DELTAS:
    emit(k, l, c)
for k, l, c in SIG:
    emit(k, l, c)
for i, (idx, mid, val) in enumerate(DW):
    emit(f"dw{i}_p", r"\Delta W_{%s} =" % idx, "FF0000", 12)
    emit(f"dw{i}_r", mid + " = " + val, "000000", 12)
for i, (idx, mid, val) in enumerate(W):
    emit(f"w{i}_p", r"W_{%s} =" % idx, "0000FF", 12)
    emit(f"w{i}_r", mid + " = " + val, "000000", 12)

with open(f"{OUT}/manifest.json", "w") as f:
    json.dump(manifest, f, indent=1)
print("wrote", len(manifest), "assets ->", OUT)
for k, v in list(manifest.items())[:5]:
    print(k, v["w_px"], v["h_px"], v["w_in"], v["h_in"])
