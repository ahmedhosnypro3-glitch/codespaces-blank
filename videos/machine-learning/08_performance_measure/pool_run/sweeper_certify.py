#!/usr/bin/env python3
"""Certify-and-merge sweeper for 08_performance_measure.

Loop until all 37 pages are status=certified in final_deck_ledger.json:
  1. Scan recreated_pptx/qa/slide*/ for slides with BOTH a judge_attempt_*
     and a judge_verify_* whose FINAL VERDICT is PASS (verdict.py semantics)
     that are not yet certified -> flock-append a row to
     pool_run/verification_ledger.md, run merge_final_deck.py update N ...,
     and set mission.db scope slide-N done.
  2. If a slide's corroboration read (judge_verify PASS) is missing, run the
     REBUILD_BRIEF judge command (original first) through the vision gate to
     produce it; same for a missing attempt PASS. Sleep 90-150s before each
     call; on 429 sleep 300s and retry up to 8x. Unique transcript filenames.
  3. Sleep 60s and rescan.
"""
import fcntl
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
REPO = Path("/home/codespace/ai_llm_slides")
PYBIN = "/home/codespace/.pyenv/versions/3.15.2/bin/python3"
QA = NS / "recreated_pptx" / "qa"
PPTX_DIR = NS / "recreated_pptx"
LEDGER_JSON = NS / "final_deck_ledger.json"
VLEDGER = NS / "pool_run" / "verification_ledger.md"
DB = NS / "pool_run" / "mission.db"
PROMPT = NS / "pool_run" / "judge_prompt_template.txt"
LOG = NS / "pool_run" / "sweeper_certify.log"

sys.path.insert(0, str(NS / "pool_run"))
import verdict as verdict_mod  # noqa: E402


def log(msg):
    line = f"[{time.strftime('%F %T')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def certified_set():
    d = json.load(open(LEDGER_JSON))
    return {p["slide_num"] for p in d["pages"] if p["status"] == "certified"}


def qa_dir(n):
    best = None
    for name in (f"slide{n:03d}", f"slide{n}", f"slide_{n:03d}"):
        d = QA / name
        if d.is_dir():
            score = len(list(d.glob("judge_*.txt")))
            if best is None or score > best[0]:
                best = (score, d)
    return best[1] if best else QA / f"slide{n:03d}"


def original_for(n):
    padded = f"{n:03d}"
    for f in sorted((NS / "unique_slides").glob(f"slide_{padded}*.jpg")):
        return f
    return None


def pass_files(d, pattern):
    out = []
    for f in sorted(d.glob(pattern)):
        try:
            if verdict_mod.verdict(str(f)) == "PASS":
                out.append(f)
        except OSError:
            pass
    return out


def recent_activity(d, minutes=20):
    cutoff = time.time() - minutes * 60
    for f in d.glob("judge_*.txt*"):
        try:
            if f.stat().st_mtime > cutoff:
                return True
        except OSError:
            pass
    return False


def scan():
    certified = certified_set()
    per_slide = {}  # n -> (dir, attempt PASS list, verify PASS list)
    for d in sorted(QA.iterdir()):
        if not d.is_dir():
            continue
        m = re.match(r"slide_?(\d+)$", d.name)
        if not m:
            continue
        n = int(m.group(1))
        if n < 1 or n > 37 or n in certified:
            continue
        if not (PPTX_DIR / f"slide_{n:03d}_recreated.pptx").exists():
            continue
        att = pass_files(d, "judge_attempt_*.txt")
        ver = pass_files(d, "judge_verify_*.txt")
        prev = per_slide.get(n)
        # Prefer the dir that carries evidence (attempt PASS, then any judge files).
        def score(att_l, ver_l, d):
            return (len(att_l), len(ver_l), len(list(d.glob("judge_*.txt"))))
        if prev is None or score(att, ver, d) > score(prev[1], prev[2], prev[0]):
            per_slide[n] = (d, att, ver)
    both, need_verify, need_attempt = [], [], []
    for n in sorted(per_slide):
        d, att, ver = per_slide[n]
        if att and ver:
            both.append((n, att[-1], ver[-1]))
        else:
            if not att:
                need_attempt.append(n)
            if not ver:
                need_verify.append(n)
    return certified, both, need_attempt, need_verify


