#!/usr/bin/env bash
# S20a pre-phase GROUND-TRUTH description dispatch (analysis mode, one image).
# Probe law: yield to cert lanes while pgrep -c -f analyze_image.py >= 8.
# Usage: dispatch_desc.sh IMG PROMPT_FILE TRANSCRIPT VIEW
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
IMG="$1"; PROMPT="$2"; OUT="$3"; VIEW="$4"
n=0
while [ "$(pgrep -c -f analyze_image.py)" -ge 8 ]; do
  n=$((n+1))
  if [ "$n" -gt 30 ]; then echo "PROBE-WALL: load >= 8 after 30 checks (~60 min); PARK this leg, do not dispatch"; exit 42; fi
  sleep 120
done
exec scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  "$IMG" --view "$VIEW" --thinking high --max-tokens 16000 \
  --timeout 1200 --rounds "${ROUNDS:-2}" --tries "${TRIES:-1}" \
  --transcript "$OUT" -p "$(cat "$PROMPT")"
