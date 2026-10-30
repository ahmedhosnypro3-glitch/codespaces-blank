#!/usr/bin/env bash
# Orchestrator re-analysis lane (background, not agents).
# Refresh reanalysis_v2 for slides whose transcript is missing or is an error stub.
set -u
V=/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks
IMG=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
GATE=/home/codespace/ai_llm_slides/scripts/16_vision_gate.sh
PROMPT="$V/recreated_pptx/build/reanalyze_prompt.md"
OUT="$V/analysis/reanalysis_v2"
LOG="$V/pooled_missions/runs/run-1793126532/reanalysis_lane.log"
mkdir -p "$OUT"

run_one() {
  n="$1"
  img="$V/unique_slides/slide_${n}.jpg"
  out="$OUT/slide_${n}_reanalysis.txt"
  [ -f "$img" ] || { echo "$(date +%F\ %T) slide_$n NO_IMAGE" >> "$LOG"; return; }
  sz=$(stat -c%s "$out" 2>/dev/null || echo 0)
  if [ "$sz" -ge 3000 ]; then echo "$(date +%F\ %T) slide_$n SKIP(ok $sz)" >> "$LOG"; return; fi
  tmp="$out.tmp.$$"
  timeout 900 bash "$GATE" python3 "$IMG" analysis "$img" \
    --timeout 750 --rounds 1 --tries 1 --max-tokens 16000 \
    --view "slide $n — original lecture frame, 09_introduction_to_neural_networks" \
    --capture "960x540 lecture slide frame, original" \
    -p "$(cat "$PROMPT")" > "$tmp" 2>&1
  rc=$?
  sz2=$(stat -c%s "$tmp" 2>/dev/null || echo 0)
  if [ "$sz2" -ge 3000 ] && grep -q '^\[winner\]' "$tmp"; then
    mv "$tmp" "$out"
    echo "$(date +%F\ %T) slide_$n DONE($sz2) rc=$rc" >> "$LOG"
  else
    cp "$tmp" "$OUT/slide_${n}_reanalysis.lastfail.txt"
    echo "$(date +%F\ %T) slide_$n FAIL(sz=$sz2 rc=$rc)" >> "$LOG"
  fi
}
export -f run_one
export V IMG GATE PROMPT OUT LOG

SLIDES="$*"
i=0
for n in $SLIDES; do
  run_one "$n" &
  i=$((i+1))
  if [ $((i % 4)) -eq 0 ]; then wait; fi
done
wait
echo "$(date +%F\ %T) LANE COMPLETE" >> "$LOG"

# retry pass for anything still short
for n in $SLIDES; do
  sz=$(stat -c%s "$OUT/slide_${n}_reanalysis.txt" 2>/dev/null || echo 0)
  [ "$sz" -ge 3000 ] || { echo "$(date +%F\ %T) slide_$n RETRY" >> "$LOG"; run_one "$n"; }
done
echo "$(date +%F\ %T) LANE ALL DONE" >> "$LOG"
