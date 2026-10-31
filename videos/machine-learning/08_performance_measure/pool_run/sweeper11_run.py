#!/usr/bin/env python3
"""Sweeper #11 (python) — certify-and-merge loop for 08_performance_measure.

loop: every 60s rescan qa dirs; dual-PASS uncertified slides get a flock-appended
verification_ledger.md row, merge_final_deck.py update into 08-performance_final.pptx,
and mission.db slide-N done; attempt-PASS slides without a verify PASS get a detached
verify judge (fresh render if needed, sleep 90-150s, original-first, 429/no-verdict =>
sleep 300s, up to 8 tries, unique judge_verify_s11_<n>_try<k>.txt transcripts).
Exits at 37/37 certified.
"""
import fcntl
import json
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

NS = Path("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
REPO = NS.parent.parent.parent
QA = NS / "recreated_pptx" / "qa"
PPTX_DIR = NS / "recreated_pptx"
LEDGER_JSON = NS / "final_deck_ledger.json"
VLEDGER = NS / "pool_run" / "verification_ledger.md"
MISSION_DB = NS / "pool_run" / "mission.db"
PROMPT_FILE = NS / "pool_run" / "judge_prompt_template.txt"
LOG = NS / "pool_run" / "sweeper11_run.log"
TMP = NS / "pool_run" / "tmp"
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
        m = re.match(r"FINAL\s+VERDICT[^A-Za-z]{0,8}?(PASS|FAIL)", text[start:], re.I)
        if not m:
            continue
        word = m.group(1).upper()
        if word == "PASS" and re.match(r"\W*or\W*FAIL", text[start:][m.end():], re.I):
            continue
        return word
    return "NONE"


def qa_dir(n):
    for name in (f"slide{n:03d}", f"slide{n}", f"slide_{n:03d}"):
        d = QA / name
        if d.is_dir():
            return d
    return None


def original(n):
    padded = f"{n:03d}"
    for pat in (f"slide_{padded}.jpg", f"slide_{padded}-*.jpg"):
        hits = sorted((NS / "unique_slides").glob(pat))
        if hits:
            return hits[0]
    return None


def pass_files(d, kind):
    return [f for f in sorted(d.glob(f"judge_{kind}_*.txt")) if verdict(f) == "PASS"]


def certified_set():
    d = json.loads(LEDGER_JSON.read_text())
    return {p["slide_num"] for p in d["pages"] if p["status"] == "certified"}


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
            needverify.append((n, att[-1]))
    return cands, needverify, certified


def append_ledger_row(n, att, ver):
    with open(VLEDGER, "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        for line in f:
            m = re.match(r"\|\s*(\d+)\s*\|", line)
            if m and int(m.group(1)) == n and "superseded" not in line:
                cols = [c.strip() for c in line.split("|")]
                v = cols[4] if len(cols) > 4 else ""
                if "PASS" in v and "FAIL" not in v:
                    fcntl.flock(f, fcntl.LOCK_UN)
                    return False
        f.write(
            f"| {n} | {att.relative_to(NS)} | {ver.relative_to(NS)} | "
            f"PASS / PASS (original-first dual-read; sweeper-11) | — | yes | |\n")
        fcntl.flock(f, fcntl.LOCK_UN)
    return True


def merge_update(n):
    pptx = PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
    r = subprocess.run(
        ["python3", "pool_run/merge_final_deck.py", "update", str(n),
         str(pptx.relative_to(NS)), "08-performance_final.pptx"],
        cwd=NS, capture_output=True, text=True)
    log(f"slide {n} merge update rc={r.returncode} {r.stdout.strip()} {r.stderr.strip()[:200]}")
    return r.returncode == 0


def db_done(n):
    r = None
    for _ in range(6):
        r = subprocess.run(
            ["sqlite3", str(MISSION_DB.relative_to(NS)),
             f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
            cwd=NS, capture_output=True, text=True)
        if r.returncode == 0:
            log(f"slide {n} mission.db scope slide-{n} done")
            return True
        time.sleep(5)
    log(f"slide {n} mission.db UPDATE kept failing: {r.stderr.strip()[:200]}")
    return False


def certify(n, att, ver):
    if not (PPTX_DIR / f"slide_{n:03d}_recreated.pptx").exists():
        log(f"slide {n} candidate but pptx missing — skip")
        return False
    row = append_ledger_row(n, att, ver)
    log(f"slide {n} ledger row {'appended' if row else 'already present'} "
        f"(att={att.name} ver={ver.name})")
    if not merge_update(n):
        return False
    ok = n in certified_set()
    log(f"slide {n} certified in final_deck_ledger.json: {ok}")
    db_done(n)
    return ok


def render_fresh(n, d):
    pptx = PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
    scratch = TMP / f"render_s11_{n}_{int(time.time())}"
    scratch.mkdir(parents=True, exist_ok=True)
    subprocess.run(["soffice", "--headless",
                    f"-env:UserInstallation=file://{scratch}/lo",
                    "--convert-to", "pdf", "--outdir", str(scratch), str(pptx)],
                   capture_output=True)
    subprocess.run(["pdftoppm", "-png", "-r", "150",
                    str(scratch / f"{pptx.stem}.pdf"), str(scratch / "pg")],
                   capture_output=True)
    pngs = sorted(scratch.glob("pg*.png"))
    dest = d / f"render_s11_{n}.png"
    if pngs:
        shutil.copy(pngs[0], dest)
    shutil.rmtree(scratch, ignore_errors=True)
    log(f"slide {n} fresh render -> {dest.name}: {dest.exists()}")
    return dest if dest.exists() else None


def verify(n):
    d = qa_dir(n)
    orig = original(n)
    if d is None or orig is None:
        log(f"verify {n}: qa dir or original missing — skip")
        return 1
    TMP.mkdir(parents=True, exist_ok=True)
    lf = open(TMP / f"s11_verify_{n}.lock", "w")
    try:
        fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return 0
    try:
        if pass_files(d, "verify"):
            log(f"verify {n}: verify PASS already banked — exit")
            return 0
        banked = [f for f in d.glob(f"judge_verify_s11_{n}_try*.txt")
                  if verdict(f) in ("PASS", "FAIL")]
        if banked:
            log(f"verify {n}: sweeper-11 verdict already banked ({banked[-1].name}) — exit")
            return 0
        pptx = PPTX_DIR / f"slide_{n:03d}_recreated.pptx"
        renders = sorted(d.glob("render_*.png"), key=lambda p: p.stat().st_mtime)
        render = renders[-1] if renders else None
        if render is None or (pptx.exists() and pptx.stat().st_mtime > render.stat().st_mtime):
            render = render_fresh(n, d)
        if render is None:
            log(f"verify {n}: no render available — abort")
            return 1
        log(f"verify {n}: orig={orig.name} render={render.name} — sleeping 90-150s before judge")
        time.sleep(random.randint(90, 150))
        prompt = PROMPT_FILE.read_text()
        for t in range(1, 9):
            vt = d / f"judge_verify_s11_{n}_try{t}.txt"
            log(f"verify {n}: corroboration attempt {t}/8 -> {vt.name}")
            r = subprocess.run(
                ["bash", str(GATE), "timeout", "540", PYBIN, str(ANALYZE), "comparison",
                 str(orig), str(render),
                 "--view", f"Slide {n} recreation — INDEPENDENT corroboration read vs original lecture frame (try {t})",
                 "--capture", "IMG1=original lecture video frame (ground truth, read FIRST); IMG2=150dpi PNG render of the current 13.33x7.5in PPTX recreation (read SECOND)",
                 "--thinking", "high", "--max-tokens", "65536",
                 "--timeout", "420", "--rounds", "1", "--tries", "1",
                 "--transcript", str(vt), "-p", prompt],
                cwd=REPO, capture_output=True, text=True)
            v = verdict(vt)
            log(f"verify {n}: attempt {t} rc={r.returncode} verdict={v}")
            if v in ("PASS", "FAIL"):
                log(f"verify {n}: finished verdict={v} transcript={vt.relative_to(NS)}")
                return 0 if v == "PASS" else 2
            body = ""
            try:
                body = vt.read_text(errors="replace") + r.stderr
            except OSError:
                pass
            if re.search(r"429|rate.?limit|too many requests", body, re.I):
                log(f"verify {n}: attempt {t} hit 429 — sleep 300s before retry")
                time.sleep(300)
            else:
                log(f"verify {n}: attempt {t} no verdict (infra) — sleep 120s before retry")
                time.sleep(120)
        log(f"verify {n}: exhausted 8 attempts without a verdict")
        return 1
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)
        lf.close()


def loop():
    log("sweeper-11 (python) loop start")
    while True:
        cands, needverify, certified = scan()
        log(f"scan: certified={len(certified)}/37 candidates={len(cands)} "
            f"needverify={sorted(n for n, _ in needverify)}")
        for n, att, ver in cands:
            certify(n, att, ver)
        for n, _att in needverify:
            subprocess.Popen([PYBIN, str(Path(__file__).resolve()), "verify", str(n)],
                             cwd=NS, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        if len(certified_set()) >= 37:
            log("37/37 certified — loop exit")
            return 0
        time.sleep(60)


if __name__ == "__main__":
    if sys.argv[1] == "verify":
        sys.exit(verify(int(sys.argv[2])))
    elif sys.argv[1] == "scan":
        cands, needverify, certified = scan()
        for n, att, ver in cands:
            print(f"CAND\t{n}\t{att.relative_to(NS)}\t{ver.relative_to(NS)}")
        for n, att in needverify:
            print(f"NEEDVERIFY\t{n}\t{att.relative_to(NS)}")
        print(f"CERTIFIED\t{len(certified)}\t{sorted(certified)}")
    else:
        sys.exit(loop())
