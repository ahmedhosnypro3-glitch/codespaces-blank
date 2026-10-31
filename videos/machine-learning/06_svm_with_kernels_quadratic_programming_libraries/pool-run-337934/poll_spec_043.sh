#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_043_analysis.txt
LOG=$NS/pool-run-337934/poll_spec_043.log
end=$(( $(date +%s) + 5400 ))
while [ $(date +%s) -lt $end ]; do
  sz=$(wc -c < "$F" 2>/dev/null || echo 0)
  has=$(grep -c "1. SLIDE_TITLE" "$F" 2>/dev/null || true)
  echo "$(date '+%H:%M:%S') size=$sz title=$has" >> "$LOG"
  if [ "$sz" -ge 4000 ] && [ "$has" -ge 1 ]; then
    echo "$(date '+%H:%M:%S') READY size=$sz" >> "$LOG"
    echo READY
    exit 0
  fi
  sleep 60
done
echo "$(date '+%H:%M:%S') TIMEOUT" >> "$LOG"
echo TIMEOUT
exit 1
