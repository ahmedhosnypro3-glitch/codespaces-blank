#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F="$NS/qa/reanalysis2/slide_042_analysis.txt"
END=$(( $(date +%s) + 40*60 ))
while [ $(date +%s) -lt $END ]; do
  if [ -f "$F" ]; then
    SZ=$(stat -c%s "$F")
    if [ "$SZ" -ge 4000 ] && grep -q "1. SLIDE_TITLE" "$F"; then
      echo "READY size=$SZ at $(date -u +%H:%M:%S)"
      exit 0
    fi
    echo "$(date -u +%H:%M:%S) present size=$SZ waiting..."
  else
    echo "$(date -u +%H:%M:%S) missing, waiting..."
  fi
  sleep 60
done
echo "TIMEOUT after 40 min"
exit 1
