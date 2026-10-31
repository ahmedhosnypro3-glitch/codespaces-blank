#!/bin/bash
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_039_analysis.txt
for i in $(seq 1 40); do
  if [ -f "$F" ] && [ $(wc -c < "$F") -ge 4000 ] && grep -q '1. SLIDE_TITLE' "$F"; then
    echo "READY at $(date) iter=$i bytes=$(wc -c < $F)"
    exit 0
  fi
  sleep 60
done
echo "TIMEOUT after 40 min; bytes=$(wc -c < $F 2>/dev/null || echo missing)"
exit 1
