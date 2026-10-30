#!/usr/bin/env bash
# Slide 045 judge dispatch, worker-fresh-045-legs4.
# Gate law: probe after one 240s drain wait; heartbeats; never retry-loop.
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides" || exit 99
export TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
WORKER=worker-fresh-045-legs4
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045
LOG=$Q/gate_logs/gate_worker_legs4_probe1.log
mkdir -p "$Q/gate_logs"
exec >>"$LOG" 2>&1

hb() { python3 scripts/15_progress.py heartbeat 45 "$WORKER"; }
echo "=== 045 worker-fresh-045-legs4 protocol probe1 $(date -u +%FT%TZ) ==="
hb
echo "fleet_procs_before=$(pgrep -c -f analyze_image.py || true)"
sleep 240
hb
echo "fleet_procs_after_wait=$(pgrep -c -f analyze_image.py || true)"
echo "probe_command=analysis render_1.png --timeout 120 (protocol probe)"
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  "$Q/render_1.png" \
  --view "Slide 045 recreation attempt 1 — probe" \
  --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
  --timeout 120 --rounds 1 --tries 1 \
  --transcript "$Q/probe_worker_legs4_1.txt"
rc=$?
echo "PROBE_EXIT=$rc $(date -u +%FT%TZ)"
hb
exit $rc
