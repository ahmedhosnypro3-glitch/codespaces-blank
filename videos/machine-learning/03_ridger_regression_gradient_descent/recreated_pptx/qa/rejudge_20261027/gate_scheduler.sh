#!/bin/bash
# gate_scheduler.sh — merge-gate scheduler (agent-408). Poll 5 min up to 3h;
# restage md5-mismatched ledger pages (except page 10 SKIP) once DB is 51/51;
# then run the FULL 51-page merge gate and bank the result. No git, no deletes.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent
D=$NS/recreated_pptx/build/final_deck
RJ=$NS/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/gate_scheduler.log
FINAL=$RJ/merge_gate_FINAL.md
DB=$NS/slides_progress.db
DECK=$NS/recreated_pptx/03_ridger_regression_gradient_descent_final.pptx
GATES=$NS/recreated_pptx/qa/final_deck_updates
POLL=300
DEADLINE=$(( SECONDS + 10800 ))  # 3h
START=$(date -u +%FT%TZ)

log(){ echo "$(date -u +%FT%TZ) $*" >> "$LOG"; }

dbcount(){
  sqlite3 "$DB" ".timeout 20000" "SELECT COUNT(*) FROM slides WHERE gen_status='passed' AND visual_check='PASS';" 2>/dev/null
}

mismatches(){  # ledger source_md5 != disk md5, page 10 SKIPped
  python3 - "$NS" <<'EOF'
import json, hashlib, os, sys
NS = sys.argv[1]
s = json.load(open(NS + "/recreated_pptx/final_deck_state.json"))
def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()
out = []
for k, v in sorted(s["pages"].items(), key=lambda kv: int(kv[0])):
    n = int(k)
    if n == 10:
        continue
    p = v["source_pptx"].replace("/home/ahmed/Projects/ai_llm_slides", "/home/codespace/ai_llm_slides")
    if (not os.path.exists(p)) or md5(p) != v["source_md5"]:
        out.append(n)
print(" ".join(map(str, out)))
EOF
}

profile_busy(){
  if pgrep -f 's21_lo_profile_299640' >/dev/null 2>&1; then echo yes; else echo no; fi
}

log "=== gate_scheduler start pid=$$ started=$START deadline=+10800s poll=${POLL}s ==="

while [ $SECONDS -lt $DEADLINE ]; do
  db=$(dbcount); mis=$(mismatches); busy=$(profile_busy)
  log "poll db51='$db' mismatches_excl_p10='$mis' lo_profile_busy=$busy"

  if [ "$db" = "51" ]; then
    if [ -n "$mis" ] && [ "$busy" = "yes" ]; then
      log "  db=51 but shared LO profile busy — restage deferred to next poll"
    elif [ -n "$mis" ]; then
      for n in $mis; do
        log "  restage page $n: final_deck_tool.py update $n && render_check_pages.py $n"
        ( cd "$D" && python3 final_deck_tool.py update "$n" && python3 render_check_pages.py "$n" ) >> "$LOG" 2>&1
        log "  restage page $n done exit=$?"
      done
      mis=$(mismatches)
      log "  after restage mismatches_excl_p10='$mis'"
    fi

    if [ -z "$mis" ] && [ "$busy" = "yes" ]; then
      log "  md5-clean but shared LO profile busy — gate deferred to next poll"
    fi

    if [ -z "$mis" ] && [ "$busy" = "no" ]; then
      log "  ENTRY CONDITIONS MET (db=51, all ledger source_md5 == disk md5 except p10 SKIP, LO profile quiescent) — RUNNING FULL MERGE GATE"
      before=$(ls "$GATES" 2>/dev/null | sort)
      gstart=$(date -u +%FT%TZ)
      ( cd "$D" && python3 render_check_pages.py $(seq 1 51) ) >> "$LOG" 2>&1
      EXIT=$?
      gend=$(date -u +%FT%TZ)
      log "  MERGE GATE finished $gend EXIT=$EXIT (started $gstart)"

      ( cd "$D" && python3 final_deck_tool.py verify-structure ) >> "$LOG" 2>&1
      VEXIT=$?
      log "  verify-structure EXIT=$VEXIT"

      newdir=$(comm -13 <(echo "$before") <(ls "$GATES" 2>/dev/null | sort) | head -1)
      [ -z "$newdir" ] && newdir=$(ls -t "$GATES" 2>/dev/null | head -1)
      GR="$GATES/$newdir/gate_report.txt"
      deckmd5=$(md5sum "$DECK" | awk '{print $1}')
      echo "$deckmd5  $DECK" > "$DECK.md5"
      log "  deck md5=$deckmd5 banked to $DECK.md5"

      if [ -f "$GR" ]; then
        nfail=$(grep -c ': FAIL' "$GR")
        faillist=$(grep ': FAIL' "$GR" | sed 's/:.*//;s/page //' | tr '\n' ' ')
      else
        nfail="?"; faillist="(no gate_report.txt written — gate died before report, see log)"
      fi
      log "  gate dir=$newdir report=$GR mismatched=${nfail}/51 pages='$faillist'"

      {
        echo "# merge_gate_FINAL.md — S9 merge gate result (scheduler pid $$, started $START)"
        echo
        echo "- Gate run: $gstart → $gend UTC, from \$D = $D"
        echo "- Command: cd \$D && python3 render_check_pages.py 1 2 ... 51 (one LO session, 150dpi, PIL 0-px diff per page)"
        echo "- EXIT code: $EXIT"
        echo "- verify-structure EXIT: $VEXIT"
        echo "- Mismatched pages: ${nfail}/51"
        if [ "$nfail" != "0" ] && [ "$nfail" != "?" ]; then
          echo "- Mismatch list: $faillist"
          echo "- Per-page detail: $GR"
        fi
        echo "- Deck: $DECK"
        echo "- Deck md5 (post-gate): $deckmd5"
        echo "- gate_report.txt: $GR"
        echo "- Gate artifacts dir: $GATES/$newdir"
        echo
        echo "Entry conditions at gate time: DB gen_status='passed' AND visual_check='PASS' count = 51/51;"
        echo "all ledger pages source_md5 == disk md5 except page 10 (SKIP per instruction); shared LO profile quiescent."
        echo
        echo "Per task: the deck is NOT declared closed here — this file banks the gate result only."
      } > "$FINAL"
      log "  WROTE $FINAL — gate EXIT=$EXIT mismatched=${nfail}/51 deck_md5=$deckmd5"
      exit 0
    fi
  fi
  sleep $POLL
done

db=$(dbcount); mis=$(mismatches)
log "TIMEOUT after 3h (started $START) — gate NOT run. db51='$db' mismatches_excl_p10='$mis'"
{
  echo "# merge_gate_FINAL.md — S9 merge gate NOT RUN (scheduler timeout, started $START)"
  echo
  echo "- Polled every ${POLL}s for 3h; entry conditions never all held at once."
  echo "- Final poll: db51='$db', mismatches_excl_p10='$mis'"
  echo "- No gate executed; no deck/DB/ledger changes by the scheduler beyond restage attempts logged in gate_scheduler.log."
} > "$FINAL"
exit 2
