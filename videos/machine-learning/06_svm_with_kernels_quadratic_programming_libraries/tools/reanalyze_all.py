#!/usr/bin/env python3
# Re-analyze slide originals through the image-analysis script, via the shared vision
# gate. Background-job friendly: launch with nohup, poll the out dir for banked transcripts.
import argparse, os, subprocess, sys, time

BASE = "/home/codespace/ai_llm_slides"
NS = BASE + "/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ANALYZE = BASE + "/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE = BASE + "/scripts/16_vision_gate.sh"
OUT = NS + "/qa/reanalysis2"
PROMPT = NS + "/analysis_prompt_v2.txt"

p = argparse.ArgumentParser()
p.add_argument("--start", type=int, required=True)
p.add_argument("--end", type=int, required=True)
p.add_argument("--concurrency", type=int, default=6)
p.add_argument("--timeout", type=int, default=420)
p.add_argument("--wall", type=int, default=780)
p.add_argument("--rounds", type=int, default=1)
p.add_argument("--tries", type=int, default=1)
p.add_argument("--max-tokens", type=int, default=24000)
a = p.parse_args()

os.makedirs(OUT, exist_ok=True)
RULES = open(PROMPT).read().strip()

def cmd_for(n):
    ss = f"{n:03d}"
    # The wall covers BOTH waiting for a shared gate slot and the request itself, so it
    # must exceed gate_wait_estimate + (rounds*tries*timeout). Never infer from mtimes.
    return ["timeout", str(a.wall), GATE, "python3", ANALYZE, "analysis",
            NS + f"/qa/rejudge2/orig_png/slide_{ss}.png", "-p", RULES,
            "--view", f"original lecture slide {n} of 55 (SVM/kernels/QP math lecture)",
            "--capture", "960x540 CSS px, scale 1, app=lecture-video-frame",
            "--timeout", str(a.timeout), "--rounds", str(a.rounds),
            "--tries", str(a.tries), "--max-tokens", str(a.max_tokens),
            "--transcript", OUT + f"/slide_{ss}_analysis.txt"]

def done(n):
    d = OUT + f"/slide_{n:03d}_analysis.txt"
    if not os.path.exists(d) or os.path.getsize(d) < 4000:
        return False
    body = open(d, errors="replace").read()
    need = [f"{i}." for i in range(1, 12)]
    return all(s in body for s in need)

nums = [n for n in range(a.start, a.end + 1) if not done(n)]
print(f"todo={len(nums)} of range {a.start}-{a.end} (concurrency={a.concurrency})",
      flush=True)
alive, i = {}, 0
while i < len(nums) or alive:
    while len(alive) < a.concurrency and i < len(nums):
        n = nums[i]
        alive[n] = subprocess.Popen(cmd_for(n), stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True)
        print(f"[{n:03d}] launched {time.strftime('%F %T')}", flush=True)
        i += 1
        time.sleep(3)
    for n in [n for n, q in alive.items() if q.poll() is not None]:
        q = alive.pop(n)
        tail = q.communicate()[0] or ""
        with open(OUT + f"/slide_{n:03d}_driver.log", "w") as f:
            f.write(tail)
        sz = os.path.getsize(OUT + f"/slide_{n:03d}_analysis.txt") \
            if os.path.exists(OUT + f"/slide_{n:03d}_analysis.txt") else 0
        print(f"[{n:03d}] rc={q.returncode} banked_bytes={sz} {time.strftime('%F %T')}",
              flush=True)
    if not alive:
        break
    time.sleep(4)
print("DONE", flush=True)
