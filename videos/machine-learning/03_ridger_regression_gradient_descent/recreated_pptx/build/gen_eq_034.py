#!/usr/bin/env python3
"""Render slide 034's equation (stacked fraction, professional 2D format)."""
import sys, json
sys.path.insert(0, "/home/codespace/ai_llm_slides/scripts")
from render_eq import render

OUT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "03_ridger_regression_gradient_descent/recreated_pptx/build/assets/"
       "eq_034_main.png")

latex = r"f(x) = \frac{x^2 \cos(x) - x}{10}"
info = render(latex, OUT, 18, "000000")
print(json.dumps(info))
