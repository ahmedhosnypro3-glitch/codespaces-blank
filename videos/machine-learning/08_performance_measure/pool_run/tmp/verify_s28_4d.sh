#!/usr/bin/env bash
# VERIFY-WING runner — slide 28 corroboration read (fresh, original-first).
# Banks transcript to recreated_pptx/qa/slide028/judge_verify_4d.txt.
set -uo pipefail
REPO=/home/codespace/ai_llm_slides
VD=$REPO/videos/machine-learning/08_performance_measure
PYBIN=/home/codespace/.pyenv/versions/3.15.2/bin/python3
ANALYZE=$REPO/.agents/skills/image-analysis/scripts/analyze_image.py
ORIG=$VD/unique_slides/slide_028-.jpg
RENDER=$VD/recreated_pptx/qa/slide028/render_3.png
VERIFY=$VD/recreated_pptx/qa/slide028/judge_verify_4d.txt
PROMPT=$VD/pool_run/judge_prompt_template.txt
LOG=$VD/pool_run/tmp/verify_s28_4d.log

echo "[$(date '+%F %T')] verify-wing slide 28: sleeping 240s before first gateway call" >>"$LOG"
sleep 240

cd "$REPO"
for i in $(seq 1 8); do
  echo "[$(date '+%F %T')] attempt $i/8: launching comparison (IMG1=original, IMG2=render_3.png)" >>"$LOG"
  out=$(bash scripts/16_vision_gate.sh timeout 540 "$PYBIN" "$ANALYZE" comparison "$ORIG" "$RENDER" \
    --view "Slide 28 recreation — INDEPENDENT corroboration read vs original lecture frame" \
    --capture "IMG1=original lecture video frame (ground truth, read first); IMG2=150dpi PNG render of a 13.33x7.5in PPTX recreation (read second)" \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    --transcript "$VERIFY" \
    -p "$(cat "$PROMPT")" 2>&1)
  rc=$?
  printf '%s\n' "$out" >>"$LOG"
  v=$("$PYBIN" "$VD/pool_run/verdict.py" "$VERIFY" 2>/dev/null || echo NONE)
  echo "[$(date '+%F %T')] attempt $i rc=$rc verdict=$v" >>"$LOG"
  if [ "$v" = "PASS" ] || [ "$v" = "FAIL" ]; then
    echo "[$(date '+%F %T')] banked transcript with verdict $v — stopping retry loop" >>"$LOG"
    break
  fi
  if printf '%s' "$out" | grep -qiE '429|too many requests|rate.?limit'; then
    echo "[$(date '+%F %T')] 429 detected — sleeping 300s before retry" >>"$LOG"
    sleep 300
  else
    echo "[$(date '+%F %T')] non-429 failure — short backoff 30s before retry" >>"$LOG"
    sleep 30
  fi
done
echo "[$(date '+%F %T')] runner done. final verdict=$("$PYBIN" "$VD/pool_run/verdict.py" "$VERIFY" 2>/dev/null || echo NONE) transcript=$VERIFY" >>"$LOG"
