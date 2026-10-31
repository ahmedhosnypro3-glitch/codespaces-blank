#!/usr/bin/env python3
"""Persistent judge loop for slide 037: retry until a real PASS/FAIL transcript.

Each attempt: wall 540s through the vision gate, fresh transcript tag.
Sleeps 60s between attempts. Stops on PASS/FAIL. Max 8 attempts.
"""
import hashlib, json, os, re, subprocess, sys, time

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE = "/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh"
OUTDIR = os.path.join(BASE, "qa", "rejudge2")
LEDGER = os.path.join(OUTDIR, "ledger.jsonl")
RULES = open(os.path.join(BASE, "judge_prompt_active.txt")).read().strip()

ss = "037"
paths = {"pptx": os.path.join(BASE, "recreated_pptx", f"slide_{ss}_recreated.pptx"),
         "orig": os.path.join(BASE, "unique_slides", f"slide_{ss}.jpg"),
         "render": os.path.join(BASE, "recreated_pptx", "renders", f"slide_{ss}_recreated-1.png")}
ctx = f"""VIEW: Slide {ss} — original lecture frame vs its PowerPoint recreation (SVM/kernels/QP lecture)
FACTS: the printed slide number is 37. House chrome is MANDATORY in [2] and never a discrepancy.
Images are attached in this order: image 1 = ORIGINAL, image 2 = RECREATION.
List every discrepancy as: SEVERITY (BLOCKER|MAJOR|MINOR) — element — defect — confidence.
End with exactly one terminal line: FINAL VERDICT: PASS   or   FINAL VERDICT: FAIL
"""

for attempt in range(1, 9):
    tag = f"rb3fix2{attempt}"
    m = hashlib.md5(open(paths["pptx"], "rb").read()).hexdigest()
    transcript = os.path.join(OUTDIR, f"slide_{ss}_judge_{tag}.txt")
    log = os.path.join(OUTDIR, f"slide_{ss}_judge_{tag}.log")
    cmd = ["timeout", "540", GATE, "python3", ANALYZE, "comparison",
           paths["orig"], paths["render"], "-p", ctx + "\n" + RULES,
           "--timeout", "420", "--rounds", "1", "--tries", "1",
           "--max-tokens", "32000", "--transcript", transcript]
    with open(log, "w") as fh:
        subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT)
    v = "NO_TRANSCRIPT"
    if os.path.exists(transcript):
        for line in reversed(open(transcript, errors="replace").read().splitlines()):
            mm = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", line, re.I)
            if mm:
                v = mm.group(1).upper()
                break
    row = {"slide": ss, "attempt": tag, "ts": time.strftime("%F %T"),
           "pptx_md5": m, "verdict": v, "transcript": transcript}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(row) + "\n")
    print(json.dumps(row), flush=True)
    if v in ("PASS", "FAIL"):
        break
    time.sleep(60)
