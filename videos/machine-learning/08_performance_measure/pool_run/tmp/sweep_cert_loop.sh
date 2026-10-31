#!/bin/bash
# Certify-and-merge sweeper loop for 08_performance_measure.
# Each pass: scan -> merge qualifying slides -> confirm ledger. Sleep 45s.
cd /home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
LOG=pool_run/tmp/sweep_cert_loop.out
DEADLINE=$((SECONDS + 2400))  # ~40 min
while [ $SECONDS -lt $DEADLINE ]; do
  echo "[$(date +%H:%M:%S)] PASS start" >> $LOG
  python3 pool_run/tmp/sweep_scan_cert.py > pool_run/tmp/scan.json 2>>$LOG
  python3 - <<'EOF' >> $LOG 2>&1
import json, os, subprocess, time
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
os.chdir(NS)
scan = json.load(open("pool_run/tmp/scan.json"))
cert = scan["certified"]
print(f"  certified {len(cert)}/37: {cert}")
if len(cert) >= 37:
    print("  ALL 37 CERTIFIED — running final gate")
    r = subprocess.run(["python3", "pool_run/merge_final_deck.py", "gate",
                        "08-performance_final.pptx", "recreated_pptx", "37"],
                       capture_output=True, text=True)
    print("  gate rc=", r.returncode)
    print(r.stdout[-3000:])
    print(r.stderr[-1000:])
    with open("pool_run/tmp/final_gate_report.txt", "w") as f:
        f.write(f"gate rc={r.returncode}\n{r.stdout}\n{r.stderr}")
    raise SystemExit(0)
for q in scan["qualifying"]:
    n = q["n"]
    padded = "%03d" % n
    reanalysis = f"analysis/reanalysis/slide_{padded}_raw.json"
    if not os.path.exists(reanalysis):
        cands = [f for f in os.listdir("analysis") if f == f"slide_{padded}_raw.json"]
        if cands:
            reanalysis = f"analysis/slide_{padded}_raw.json"
        else:
            reanalysis = "-"
    row = (f"| {n} | {q['attempt']} | {q['verify']} | PASS / PASS (original-first, "
           f"post-newest-render {q['render']}) | {reanalysis} | yes | "
           f"certify-and-merge sweeper 2026-10-31 |\n")
    subprocess.run(["flock", "pool_run/verification_ledger.md", "bash", "-c",
                    'printf %s "$1" >> "$2"', "bash", row,
                    "pool_run/verification_ledger.md"], check=True)
    r = subprocess.run(["python3", "pool_run/merge_final_deck.py", "update", str(n),
                        f"recreated_pptx/slide_{padded}_recreated.pptx",
                        "08-performance_final.pptx"], capture_output=True, text=True)
    print(f"  slide {n}: merge rc={r.returncode} out={r.stdout.strip()!r} err={r.stderr.strip()[:200]!r}")
    if r.returncode != 0:
        subprocess.run(["flock", "pool_run/verification_ledger.md", "bash", "-c",
                        'printf %s "$1" >> "$2"', "bash",
                        f"| {n} | {q['attempt']} | {q['verify']} | MERGE FAILED rc={r.returncode} | {reanalysis} | no | merge error: {r.stderr.strip()[:120]} |\n",
                        "pool_run/verification_ledger.md"], check=True)
        continue
    for _ in range(5):
        r2 = subprocess.run(["sqlite3", "pool_run/mission.db",
                             f"UPDATE scopes SET status='done' WHERE name='slide-{n}';"],
                            capture_output=True, text=True)
        if r2.returncode == 0:
            break
        time.sleep(5)
    d = json.load(open("final_deck_ledger.json"))
    now = [p["slide_num"] for p in d["pages"] if p["status"] == "certified"]
    print(f"  slide {n}: ledger certified now has {n}: {n in now} ({len(now)}/37)")
EOF
  echo "[$(date +%H:%M:%S)] PASS end" >> $LOG
  sleep 45
done
echo "[$(date +%H:%M:%S)] DEADLINE reached" >> $LOG
