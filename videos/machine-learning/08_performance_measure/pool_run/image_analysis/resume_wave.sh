#!/usr/bin/env bash
# Resume the re-analysis wave for slides whose transcript is a stub (failed/aborted call).
# Done predicate: transcript exists, >5000 bytes, and carries a VERDICT section.
# Background-task driven (no subagents), through the fleet vision gate, CONC=6.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
PYBIN=/home/codespace/.pyenv/versions/3.15.2/bin/python3
SCRIPT=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT="$NS/pool_run/image_analysis/analysis_prompt.txt"
SLIDES="$NS/unique_slides"
OUT="$NS/pool_run/image_analysis"
TITLES="$NS/pool_run/image_analysis/titles.map"
LOG="$OUT/resume.log"
CONC=6
mkdir -p "$OUT"
log(){ echo "[$(date '+%F %T')] $*" >> "$LOG"; }
title_for(){ awk -F'\t' -v n="$1" '$1==n{print $2; exit}' "$TITLES" 2>/dev/null; }

done_ok(){
  local out="$1"
  [ -s "$out" ] || return 1
  local b; b=$(wc -c < "$out")
  [ "$b" -gt 5000 ] || return 1
  grep -qi "verdict" "$out" || return 1
  return 0
}

run_one(){
  local f="$1" base n num title out rc
  base="$(basename "$f")"; n="${base%.*}"
  num="$(echo "$base" | sed -E 's/^slide_0*([0-9]+).*$/\1/')"
  out="$OUT/${n}_analysis.txt"
  if done_ok "$out"; then log "$n: SKIP (complete)"; return 0; fi
  title="$(title_for "$num")"
  [ -n "$title" ] || title="lecture slide (topic unlabeled)"
  log "$n: re-running analysis"
  bash /home/codespace/ai_llm_slides/scripts/16_vision_gate.sh "$PYBIN" "$SCRIPT" analysis "$f" \
    --timeout 420 --rounds 1 --tries 1 \
    --view "Slide $num — $title" \
    --capture "960x540 CSS px, 1x scale, lecture video frame" \
    -p "$(cat "$PROMPT")" > "$out" 2>&1
  rc=$?
  log "$n: exit=$rc bytes=$(wc -c < "$out" 2>/dev/null) verdict=$(grep -ci verdict "$out" 2>/dev/null)"
}
export -f run_one done_ok title_for log
export PYBIN SCRIPT PROMPT OUT TITLES

mapfile -t FILES < <(ls "$SLIDES"/slide_*.jp*g 2>/dev/null | sort)
TODO=()
for f in "${FILES[@]}"; do
  n="$(basename "${f%.*}")"
  done_ok "$OUT/${n}_analysis.txt" || TODO+=("$f")
done
log "resume wave start: ${#TODO[@]} slides to redo of ${#FILES[@]}"
running=0
for f in "${TODO[@]}"; do
  run_one "$f" &
  running=$((running+1))
  if [ "$running" -ge "$CONC" ]; then wait -n; running=$((running-1)); fi
done
wait
ok=$(grep -l -i "verdict" "$OUT"/*_analysis.txt 2>/dev/null | while read -r t; do [ "$(wc -c < "$t")" -gt 5000 ] && echo "$t"; done | wc -l)
log "resume wave done: $ok/${#FILES[@]} transcripts complete"
