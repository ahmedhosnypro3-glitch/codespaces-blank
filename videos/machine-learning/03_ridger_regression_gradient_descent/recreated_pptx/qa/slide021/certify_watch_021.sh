#!/usr/bin/env bash
# slide 021 — strict auto-certifier for the Procedure B crop legs.
#
# Watches the five crop transcripts and certifies ONLY when every one of them carries
# a real "FINAL VERDICT: PASS" body. It refuses to certify on anything else:
#   - a missing transcript                     -> keep waiting
#   - a FINAL VERDICT that is not PASS         -> STOP, do not certify (needs PIL adjudication)
#   - the payload md5 drifted                  -> STOP (K-token law)
#   - render_10 drifted from the current pptx  -> STOP (re-render + re-cut first)
#   - leg A transcript no longer PASS          -> STOP
# Certification is the DB law's `set` sequence; there is no record-visual subcommand.
#
# One dispatch per crop is already spent by dispatch_leg2_crops_fresh.sh; this script
# NEVER dispatches a vision call. It only observes and, at the end, writes the DB.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
V="machine-learning/03_ridger_regression_gradient_descent"
QADIR="$ROOT/videos/$V/recreated_pptx/qa/slide021"
LOG="$QADIR/certify_watch.log"
WID="${WID:-w021-legs-20261024}"
PAYLOAD_MD5="b5b152e31e2ca54989eff597374025fb"
RENDER_MD5="a17310a3cac93cf23e3c8daed2bd0cea"
SLUGS="top_table_eq top_chain mid_table_eq mid_chain bot_eq_table"
POLL_MAX="${POLL_MAX:-21600}"
POLL_EVERY="${POLL_EVERY:-60}"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }
hb() {
  cd "$ROOT" && VIDEO=$V python3 scripts/15_progress.py heartbeat 21 "$WID" >/dev/null 2>&1
  cd "$ROOT"
}

cd "$ROOT"
note "certify-watcher started (WID=$WID, poll every ${POLL_EVERY}s, cap ${POLL_MAX}s)"

t0=$(date +%s)
while :; do
  el=$(( $(date +%s) - t0 ))
  if [ "$el" -ge "$POLL_MAX" ]; then
    note "POLL CAP ${el}s reached — honest park, NOT certified, no verdict fabricated"
    exit 42
  fi

  # --- gate 1: every transcript must carry a real FINAL VERDICT line ---
  ready=1
  for s in $SLUGS; do
    f="$QADIR/crop_10_${s}_judge.txt"
    if [ ! -f "$f" ]; then ready=0; break; fi
    if ! grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then ready=0; break; fi
  done

  if [ "$ready" -eq 1 ]; then
    # every transcript has a verdict — now insist they are ALL PASS
    allpass=1
    for s in $SLUGS; do
      v=$(grep -o "FINAL VERDICT:.*" "$QADIR/crop_10_${s}_judge.txt" | tail -1 | sed 's/[[:space:]]*$//')
      case "$v" in
        "FINAL VERDICT: PASS") ;;
        *) allpass=0; note "crop $s verdict is '$v' — NOT PASS; refusing to certify (needs PIL adjudication)" ;;
      esac
    done

    # gate 2: payload bytes unchanged (K-token law)
    pm=$(md5sum "$QADIR/crop_prompt_template_10.txt" | cut -d' ' -f1)
    [ "$pm" = "$PAYLOAD_MD5" ] || { note "payload md5 drifted ($pm) — STOP"; exit 43; }

    # gate 3: render_10 still banked and unchanged
    rm=$(md5sum "$QADIR/render_10.png" | cut -d' ' -f1)
    [ "$rm" = "$RENDER_MD5" ] || { note "render_10 md5 drifted ($rm) — STOP"; exit 44; }

    # gate 4: leg A transcript must still be PASS
    grep -q "FINAL VERDICT: PASS" "$QADIR/judge_attempt_10.txt" 2>/dev/null \
      || { note "leg A judge_attempt_10.txt is not PASS — STOP"; exit 45; }

    if [ "$allpass" -eq 1 ]; then
      note "ALL FIVE crop transcripts carry FINAL VERDICT: PASS — running PIL adjudication for the record"
      python3 "$QADIR/adjudicate_crops_1200.py" > "$QADIR/adjudicate_crops_final.txt" 2>&1
      note "PIL adjudication banked to adjudicate_crops_final.txt"
      note "certifying: visual_check PASS, visual_transcript judge_attempt_10.txt, visual_attempts 10, gen_status passed"
      VIDEO=$V python3 scripts/15_progress.py set 21 visual_check PASS --worker "$WID" >>"$LOG" 2>&1
      VIDEO=$V python3 scripts/15_progress.py set 21 visual_transcript \
        "videos/$V/recreated_pptx/qa/slide021/judge_attempt_10.txt" --worker "$WID" >>"$LOG" 2>&1
      VIDEO=$V python3 scripts/15_progress.py set 21 visual_attempts 10 --worker "$WID" >>"$LOG" 2>&1
      VIDEO=$V python3 scripts/15_progress.py set 21 gen_status passed --worker "$WID" >>"$LOG" 2>&1
      VIDEO=$V python3 scripts/15_progress.py release 21 "$WID" >>"$LOG" 2>&1
      note "--- final DB row ---"
      VIDEO=$V python3 scripts/15_progress.py get 21 >>"$LOG" 2>&1
      note "CERTIFIED (both legs banked: leg A PASS + all five Procedure B crops PASS)"
      exit 0
    fi
    note "not all crops PASS — holding, will re-check (a FAIL/MINOR needs PIL adjudication, never auto-certify)"
  fi

  hb
  sleep "$POLL_EVERY"
done
