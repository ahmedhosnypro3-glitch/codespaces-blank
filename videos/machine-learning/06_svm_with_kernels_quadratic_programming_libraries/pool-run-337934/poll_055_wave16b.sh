#!/bin/bash
# Round 2: poll until slide_055 reanalysis spec is >=4000 bytes and contains "1. SLIDE_TITLE".
NS=/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries
F=$NS/qa/reanalysis2/slide_055_analysis.txt
OUT=$NS/pool-run-337934/poll_055_wave16b.out
END=$((SECONDS + 90*60))
: > "$OUT"
while [ $SECONDS -lt $END ]; do
  if [ -f "$F" ]; then
    SZ=$(wc -c < "$F")
    if grep -q "1. SLIDE_TITLE" "$F" 2>/dev/null && [ "$SZ" -ge 4000 ]; then
      echo "READY size=$SZ at $(date '+%H:%M:%S')" >> "$OUT"
      exit 0
    fi
    echo "poll $(date '+%H:%M:%S') size=$SZ" >> "$OUT"
  else
    echo "poll $(date '+%H:%M:%S') missing" >> "$OUT"
  fi
  sleep 60
done
echo "TIMEOUT after 90min" >> "$OUT"
exit 1
