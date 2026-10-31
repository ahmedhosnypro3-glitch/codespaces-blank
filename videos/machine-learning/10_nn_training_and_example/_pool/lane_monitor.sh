#!/usr/bin/env bash
# Fleet monitor: reconstruct lane state from FILES and DB, not driver logs
# (the drivers' `log` helper is not exported to worker shells — known, benign).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
DB=_pool/mission.db

echo "===== $(date '+%F %T') FLEET MONITOR ====="

echo "--- drivers alive ---"
pgrep -f "reanalysis_driver.sh" >/dev/null && echo "reanalysis_driver: ALIVE" || echo "reanalysis_driver: DEAD"
pgrep -f "rejudge_certified_driver.sh" >/dev/null && echo "rejudge_certified: ALIVE" || echo "rejudge_certified: DEAD"
echo "s11 judge: $(pgrep -f s11_judge_task.sh >/dev/null && echo ALIVE || echo DEAD)"

echo "--- vision processes ---"
echo "analyze_image procs total: $(pgrep -fc analyze_image.py 2>/dev/null || echo 0)"
echo "vision_gate wrappers here: $(pgrep -f 'vision_gate.sh' | wc -l)"

echo "--- LANE: fresh re-analysis (analysis/reanalysis_skill) ---"
have=0; debt=0
for i in $(seq 1 34); do
  n=$(printf "%03d" $i)
  if [ -s "analysis/reanalysis_skill/slide_${n}.analysis.txt" ]; then have=$((have+1)); fi
  [ -f "analysis/reanalysis_skill/slide_${n}.analysis.txt.debt" ] && debt=$((debt+1))
done
echo "banked coherent bodies: $have/34 ; debt: $debt ; attempts in flight: $(ls analysis/reanalysis_skill/*.a[0-9] 2>/dev/null | wc -l)"

echo "--- LANE: re-judge certified (qa/slideNNN/rejudge_r2) ---"
pass=0; fail=0; none=0; rend=0
for n in 001 004 005 006 007 008 009 010 012 013 014 016 017 023 024 025 026 027 029 032; do
  ls "qa/slide${n}/rejudge_r2"/render-*.png >/dev/null 2>&1 && rend=$((rend+1))
  v=""
  for f in "qa/slide${n}/rejudge_r2"/judge_attempt_*.txt; do
    [ -f "$f" ] || continue
    x=$(grep -o 'FINAL VERDICT: [A-Z]*' "$f" 2>/dev/null | tail -1)
    [ -n "$x" ] && v="$x"
  done
  case "$v" in
    *PASS) pass=$((pass+1));;
    *FAIL) fail=$((fail+1));;
    *) none=$((none+1)); echo "  slide $n: NO VERDICT ($(ls "qa/slide${n}/rejudge_r2"/judge_attempt_*.txt 2>/dev/null | wc -l) attempts)";;
  esac
done
echo "renders: $rend/20 | PASS: $pass | FAIL: $fail | no verdict: $none"

echo "--- LANE: geometry ---"
echo "geom reports: $(ls qa/slide*/geom_*.md 2>/dev/null | wc -l)/20 expected"

echo "--- LANE: parse adjudication ---"
echo "parse adjudications: $(ls analysis/parse/adjudication/*.md 2>/dev/null | wc -l)/34 expected"

echo "--- LANE: sources audit ---"
aud=0
for i in $(seq 1 34); do n=$(printf "%03d" $i); grep -q '^## Audit' "sources/slide_${n}_source/SOURCES.md" 2>/dev/null && aud=$((aud+1)); done
echo "audited SOURCES.md: $aud/34"

echo "--- final deck ledger ---"
python3 - <<'PY'
import json
d = json.load(open("final_deck_ledger.json"))
pages = d.get("pages", d)
if isinstance(pages, dict):
    items = list(pages.values())
else:
    items = pages
cert = [p.get("slide_num") or p.get("num") or p.get("page") for p in items
        if (p.get("status") == "certified" or p.get("state") == "certified")]
ph = [p.get("slide_num") or p.get("num") or p.get("page") for p in items
      if not (p.get("status") == "certified" or p.get("state") == "certified")]
print(f"certified {len(cert)}: {' '.join(str(x) for x in cert)}")
print(f"placeholder {len(ph)}: {' '.join(str(x) for x in ph)}")
PY

echo "--- runaway checkbox: gateway-wide procs by owning session ---"
echo "analyze_image total: $(pgrep -fc analyze_image.py 2>/dev/null || echo 0)"
echo "host RAM: $(free -m | awk 'NR==2{print "avail "$7"MB"}') ; disk free: $(df -h . | awk 'NR==2{print $4}')"

echo "--- DB scopes ---"
sqlite3 $DB "select name,status from scopes where name like 'b_%' and name not like 'b0_' order by name;" 2>/dev/null | tail -20
echo "===== END MONITOR ====="
