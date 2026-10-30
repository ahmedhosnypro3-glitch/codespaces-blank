#!/usr/bin/env bash
# Bounded retry loop for slide 032 leg B crop judges (crop_11 prompt set).
# The vision router intermittently 504s (provider Nvidia) — retries are a lottery,
# so round-robin over the crops that still lack a verdict until the deadline.
set -u
QA="/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide032"
cd "/worksp""aces/codespaces-blank/ai_llm_slides" || exit 2
CROPS="graph table callouts title params"
DEADLINE=$(( $(date +%s) + 2700 ))   # 45 min wall-clock budget
k=0
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  missing=""
  for n in $CROPS; do
    grep -q "FINAL VERDICT" "$QA/crop_11_${n}_judge.txt" 2>/dev/null || missing="$missing $n"
  done
  if [ -z "$missing" ]; then echo "ALL CROPS HAVE VERDICTS"; break; fi
  n=${missing%% *}
  k=$((k+1))
  echo "[$(date -u +%H:%M:%S)] round $k: dispatch $n (load=$(pgrep -c -f analyze_image.py)) missing:$missing"
  bash "$QA/crop_11_${n}_prompt.txt" > "$QA/crop_11_${n}_run.log" 2>&1
  cp "$QA/crop_11_${n}_run.log" "$QA/crop_11_${n}_retry12_${k}.log"
  if grep -q "FINAL VERDICT" "$QA/crop_11_${n}_judge.txt" 2>/dev/null; then
    echo "[$(date -u +%H:%M:%S)] round $k: $n VERDICT LANDED"
  else
    echo "[$(date -u +%H:%M:%S)] round $k: $n no verdict; sleeping 120s"
    sleep 120
  fi
done
echo "loop end $(date -u +%H:%M:%S)"
for n in $CROPS; do
  if grep -q "FINAL VERDICT" "$QA/crop_11_${n}_judge.txt" 2>/dev/null; then echo "$n: VERDICT"; else echo "$n: pending"; fi
done
