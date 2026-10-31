#!/usr/bin/env bash
# Detached single-slide judge runner. Retries until a terminal verdict or MAX attempts.
# Designed to be launched with nohup so an agent's own 2h cap can never kill an
# in-flight judge: the runner lives on, the transcript is banked to a file.
#
# Usage: judge_one_slide.sh <NNN> <render_png> [outdir] [max_attempts]
# Exit: 0 = PASS, 10 = FAIL verdict, 2 = usage/IO error, 1 = exhausted (debt)
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
N="${1:-}"; RENDER="${2:-}"; OUTDIR="${3:-qa/slide${N}/rejudge}"; MAX="${4:-8}"
[ -n "$N" ] && [ -n "$RENDER" ] || { echo "usage: judge_one_slide.sh <NNN> <render.png> [outdir] [max]" >&2; exit 2; }
[ -f "$RENDER" ] || { echo "ABORT: render not found: $RENDER" >&2; exit 2; }
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
mkdir -p "$OUTDIR"
LOG="$OUTDIR/judge_runner.log"
# gate budget shared across the namespace's lanes; the gate itself enforces N
export VISION_SLOTS="${VISION_GATE_SLOTS:-3}"
att=0
while [ "$att" -lt "$MAX" ]; do
  att=$((att+1))
  F="$OUTDIR/judge_attempt_${att}.txt"
  if [ -e "$F" ]; then
    # an earlier attempt already wrote this slot — check it before reusing
    if grep -q 'FINAL VERDICT: PASS' "$F"; then echo "PASS (pre-existing $F)" >> "$LOG"; exit 0; fi
    if grep -q 'FINAL VERDICT: FAIL' "$F"; then echo "FAIL (pre-existing $F)" >> "$LOG"; exit 10; fi
    continue
  fi
  echo "=== slide $N attempt $att start $(date '+%F %T') ===" >> "$LOG"
  bash _pool/vision_gate.sh python3 -u "$SKILL/scripts/analyze_image.py" comparison \
    "$RENDER" "unique_slides/slide_${N}.jpg" \
    --max-tokens 24000 --timeout 780 --rounds 1 --tries 1 \
    --view "Slide $N recreation render vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    -p "$(cat judge_template.txt)" > "$F" 2>&1
  rc=$?
  echo "rc=$rc bytes=$(wc -c < "$F") winners=$(grep -c '\[winner\]' "$F" 2>/dev/null) verdict=$(grep -o 'FINAL VERDICT: [A-Z]*' "$F" 2>/dev/null | tail -1) end=$(date '+%F %T')" >> "$LOG"
  if grep -q 'FINAL VERDICT: PASS' "$F"; then echo "VERDICT PASS $N attempt $att" >> "$LOG"; exit 0; fi
  if grep -q 'FINAL VERDICT: FAIL' "$F"; then echo "VERDICT FAIL $N attempt $att" >> "$LOG"; exit 10; fi
  echo "no terminal verdict — storm sleep 120" >> "$LOG"
  sleep 120
done
echo "VERDICT DEBT $N (no terminal verdict in $MAX attempts)" >> "$LOG"
exit 1
