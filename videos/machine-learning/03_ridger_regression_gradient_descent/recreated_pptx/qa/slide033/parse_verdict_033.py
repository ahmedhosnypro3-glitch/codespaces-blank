#!/usr/bin/env python3
"""Read a slide-033 judge transcript, extract the verdict + issues, and print
the certification/resume commands. Read-only: fixes nothing.

Usage: parse_verdict_033.py <transcript.txt> [more.txt ...]
Exit 0 if every listed transcript carries FINAL VERDICT: PASS, else 1.
"""
import re
import sys

CERT = """# certification (only after BOTH legs are real + PASS or PIL-refuted):
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
python3 scripts/15_progress.py set 33 visual_check PASS
python3 scripts/15_progress.py set 33 visual_transcript {fullslide}
python3 scripts/15_progress.py set 33 pptx_path videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_033_recreated.pptx
python3 scripts/15_progress.py set 33 build_script videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_033.js
python3 scripts/15_progress.py set 33 gen_status passed
python3 scripts/15_progress.py set 33 visual_attempts 9
python3 scripts/15_progress.py release 33 w033-fresh-20261024
python3 scripts/15_progress.py get 33   # verify gen passed + visual PASS + worker_id ""
"""

ok_all = True
for path in sys.argv[1:]:
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as e:
        print(f"{path}: UNREADABLE ({e})"); ok_all = False; continue
    m = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)\b([^\n]*)", text, re.I)
    if not m:
        print(f"{path}: NO FINAL VERDICT LINE -> not usable evidence"); ok_all = False; continue
    verdict = m.group(1).upper()
    if verdict != "PASS":
        ok_all = False
    issues = re.findall(r"^\s*(?:[-*]\s*)?(?!GROUND)(.{0,400}?\b(?:BLOCKER|MAJOR|MINOR)\b.{0,160})",
                        text, re.M)
    print(f"{path}: {verdict} {m.group(2).strip()}")
    seen = set()
    for i in issues[:40]:
        k = i.strip()[:200]
        if k in seen: continue
        seen.add(k)
        print(f"    issue: {k}")
print()
print(CERT.format(fullslide=sys.argv[1] if len(sys.argv) > 1 else "<full-slide transcript path>"))
sys.exit(0 if ok_all else 1)
