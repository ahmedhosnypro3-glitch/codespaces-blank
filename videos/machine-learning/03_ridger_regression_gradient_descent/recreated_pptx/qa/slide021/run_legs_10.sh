#!/usr/bin/env bash
# slide 021 attempt-10 judge legs: gate poll + leg 1 (full-slide) + leg 2 (5 crop pairs).
# Written by the LEGS-ONLY worker lane. Wall frozen (founder decision open): outer
# timeout 1700, analyzer --timeout 600. Never retry-loops. No verdict => honest bank.
set -u
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
QADIR="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021"
LOG="$QADIR/legs_status_20261024.md"
POLL_MAX=${POLL_MAX:-9000}        # seconds of polling before giving up (default 2.5h)
POLL_EVERY=${POLL_EVERY:-60}

DISPATCH1="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021/dispatch_leg1_fullslide.sh"
DISPATCH2="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide021/dispatch_leg2_crops.sh"
T1="$QADIR/judge_attempt_10.txt"
CROPS="top_table_eq top_chain mid_table_eq mid_chain bot_eq_table"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }
q() { pgrep -c -f analyze_image.py 2>/dev/null || echo 0; }
note() { echo "[$(ts)] $*" | tee -a "$LOG"; }

rm -f "$LOG"
{
  echo "# Slide 021 judge legs — status note (attempt 10), $0 started $(ts)"
  echo
} >> "$LOG"

note "polling the vision gate; threshold pgrep<8; poll cap ${POLL_MAX}s @ ${POLL_EVERY}s"

t0=$(date +%s)
window_open=0
while :; do
  now=$(date +%s); el=$(( now - t0 ))
  c=$(q)
  note "gate probe #$(( el / POLL_EVERY + 1 )): pgrep=$c (elapsed ${el}s)"
  if [ "$c" -lt 8 ]; then
    window_open=1
    break
  fi
  if [ "$el" -ge "$POLL_MAX" ]; then
    note "POLL CAP REACHED (${el}s) with pgrep=$c — window never opened; stopping honestly."
    exit 42
  fi
  sleep "$POLL_EVERY"
done

note "WINDOW OPEN at $(ts) (pgrep=$c) — dispatching LEG 1 (full-slide Template A)"
dstart=$(date +%s)
qd=$(q)
rm -f "$T1"
bash "$DISPATCH1" >> "$LOG" 2>&1
rc1=$?
dend=$(date +%s)
d1=$(( dend - dstart ))
note "LEG 1 finished rc=$rc1 elapsed=${d1}s queue_at_dispatch=$qd"

v1="NO-VERDICT"
if [ -f "$T1" ] && grep -q "FINAL VERDICT:" "$T1" 2>/dev/null; then
  v1=$(grep -o "FINAL VERDICT:.*" "$T1" | tail -1 | cut -c1-60)
fi

if [ "$rc1" -eq 124 ] || [ ! -f "$T1" ] || [ "$v1" = "NO-VERDICT" ]; then
  {
    echo
    echo "## LEG 1 — WALL ABORT / NO VERDICT"
    echo
    echo "- dispatched $(date -u -d @"$dstart" +%H:%M:%S)Z with queue depth $qd"
    echo "- outer timeout 1700 wrapper returned rc=$rc1 after ${d1}s"
    echo "- transcript \`judge_attempt_10.txt\` written: $([ -f "$T1" ] && echo yes || echo NO)"
    echo "- verdict line: $v1"
  } >> "$LOG"
  if [ "$rc1" -eq 124 ]; then
    echo "- attribution: killed by the outer \`timeout 1700\` wrapper (no verdict). This reproduces" >> "$LOG"
    echo "  the 09:39-10:07 leg-1 abort banked in \`wall_abort_evidence_10.txt\` — second identical" >> "$LOG"
    echo "  outer-wall death of the frozen command form. The founder wall decision stays open;" >> "$LOG"
    echo "  one hard-wall retry per leg remains UNSPENT and is left for the next lane rather than" >> "$LOG"
    echo "  burned here to re-produce a known failure." >> "$LOG"
  else
    echo "- attribution: gate/pipe error or empty output (not a timeout 124); see log above." >> "$LOG"
  fi
  note "STOP: leg 1 produced no verdict. Leg 2 not dispatched. NO certification."
  exit 43
fi

note "LEG 1 verdict = $v1"

case "$v1" in
  *PASS*)
    ;;
  *)
    note "LEG 1 = FAIL — PIL adjudication required by a worker before any build change. Stopping."
    exit 44
    ;;
esac

note "LEG 1 PASS — dispatching LEG 2 (five Procedure B crop pairs)"
bash "$DISPATCH2" >> "$LOG" 2>&1
rc2=$?
note "LEG 2 finished rc=$rc2"

for s in $CROPS; do
  f="$QADIR/crop_10_${s}_judge.txt"
  if [ -f "$f" ] && grep -q "FINAL VERDICT:" "$f" 2>/dev/null; then
    note "crop $s: $(grep -o 'FINAL VERDICT:.*' "$f" | tail -1 | cut -c1-60)"
  else
    note "crop $s: NO VERDICT (transcript $([ -f "$f" ] && echo present-empty || echo missing))"
  fi
done
note "legs complete; see transcripts in $QADIR"
exit 0
