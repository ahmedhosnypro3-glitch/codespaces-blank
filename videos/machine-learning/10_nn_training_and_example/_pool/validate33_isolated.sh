#!/bin/bash
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
for i in 1 2 3 4 5 6; do
  echo "=== attempt $i $(date) ===" >> _pool/storm_log/validate33_isolated.log
  python3 /home/codespace/ai_llm_slides/scripts/13_validate_slides.py analysis/isolated_033 \
    >> _pool/storm_log/validate33_isolated.log 2>&1
  if [ -f analysis/isolated_033/slide_033_final.json ]; then
    echo "SLIDE_033_VALIDATED_OK" >> _pool/storm_log/validate33_isolated.log
    cp analysis/isolated_033/slide_033_final.json analysis/slide_033_final.json
    break
  fi
  echo "  empty/parse-error transient — sleeping 120s" >> _pool/storm_log/validate33_isolated.log
  sleep 120
done
echo "ISOLATED_VALIDATE_DONE $(date)" >> _pool/storm_log/validate33_isolated.log
