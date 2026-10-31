#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_049_analysis.txt
FLAG=$NS/pool-run-337934/slide_049_spec_ready.flag
for i in $(seq 1 40); do
  if [ -f "$F" ]; then
    SZ=$(stat -c %s "$F")
    if [ "$SZ" -ge 4000 ] && grep -q "1. SLIDE_TITLE" "$F"; then
      echo "READY size=$SZ after $i polls" > $FLAG
      exit 0
    fi
  fi
  sleep 60
done
echo "TIMEOUT after 40 polls" > $FLAG
exit 1
