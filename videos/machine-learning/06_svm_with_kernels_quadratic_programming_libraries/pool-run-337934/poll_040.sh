#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_040_analysis.txt
for i in $(seq 1 40); do
  if [ -f "$F" ]; then
    SZ=$(stat -c%s "$F")
    if [ "$SZ" -ge 4000 ] && grep -q "1. SLIDE_TITLE" "$F"; then
      echo "READY size=$SZ after $((i*60))s"
      exit 0
    fi
    echo "poll $i: size=$SZ"
  else
    echo "poll $i: missing"
  fi
  sleep 60
done
echo "TIMEOUT after 40min"
exit 1
