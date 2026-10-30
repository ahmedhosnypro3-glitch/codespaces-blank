#!/usr/bin/env python3
"""Driver: render every equation PNG for slide 048 via render_stackeq.py.
Writes eq_*.json sidecars next to each PNG (contract of render_eq.py).
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)
S = {"fontsize": 13, "color": "000000"}

V4 = ["4", "-2", "-2"]      # [4; -2; -2]
V5 = ["5", "-1", "-1"]      # [5; -1; -1]
V11 = ["1", "1", "1"]       # [1; 1; 1]


def eq(name, segments, fontsize=13, tw=None, th=None):
    spec = {"segments": segments, "fontsize": fontsize, "color": "000000"}
    if tw: spec["target_w_in"] = tw
    if th: spec["target_h_in"] = th
    out = os.path.join(ASSETS, name + ".png")
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, "render_stackeq.py"),
         json.dumps(spec), out],
        capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"FAIL {name}: {r.stderr[-500:]}")
    info = json.loads(r.stdout.strip().splitlines()[-1])
    info.pop("path", None)
    with open(os.path.join(ASSETS, name + ".json"), "w") as f:
        json.dump(info, f, indent=2)
    print(f"{name}: {info['w_in']}x{info['h_in']} in, baseline_frac={info['baseline_frac']}")
    return info


# --- top-centre: Initial W vector on its own line (stacked, measured 23x40px) ---
# Entries: 4 (black), -2 (RED), -2 (RED) per judge finding
eq("eq_initial_w_col", [
    {"col": V4, "colors": ["000000", "FF0000", "FF0000"]},
], tw=23/72, th=40/72)

# --- six calculation rows (measured widths in frame px) ---
LEFT_W = 128          # d(xN) = ... = R  (box1 measured cols 301-429)
ROW1_W = 182          # W = [4;-2;-2]+1.[1;1;1]=[5;-1;-1]  (cols 617-799)

# Row 1: d(x1) = (1 1 1) · [4 -2 -2] = 0
# (1 1 1) - first entry RED (non-unity? No, all 1s are unity so black), wait judge says row vector entries in RED
# Actually judge says: "Row-vector entry colors in d(x1) equation: (1 1 1) rendered in red"
# But all three are 1s... maybe the original colors them red as a vector? Let's check original.
# Per judge: "(1 1 1) rendered in red" - so all red.
# Column vector [4; -2; -2] - 4 black, -2 red, -2 red (non-unity red)
for i, (vec, col_vec, res, vec_colors, col_colors) in enumerate([
        (["1", "1", "1"], V4, "0",
         ["FF0000", "FF0000", "FF0000"],  # row vector all red
         ["000000", "FF0000", "FF0000"]), # col vector: 4 black, -2 red, -2 red
        (["1", "2", "1"], V5, "2",
         ["000000", "FF0000", "000000"],  # row: 1 black, 2 red, 1 black
         ["000000", "FF0000", "FF0000"]), # col: 5 black, -1 red, -1 red
        (["1", "1", "2"], V5, "2",
         ["000000", "000000", "FF0000"],  # row: 1,1 black, 2 red
         ["000000", "FF0000", "FF0000"]), # col same
        (["1", "5", "4"], V5, "-4",
         ["000000", "FF0000", "FF0000"],  # row: 1 black, 5 red, 4 red
         ["000000", "FF0000", "FF0000"]),
        (["1", "6", "5"], V5, "-6",
         ["000000", "FF0000", "FF0000"],
         ["000000", "FF0000", "FF0000"]),
        (["1", "6", "6"], V5, "-7",
         ["000000", "FF0000", "FF0000"],
         ["000000", "FF0000", "FF0000"])]):
    eq(f"eq_r{i+1}_l", [
        {"t": f"d(x_{{{i + 1}}}) = "}, {"row": vec, "colors": vec_colors},
        {"t": " \\cdot "}, {"col": col_vec, "colors": col_colors},
        {"t": f" = {res}"}], tw=LEFT_W/72)

# Row 1 right side: W = [4;-2;-2] + 1·[1;1;1] = [5;-1;-1]
# Colors: [4;-2;-2] - 4 black, -2 red, -2 red
# [1;1;1] - all 1s (unity) black
# [5;-1;-1] - 5 black, -1 red, -1 red
eq("eq_r1_w", [
    {"t": "W = "}, {"col": V4, "colors": ["000000", "FF0000", "FF0000"]},
    {"t": " + 1 \\cdot "}, {"col": V11, "colors": ["000000", "000000", "000000"]},
    {"t": " = "}, {"col": V5, "colors": ["000000", "FF0000", "FF0000"]},
], tw=ROW1_W/72)

# Rows 2-6 right side: W = [5;-1;-1] (all same)
# 5 black, -1 red, -1 red
eq("eq_r_kw", [
    {"t": "W = "}, {"col": V5, "colors": ["000000", "FF0000", "FF0000"]},
], tw=96/72)
print("done")