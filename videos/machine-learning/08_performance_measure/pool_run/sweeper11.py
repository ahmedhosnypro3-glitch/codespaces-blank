#!/usr/bin/env python3
"""sweeper11.py — CLI shim for the 08_performance_measure certify-and-merge sweeper.

The actual loop lives in pool_run/sweeper11_loop.sh (self-contained: 60s rescan,
flock ledger rows, merge_final_deck.py update, mission.db scope done, and
original-first verify judges with 90-150s spacing and 429/no-verdict -> 300s
retry x8).

Subcommands:
  loop          — exec sweeper11_loop.sh (the loop; loops until 37/37)
  verify <n>    — ONE corroboration verify judge for slide n, guarded by a
                  non-blocking flock so parallel callers exit instead of
                  duplicating the vision call. Transcript:
                  recreated_pptx/qa/slideNNN/judge_verify_s11_<n>_try<k>.txt
  (no args)     — same as loop
"""
import os
import random
import subprocess
import sys
import time
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
REPO = Path("/home/codespace/ai_llm_slides")
LOG = NS / "pool_run" / "sweeper11.log"
LOCK = NS / "pool_run" / ".sweeper11_verify.lock"
PYBIN = "/home/codespace/.pyenv/versions/3.15.2/bin/python3"
GATE = str(REPO / "scripts" / "16_vision_gate.sh")
ANALYZE = str(REPO / ".agents" / "skills" / "image-analysis" / "scripts" / "analyze_image.py")
PROMPT = (NS / "pool_run" / "judge_prompt_template.txt").read_text()


def log(msg):
    line = f"[{time.strftime('%F %T')}] {msg}"
    with open(LOG, "a") as f:
        f.write(line + "\n")


def run_loop():
    os.chdir(NS)
    os.execvp("bash", ["bash", "pool_run/sweeper11_loop.sh"])


def verify(n):
    import fcntl
    d = NS / "recreated_pptx" / "qa" / f"slide{n:03d}"
    pptx = NS / "recreated_pptx" / f"slide_{n:03d}_recreated.pptx"
    orig = NS / "unique_slides" / f"slide_{n:03d}.jpg"
    if not orig.exists():
        c = sorted((NS / "unique_slides").glob(f"slide_{n:03d}*.jpg"))
        if not c:
            log(f"verify {n}: original frame missing — skip")
            return 1
        orig = c[0]
    renders = [r for r in d.glob("render_*.png")
               if pptx.exists() and r.stat().st_mtime >= pptx.stat().st_mtime]
    if not renders:
        log(f"verify {n}: no render at least as new as the pptx — skip")
        return 1
    render = max(renders, key=lambda r: r.stat().st_mtime)

    lf = open(LOCK, "a")
    try:
        fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        log(f"verify {n}: another sweeper-11 verify holds the lock — exit")
        return 0
    try:
        k = 1
        while (d / f"judge_verify_s11_{n}_try{k}.txt").exists():
            k += 1
        vt = d / f"judge_verify_s11_{n}_try{k}.txt"
        log(f"verify {n}: orig={orig.name} render={render.name} — sleeping 90-150s before judge")
        time.sleep(90 + random.randint(0, 60))
        for t in range(1, 9):
            log(f"verify {n}: corroboration attempt {t}/8 -> {vt.name}")
            with open(vt, "w") as tf:
                subprocess.run(
                    ["bash", GATE, "timeout", "540", PYBIN, ANALYZE, "comparison",
                     str(orig), str(render),
                     "--view", f"Slide {n} recreation — sweeper-11 corroboration read try {t} (original first, render second)",
                     "--capture", "IMG1=original lecture video frame (ground truth, read FIRST); IMG2=150dpi PNG render of the current PPTX recreation (read SECOND)",
                     "--thinking", "high", "--max-tokens", "65536",
                     "--timeout", "420", "--rounds", "1", "--tries", "1",
                     "-p", PROMPT],
                    cwd=REPO, stdout=tf, stderr=subprocess.STDOUT, timeout=600)
            v = subprocess.run([PYBIN, str(NS / "pool_run" / "verdict.py"), str(vt)],
                               capture_output=True, text=True).stdout.strip() or "NONE"
            log(f"verify {n}: attempt {t} rc verdict={v}")
            if v in ("PASS", "FAIL"):
                return 0 if v == "PASS" else 2
            log(f"verify {n}: no verdict — sleep 300s before retry")
            time.sleep(300)
        log(f"verify {n}: exhausted 8 tries without verdict")
        return 1
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)
        lf.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "verify" and len(args) > 1:
        sys.exit(verify(int(args[1])))
    run_loop()
