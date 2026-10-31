import json, os, re, sys, glob, time, fcntl, subprocess, datetime

ROOT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "pool_run/tmp"))
from sweeper_scan_cert import scan, qa_dir, PASS_RE  # reuse scan logic

LOG = open(os.path.join(ROOT, "pool_run/tmp/sweeper_cert_loop.log"), "a", buffering=1)
def log(msg):
    line = "%s %s" % (datetime.datetime.now().isoformat(timespec="seconds"), msg)
    print(line)
    LOG.write(line + "\n")

def ledger_append(row):
    lock_path = os.path.join(ROOT, "pool_run/.verification_ledger.lock")
    with open(lock_path, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        with open(os.path.join(ROOT, "pool_run/verification_ledger.md"), "a") as f:
            f.write(row + "\n")
        fcntl.flock(lk, fcntl.LOCK_UN)

def certified_set():
    d = json.load(open(os.path.join(ROOT, "final_deck_ledger.json")))
    return set(p["slide_num"] for p in d["pages"] if p["status"] == "certified")

def merge_slide(n):
    pptx = "recreated_pptx/slide_%03d_recreated.pptx" % n
    r = subprocess.run([sys.executable, "pool_run/merge_final_deck.py", "update", str(n), pptx, "08-performance_final.pptx"],
                       capture_output=True, text=True, cwd=ROOT)
    ok = r.returncode == 0 and n in certified_set()
    return ok, (r.stdout + r.stderr).strip()

def process(n, render, att, ver, qd):
    src = "analysis/reanalysis/slide_%03d_raw.json" % n
    if not os.path.exists(os.path.join(ROOT, src)):
        alt = glob.glob(os.path.join(ROOT, "analysis/reanalysis/slide_%03d*" % n))
        src = os.path.relpath(alt[0], ROOT) if alt else "analysis/reanalysis/slide_%03d_raw.json (missing)" % n
    row = "| %d | %s | %s | PASS / PASS (original-first dual-read, both postdate newest render %s) | %s | " % (
        n, os.path.relpath(att, ROOT), os.path.relpath(ver, ROOT), os.path.basename(render), src)
    ok, out = merge_slide(n)
    if ok:
        subprocess.run(["sqlite3", "pool_run/mission.db", "UPDATE scopes SET status='done', updated_at=datetime('now') WHERE name='slide-%d';" % n], cwd=ROOT)
        row += "certified=yes | sweeper dual-read merge 2026-10-31 |"
        log("MERGED slide %d: attempt=%s verify=%s -> certified confirmed in final_deck_ledger.json; scope slide-%d done" % (n, os.path.basename(att), os.path.basename(ver), n))
    else:
        row += "merge FAILED: %s |" % out.splitlines()[-1][:200] if out else "merge FAILED (no output) |"
        log("MERGE FAILED slide %d: %s" % (n, out[-400:]))
    ledger_append(row)
    return ok

def main():
    deadline = time.time() + 40 * 60
    while time.time() < deadline:
        cert = certified_set()
        remaining = [n for n in range(1, 38) if n not in cert]
        if not remaining:
            log("ALL 37 CERTIFIED -> running final gate")
            r = subprocess.run([sys.executable, "pool_run/merge_final_deck.py", "gate", "08-performance_final.pptx", "recreated_pptx", "37"],
                               capture_output=True, text=True, cwd=ROOT)
            report = "pool_run/tmp/final_gate_report_2026-10-31.txt"
            with open(os.path.join(ROOT, report), "w") as f:
                f.write("FINAL GATE 2026-10-31 rc=%d\n%s\n%s\n" % (r.returncode, r.stdout, r.stderr))
            log("GATE rc=%d report banked at %s\n%s" % (r.returncode, report, (r.stdout + r.stderr)[-800:]))
            return
        results = scan()
        did = False
        for row in results:
            n, status = row[0], row[1]
            if status == "QUALIFIES":
                log("slide %d QUALIFIES (attempt=%s verify=%s render=%s)" % (n, os.path.basename(row[3]), os.path.basename(row[4]), os.path.basename(row[2])))
                process(n, row[2], row[3], row[4], row[5])
                did = True
        if not did:
            q = sum(1 for r in results if r[1] == "QUALIFIES")
            log("pass: certified=%d/37, qualifying now=%d" % (len(cert), q))
        time.sleep(45)
    log("40-minute window elapsed; stopping loop")

if __name__ == "__main__":
    main()
