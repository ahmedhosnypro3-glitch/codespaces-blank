#!/usr/bin/env bash
# Auto-certification watcher for slide 047 attempt 6 (worker w047-root-20261024).
# Waits for the judge batch to finish, then certifies ONLY if both legs PASS.
# Never fabricates a verdict: any non-PASS leg leaves the row un-certified and banks the state.
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047
DONE="$Q/attempt6_all_done.txt"
NOTE="$Q/autocertify_note.txt"

# wait for the dispatcher to finish (it writes DONE)
for i in $(seq 1 120); do
  [ -f "$DONE" ] && break
  VIDEO=machine-learning/03_ridger_regression_gradient_descent TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp" \
    python3 scripts/15_progress.py heartbeat 47 w047-root-20261024 >/dev/null 2>&1
  sleep 30
done
[ -f "$DONE" ] || { echo "$(date -u +%FT%TZ) dispatcher never finished; no certification" > "$NOTE"; exit 0; }

ok=1
grep -q "FINAL VERDICT: PASS" "$Q/judge_attempt_6.txt" 2>/dev/null || ok=0
for n in topband augmatrix calceq calcright button; do
  grep -q "FINAL VERDICT: PASS" "$Q/crop_6_${n}_judge.txt" 2>/dev/null || ok=0
done
if [ "$ok" = "1" ]; then
  bash "$Q/certify_attempt6.sh" > "$Q/certify_attempt6.log" 2>&1
  echo "$(date -u +%FT%TZ) certified: all 6 legs PASS" > "$NOTE"
else
  {
    echo "$(date -u +%FT%TZ) NOT certified — verdicts:"
    grep -h "FINAL VERDICT" "$Q/judge_attempt_6.txt" "$Q"/crop_6_*_judge.txt 2>/dev/null
  } > "$NOTE"
fi
