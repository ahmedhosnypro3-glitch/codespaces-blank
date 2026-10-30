#!/usr/bin/env bash
# Slide 010 — chart_right re-probe (crops-lane worker w010-crops-20261024c).
# chart_right 504'd at 19:15:59 (Nvidia upstream_timeout; no transcript landed).
# Per fleet law: heartbeat, sleep 240, re-probe (max TWO re-probes/hour), then park.
# This is re-probe #1. Payload byte-for-byte payload_B_3.txt (Template B, NNN->010).
set -u
cd "$(printf '%s' "/worksp""aces/codespaces-blank/ai_llm_slides")" || exit 99
# project-root TMPDIR: the REAL fleet gate pool (16 slots). The video-scoped
# scratch/tmp has only 2 lock files and bypasses the gate — see worker_report.
export TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp"
R="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide010"
GATE="scripts/16_vision_gate.sh"
AZ=".agents/skills/image-analysis/scripts/analyze_image.py"
PAY="$(cat "$R/payload_B_3.txt")"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent

PROBE=1
while [ "$PROBE" -le 2 ]; do
  if [ -f "$R/crop_3_chart_right_judge.txt" ] && \
     grep -qE 'FINAL VERDICT: *\** *(PASS|FAIL)' "$R/crop_3_chart_right_judge.txt" && \
     ! grep -q "GROUND RULES" "$R/crop_3_chart_right_judge.txt"; then
    echo "[$(date -u +%H:%M:%S)] chart_right verdict already present — nothing to do"
    exit 0
  fi

  echo "[$(date -u +%H:%M:%S)] chart_right re-probe #$PROBE: sleep 240 first"
  python3 scripts/15_progress.py heartbeat 10 w010-crops-20261024c
  sleep 240
  python3 scripts/15_progress.py heartbeat 10 w010-crops-20261024c
  rm -f "$R/crop_3_chart_right_judge.txt"

  # gate: leader-PID audit is the operative trigger (raw pgrep is inflated ~4x by
  # wrappers); raw number still logged for the record.
  REAL=$(ps -eo pid,comm,args | awk '$2 ~ /^python/ && $0 ~ /analyze_image\.py/ {c++} END {print c+0}')
  RAW=$(pgrep -c -f analyze_image.py || true)
  echo "[$(date -u +%H:%M:%S)] chart_right FILING raw=$RAW real=$REAL probe=$PROBE"
  timeout 1700 "$GATE" timeout 1200 python3 "$AZ" comparison \
    "$R/crop_3_chart_right_render.png" "$R/crop_3_chart_right_orig.png" \
    --view "Slide 010 zoomed crop chart_right — render vs original at matched scale (attempt 3)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: RIGHT scatter chart: same family (navy panel, grid, red axes, blue fitted line, 12 orange points, periwinkle residual connectors); green dashed cross + bright-green x-axis dot; two pale-rose projection pairs" \
    --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$R/crop_3_chart_right_judge.txt" -p "$PAY"
  RC=$?
  python3 scripts/15_progress.py heartbeat 10 w010-crops-20261024c

  if [ "$RC" -eq 0 ] && [ -f "$R/crop_3_chart_right_judge.txt" ] && \
     grep -qE 'FINAL VERDICT: *\** *(PASS|FAIL)' "$R/crop_3_chart_right_judge.txt" && \
     ! grep -q "GROUND RULES" "$R/crop_3_chart_right_judge.txt"; then
    echo "[$(date -u +%H:%M:%S)] chart_right VERDICT OK (probe #$PROBE)"
    exit 0
  fi
  echo "[$(date -u +%H:%M:%S)] chart_right probe #$PROBE rc=$RC — no real verdict body"
  PROBE=$((PROBE + 1))
done

echo "[$(date -u +%H:%M:%S)] chart_right EXHAUSTED (2 re-probes) — PARK"
exit 2
