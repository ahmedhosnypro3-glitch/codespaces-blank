#!/bin/bash
# worker-016-finish-20261024: remaining leg-2 crop pairs, sequentially, gate law between calls.
set -u
cd /workspaces/codespaces-blank/ai_llm_slides || exit 3
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
for NAME in bullet2 last_bullet; do
  for i in 1 2 3 4 5 6; do
    n=$(pgrep -c -f analyze_image.py || true)
    if [ "${n:-0}" -lt 8 ]; then break; fi
    python3 scripts/15_progress.py heartbeat 16 w016-finish-20261024 >/dev/null
    sleep 240
  done
  echo "=== dispatching $NAME at $(date +%H:%M) (load $(pgrep -c -f analyze_image.py || echo 0)) ==="
  bash "$Q/dispatch_judge_B_5.sh" "$NAME" > "$Q/crop_5_${NAME}_dispatch.log" 2>&1
  echo "=== $NAME rc=$? at $(date +%H:%M) ==="
done
python3 scripts/15_progress.py heartbeat 16 w016-finish-20261024 >/dev/null
echo "ALL CROPS DONE at $(date +%H:%M)"
