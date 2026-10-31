#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_011_analysis.txt
LOG=$NS/pool-run-337934/poll_011.out
end=$(( $(date +%s) + 5400 ))
while [ $(date +%s) -lt $end ]; do
  sz=$(wc -c < "$F" 2>/dev/null || echo 0)
  if grep -q "^1\. SLIDE_TITLE" "$F" 2>/dev/null && [ "$sz" -ge 4000 ]; then
    echo "$(date) SPEC_READY bytes=$sz" >> "$LOG"
    exit 0
  fi
  echo "$(date) waiting bytes=$sz marker=$(grep -c '^1\. SLIDE_TITLE' "$F" 2>/dev/null || echo 0)" >> "$LOG"
  sleep 60
done
echo "$(date) TIMEOUT" >> "$LOG"
exit 1
