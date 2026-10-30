#!/usr/bin/env bash
# S20d prephase — slide 044 STACK region ground-truth read of the ORIGINAL frame (description, not a judge leg)
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 1
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
GATE="scripts/16_vision_gate.sh"
PY="python3 .agents/skills/image-analysis/scripts/analyze_image.py"
PRE="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide044/prephase/orig_judges"

# GATE LAW: yield to cert lanes at >=8 concurrent analyzers
for i in $(seq 1 10); do
  n=$(pgrep -f "python3 .*analyze_image.py" | wc -l)
  if [ "${n:-0}" -lt 8 ]; then break; fi
  echo "GATE BUSY: $n analyzers — sleep 120 (probe $i)"; sleep 120
done
n=$(pgrep -f "python3 .*analyze_image.py" | wc -l)
if [ "${n:-0}" -ge 8 ]; then echo "GATE STILL BUSY after 10 probes — PARK"; exit 97; fi

$GATE timeout 1700 $PY analysis \
  "$PRE/crops/slide_044_stack.png" \
  -p "$(cat $PRE/prompt_044_stack.txt)" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$PRE/slide_044_stack_desc.txt"
echo "STACK EXIT=$?"
