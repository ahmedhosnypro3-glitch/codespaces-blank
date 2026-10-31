#!/bin/bash
# Sweeper #5: certify+merge loop. Every ~60s scans for dual-PASS uncertified
# slides; appends verification_ledger.md row under flock (only if no PASS row
# exists for that slide yet), merges into the final deck, marks scope done in
# mission.db (sleep 5 on lock). Never rebuilds/re-judges, never deletes evidence.
set -u
cd /home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
SLEEP=${1:-60}
LOG=pool_run/sweeper5.log
LED=pool_run/verification_ledger.md

while true; do
  echo "[$(date -u +%H:%M:%S)] iteration scan" >> "$LOG"
  while IFS=$'\t' read -r n att ver; do
    [ -z "$n" ] && continue
    pptx=$(printf 'recreated_pptx/slide_%03d_recreated.pptx' "$n")
    if [ ! -f "$pptx" ]; then
      echo "[$(date -u +%H:%M:%S)] slide $n: pptx missing ($pptx), skip" >> "$LOG"
      continue
    fi
    cert=$(python3 -c "
import json
d=json.load(open('final_deck_ledger.json'))
print('yes' if any(p['slide_num']==$n and p['status']=='certified' for p in d['pages']) else 'no')")
    if [ "$cert" = "yes" ]; then
      echo "[$(date -u +%H:%M:%S)] slide $n already certified, skip" >> "$LOG"
      continue
    fi
    row="| $n | $att | $ver | PASS/PASS (original-first, dual-read) |  | certified=yes | sweeper-5 |"
    have_row=$( ( flock -x 9
      grep -E "^\| $n \|" "$LED" | grep -v FAIL || true
    ) 9>>pool_run/.verification_ledger.lock )
    if [ -n "$have_row" ]; then
      echo "[$(date -u +%H:%M:%S)] slide $n already has PASS ledger row, skip append" >> "$LOG"
    else
      ( flock -x 9; printf '%s\n' "$row" >> "$LED" ) 9>>pool_run/.verification_ledger.lock
      echo "[$(date -u +%H:%M:%S)] slide $n ledger row appended: $row" >> "$LOG"
    fi
    if python3 pool_run/merge_final_deck.py update "$n" "$pptx" 08-performance_final.pptx >> "$LOG" 2>&1; then
      echo "[$(date -u +%H:%M:%S)] slide $n merged into 08-performance_final.pptx page $n" >> "$LOG"
    else
      echo "[$(date -u +%H:%M:%S)] slide $n MERGE FAILED" >> "$LOG"
      continue
    fi
    for try in 1 2 3 4 5 6; do
      if sqlite3 pool_run/mission.db "UPDATE scopes SET status='done', note='sweeper-5 certified+merged: dual-PASS ($att + $ver), ledger row appended, merged to final deck page $n', updated_at=datetime('now') WHERE name='slide-$n';" 2>>"$LOG"; then
        echo "[$(date -u +%H:%M:%S)] slide $n scope slide-$n marked done" >> "$LOG"
        break
      else
        echo "[$(date -u +%H:%M:%S)] slide $n db lock, sleep 5 (try $try)" >> "$LOG"
        sleep 5
      fi
    done
    cert2=$(python3 -c "
import json
d=json.load(open('final_deck_ledger.json'))
print('yes' if any(p['slide_num']==$n and p['status']=='certified' for p in d['pages']) else 'no')")
    echo "[$(date -u +%H:%M:%S)] slide $n ledger now certified=$cert2" >> "$LOG"
  done < <(python3 pool_run/sweeper5_scan.py)
  sleep "$SLEEP"
done
