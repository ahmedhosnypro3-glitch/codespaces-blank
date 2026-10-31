#!/usr/bin/env bash
# verify_sweep_runner.sh — ONE corroboration read for a slide, with 429 retry.
# usage: verify_sweep_runner.sh <num> <orig.jpg> <render.png> <verify.txt> <run.log>
# Verdict loop: up to 8 tries; on 429 (or no verdict) sleep 300s before retry.
set -u
REPO=/home/codespace/ai_llm_slides
VD=$REPO/videos/machine-learning/08_performance_measure
PYBIN=/home/codespace/.pyenv/versions/3.15.2/bin/python3
GATE=$REPO/scripts/16_vision_gate.sh
ANALYZE=$REPO/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT=$VD/pool_run/judge_prompt_template.txt
NUM=$1; ORIG=$2; RENDER=$3; VERIFY=$4; LOG=$5
MAX=8
for i in $(seq 1 $MAX); do
  echo "[$(date '+%F %T')] corroboration attempt $i/$MAX start (render=$(basename "$RENDER"))" >>"$LOG"
  ( cd "$REPO" && bash "$GATE" timeout 540 "$PYBIN" "$ANALYZE" comparison "$ORIG" "$RENDER" \
      --view "Slide $NUM recreation — INDEPENDENT corroboration read vs original lecture frame" \
      --capture "IMG1=original lecture video frame (ground truth, read first); IMG2=150dpi PNG render of a 13.33x7.5in PPTX recreation (read second)" \
      --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
      --transcript "$VERIFY" \
      -p "$(cat "$PROMPT")" ) >>"$LOG" 2>&1
  rc=$?
  v=$("$PYBIN" "$VD/pool_run/verdict.py" "$VERIFY" 2>/dev/null || true)
  [ -n "$v" ] || v=NONE
  echo "[$(date '+%F %T')] attempt $i rc=$rc verdict=$v" >>"$LOG"
  if [ "$v" = "PASS" ] || [ "$v" = "FAIL" ]; then
    echo "VERDICT=$v" >>"$LOG"
    exit 0
  fi
  if [ "$i" -lt "$MAX" ]; then
    if tail -60 "$LOG" | grep -aq "429\|rate_limit"; then
      echo "[$(date '+%F %T')] 429 detected — sleep 300s before retry $((i+1))" >>"$LOG"
      sleep 300
    else
      echo "[$(date '+%F %T')] no verdict (hang/abort) — sleep 120s before retry $((i+1))" >>"$LOG"
      sleep 120
    fi
  fi
done
echo "VERDICT=EXHAUSTED" >>"$LOG"
exit 1
