#!/usr/bin/env python3
"""Force a fresh judge run for slide 001 despite a stale FAIL ledger row:
wrap tools/judge_slides.py with ledger_rows disabled so the md5 skip never fires."""
import os, sys

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
sys.path.insert(0, os.path.join(BASE, "tools"))
import judge_slides as j

j.ledger_rows = lambda: {}
j.run(1)
