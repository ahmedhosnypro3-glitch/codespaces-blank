#!/usr/bin/env python3
# Manual single-comparison judge for slide 048 with 429 backoff.
# Mirrors tools/judge_slides.py but writes a FRESH transcript and retries
# on 429/empty output up to 4 tries with 60s sleeps.
import hashlib, json, os, re, subprocess, sys, time

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE = "/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh"
OUTDIR = os.path.join(BASE, "qa", "rejudge2")
RULES = open(os.path.join(BASE, "judge_prompt_active.txt")).read().strip()
CONTEXT = """VIEW: Slide 048 — original lecture frame vs its PowerPoint recreation (SVM/kernels/QP lecture)
FACTS: the printed slide number is 48. House chrome is MANDATORY in [2] and never a discrepancy.
Images are attached in this order: image 1 = ORIGINAL, image 2 = RECREATION.
List every discrepancy as: SEVERITY (BLOCKER|MAJOR|MINOR) — element — defect — confidence.
End with exactly one terminal line: FINAL VERDICT: PASS   or   FINAL VERDICT: FAIL
"""

ss = "048"
paths = {"pptx": f"{BASE}/recreated_pptx/slide_{ss}_recreated.pptx",
         "orig": f"{BASE}/unique_slides/slide_{ss}.jpg",
         "render": f"{BASE}/recreated_pptx/renders/slide_{ss}_recreated-1.png"}
m = hashlib.md5(open(paths["pptx"], "rb").read()).hexdigest()
print("pptx_md5", m, flush=True)
prompt = CONTEXT + "\n" + RULES

for attempt in range(1, 5):
    out = os.path.join(OUTDIR, f"slide_{ss}_judge_manual_a{attempt}.txt")
    if os.path.exists(out):
        os.remove(out)
    cmd = ["timeout", "2400", GATE, "python3", ANALYZE, "comparison",
           paths["orig"], paths["render"], "-p", prompt,
           "--timeout", "420", "--rounds", "1", "--tries", "1",
           "--max-tokens", "32000", "--transcript", out]
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    tail = (r.stdout or "") + (r.stderr or "")
    print(f"attempt {attempt}: rc={r.returncode} {time.time()-t0:.0f}s tail={tail[-300:]!r}", flush=True)
    if os.path.exists(out):
        txt = open(out, errors="replace").read()
        vm = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", txt, re.I)
        if vm:
            v = vm.group(1).upper()
            row = {"slide": ss, "attempt": attempt, "ts": time.strftime("%F %T"),
                   "pptx_md5": m, "verdict": v, "transcript": out, "manual": True}
            with open(os.path.join(OUTDIR, "ledger.jsonl"), "a") as f:
                f.write(json.dumps(row) + "\n")
            print("VERDICT", v, "transcript", out, flush=True)
            sys.exit(0 if v == "PASS" else 2)
    if "429" in tail or "rate_limit" in tail:
        print("429 detected — sleep 60", flush=True)
        time.sleep(60)
    else:
        time.sleep(20)
print("UNRESOLVED after 4 attempts", flush=True)
sys.exit(1)
