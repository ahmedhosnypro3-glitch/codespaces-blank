#!/usr/bin/env bash
# Slide 049 Template B zoomed crop-pair certificates — leg 2 (worker-fresh-049d).
# Canonical tree: /workspaces/codespaces-blank/ai_llm_slides (plural).
set -u
PROJ=/workspaces/codespaces-blank/ai_llm_slides
QA=$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide049
VID=$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent
SCRIPT=$PROJ/.agents/skills/image-analysis/scripts/analyze_image.py
export TMPDIR=$PROJ/scratch/tmp
mkdir -p "$TMPDIR"
LOG=$QA/worker_report_progress.log
WID=worker-fresh-049d
say() { echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
hb() { (cd "$PROJ" && VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 49 "$WID" >/dev/null 2>&1); }
wait_slot() {
  # Vision-gate law: fire only when concurrent analyze_image.py VISION CLIENTS < 8.
  # `pgrep -f analyze_image.py` over-counts ~4x (dispatch wrappers carry the payload
  # in cmdline); count real python3 clients (argv[0] python3, argv[1] the script).
  for round in $(seq 1 90); do
    load=$(ps -eo args= | awk '$1 ~ /python3$/ && $2 ~ /analyze_image\.py$/ {n++} END {print n+0}')
    if [ "${load:-0}" -ge 8 ]; then say "leg B/$1: real vision clients=$load (>=8) - heartbeat + sleep 240"; hb; sleep 240; continue; fi
    say "leg B/$1: slot open (real vision clients=$load)"; return 0
  done
  say "leg B/$1: no slot after 90 rounds - ABORT"; exit 99
}

say "=== worker-fresh-049d leg B START: crops re-cut to spec bboxes (calc_table x273..852 y140..527; callout x74..218 y270..400), matched scale ==="

for NAME in calc_table callout; do
  wait_slot "$NAME"; hb
  CAP=$(cat "$QA/capture_6_${NAME}.txt")
  say "B/$NAME firing (load=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0))"
  rm -f "$QA/crop_6_${NAME}_judge.txt"
  cd "$PROJ" && timeout 1700 bash scripts/16_vision_gate.sh python3 "$SCRIPT" comparison \
    "$QA/crop_6_${NAME}_render.png" "$QA/crop_6_${NAME}_orig.png" \
    --view "Slide 049 zoomed crop ${NAME} - render vs original at matched scale (attempt 6)" \
    --capture "$CAP" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript "$QA/crop_6_${NAME}_judge.txt" \
    -p "$(cat "$QA/crop_prompt_6_${NAME}.txt")" \
    > "$QA/crop_6_${NAME}_dispatch.log" 2>&1
  rc=$?
  say "B/$NAME rc=$rc transcript=$(wc -c < "$QA/crop_6_${NAME}_judge.txt" 2>/dev/null || echo 0)B"
  if [ -s "$QA/crop_6_${NAME}_judge.txt" ]; then
    say "B/$NAME VERDICT: $(grep -o 'FINAL VERDICT: [A-Z]*' "$QA/crop_6_${NAME}_judge.txt" | tail -1)"
  else
    say "B/$NAME produced no transcript - banked in crop_6_${NAME}_dispatch.log"
  fi
done
say "=== leg B done ==="
