#!/usr/bin/env bash
# verify-wing slide 11 corroboration read — fresh original-first comparison of
# unique_slides/slide_011.jpg vs qa/slide011/render_12.png (render of CURRENT pptx).
set -u
REPO=/home/codespace/ai_llm_slides
V=$REPO/videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
QA=$V/recreated_pptx/qa/slide011
VERIFY=$QA/judge_verify_12.txt
RUNLOG=$QA/judge_verify_12_run.log
WLOG=$V/pool_run/verify_wing_11.log

log() { echo "[$(date '+%F %T')] $*" >>"$WLOG"; }

log "verify-wing slide-11: sleeping 100s before gateway call"
sleep 100

for i in $(seq 1 8); do
  log "slide-11 corroboration attempt $i/8 (timeout 540)"
  ( cd "$REPO" && bash scripts/16_vision_gate.sh timeout 540 "$PY" \
      .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$V/unique_slides/slide_011.jpg" "$QA/render_12.png" \
      --view "Slide 11 recreation — INDEPENDENT corroboration read vs original lecture frame" \
      --capture "IMG1=original lecture video frame (ground truth, read first); IMG2=150dpi PNG render of a 13.33x7.5in PPTX recreation (read second)" \
      --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
      --transcript "$VERIFY" \
      -p "$(cat "$V/pool_run/judge_prompt_template.txt")" ) >"$RUNLOG" 2>&1
  rc=$?
  v=$("$PY" "$V/pool_run/verdict.py" "$VERIFY" 2>/dev/null)
  [ -n "$v" ] || v=NONE
  log "slide-11 attempt $i rc=$rc verdict=$v"
  if [ "$v" = "PASS" ] || [ "$v" = "FAIL" ]; then
    log "slide-11 corroboration finished with verdict=$v"
    exit 0
  fi
  if grep -qi "429\|rate.limit\|too many requests" "$RUNLOG"; then
    log "slide-11 attempt $i hit 429 — sleeping 300s before retry"
    sleep 300
  else
    log "slide-11 attempt $i infra failure (rc=$rc) — sleeping 60s before retry"
    sleep 60
  fi
done
log "slide-11 corroboration exhausted 8 attempts without a verdict"
exit 1
