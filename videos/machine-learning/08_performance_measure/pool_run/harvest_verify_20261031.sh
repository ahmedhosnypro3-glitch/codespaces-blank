#!/usr/bin/env bash
# harvest_verify_20261031.sh — verdict harvester for 08_performance_measure.
# For each qa/slideNNN with a judge_attempt_* PASS but no judge_verify_* PASS,
# run the corroboration verify judge (IMG1=original, IMG2=render.png) into
# judge_verify_<nextK>.txt. Pacing: 90-150s before heavy calls, 300s on
# 429/HangError (max 8 retries per slide). Never deletes evidence.
set -uo pipefail
REPO=/home/codespace/ai_llm_slides
NS=$REPO/videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa
LOG=$NS/pool_run/harvest_verify_20261031.log
ANALYZE=$REPO/.agents/skills/image-analysis/scripts/analyze_image.py
PROMPT_FILE=$NS/pool_run/judge_prompt_template.txt

log() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }
DONE_FILE=$NS/pool_run/harvest_verify_20261031.done
touch "$DONE_FILE"
# already_judged <num> <passfile> — skip if this exact PASS attempt was judged already
already_judged() { grep -qF "$1|$2" "$DONE_FILE" 2>/dev/null; }
mark_judged() { echo "$1|$2" >>"$DONE_FILE"; }

find_original() {
  local num=$1 padded
  padded=$(printf '%03d' "$num")
  local f
  for f in "$NS/unique_slides/slide_${padded}.jpg" "$NS/unique_slides/slide_${padded}"-*.jpg; do
    [ -f "$f" ] && { printf '%s' "$f"; return 0; }
  done
  return 1
}

has_pass() { grep -l "FINAL VERDICT: PASS" "$@" 2>/dev/null | head -1; }

next_k() {
  local d=$1 max=0 f b k
  for f in "$d"/judge_verify_*.txt; do
    [ -e "$f" ] || continue
    b=$(basename "$f"); k=${b#judge_verify_}; k=${k%.txt}
    case "$k" in ''|*[!0-9]*) continue ;; esac
    [ "$k" -gt "$max" ] && max=$k
  done
  echo $((max+1))
}

scan() {
  local d base digits num pf
  for d in "$QA"/slide*/; do
    [ -d "$d" ] || continue
    base=$(basename "$d")
    digits=$(printf '%s' "$base" | tr -cd '0-9')
    [ -n "$digits" ] || continue
    num=$((10#$digits))
    pf=$(has_pass "$d"judge_attempt_*.txt 2>/dev/null)
    [ -n "$pf" ] || continue
    [ -z "$(has_pass "$d"judge_verify_*.txt 2>/dev/null)" ] || continue
    already_judged "$num" "$(basename "$pf")" && continue
    echo "$num|$d|$pf"
  done
}

run_verify() {
  local num=$1 d=$2 orig render out tries=0 rc
  orig=$(find_original "$num") || { log "slide $num: original frame missing, skip"; return 1; }
  render=$d/render.png
  if [ ! -f "$render" ]; then
    log "slide $num: render.png missing, skip"
    return 1
  fi
  local k; k=$(next_k "$d")
  out=$d/judge_verify_${k}_hv.txt
  while :; do
    tries=$((tries+1))
    local nap=$((90 + RANDOM % 61))
    log "slide $num: verify call -> $(basename "$out") (try $tries, nap ${nap}s)"
    sleep "$nap"
    ( cd "$REPO" && timeout 540 python3 "$ANALYZE" comparison \
        "$orig" "$render" \
        --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
        -p "$(cat "$PROMPT_FILE")" \
        > "$out" 2>&1 )
    rc=$?
    if grep -qiE '429|rate.?limit|HangError|ServiceTimeout' "$out" 2>/dev/null && [ $tries -lt 8 ]; then
      log "slide $num: throttled/err (rc=$rc) — sleep 300 and retry ($tries/8)"
      sleep 300
      continue
    fi
    if [ $rc -ne 0 ] && [ $tries -lt 8 ] && ! grep -q "FINAL VERDICT" "$out" 2>/dev/null; then
      log "slide $num: call failed rc=$rc without verdict — sleep 300 and retry ($tries/8)"
      sleep 300
      continue
    fi
    break
  done
  if grep -q "FINAL VERDICT: PASS" "$out" 2>/dev/null; then
    log "slide $num: verify PASS ($(basename "$out"))"
  elif grep -q "FINAL VERDICT" "$out" 2>/dev/null; then
    log "slide $num: verify verdict non-PASS ($(basename "$out"))"
  else
    log "slide $num: verify produced no verdict rc=$rc ($(basename "$out"))"
  fi
}

log "harvest run starting"
while :; do
  found=$(scan)
  if [ -z "$found" ]; then
    log "scan: no uncorroborated PASS slides remain"
    break
  fi
  log "scan found candidates: $(echo "$found" | cut -d'|' -f1 | tr '\n' ' ')"
  while IFS='|' read -r num d pf; do
    [ -n "$num" ] || continue
    # re-check inside the loop in case a previous pass landed a verify PASS
    [ -z "$(has_pass "$d"judge_verify_*.txt 2>/dev/null)" ] || continue
    mark_judged "$num" "$(basename "$pf")"
    run_verify "$num" "$d"
    sleep 60
  done <<<"$found"
  log "scan cycle done; sleeping 60s before rescan"
  sleep 60
done
log "harvest run finished"