def ledger_append(row):
    with open(VLEDGER, "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(row + "\n")
        f.flush()
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def merge_update(n):
    r = subprocess.run(
        ["python3", "pool_run/merge_final_deck.py", "update", str(n),
         f"recreated_pptx/slide_{n:03d}_recreated.pptx", "08-performance_final.pptx"],
        cwd=NS, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        log(f"slide {n}: merge update FAILED rc={r.returncode} {r.stderr[-300:]}")
        return False
    log(f"slide {n}: merge update ok ({r.stdout.strip()})")
    return True


def db_done(n):
    for attempt in range(10):
        r = subprocess.run(
            ["sqlite3", str(DB), f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
            capture_output=True, text=True)
        if r.returncode == 0:
            log(f"slide {n}: mission.db scope slide-{n} set done")
            return True
        if "locked" in (r.stderr or ""):
            time.sleep(5)
            continue
        log(f"slide {n}: sqlite error: {r.stderr.strip()}")
        return False
    log(f"slide {n}: sqlite kept failing (locked)")
    return False


def certify(n, att, ver):
    row = (f"| {n} | {att.relative_to(NS)} | {ver.relative_to(NS)} | "
           f"PASS / PASS (original-first dual-read) | | certified=yes | "
           f"sweeper certify-and-merge |")
    ledger_append(row)
    if merge_update(n):
        db_done(n)


def render_fresh(n, tag):
    d = qa_dir(n)
    r = subprocess.run(["bash", str(PPTX_DIR / "render_slide.sh"), str(n), tag],
                       capture_output=True, text=True, timeout=400)
    render = d / f"render_{tag}.png"
    if r.returncode != 0 or not render.exists():
        log(f"slide {n}: fresh render FAILED rc={r.returncode} {r.stderr[-200:]}")
        return None
    log(f"slide {n}: fresh render {render.name}")
    return render


def judge_call(n, kind, tag):
    """Run the REBUILD_BRIEF judge command, original first. kind=attempt|verify."""
    d = qa_dir(n)
    orig = original_for(n)
    if orig is None:
        log(f"slide {n}: original frame not found — skip")
        return None
    render = render_fresh(n, tag)
    if render is None:
        return None
    transcript = d / f"judge_{kind}_sweep_{tag}.txt"
    if transcript.exists():
        transcript = d / f"judge_{kind}_sweep_{tag}_{int(time.time())}.txt"
    sleep_s = random.randint(90, 150)
    log(f"slide {n}: sleeping {sleep_s}s before {kind} judge call")
    time.sleep(sleep_s)
    prompt = PROMPT.read_text()
    cmd = ["bash", "scripts/16_vision_gate.sh", "timeout", "540", PYBIN,
           ".agents/skills/image-analysis/scripts/analyze_image.py", "comparison",
           str(orig), str(render),
           "--thinking", "high", "--max-tokens", "65536",
           "--timeout", "420", "--rounds", "1", "--tries", "1",
           "--transcript", str(transcript), "-p", prompt]
    for i in range(1, 9):
        try:
            r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, timeout=900)
            out = (r.stdout or "") + (r.stderr or "")
            rc = r.returncode
        except subprocess.TimeoutExpired as e:
            rc = -1
            out = ((e.stdout or b"") + (e.stderr or b"")).decode("utf-8", "replace") if isinstance(e.stdout, bytes) else ((e.stdout or "") + (e.stderr or ""))
            log(f"slide {n}: {kind} call exceeded outer timeout (try {i}/8)")
        if "429" in out:
            log(f"slide {n}: {kind} call hit 429 (try {i}/8) — sleep 300s")
            time.sleep(300)
            continue
        if rc != 0:
            log(f"slide {n}: {kind} call rc={rc} (try {i}/8) tail: {out[-300:]}")
            if i < 8:
                time.sleep(60)
                continue
            return None
        v = verdict_mod.verdict(str(transcript)) if transcript.exists() else "NONE"
        log(f"slide {n}: {kind} call done, transcript={transcript.relative_to(NS)} verdict={v}")
        return transcript if v == "PASS" else None
    return None


def main():
    log("sweeper start")
    idle_rounds = 0
    while True:
        certified, both, need_attempt, need_verify = scan()
        log(f"scan: certified={len(certified)}/37 both-PASS-uncertified={[n for n, _, _ in both]} "
            f"need_verify={need_verify} need_attempt={need_attempt}")
        for n, att, ver in both:
            certify(n, att, ver)
        certified = certified_set()
        if len(certified) >= 37:
            log("ALL 37 CERTIFIED — sweeper done")
            return
        # Gateway call only when a read is missing and no other lane is active
        # on that slide's QA dir recently.
        target = None
        kind = None
        for n in need_verify:
            if not recent_activity(qa_dir(n)):
                target, kind = n, "verify"
                break
        if target is None:
            for n in need_attempt:
                if not recent_activity(qa_dir(n)):
                    target, kind = n, "attempt"
                    break
        if target is not None:
            tag = f"{int(time.time())}"
            judge_call(target, kind, tag)
        else:
            idle_rounds += 1
            log(f"no gateway target this round (idle round {idle_rounds})")
        time.sleep(60)


if __name__ == "__main__":
    main()
