#!/usr/bin/env bash
# verify-wing slide 34 corroboration read — fresh original-first comparison of
# unique_slides/slide_034.jpg vs qa/slide034/render.png (fresh render of the
# CURRENT slide_034_recreated.pptx). Transcript: judge_verify_7.txt.
set -u
REPO=/home/codespace/ai_llm_slides
V=$REPO/videos/machine-learning/08_performance_measure
QA=$V/recreated_pptx/qa/slide034
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
VERIFY=$QA/judge_verify_7.txt
RUNLOG=$QA/judge_verify_7_run.log
WLOG=$V/pool_run/verify_wing_34.log

log() { echo "[$(date '+%F %T')] $*" >>"$WLOG"; }

# 1. Fresh render of the current deliverable pptx -> render.png
SCRATCH=$V/pool_run/tmp/render34_$$
mkdir -p "$SCRATCH"
soffice --headless -env:UserInstallation=file://$SCRATCH/lo --convert-to pdf --outdir "$SCRATCH" "$V/recreated_pptx/slide_034_recreated.pptx" >>"$WLOG" 2>&1
pdftoppm -png -r 150 "$SCRATCH/slide_034_recreated.pdf" "$SCRATCH/slide" >>"$WLOG" 2>&1
cp "$SCRATCH/slide-1.png" "$QA/render.png"
log "render.png refreshed from current pptx: $(md5sum "$QA/render.png")"
rm -rf "$SCRATCH"

# 2. Pre-heavy-call pause
log "sleeping 120s before heavy call"
sleep 120

# 3. Corroboration judge loop (429/HangError -> sleep 300, retry up to 8x)
for i in $(seq 1 8); do
  log "slide-34 corroboration attempt $i/8 (timeout 540)"
  ( cd "$REPO" && timeout 540 python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$V/unique_slides/slide_034.jpg" "$QA/render.png" \
      --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 ) >"$VERIFY" 2>"$RUNLOG"
  rc=$?
  v=$("$PY" "$V/pool_run/verdict.py" "$VERIFY" 2>/dev/null)
  [ -n "$v" ] || v=NONE
  log "slide-34 attempt $i rc=$rc verdict=$v"
  if [ "$v" = "PASS" ] || [ "$v" = "FAIL" ]; then
    log "slide-34 corroboration finished with verdict=$v"
    exit 0
  fi
  if grep -qiE "429|rate.?limit|too many requests|HangError" "$RUNLOG" "$VERIFY" 2>/dev/null; then
    log "slide-34 attempt $i hit 429/HangError — sleeping 300s before retry"
    sleep 300
  else
    log "slide-34 attempt $i infra failure (rc=$rc) — sleeping 60s before retry"
    sleep 60
  fi
done
log "slide-34 corroboration exhausted 8 attempts without a verdict"
exit 1
