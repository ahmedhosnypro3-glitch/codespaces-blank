#!/usr/bin/env bash
# Sequential driver for scope R04 (slides 010, 011, 012).
# Waits for the already-running 010 runner, then runs 011 and 012 one at a time.
# The rejudge runner itself handles render/chrome/crop and both judge legs.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
RJ=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027

wait_for_result() {
  local n="$1"
  for _ in $(seq 1 720); do
    [ -s "$RJ/slide$n/result.txt" ] && return 0
    sleep 30
  done
  return 1
}

# 010 is already running under its own pid; wait for its result file.
wait_for_result 010 || echo "R04_DRIVER 010 no result after wait"
echo "R04_DRIVER 010 done: $(tr '\n' ' ' < "$RJ/slide010/result.txt" 2>/dev/null)"

for n in 011 012; do
  echo "R04_DRIVER starting $n at $(date +%H:%M:%S)"
  bash "$RJ/rejudge_slide.sh" "$n"
  echo "R04_DRIVER finished $n at $(date +%H:%M:%S): $(tr '\n' ' ' < "$RJ/slide$n/result.txt" 2>/dev/null)"
done
echo "R04_DRIVER ALL DONE $(date +%H:%M:%S)"
