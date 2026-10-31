#!/usr/bin/env bash
# sweeper_cert_loop.sh — certify-and-merge sweeper for 08_performance_measure.
# Loop: scan qa dirs; certify dual-PASS uncertified slides (flock ledger row,
# merge update, mission.db done); kick verify judges for fresh attempt-PASS
# slides missing a verify PASS; sleep 60s; rescan until 37/37 certified.
set -u
NS="/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
cd "$NS"
LOG="pool_run/sweeper_cert.log"
log() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }

log "sweeper_cert start"
ITER=0
while true; do
  ITER=$((ITER+1))
  SCAN=$(python3 pool_run/sweeper_cert_scan.py 2>>"$LOG")
  CERT=$(python3 -c "import json,sys;print(' '.join(map(str,json.load(sys.stdin)['certified'])))" <<<"$SCAN")
  NCERT=$(python3 -c "import json,sys;print(len(json.load(sys.stdin)['certified']))" <<<"$SCAN")
  log "iter $ITER certified=$NCERT/37 [$CERT]"
  [ "$NCERT" -eq 37 ] && { log "ALL 37 CERTIFIED — sweeper done"; break; }

  # --- certify dual-PASS slides ---
  python3 -c "
import json,sys
for c in json.load(sys.stdin)['certifiable']:
    print(c['n'], c['attempts'][-1], c['verifies'][-1])
" <<<"$SCAN" | while IFS=' ' read -r n att ver; do
    [ -z "$n" ] && continue
    pptx="recreated_pptx/slide_$(printf '%03d' "$n")_recreated.pptx"
    [ -f "$pptx" ] || { log "slide $n candidate but pptx missing — skip"; continue; }
    flock pool_run/verification_ledger.md bash -c '
      n="$1"; att="$2"; ver="$3"; ns="$4"
      if awk -v n="$n" -F"|" "\$2 ~ (\"^ *\" n \" *\$\") {v=\$5; gsub(/ /,\"\",v); if (v ~ /PASS/ && v !~ /FAIL/ && \$0 !~ /superseded/) found=1} END{exit !found}" pool_run/verification_ledger.md; then
        exit 0
      fi
      reana="—"
      [ -f "analysis/reanalysis/slide_$(printf %03d "$n")_raw.json" ] && reana="analysis/reanalysis/slide_$(printf %03d "$n")_raw.json"
      printf "| %s | %s | %s | PASS / PASS (original-first dual-read; sweeper-cert) | %s | yes | |\n" "$n" "$att" "$ver" "$reana" >> pool_run/verification_ledger.md
    ' _ "$n" "$att" "$ver" "$NS"
    python3 pool_run/merge_final_deck.py update "$n" "$pptx" 08-performance_final.pptx >>"$LOG" 2>&1 \
      && log "slide $n merge update OK" || log "slide $n merge update FAILED"
    for i in 1 2 3 4 5; do
      sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-$n';" 2>>"$LOG" && break
      sleep 5
    done
    log "slide $n scope done (att=$att ver=$ver)"
  done

  # --- kick verify judges for fresh attempt-PASS slides missing verify ---
  python3 -c "
import json,sys
for c in json.load(sys.stdin)['needs_verify']:
    print(c['n'], c['attempt'].replace('judge_attempt_','').replace('.txt',''), c['render_path'])
" <<<"$SCAN" | while IFS=' ' read -r n att render; do
    [ -z "$n" ] && continue
    if pgrep -f "sweeper_verify_one.sh $n " >/dev/null 2>&1; then
      log "slide $n verify already in flight — skip"
      continue
    fi
    nohup bash pool_run/sweeper_verify_one.sh "$n" "$att" "$render" >>"pool_run/verify_sw_${n}.log" 2>&1 &
    log "slide $n verify kicked (attempt=$att render=$render pid=$!)"
  done

  sleep 60
done
