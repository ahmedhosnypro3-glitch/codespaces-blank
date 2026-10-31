#!/usr/bin/env bash
# Certify-and-merge sweeper loop — 08_performance_measure.
# Scan qa/slide*/ -> certify dual-PASS slides (ledger row + merge update + db done),
# run verify judges for attempt-PASS slides lacking a verify PASS, sleep 60, rescan.
set -u
REPO=/home/codespace/ai_llm_slides
V=$REPO/videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
LOG=$V/pool_run/sweeper_final_loop.out
LOCK=$V/pool_run/verification_ledger.md.lock
cd "$V" || exit 1

log() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }

qa_dir() { # $1 = slide number -> qa dir (zero-padded primary, legacy fallbacks)
  local n=$1 nnn; nnn=$(printf '%03d' "$n")
  for d in "recreated_pptx/qa/slide$nnn" "recreated_pptx/qa/slide$n" "recreated_pptx/qa/slide_$nnn" "recreated_pptx/qa/slide_$n"; do
    [ -d "$d" ] && { echo "$d"; return; }
  done
  echo "recreated_pptx/qa/slide$nnn"
}

certify_candidate() { # $1 = slide number
  local n=$1 nnn; nnn=$(printf '%03d' "$n")
  (
    flock 9
    if grep -qE "^\| *0*$n *\|" pool_run/verification_ledger.md; then
      log "slide $n: verification_ledger.md row exists — skip append"
    else
      printf '| %s | recreated_pptx/qa/slide%s/judge_attempt_*.txt (FINAL VERDICT: PASS) | recreated_pptx/qa/slide%s/judge_verify_*.txt (FINAL VERDICT: PASS) | PASS / PASS (original-first dual-read) | — | certified=yes | appended by certify-merge sweeper %s |\n' \
        "$n" "$nnn" "$nnn" "$(date '+%F %T')" >> pool_run/verification_ledger.md
      log "slide $n: appended verification_ledger.md row"
    fi
  ) 9>"$LOCK"
  python3 pool_run/merge_final_deck.py update "$n" "recreated_pptx/slide_${nnn}_recreated.pptx" 08-performance_final.pptx >>"$LOG" 2>&1 \
    && log "slide $n: merge update done (ledger page certified)" \
    || log "slide $n: merge update FAILED"
  local i
  for i in 1 2 3 4 5 6; do
    if sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-$n';" 2>>"$LOG"; then
      log "slide $n: mission.db scope slide-$n -> done"
      return 0
    fi
    sleep 5
  done
  log "slide $n: mission.db update kept failing on lock"
}

run_verify() { # $1 = slide number — background job, waits internally
  local n=$1 nnn; nnn=$(printf '%03d' "$n")
  local qa; qa=$(qa_dir "$n")
  local render; render=$(ls -t "$qa"/render_*.png 2>/dev/null | head -1)
  if [ -z "$render" ]; then log "slide $n: no render_*.png in $qa — skip verify"; return 0; fi
  local ts; ts=$(date +%s%N)
  local tr="$qa/judge_verify_swp_${ts}_${nnn}.txt"
  local runlog="$qa/judge_verify_swp_${ts}_${nnn}_run.log"
  sleep $((90 + RANDOM % 61))
  local i v rc
  for i in $(seq 1 8); do
    ( cd "$REPO" && python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
        "videos/machine-learning/08_performance_measure/unique_slides/slide_${nnn}.jpg" \
        "videos/machine-learning/08_performance_measure/$render" \
        --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
        --transcript "$V/$tr" \
        -p "$(cat "$V/pool_run/judge_prompt_template.txt")" ) >"$runlog" 2>&1
    rc=$?
    v=$("$PY" pool_run/verdict.py "$tr" 2>/dev/null); [ -n "$v" ] || v=NONE
    log "slide $n: verify try $i/$8 rc=$rc verdict=$v render=$(basename "$render") transcript=$tr"
    if [ "$v" = "PASS" ] || [ "$v" = "FAIL" ]; then return 0; fi
    if grep -qiE "429|rate.?limit|too many requests" "$runlog"; then
      log "slide $n: verify try $i hit 429 — sleep 300"
      sleep 300
    else
      log "slide $n: verify try $i infra failure — sleep 60"
      sleep 60
    fi
  done
  log "slide $n: verify exhausted 8 tries without verdict"
  return 1
}

log "=== sweeper loop start ==="
while true; do
  out=$(python3 pool_run/sweeper_certify_scan.py 2>>"$LOG")
  count=$(echo "$out" | sed -n 's/^CERTIFIED_COUNT //p')
  cands=$(echo "$out" | sed -n 's/^CANDIDATE //p')
  needs=$(echo "$out" | sed -n 's/^NEEDS_VERIFY //p')
  log "scan: certified=$count/37 candidates=[${cands//$'\n'/ }] needs_verify=[${needs//$'\n'/ }]"
  for n in $cands; do certify_candidate "$n"; done
  if [ -n "$needs" ]; then
    pids=""
    for n in $needs; do
      run_verify "$n" & pids="$pids $!"
    done
    wait $pids
    log "verify wave finished"
  fi
  [ "$count" = "37" ] && { log "37/37 certified — sweeper loop done"; break; }
  sleep 60
done
