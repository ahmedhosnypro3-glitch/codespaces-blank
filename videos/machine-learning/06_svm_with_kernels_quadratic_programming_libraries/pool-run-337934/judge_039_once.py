#!/usr/bin/env python3
# One-off judge for slide 039 at the CURRENT pptx md5, bypassing the ledger skip
# (the last banked row for 039 at this md5 is a stale-file FAIL; see judge_039_rb2.out).
# Mirrors tools/judge_slides.py run() exactly, but with fresh transcript names.
import hashlib, json, os, re, subprocess, sys, time

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE = "/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh"
OUTDIR = os.path.join(BASE, "qa", "rejudge2")
LEDGER = os.path.join(OUTDIR, "ledger.jsonl")
BASE_RULES = open(os.path.join(BASE, "judge_prompt_active.txt")).read().strip()
WALL = 2400
HTTP_TIMEOUT = 420
TAG = sys.argv[1] if len(sys.argv) > 1 else "rb"

CONTEXT = """VIEW: Slide {ss} — original lecture frame vs its PowerPoint recreation (SVM/kernels/QP lecture)
FACTS: the printed slide number is {num}. House chrome is MANDATORY in [2] and never a discrepancy.
Images are attached in this order: image 1 = ORIGINAL, image 2 = RECREATION.
List every discrepancy as: SEVERITY (BLOCKER|MAJOR|MINOR) — element — defect — confidence.
End with exactly one terminal line: FINAL VERDICT: PASS   or   FINAL VERDICT: FAIL
"""

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()

def verdict_of(p):
    if not os.path.exists(p):
        return "NO_TRANSCRIPT"
    for line in reversed(open(p, errors="replace").read().splitlines()):
        m = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", line, re.I)
        if m:
            return m.group(1).upper()
    return "INVALID_NO_VERDICT_LINE"

ss = "039"
pptx = os.path.join(BASE, "recreated_pptx", f"slide_{ss}_recreated.pptx")
orig = os.path.join(BASE, "unique_slides", f"slide_{ss}.jpg")
render = os.path.join(BASE, "recreated_pptx", "renders", f"slide_{ss}_recreated-1.png")
m = md5(pptx)
print("md5", m, flush=True)
prompt = CONTEXT.format(ss=ss, num=39) + "\n" + BASE_RULES

for attempt in range(1, 4):
    out_k = os.path.join(OUTDIR, f"slide_{ss}_judge_{TAG}_a{attempt}.txt")
    cmd = ["timeout", str(WALL), GATE, "python3", ANALYZE, "comparison",
           orig, render, "-p", prompt,
           "--timeout", str(HTTP_TIMEOUT), "--rounds", "1", "--tries", "1",
           "--max-tokens", "32000", "--transcript", out_k]
    log = os.path.join(OUTDIR, f"slide_{ss}_attempt_{TAG}_a{attempt}.log")
    t0 = time.time()
    with open(log, "w") as lf:
        proc = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT, text=True)
        try:
            proc.communicate(timeout=WALL + 120)
        except Exception:
            proc.kill()
    v = verdict_of(out_k)
    row = {"slide": ss, "attempt": attempt, "ts": time.strftime("%F %T"),
           "pptx_md5": m, "verdict": v, "transcript": out_k}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(row) + "\n")
    print(f"[{ss}] {v} (attempt {attempt}, {time.time()-t0:.0f}s) -> {out_k}", flush=True)
    if v in ("PASS", "FAIL"):
        sys.exit(0 if v == "PASS" else 2)
print("UNRESOLVED", flush=True)
sys.exit(3)
