#!/usr/bin/env bash
# Slide 045 — worker-fresh-045-legs4 — Template A + Procedure B dispatch.
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides" || exit 99
export TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp"
export VIDEO=machine-learning/03_ridger_regression_gradient_descent
WORKER=worker-fresh-045-legs4
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045
LOG=$Q/gate_logs/gate_worker_legs4_dispatch.log
mkdir -p "$Q/gate_logs"
exec >>"$LOG" 2>&1

hb() { VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 45 "$WORKER"; }
wait_slot() {
  local n=0 c
  while [ "$n" -lt 2 ]; do
    c=$(pgrep -c -f analyze_image.py || true)
    echo "$(date -u +%FT%TZ) gate_check n=$n analyze_procs=$c"
    if [ "$c" -lt 8 ]; then return 0; fi
    hb
    sleep 240
    n=$((n + 1))
  done
  c=$(pgrep -c -f analyze_image.py || true)
  echo "$(date -u +%FT%TZ) gate_check_final n=$n analyze_procs=$c"
  [ "$c" -lt 8 ]
}

heartbeat_loop() {
  while true; do
    sleep 540
    hb
  done
}
heartbeat_loop &
HB_PID=$!
trap 'kill "$HB_PID" 2>/dev/null || true' EXIT

echo "=== 045 worker-fresh-045-legs4 comparison dispatch $(date -u +%FT%TZ) ==="
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py set 45 gen_status judging --worker "$WORKER"
hb

if ! wait_slot; then
  echo "GATE_PARKED fleet remained at or above threshold after two drain intervals"
  exit 75
fi

echo "=== TEMPLATE A attempt 1 $(date -u +%FT%TZ) ==="
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/render_1.png" \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_045.jpg \
  --view "Slide 045 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$Q/judge_worker_legs4_attempt_1.txt" \
  -p "$(cat "$Q/judge_prompt_1.txt")"
rc_a=$?
echo "TEMPLATE_A_EXIT=$rc_a $(date -u +%FT%TZ)"
hb

for name in calcs toppanel augtable; do
  if ! wait_slot; then
    echo "GATE_PARKED before crop leg $name"
    exit 75
  fi
  case "$name" in
    calcs) desc="calculation panel: six ruled rows of dotted-product arithmetic with two bracket column vectors per row" ;;
    toppanel) desc="top worked-example panel: data table x1..x6, Initial W bracket vector, Step eta, check-classes matrix and pointer arrow" ;;
    augtable) desc="augmented vectors table with class row" ;;
  esac
  echo "=== PROCEDURE B $name attempt 1 $(date -u +%FT%TZ) ==="
  timeout 1700 bash scripts/16_vision_gate.sh python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$Q/crop_1_r2_${name}_render.png" "$Q/crop_1_r2_${name}_orig.png" \
    --view "Slide 045 zoomed crop $name — render vs original at matched scale (attempt 1)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $desc" \
    --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$Q/crop_${name}_worker_legs4_attempt_1.txt" \
    -p "$(cat "$Q/crop_prompt_1_r2_${name}.txt")"
  rc=$?
  echo "PROCEDURE_B_${name}_EXIT=$rc $(date -u +%FT%TZ)"
  hb
done

echo "=== DISPATCH COMPLETE $(date -u +%FT%TZ) ==="
exit 0
