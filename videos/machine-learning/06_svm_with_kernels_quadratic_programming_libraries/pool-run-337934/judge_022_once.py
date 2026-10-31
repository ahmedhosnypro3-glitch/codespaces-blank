#!/usr/bin/env python3
"""Force one fresh judge attempt for slide 022 (driver skips FAIL-at-md5 rows)."""
import hashlib, json, os, re, subprocess, sys, time

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE = "/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh"
OUTDIR = os.path.join(BASE, "qa", "rejudge2")
LEDGER = os.path.join(OUTDIR, "ledger.jsonl")
RULES = open(os.path.join(BASE, "judge_prompt_active.txt")).read().strip()

CONTEXT = """VIEW: Slide {ss} — original lecture frame vs its PowerPoint recreation (SVM/kernels/QP lecture)
FACTS: the printed slide number is {num}. House chrome is MANDATORY in [2] and never a discrepancy.
Images are attached in this order: image 1 = ORIGINAL, image 2 = RECREATION.
List every discrepancy as: SEVERITY (BLOCKER|MAJOR|MINOR) — element — defect — confidence.
End with exactly one terminal line: FINAL VERDICT: PASS   or   FINAL VERDICT: FAIL
"""

ss, num = "022", 22
paths = {"pptx": f"{BASE}/recreated_pptx/slide_{ss}_recreated.pptx",
         "orig": f"{BASE}/unique_slides/slide_{ss}.jpg",
         "render": f"{BASE}/recreated_pptx/renders/slide_{ss}_recreated-1.png"}
m = hashlib.md5(open(paths["pptx"], "rb").read()).hexdigest()
print("pptx md5", m, flush=True)
prompt = CONTEXT.format(ss=ss, num=num) + "\n" + RULES

for attempt in range(1, 4):
    out = os.path.join(OUTDIR, f"slide_{ss}_judge_fix{attempt}.txt")
    log = os.path.join(OUTDIR, f"slide_{ss}_judge_fix{attempt}.log")
    cmd = ["timeout", "2400", GATE, "python3", ANALYZE, "comparison",
           paths["orig"], paths["render"], "-p", prompt,
           "--timeout", "420", "--rounds", "1", "--tries", "1",
           "--max-tokens", "32000", "--transcript", out]
    with open(log, "w") as lf:
        p = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, text=True)
    tail = open(log, errors="replace").read()
    v = "NO_TRANSCRIPT"
    if os.path.exists(out):
        for line in reversed(open(out, errors="replace").read().splitlines()):
            mm = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", line, re.I)
            if mm:
                v = mm.group(1).upper()
                break
    row = {"slide": ss, "attempt": f"fix{attempt}", "ts": time.strftime("%F %T"),
           "pptx_md5": m, "verdict": v, "transcript": out}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(row) + "\n")
    print(f"[022] fix{attempt} {v} (transcript {out}, {os.path.getsize(out) if os.path.exists(out) else 0} bytes)", flush=True)
    if v in ("PASS", "FAIL") and os.path.getsize(out) > 5000:
        break
    print("[022] transcript stale/short or infra error — sleep 60 and retry", flush=True)
    time.sleep(60)
