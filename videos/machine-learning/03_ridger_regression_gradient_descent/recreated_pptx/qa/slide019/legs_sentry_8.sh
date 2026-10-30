#!/usr/bin/env bash
# Slide 019 attempt-8 LEGS SENTRY (w019-legs-20261024).
# Waits for the fleet gate to drain, then fires the attempt-8 judge legs.
#
# Guards (hard, non-negotiable):
#   * Template A fires AT MOST ONCE from dispatch_A8.sh's exact form.
#   * Template A gets AT MOST ONE hard-wall retry (--timeout 1200 extension),
#     and only if the first dispatch produced NO verdict.
#   * Procedure B fires ONLY after Template A returns FINAL VERDICT: PASS,
#     one attempt per crop.
#   * Before every dispatch: gate law check (load must be < 8).
#   * Never a retry-loop.
set -u
ROOT=/workspaces/codespaces-blank/ai_llm_slides
export TMPDIR=$ROOT/scratch/tmp
VID=machine-learning/03_ridger_regression_gradient_descent
Q=$ROOT/videos/$VID/recreated_pptx/qa/slide019
LOG=$ROOT/scratch/tmp/legs_sentry_8.log
POLL=45
MAX_WAIT_SECONDS=7200          # 2h cap; exit (parked) if the gate never opens
LEGS=(header_strip table_left noreg_rows table_right)

hb() { pgrep -c -f analyze_image.py; }

wait_for_gate() {
  local deadline=$(( $(date +%s) + MAX_WAIT_SECONDS ))
  local last_hb=0
  while :; do
    local L; L=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 99)
    local now; now=$(date +%s)
    if [ "$L" -lt 8 ]; then
      echo "[$(date +%H:%M:%S)] GATE OPEN: load=$L" >> "$LOG"
      return 0
    fi
    if [ $((now - last_hb)) -ge 240 ]; then
      echo "[$(date +%H:%M:%S)] gate congested load=$L — heartbeat" >> "$LOG"
      (cd "$ROOT" && VIDEO=$VID python3 scripts/15_progress.py heartbeat 19 w019-legs-20261024 >> "$LOG" 2>&1)
      last_hb=$now
    fi
    if [ "$now" -ge "$deadline" ]; then
      echo "[$(date +%H:%M:%S)] GATE NEVER OPENED within cap — PARKED" >> "$LOG"
      return 1
    fi
    sleep "$POLL"
  done
}

has_verdict() { [ -f "$1" ] && grep -q "FINAL VERDICT:" "$1"; }

echo "[$(date +%H:%M:%S)] sentry start (initial load=$(hb))" >> "$LOG"

# ---------- Template A ----------
if ! wait_for_gate; then
  echo "[$(date +%H:%M:%S)] Template A not dispatched — gate never opened" >> "$LOG"
  exit 20
fi
echo "[$(date +%H:%M:%S)] firing Template A (dispatch_A8.sh exact form)" >> "$LOG"
bash "$Q/dispatch_A8.sh" >> "$LOG" 2>&1
A_EXIT=$?

if ! has_verdict "$Q/judge_attempt_8.txt"; then
  echo "[$(date +%H:%M:%S)] Template A produced NO verdict (exit=$A_EXIT)" >> "$LOG"
  echo "[$(date +%H:%M:%S)] the ONE permitted hard-wall retry (--timeout 1200)" >> "$LOG"
  if wait_for_gate; then
    bash "$Q/dispatch_A8rr.sh" >> "$LOG" 2>&1
    echo "[$(date +%H:%M:%S)] retry exit=$? verdict=$(has_verdict "$Q/judge_attempt_8.txt" && echo YES || echo NO)" >> "$LOG"
  else
    echo "[$(date +%H:%M:%S)] retry skipped — gate never opened" >> "$LOG"
  fi
fi

if ! has_verdict "$Q/judge_attempt_8.txt"; then
  echo "[$(date +%H:%M:%S)] PARKED: Template A produced no verdict after main+retry" >> "$LOG"
  exit 21
fi

A_VERDICT=$(grep -o "FINAL VERDICT: [A-Z]*" "$Q/judge_attempt_8.txt" | tail -1)
echo "[$(date +%H:%M:%S)] Template A verdict: $A_VERDICT" >> "$LOG"

if ! echo "$A_VERDICT" | grep -q "PASS"; then
  echo "[$(date +%H:%M:%S)] Template A FAIL — Procedure B NOT dispatched (PIL adjudication required)" >> "$LOG"
  exit 22
fi

# ---------- Procedure B ----------
for NAME in "${LEGS[@]}"; do
  if ! wait_for_gate; then
    echo "[$(date +%H:%M:%S)] Procedure B stopped at $NAME — gate never opened" >> "$LOG"
    exit 23
  fi
  echo "[$(date +%H:%M:%S)] firing leg $NAME" >> "$LOG"
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$Q/crop_8_${NAME}_render.png" "$Q/crop_8_${NAME}_orig.png" \
    --view "Slide 019 zoomed crop ${NAME} - render vs original at matched scale (attempt 8)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: see worker_report_ROOT.md Procedure B table" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript "$Q/crop_8_${NAME}_judge.txt" \
    -p "$(cat $Q/judgeB8_payload_20261024.txt)" >> "$LOG" 2>&1
  echo "[$(date +%H:%M:%S)] leg $NAME exit=$? verdict=$(has_verdict "$Q/crop_8_${NAME}_judge.txt" && grep -o 'FINAL VERDICT: [A-Z]*' "$Q/crop_8_${NAME}_judge.txt" | tail -1 || echo NONE)" >> "$LOG"
done

echo "[$(date +%H:%M:%S)] sentry complete — all legs fired" >> "$LOG"
exit 0
