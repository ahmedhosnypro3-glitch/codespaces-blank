#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_046_analysis.txt
OUT=$NS/pool-run-337934/poll_046.out
for i in $(seq 1 90); do
  if [ -f "$F" ]; then
    SZ=$(stat -c%s "$F")
    if [ "$SZ" -ge 4000 ] && grep -q "1. SLIDE_TITLE" "$F"; then
      echo "READY size=$SZ $(date -u +%H:%M:%S)" > $OUT
      exit 0
    fi
    echo "poll $i: size=$SZ $(date -u +%H:%M:%S)" >> $OUT
  else
    echo "poll $i: missing $(date -u +%H:%M:%S)" >> $OUT
  fi
  sleep 60
done
echo "TIMEOUT $(date -u +%H:%M:%S)" > $OUT
exit 1
