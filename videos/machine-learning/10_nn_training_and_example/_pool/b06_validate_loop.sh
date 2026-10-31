#!/usr/bin/env bash
set -u
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
for k in 1 2 3 4; do
  echo "=== validate slide 012 try $k $(date +%T)" >> _pool/b06_validate_loop.status
  VISION_SLOTS=2 ./_pool/vision_gate.sh python3 /home/codespace/ai_llm_slides/scripts/13_validate_slides.py \
    analysis/reanalysis --from 12 --to 12 --slides 1 >> _pool/b06_validate_12.log 2>&1
  if [ -f analysis/reanalysis/slide_012_final.json ]; then
    echo "OK slide_012_final.json banked $(date +%T)" >> _pool/b06_validate_loop.status
    break
  fi
  sleep 120
done
