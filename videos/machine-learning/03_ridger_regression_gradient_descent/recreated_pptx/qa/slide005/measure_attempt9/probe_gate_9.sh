#!/usr/bin/env bash
# Slow-poll probe for slide 005 attempt 9.
#
# Runs from a SCRIPT FILE, so the shell's own cmdline does not contain the
# literal "analyze_image.py" — pgrep therefore does not count this probe
# itself (an inline `pgrep -c -f analyze_image.py` in a bash -c DOES self-match
# and inflates the reading by 1).
#
# Reports three numbers:
#   gate_count    = pgrep -c -f analyze_image.py   (the deck gate law's meter)
#   analyzer_procs= real python3 analyzer processes (one per in-flight leg)
#   leg_procs     = gate_count - analyzer_procs    (wrapper multiplicity:
#                   each leg also shows as `bash 16_vision_gate.sh` + `timeout`)
# Appends one line per probe to fleet_counts_slide005.txt.
Q="/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005"
LOG="$Q/measure_attempt9/fleet_counts_slide005.txt"
PAT="analyze""_image.py"
GATE=$(pgrep -c -f "$PAT" 2>/dev/null || echo 0)
ANA=$(ps -eo args | grep -c "^/.*python3 .*${PAT##*/}" 2>/dev/null || echo 0)
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "$TS gate_count=$GATE analyzer_procs=$ANA" | tee -a "$LOG"
if [ "$GATE" -lt 8 ]; then
  echo "GATE OPEN: $GATE < 8 — dispatch permitted"
  exit 0
fi
echo "GATE CONGESTED: $GATE >= 8 — do NOT dispatch"
exit 3
