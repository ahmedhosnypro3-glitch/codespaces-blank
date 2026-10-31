#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_042_analysis.txt
for i in $(seq 1 50); do
  if [ -f "$F" ]; then
    sz=$(wc -c < "$F")
    if [ "$sz" -ge 4000 ] && grep -q "1. SLIDE_TITLE" "$F"; then
      echo "READY size=$sz iter=$i $(date -Iseconds)" > $NS/pool-run-337934/.poll_042_result.txt
      exit 0
    fi
  fi
  sleep 60
done
echo "TIMEOUT $(date -Iseconds)" > $NS/pool-run-337934/.poll_042_result.txt
exit 1
