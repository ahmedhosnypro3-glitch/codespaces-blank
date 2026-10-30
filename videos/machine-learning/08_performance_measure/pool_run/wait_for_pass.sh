#!/usr/bin/env bash
# wait_for_pass.sh — block until a genuine PASS verdict appears in any QA dir,
# then print the path. Exits immediately if one already exists.
set -uo pipefail
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
PYBIN=/home/codespace/.pyenv/versions/3.15.2/bin/python3
TIMEOUT="${1:-7200}"

t0=$SECONDS
while (( SECONDS - t0 < TIMEOUT )); do
  found=""
  for f in "$NS"/recreated_pptx/qa/slide*/judge_attempt_*.txt; do
    [ -f "$f" ] || continue
    if [ "$("$PYBIN" "$NS/pool_run/verdict.py" "$f" 2>/dev/null)" = "PASS" ]; then
      found="$f"
      break
    fi
  done
  if [ -n "$found" ]; then
    echo "PASS FOUND: $found"
    exit 0
  fi
  sleep 20
done
echo "NO PASS within ${TIMEOUT}s"
exit 1
