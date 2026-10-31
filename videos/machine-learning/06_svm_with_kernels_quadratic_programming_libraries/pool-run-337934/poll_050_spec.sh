#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_050_analysis.txt
OUT=$NS/pool-run-337934/poll_050_spec.out
echo "poll start $(date -u +%H:%M:%S)" > $OUT
for i in $(seq 1 90); do
  if [ -f "$F" ]; then
    sz=$(stat -c %s "$F")
    if [ "$sz" -ge 4000 ] && grep -q "1. SLIDE_TITLE" "$F"; then
      echo "READY size=$sz iter=$i $(date -u +%H:%M:%S)" >> $OUT
      exit 0
    fi
    echo "iter=$i size=$sz $(date -u +%H:%M:%S)" >> $OUT
  else
    echo "iter=$i missing $(date -u +%H:%M:%S)" >> $OUT
  fi
  sleep 60
done
echo "TIMEOUT after 90 iters $(date -u +%H:%M:%S)" >> $OUT
exit 1
