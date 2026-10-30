#!/usr/bin/env python3
"""Re-analysis wave for 10_nn_training_and_example.

Drives the image-analysis script directly (background task, no subagents) over
all 34 unique frames, through the namespace-local vision gate, and banks one
transcript per slide under _pool/audit/. Idempotent: slides with a valid banked
transcript are skipped. One retry on a hard-wall abort (W4 doctrine).
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

VIDEO = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
GATE = VIDEO + "/_pool/vision_gate.sh"
SCRIPT = "/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py"
OUT = VIDEO + "/_pool/audit"
PROMPT_FILE = VIDEO + "/_pool/audit_prompt.txt"
LOG = OUT + "/run.log"
SLOTS = 4


def log(msg):
    line = msg + "\n"
    with open(LOG, "a") as f:
        f.write(line)
    print(line, end="")


def valid(path):
    if not os.path.exists(path) or os.path.getsize(path) < 2500:
        return False
    with open(path, errors="replace") as f:
        t = f.read()
    return "## 1. VERBATIM TEXT" in t and "## 9. VERDICT" in t


def run_one(n):
    out = f"{OUT}/slide_{n:03d}.txt"
    img = f"{VIDEO}/unique_slides/slide_{n:03d}.jpg"
    if not os.path.exists(img):
        log(f"slide {n}: MISSING FRAME {img}")
        return f"{n}:missing"
    if valid(out):
        log(f"slide {n}: skip (banked valid transcript)")
        return f"{n}:skip"
    cmd = [
        GATE, "timeout", "540",
        "python3", SCRIPT, "analysis", img,
        "--view", f"Slide {n} — 'Neural Network Training and Example' lecture slide",
        "--capture", "960x540 CSS px, 1x scale, lecture video frame",
        "-p", open(PROMPT_FILE).read(),
        "--timeout", "420", "--rounds", "1", "--tries", "1",
        "--max-tokens", "24000",
    ]
    attempts = 0
    while attempts < 2:
        attempts += 1
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=600)
        except subprocess.TimeoutExpired:
            log(f"slide {n}: attempt {attempts} hard timeout 600s wrapper")
            continue
        with open(out, "ab") as f:
            pass
        with open(out, "w") as f:
            f.write(r.stdout.decode("utf-8", "replace"))
            if r.stderr:
                f.write("\n--- stderr ---\n")
                f.write(r.stderr.decode("utf-8", "replace"))
        if valid(out):
            log(f"slide {n}: attempt {attempts} OK rc={r.returncode} bytes={os.path.getsize(out)}")
            return f"{n}:ok"
        log(f"slide {n}: attempt {attempts} INVALID rc={r.returncode} bytes={os.path.getsize(out)}")
    return f"{n}:failed"


def main():
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    nums = [int(x) for x in only] if only else list(range(1, 35))
    log(f"=== audit wave start: {nums[0]}..{nums[-1]} slots={SLOTS} n={len(nums)}")
    with ThreadPoolExecutor(max_workers=SLOTS) as ex:
        results = list(ex.map(run_one, nums))
    log("=== audit wave done: " + " ".join(results))


if __name__ == "__main__":
    main()
