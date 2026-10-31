#!/usr/bin/env python3
"""Certify-and-merge sweeper loop for 08_performance_measure (2026-10-31).

Each iteration:
  1. Scan recreated_pptx/qa/slide*/ for slides with BOTH a judge_attempt_*.txt
     and a judge_verify_*.txt ending FINAL VERDICT: PASS but not certified in
     final_deck_ledger.json -> flock-append a row to pool_run/verification_ledger.md
     (skip if a non-superseded PASS row already exists), then
     `python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx`
     from the namespace root, then sqlite3 mission.db scope done.
  2. For attempt-PASS slides lacking a verify PASS: run the corroboration judge
     per REBUILD_BRIEF.md (frozen judge template -p, IMAGE 1 = original,
     IMAGE 2 = newest render_*.png), sleeping 90-150s before the call;
     on 429 sleep 300s and retry up to 8x. Unique transcript names.
  3. Sleep 60s and rescan until 37/37 certified.

Run from namespace root:  python3 pool_run/sweeper_cm_loop.py
"""
import fcntl
import json
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path

NS = Path(__file__).resolve().parent.parent
REPO = NS.parent.parent.parent
QA = NS / "recreated_pptx" / "qa"
PPTX_DIR = NS / "recreated_pptx"
LEDGER_JSON = NS / "final_deck_ledger.json"
VLEDGER = NS / "pool_run" / "verification_ledger.md"
MISSION_DB = NS / "pool_run" / "mission.db"
PROMPT_FILE = NS / "pool_run" / "judge_prompt_template.txt"
LOG = NS / "pool_run" / "sweeper_cm_loop.log"
PYBIN = "/home/codespace/.pyenv/versions/3.15.2/bin/python3"
GATE = REPO / "scripts" / "16_vision_gate.sh"
ANALYZE = REPO / ".agents" / "skills" / "image-analysis" / "scripts" / "analyze_image.py"


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"[{time.strftime('%F %T')}] {msg}\n")


