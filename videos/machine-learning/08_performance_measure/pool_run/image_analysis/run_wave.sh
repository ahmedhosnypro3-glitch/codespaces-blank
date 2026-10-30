#!/usr/bin/env bash
# Parallel re-analysis wave: image-analysis script over ALL unique slides.
# Background-task driven (no subagents). Idempotent: skips slides whose
# transcript already carries a VERDICT section. Vision calls route through
# the fleet gate (16_vision_gate.sh) at CONC=6 in flight.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
PYBIN=/home/codespace/.pyenv/versions/3.15.2/bin/python3
SCRIPT=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$NS/pool_run/image_analysis/analysis_prompt.txt"
SLIDES="$NS/unique_slides"
OUT="$NS/pool_run/image_analysis"
TITLES="$NS/pool_run/image_analysis/titles.map"
LOG="$OUT/wave.log"
CONC=6
mkdir -p "$OUT"
log(){ echo "[$(date '+%F %T')] $*" >> "$LOG"; }
title_for(){ awk -F'\t' -v n="$1" '$1==n{print $2; exit}' "$TITLES" 2>/dev/null; }

mapfile -t FILES < <(ls "$SLIDES"/slide_*.jp*g 2>/dev/null | sort)
log "wave start: ${#FILES[@]} slide files, CONC=$CONC"

run_one(){
  local f="$1" base n num title out rc
  base="$(basename "$f")"; n="${base%.*}"
  num="$(echo "$base" | sed -E 's/^slide_0*([0-9]+).*$/\1/')"
  out="$OUT/${n}_analysis.txt"
  if grep -q "## 9. VERDICT" "$out" 2>/dev/null; then log "$n: SKIP (already analyzed)"; return 0; fi
  title="$(title_for "$num")"
  [ -n "$title" ] || title="lecture slide (topic unlabeled)"
  bash /home/codespace/ai_llm_slides/scripts/16_vision_gate.sh "$PYBIN" "$SCRIPT" analysis "$f" \
    --timeout 420 --rounds 1 --tries 1 \
    --view "Slide $num — $title" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    -p "$(cat "$PROMPT")" > "$out" 2>&1
  rc=$?
  log "$n: exit=$rc verdict=$(grep -c '## 9. VERDICT' "$out" 2>/dev/null) bytes=$(wc -c < "$out" 2>/dev/null)"
}
export -f run_one title_for log
export PYBIN SCRIPT PROMPT OUT TITLES

running=0
for f in "${FILES[@]}"; do
  run_one "$f" &
  running=$((running+1))
  if [ "$running" -ge "$CONC" ]; then wait -n; running=$((running-1)); fi
done
wait
log "wave done: $(grep -l '## 9. VERDICT' "$OUT"/*_analysis.txt 2>/dev/null | wc -l)/${#FILES[@]} analyzed"
