#!/usr/bin/env python3
"""Wave-3 judge for slide 005 with fresh transcript paths (avoids stale-transcript trap).
Same gated call as tools/judge_slides.py, transcript -> qa/rejudge2/slide_005_judge_w3_a{attempt}_{k}.txt
"""
import hashlib
import json
import os
import re
import subprocess
import time

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE = "/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh"
OUTDIR = os.path.join(BASE, "qa", "rejudge2")
BASE_RULES = open(os.path.join(BASE, "judge_prompt_active.txt")).read().strip()

CONTEXT = """VIEW: Slide {ss} — original lecture frame vs its PowerPoint recreation (SVM/kernels/QP lecture)
FACTS: the printed slide number is {num}. House chrome is MANDATORY in [2] and never a discrepancy.
Images are attached in this order: image 1 = ORIGINAL, image 2 = RECREATION.
List every discrepancy as: SEVERITY (BLOCKER|MAJOR|MINOR) — element — defect — confidence.
End with exactly one terminal line: FINAL VERDICT: PASS   or   FINAL VERDICT: FAIL
"""


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def verdict_of(path):
    if not os.path.exists(path):
        return "NO_TRANSCRIPT"
    for line in reversed(open(path, errors="replace").read().splitlines()):
        m = re.search(r"FINAL VERDICT:\s*(PASS|FAIL)", line, re.I)
        if m:
            return m.group(1).upper()
    return "INVALID_NO_VERDICT_LINE"


def main():
    ss = "005"
    paths = {"orig": os.path.join(BASE, "unique_slides", "slide_005.jpg"),
             "render": os.path.join(BASE, "recreated_pptx", "renders", "slide_005_recreated-1.png"),
             "pptx": os.path.join(BASE, "recreated_pptx", "slide_005_recreated.pptx")}
    m = md5(paths["pptx"])
    print("pptx md5:", m, flush=True)
    prompt = CONTEXT.format(ss=ss, num=5) + "\n" + BASE_RULES
    for attempt in range(1, 4):
        for k in range(2):
            out_k = os.path.join(OUTDIR, f"slide_{ss}_judge_w3_a{attempt}_{k}.txt")
            cmd = ["timeout", "2400", GATE, "python3", ANALYZE, "comparison",
                   paths["orig"], paths["render"], "-p", prompt,
                   "--timeout", "420", "--rounds", "1", "--tries", "1",
                   "--max-tokens", "32000", "--transcript", out_k]
            t0 = time.time()
            tail = subprocess.run(cmd, capture_output=True, text=True).stdout
            v = verdict_of(out_k)
            print(f"attempt {attempt} k{k}: {v} ({time.time()-t0:.0f}s) {out_k}", flush=True)
            row = {"slide": ss, "wave": "w3", "attempt": attempt, "k": k,
                   "ts": time.strftime("%F %T"), "pptx_md5": m, "verdict": v, "transcript": out_k}
            with open(os.path.join(OUTDIR, "ledger_w3.jsonl"), "a") as f:
                f.write(json.dumps(row) + "\n")
            if v in ("PASS", "FAIL"):
                print("terminal verdict:", v, flush=True)
                return
        print("attempt", attempt, "unresolved — sleeping 60s", flush=True)
        time.sleep(60)
    print("UNRESOLVED after 3 attempts", flush=True)


if __name__ == "__main__":
    main()
