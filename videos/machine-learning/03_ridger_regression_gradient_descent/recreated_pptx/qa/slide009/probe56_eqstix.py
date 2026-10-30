#!/usr/bin/env python3
"""Probe 56 + equation renderer: render slide 009's two equations with matplotlib's
STIX serif mathtext fontset (the slide's typeface is serif/Times-like; STIX matches
both the look and the measured ink proportions far better than the default sans).

Loads the CERTIFIED scripts/render_eq.py unchanged and only sets the fontset rcParam —
no edit to certified tooling. Same CLI/contract as render_eq.py:
  python3 probe56_eqstix.py '<mathtext>' out.png <fontsize_pt> <hexcolor>
Prints the same JSON sidecar.
"""
import json, os, sys, importlib.util
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "stix"   # serif — matches the original

ROOT = "/home/ahmed/Projects/ai_llm_slides"
spec = importlib.util.spec_from_file_location(
    "render_eq_certified", os.path.join(ROOT, "scripts", "render_eq.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)   # __name__ != "__main__" -> CLI block skipped

latex, out, fs, color = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
print(json.dumps(mod.render(latex, out, fs, color)))
