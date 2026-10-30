#!/usr/bin/env bash
# S20f pre-phase GROUND-TRUTH description dispatch (analysis mode, one image).
# Probe law: yield to cert lanes while pgrep -c -f analyze_image.py >= 8.
# Usage: dispatch_desc.sh IMG PROMPT_FILE TRANSCRIPT VIEW
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
IMG="$1"; PROMPT="$2"; OUT="$3"; VIEW="$4"
N=$(pgrep -c -f analyze_image.py); T=0
while [ "$N" -ge 8 ] && [ "$T" -lt 10800 ]; do
  sleep 120; T=$((T+120)); N=$(pgrep -c -f analyze_image.py)
done
echo "GATE: load=$N waited=${T}s start=$(date +%H:%M:%S)"
if [ "$N" -ge 8 ]; then echo "PROBE-WALL: load >= 8 after ~3h; PARK this leg, do not dispatch"; exit 42; fi
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  "$IMG" --view "$VIEW" --thinking high --max-tokens 65536 \
  --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$OUT" -p "$(cat "$PROMPT")"
echo "EXIT=$? end=$(date +%H:%M:%S)"
