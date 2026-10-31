#!/usr/bin/env bash
# Sweeper #13 — certify-and-merge loop for 08_performance_measure.
# Every ~60s: scan qa dirs. DUAL-PASS-uncertified slides get a flock-append
# verification_ledger.md row + merge_final_deck.py update + mission.db scope done.
# Attempt-only-PASS slides get an original-first corroboration verify judge
# (sleep 90-150s before the call; 429/no-verdict => sleep 300s, retry up to 8x),
# skipped if a verify transcript for the slide was written in the last 25 min
# (another sweeper has it in flight). Loops until 37/37 certified.
set -u
NS="/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
REPO="/home/codespace/ai_llm_slides"
cd "$NS"
LOG="pool_run/sweeper13.log"
PYBIN="/home/codespace/.pyenv/versions/3.15.2/bin/python3"
GATE="$REPO/scripts/16_vision_gate.sh"
ANALYZE="$REPO/.agents/skills/image-analysis/scripts/analyze_image.py"
PROMPT="pool_run/judge_prompt_template.txt"
VLEDGER="pool_run/verification_ledger.md"
ITER=0

log() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }
cert_count() {
  python3 -c "import json;d=json.load(open('final_deck_ledger.json'));print(sum(1 for p in d['pages'] if p['status']=='certified'))"
}

log "sweeper13 start; certified=$(cert_count)/37"
while true; do
  ITER=$((ITER+1))
  C=$(cert_count)
  log "iter $ITER scan (certified=$C/37)"
  [ "$C" -ge 37 ] && { log "iter $ITER: 37/37 certified — sweeper13 done"; break; }

  while IFS=$'\t' read -r kind n rest1 rest2; do
    [ -z "${kind:-}" ] && continue
    pptx="recreated_pptx/slide_$(printf '%03d' "$n")_recreated.pptx"
    [ -f "$pptx" ] || { log "slide $n: $kind but $pptx missing — skip"; continue; }

    if [ "$kind" = "DUAL" ]; then
      att="$rest1"; ver="$rest2"
      # 1) flock-append ledger row if no non-superseded PASS row for n
      flock "$VLEDGER" bash -c '
        n="$1"; att="$2"; ver="$3"; vledger="$4"; logf="$5"
        if python3 - "$n" "$vledger" <<'"'"'PY'"'"'
import re, sys
n, path = sys.argv[1], sys.argv[2]
found = False
for line in open(path):
    m = re.match(r"\|\s*(\d+)\s*\|", line)
    if m and m.group(1) == n and "superseded" not in line:
        cols = [c.strip() for c in line.split("|")]
        v = cols[4] if len(cols) > 4 else ""
        if "PASS" in v and "FAIL" not in v:
            found = True
            break
sys.exit(0 if found else 1)
PY
        then
          echo "[$(date '+%F %T')] slide $n already has PASS ledger row — skip append" >>"$logf"
        else
          printf "| %s | %s | %s | PASS / PASS (original-first dual-read; sweeper-13) | — | yes | |\n" \
            "$n" "$att" "$ver" >>"$vledger"
          echo "[$(date '+%F %T')] slide $n ledger row appended" >>"$logf"
        fi
      ' _ "$n" "$att" "$ver" "$VLEDGER" "$LOG"
      # 2) merge update (idempotent; flips final_deck_ledger.json to certified)
      if python3 pool_run/merge_final_deck.py update "$n" "$pptx" 08-performance_final.pptx >>"$LOG" 2>&1; then
        log "slide $n: merge update OK (certified=$(cert_count)/37)"
      else
        log "slide $n: merge update FAILED rc=$?"
        continue
      fi
      # 3) mission.db scope done (retry on locked)
      ok=0
      for i in 1 2 3 4 5 6; do
        if sqlite3 pool_run/mission.db "UPDATE scopes SET status='done' WHERE name='slide-$n';" 2>>"$LOG"; then ok=1; break; fi
        sleep 5
      done
      [ "$ok" = 1 ] && log "slide $n: scope slide-$n done" || log "slide $n: scope update FAILED"

    elif [ "$kind" = "NEEDVERIFY" ]; then
      att="$rest1"; render="$rest2"
      qa=$(dirname "$att")
      # skip if another sweeper wrote a verify transcript for this slide <25 min ago
      recent=$(find "$qa" -maxdepth 1 -name 'judge_verify_*.txt' -mmin -25 2>/dev/null | head -1)
      if [ -n "$recent" ]; then
        log "slide $n: verify transcript $(basename "$recent") modified <25min ago — another sweeper in flight, skip"
        continue
      fi
      # per-slide lock so my own iterations never double-verify
      exec 8>"pool_run/.sw13_verify_$n.lock"
      if ! flock -n 8; then
        log "slide $n: my own verify lock held — skip"
        continue
      fi
      orig="unique_slides/slide_$(printf '%03d' "$n").jpg"
      [ -f "$orig" ] || { log "slide $n: original frame missing — skip verify"; flock -u 8; continue; }
      [ -f "$render" ] || { log "slide $n: render $render missing — skip verify"; flock -u 8; continue; }
      # unique transcript name: judge_verify_sw13_<n>_<k>.txt
      k=1
      while [ -f "$qa/judge_verify_sw13_${n}_${k}.txt" ]; do k=$((k+1)); done
      vt="$qa/judge_verify_sw13_${n}_${k}.txt"
      log "slide $n: verify judge starting (attempt=$(basename "$att") render=$(basename "$render") transcript=$(basename "$vt"))"
      sleep $((90 + RANDOM % 61))   # 90-150s before gateway-bound call
      done=0
      for try in 1 2 3 4 5 6 7 8; do
        # if another sweeper wrote a verify transcript for this slide <10 min ago
        # (and it is not one of ours), they own the corroboration — stop retrying
        recent_other=$(find "$qa" -maxdepth 1 -name 'judge_verify_*.txt' ! -name 'judge_verify_sw13_*' -mmin -10 2>/dev/null | head -1)
        if [ -n "$recent_other" ]; then
          log "slide $n: $(basename "$recent_other") from another sweeper <10min ago — abandon my retries"
          break
        fi
        bash "$GATE" timeout 540 "$PYBIN" "$ANALYZE" comparison "$orig" "$render" \
          --view "Slide $n recreation — sweeper-13 corroboration read try $try (original first, render second)" \
          --capture "IMG1=original lecture video frame (ground truth, read FIRST); IMG2=150dpi PNG render of the current 13.33x7.5in PPTX recreation (read SECOND)" \
          --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
          -p "$(cat "$PROMPT")" >"$vt" 2>&1
        rc=$?
        v=$("$PYBIN" pool_run/verdict.py "$vt" 2>/dev/null)
        log "slide $n: verify try $try rc=$rc verdict=${v:-NONE} size=$(wc -c <"$vt")"
        if [ "$v" = "PASS" ] || [ "$v" = "FAIL" ]; then done=1; break; fi
        if grep -qi '429' "$vt"; then
          log "slide $n: 429 seen — sleep 300s before retry $((try+1))/8"
        else
          log "slide $n: no verdict — sleep 300s before retry $((try+1))/8"
        fi
        sleep 300
      done
      [ "$done" = 1 ] || log "slide $n: verify judge exhausted 8 tries without verdict"
      flock -u 8
    fi
  done < <(python3 pool_run/sweeper13_scan.py)

  sleep 60
done
log "sweeper13 exit"
