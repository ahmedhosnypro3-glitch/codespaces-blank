#!/usr/bin/env python3
"""Certify-and-merge sweeper for 08_performance_measure (2026-10-31).

Loop (from namespace root):
  1. Scan recreated_pptx/qa/slideNNN/ for slides with BOTH a judge_attempt_*.txt
     and a judge_verify_*.txt containing FINAL VERDICT: PASS, not yet certified
     in final_deck_ledger.json. Skip a slide whose NEWEST verify transcript
     (by mtime) is FAIL — it is re-opened.
  2. For each such slide: flock-append a row to pool_run/verification_ledger.md
     (skip if a row for that slide exists), then
     `python3 pool_run/merge_final_deck.py update N recreated_pptx/slide_NNN_recreated.pptx 08-performance_final.pptx`
     and `sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-N';"`.
  3. For attempt-PASS slides lacking a verify PASS (and not re-opened), run the
     corroboration verify judge per REBUILD_BRIEF.md: frozen template (-p),
     NEWEST render (ls -t render_*.png | head -1), IMAGE 1 = ORIGINAL,
     from the repo root:
       timeout 540 python3 .agents/skills/image-analysis/scripts/analyze_image.py \
         comparison <orig> <render> --thinking high --max-tokens 65536 \
         --timeout 420 --rounds 1 --tries 1 -p <template>
     sleep 90-150s before each call; on 429 sleep 300s and retry up to 8x.
     Unique transcript name per call.
  4. Sleep 60s, rescan, until 37/37 certified.

Never deletes evidence; never writes outside the namespace; flock on ledger.
"""
import fcntl
import glob
import json
import os
import random
import re
import subprocess
import sys
import time

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
REPO = "/home/codespace/ai_llm_slides"
LOG = os.path.join(NS, "pool_run", "sweeper_final_cert_loop.log")
LEDGER = os.path.join(NS, "pool_run", "verification_ledger.md")
PROMPT = os.path.join(NS, "pool_run", "judge_prompt_template.txt")
DB = os.path.join(NS, "pool_run", "mission.db")

sys.path.insert(0, os.path.join(NS, "pool_run"))
from verdict import verdict  # noqa: E402

os.chdir(NS)


