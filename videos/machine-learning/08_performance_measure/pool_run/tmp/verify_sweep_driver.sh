#!/usr/bin/env bash
# verify_sweep_driver.sh — sequential corroboration reads for slides 11,13,17,25.
# 240s sleep before the first vision call; 200s spacing between calls.
set -u
VD=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
RUNNER=$VD/pool_run/tmp/verify_sweep_runner.sh
QA=$VD/recreated_pptx/qa
DRIVER_LOG=$VD/pool_run/tmp/verify_sweep_driver.log
log(){ echo "[$(date '+%F %T')] $*" >>"$DRIVER_LOG"; }

run_slide(){
  local num=$1 orig=$2 render=$3 verify=$4
  local rlog=$VD/pool_run/tmp/verify_sweep_slide${num}.log
  log "slide $num: launching corroboration (verify=$(basename "$verify"), render=$(basename "$render"))"
  bash "$RUNNER" "$num" "$orig" "$render" "$verify" "$rlog"
  local rc=$?
  log "slide $num: runner rc=$rc $(grep -a '^VERDICT=' "$rlog" | tail -1)"
}

log "driver start — sleeping 240s before first vision call"
sleep 240
run_slide 11 "$VD/unique_slides/slide_011.jpg" "$QA/slide011/render_10.png" "$QA/slide011/judge_verify_7.txt"
log "sleeping 200s between vision calls"; sleep 200
run_slide 13 "$VD/unique_slides/slide_013.jpg" "$QA/slide013/render_8.png"  "$QA/slide013/judge_verify_7.txt"
log "sleeping 200s between vision calls"; sleep 200
run_slide 17 "$VD/unique_slides/slide_017.jpg" "$QA/slide017/render_8.png"  "$QA/slide017/judge_verify_1.txt"
log "sleeping 200s between vision calls"; sleep 200
run_slide 25 "$VD/unique_slides/slide_025.jpg" "$QA/slide025/render_8.png"  "$QA/slide025/judge_verify_7.txt"
log "driver done"