def verdict(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return "NONE"
    hits = [m.start() for m in re.finditer(r"FINAL\s+VERDICT", text, re.I)]
    for start in reversed(hits):
        tail = text[start:]
        m = re.match(r"FINAL\s+VERDICT[^A-Za-z]{0,8}?\*{0,2}\s*(PASS|FAIL)", tail, re.I)
        if not m:
            continue
        word = m.group(1).upper()
        if word == "PASS" and re.match(r"\W*or\W*FAIL", tail[m.end():], re.I):
            continue
        return word
    return "NONE"


def qa_dir(n):
    d = QA / f"slide{n:03d}"
    return d if d.is_dir() else None


def original(n):
    padded = f"{n:03d}"
    hits = sorted((NS / "unique_slides").glob(f"slide_{padded}.jpg")) or \
        sorted((NS / "unique_slides").glob(f"slide_{padded}-*.jpg"))
    return hits[0] if hits else None


def pass_files(d, kind):
    out = []
    for f in sorted(d.glob(f"judge_{kind}_*.txt")):
        if verdict(f) == "PASS":
            out.append(f)
    return out


def certified_set():
    d = json.loads(LEDGER_JSON.read_text())
    return {p["page"] if "page" in p else p["slide_num"]
            for p in d["pages"] if p["status"] == "certified"}


def ledger_pass_row_exists(n):
    with open(VLEDGER, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.seek(0)
            for line in f:
                m = re.match(r"\|\s*(\d+)\s*\|", line)
                if m and int(m.group(1)) == n and "superseded" not in line:
                    cols = [c.strip() for c in line.split("|")]
                    v = cols[4] if len(cols) > 4 else ""
                    if "PASS" in v and "FAIL" not in v:
                        return True
            return False
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def append_ledger_row(n, att, ver):
    with open(VLEDGER, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.seek(0)
            for line in f:
                m = re.match(r"\|\s*(\d+)\s*\|", line)
                if m and int(m.group(1)) == n and "superseded" not in line:
                    cols = [c.strip() for c in line.split("|")]
                    v = cols[4] if len(cols) > 4 else ""
                    if "PASS" in v and "FAIL" not in v:
                        return False
            f.write(
                f"| {n} | {att.relative_to(NS)} | {ver.relative_to(NS)} | "
                f"PASS / PASS (original-first dual-read; sweeper-cm) | — | yes | |\n"
            )
            return True
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def merge_update(n):
    pptx = PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
    if not pptx.exists():
        log(f"slide {n}: pptx missing, skip merge")
        return False
    for _ in range(6):
        r = subprocess.run(
            ["python3", "pool_run/merge_final_deck.py", "update", str(n),
             f"recreated_pptx/slide_{n:03d}_recreated.pptx", "08-performance_final.pptx"],
            cwd=NS, capture_output=True, text=True)
        if r.returncode == 0:
            log(f"slide {n} merge update ok")
            return True
        log(f"slide {n} merge update rc={r.returncode}: {r.stderr.strip()[:200]} — retry")
        time.sleep(5)
    return False


def db_done(n):
    for _ in range(6):
        r = subprocess.run(
            ["sqlite3", "pool_run/mission.db",
             f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
            cwd=NS, capture_output=True, text=True)
        if r.returncode == 0:
            log(f"slide {n} mission.db scope done")
            return True
        time.sleep(5)
    log(f"slide {n} mission.db UPDATE kept failing")
    return False


def certify(n, att, ver):
    if ledger_pass_row_exists(n):
        log(f"slide {n}: PASS ledger row already present")
    else:
        appended = append_ledger_row(n, att, ver)
        log(f"slide {n}: ledger row {'appended' if appended else 'already present'} "
            f"(att={att.name}, ver={ver.name})")
    if not merge_update(n):
        return False
    ok = n in certified_set()
    log(f"slide {n} certified in final_deck_ledger.json: {ok}")
    db_done(n)
    return ok


def run_verify(n):
    d = qa_dir(n)
    orig = original(n)
    if d is None or orig is None:
        log(f"slide {n}: qa dir or original missing — skip verify")
        return
    renders = sorted(d.glob("render_*.png"), key=os.path.getmtime)
    if not renders:
        log(f"slide {n}: no render_*.png — skip verify")
        return
    render = renders[-1]
    transcript = d / f"judge_verify_swcm_{int(time.time())}_s{n}.txt"
    prompt = PROMPT_FILE.read_text()
    s = random.randint(90, 150)
    log(f"slide {n}: sleeping {s}s before verify vs {render.name} -> {transcript.name}")
    time.sleep(s)
    for i in range(1, 9):
        log(f"slide {n}: verify attempt {i}/8 (timeout 540, IMG1={orig.name}, IMG2={render.name})")
        with open(transcript, "w") as tf:
            r = subprocess.run(
                ["bash", str(GATE), "timeout", "540", PYBIN, str(ANALYZE), "comparison",
                 str(orig), str(render),
                 "--thinking", "high", "--max-tokens", "65536", "--timeout", "420",
                 "--rounds", "1", "--tries", "1", "-p", prompt],
                cwd=REPO, stdout=tf, stderr=subprocess.STDOUT)
        rc = r.returncode
        v = verdict(transcript)
        log(f"slide {n}: verify attempt {i} rc={rc} verdict={v} transcript={transcript.name}")
        if v in ("PASS", "FAIL"):
            return
        body = transcript.read_text(errors="replace")
        if re.search(r"429|rate.?limit|too many requests", body, re.I):
            if i >= 8:
                log(f"slide {n}: 429 after 8 tries, give up this pass")
                return
            log(f"slide {n}: 429 detected — sleep 300s retry")
            time.sleep(300)
        else:
            time.sleep(60)
    log(f"slide {n}: verify exhausted 8 attempts without verdict")


def scan():
    certified = certified_set()
    cands, needverify = [], []
    for n in range(1, 38):
        d = qa_dir(n)
        if d is None:
            continue
        att = pass_files(d, "attempt")
        ver = pass_files(d, "verify")
        if not att:
            continue
        if ver and n not in certified:
            cands.append((n, att[-1], ver[-1]))
        if not ver:
            needverify.append(n)
    return cands, needverify, certified


def main():
    log("sweeper_cm_loop start")
    it = 0
    while True:
        it += 1
        cands, needverify, certified = scan()
        log(f"iteration {it}: certified={len(certified)}/37 cands={[n for n,_,_ in cands]} needverify={needverify}")
        if len(certified) >= 37:
            log("37/37 certified — sweeper exit")
            return 0
        for n, att, ver in cands:
            certify(n, att, ver)
        for n in needverify:
            run_verify(n)
        log(f"iteration {it}: sleeping 60s")
        time.sleep(60)


if __name__ == "__main__":
    sys.exit(main())
