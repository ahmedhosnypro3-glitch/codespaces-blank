#!/usr/bin/env bash
V=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
O=$V/_pool/bparse6/out
cd "$V" || exit 9
python3 ~/.agents/skills/doc-parse/scripts/crop_cascade.py unique_slides/slide_034.jpg \
  --prompt-file ~/.agents/skills/doc-parse/references/prompts/crop_decision.md \
  --out analysis/parse/cascade/slide_034 --max-crops 16 --max-parse-calls 24 --parse-timeout 150 \
  > "$O/cascade_034.log" 2>&1
echo "cascade034 rc=$?" >> "$O/cascade_034.log"