def log(msg):
    line = f"[{time.strftime('%F %T')}] {msg}"
    with open(LOG, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


def certified_pages():
    with open(os.path.join(NS, "final_deck_ledger.json")) as f:
        d = json.load(f)
    return {p["page"] for p in d["pages"] if p["status"] == "certified"}


def qa(n):
    return os.path.join(NS, "recreated_pptx", "qa", f"slide{n:03d}")


def pass_files(qdir, kind):
    out = []
    for p in glob.glob(os.path.join(qdir, f"judge_{kind}_*.txt")):
        try:
            if verdict(p) == "PASS":
                out.append(p)
        except OSError:
            pass
    return sorted(out)


def newest_verify(qdir):
    files = glob.glob(os.path.join(qdir, "judge_verify_*.txt"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def newest_render(qdir):
    files = glob.glob(os.path.join(qdir, "render_*.png"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def original_frame(n):
    padded = f"{n:03d}"
    cands = [os.path.join(NS, "unique_slides", f"slide_{padded}.jpg")]
    cands += sorted(glob.glob(os.path.join(NS, "unique_slides", f"slide_{padded}-*.jpg")))
    for c in cands:
        if os.path.isfile(c):
            return c
    return None


def ledger_has_row(n):
    try:
        with open(LEDGER) as f:
            for line in f:
                if not line.startswith("|"):
                    continue
                cell = line.split("|")[1].strip()
                if cell.isdigit() and int(cell) == n:
                    return True
    except OSError:
        pass
    return False


def append_ledger(n, att, ver):
    rel = lambda p: os.path.relpath(p, NS)
    row = (f"| {n} | {rel(att)} | {rel(ver)} | "
           f"PASS / PASS (original-first dual-read; certify-merge sweeper {time.strftime('%Y-%m-%d')}) | "
           f"— | certified=yes | |\n")
    with open(LEDGER, "a") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.write(row)
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def merge_update(n):
    r = subprocess.run(
        ["python3", "pool_run/merge_final_deck.py", "update", str(n),
         f"recreated_pptx/slide_{n:03d}_recreated.pptx", "08-performance_final.pptx"],
        cwd=NS, capture_output=True, text=True, timeout=600)
    log(f"slide {n}: merge update rc={r.returncode} {r.stdout.strip()} {r.stderr.strip()[:300]}")
    return r.returncode == 0


def db_done(n):
    for _ in range(12):
        r = subprocess.run(
            ["sqlite3", "pool_run/mission.db",
             f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
            cwd=NS, capture_output=True, text=True)
        if r.returncode == 0:
            log(f"slide {n}: mission.db scope slide-{n} -> done")
            return True
        if "locked" in r.stderr.lower():
            time.sleep(5)
            continue
        log(f"slide {n}: mission.db error: {r.stderr.strip()[:200]}")
        return False
    log(f"slide {n}: mission.db locked after retries")
    return False


def certify(n, att, ver):
    if not ledger_has_row(n):
        append_ledger(n, att, ver)
        log(f"slide {n}: ledger row appended (attempt={os.path.basename(att)}, verify={os.path.basename(ver)})")
    else:
        log(f"slide {n}: ledger row already exists, append skipped")
    merge_update(n)
    db_done(n)


def verify_in_flight(n):
    pat = f"slide{n:03d}|slide_{n:03d}"
    r = subprocess.run(["pgrep", "-f", pat], capture_output=True, text=True)
    my_pid = os.getpid()
    for pid in r.stdout.split():
        if int(pid) == my_pid:
            continue
        try:
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                cmd = f.read().replace(b"\0", b" ").decode(errors="replace")
        except OSError:
            continue
        if "analyze_image" in cmd or "judge_verify" in cmd or "judge_attempt" in cmd or "verify" in cmd:
            return True
    return False


def run_verify(n):
    qdir = qa(n)
    render = newest_render(qdir)
    orig = original_frame(n)
    if not render or not orig:
        log(f"slide {n}: NEEDVERIFY but no render or no original — skip")
        return
    if verify_in_flight(n):
        log(f"slide {n}: another verify/judge process in flight — skip this pass")
        return
    tpath = os.path.join(qdir, f"judge_verify_cert{int(time.time())}_s{n}.txt")
    while os.path.exists(tpath):
        tpath = tpath.replace(".txt", f"_{random.randint(1000, 9999)}.txt")
    with open(PROMPT) as f:
        prompt = f.read()
    rel = lambda p: os.path.relpath(p, REPO)
    cmd = ["timeout", "540", "python3",
           ".agents/skills/image-analysis/scripts/analyze_image.py",
           "comparison", rel(orig), rel(render),
           "--thinking", "high", "--max-tokens", "65536",
           "--timeout", "420", "--rounds", "1", "--tries", "1",
           "-p", prompt]
    s = random.randint(90, 150)
    log(f"slide {n}: sleeping {s}s then verify vs {os.path.basename(render)} -> {os.path.basename(tpath)}")
    time.sleep(s)
    tries = 0
    while True:
        tries += 1
        with open(tpath, "a") as out:
            r = subprocess.run(cmd, cwd=REPO, stdout=out, stderr=subprocess.STDOUT)
        with open(tpath, "a") as out:
            out.write(f"exit={r.returncode}\n")
        with open(tpath, errors="replace") as f:
            body = f.read()
        if re.search(r"429|rate.?limit|too many requests", body, re.I):
            if tries >= 8:
                log(f"slide {n}: 429 after 8 tries, giving up this pass ({os.path.basename(tpath)})")
                return
            log(f"slide {n}: 429 detected (try {tries}) — sleep 300 retry")
            time.sleep(300)
            continue
        break
    v = verdict(tpath) if os.path.exists(tpath) else "NONE"
    log(f"slide {n}: verify verdict={v} tries={tries} transcript={os.path.basename(tpath)}")


def scan():
    cert = certified_pages()
    dual, needverify, reopened = [], [], []
    for n in range(1, 38):
        if n in cert:
            continue
        qdir = qa(n)
        if not os.path.isdir(qdir):
            continue
        nv = newest_verify(qdir)
        if nv and verdict(nv) == "FAIL":
            reopened.append(n)
            continue
        att = pass_files(qdir, "attempt")
        ver = pass_files(qdir, "verify")
        if att and ver:
            dual.append((n, att[-1], ver[-1]))
        elif att and not ver:
            needverify.append((n, att[-1]))
    return cert, dual, needverify, reopened


def main():
    log("sweeper_final_cert_loop start")
    while True:
        cert, dual, needverify, reopened = scan()
        log(f"scan: certified={len(cert)}/37 dual={[n for n, _, _ in dual]} "
            f"needverify={[n for n, _ in needverify]} reopened(skip)={reopened}")
        if len(cert) == 37:
            log("37/37 certified — sweeper exit")
            return 0
        for n, att, ver in dual:
            if n in certified_pages():
                continue
            log(f"slide {n}: DUAL PASS, certifying (attempt={os.path.basename(att)}, verify={os.path.basename(ver)})")
            certify(n, att, ver)
        for n, att in needverify:
            if n in certified_pages():
                continue
            nv = newest_verify(qa(n))
            if nv and verdict(nv) == "FAIL":
                continue
            run_verify(n)
        time.sleep(60)


if __name__ == "__main__":
    sys.exit(main())
