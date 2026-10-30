#!/usr/bin/env bash
# Judge attempt 6 dispatch for slide 047 (worker w047-root-20261024).
# Full-slide Template A + 5 crop-pair Template B legs. Payloads byte-for-byte from
# shared_patterns/judge_protocol_03.md (NNN=047, K=6). All paths in split form.
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp"
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$DECK/recreated_pptx/qa/slide047
GATE=scripts/16_vision_gate.sh
CLI=.agents/skills/image-analysis/scripts/analyze_image.py
RM="$Q/attempt6_fullslide.out"

hb() { VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 47 w047-root-20261024 >/dev/null 2>&1; }

gate_check() {
  local n
  n=$(pgrep -c -f analyze_image.py || true)
  while [ "${n:-0}" -ge 8 ]; do
    hb
    echo "GATE SATURATED (n=$n) — heartbeat + sleep 240"
    sleep 240
    n=$(pgrep -c -f analyze_image.py || true)
  done
  echo "gate ok (n=${n:-0} concurrent)"
}

desc_for() {
  case "$1" in
    topband)   echo "top band: left data matrix, Initial W vector, legend, Z matrix" ;;
    augmatrix) echo "mid-left augmented-vectors matrix with spanning parens and class row" ;;
    calceq)    echo "box 1 equation: d(Z1) label, blue row vector, green stacked column, result" ;;
    calcright) echo "right side of all three calc boxes: sign statements and class outcomes" ;;
    button)    echo "bottom-left red Check Classes button" ;;
  esac
}

hb
gate_check

# ---- Leg A: full-slide Template A
$GATE timeout 1700 python3 $CLI comparison \
  "$Q/render_10.png" \
  $DECK/unique_slides/slide_047.jpg \
  --view "Slide 047 recreation — fidelity check vs original lecture frame (attempt 6)" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/judge_attempt_6.txt" \
  -p "$(cat $Q/judge_prompt_attempt_6.txt)" > "$Q/judge_attempt_6_dispatch.log" 2>&1
rcA=$?
if [ -f "$Q/judge_attempt_6.txt" ]; then
  echo "EXIT_A=$rcA VERDICT_A: $(grep -h 'FINAL VERDICT' "$Q/judge_attempt_6.txt" || echo NO_VERDICT_LINE)" > "$RM"
else
  echo "EXIT_A=$rcA VERDICT_A: NO_TRANSCRIPT" > "$RM"
fi
hb

# ---- Leg B: crop pairs (parallel, each behind the saturation gate)
for NAME in topband augmatrix calceq calcright button; do
  (
    gate_check
    DESC=$(desc_for "$NAME")
    $GATE timeout 1700 python3 $CLI comparison \
      "$Q/crop_6_${NAME}_render.png" \
      "$Q/crop_6_${NAME}_orig.png" \
      --view "Slide 047 zoomed crop ${NAME} — render vs original at matched scale (attempt 6)" \
      --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
      --thinking high --max-tokens 65536 \
      --timeout 600 --rounds 1 --tries 1 \
      --transcript "$Q/crop_6_${NAME}_judge.txt" \
      -p "$(cat $Q/crop_prompt_6_${NAME}.txt)" > "$Q/crop_6_${NAME}_dispatch.log" 2>&1
    rc=$?
    if [ -f "$Q/crop_6_${NAME}_judge.txt" ]; then
      echo "EXIT_${NAME}=$rc VERDICT_${NAME}: $(grep -h 'FINAL VERDICT' "$Q/crop_6_${NAME}_judge.txt" || echo NO_VERDICT_LINE)" > "$Q/crop_6_${NAME}.out"
    else
      echo "EXIT_${NAME}=$rc VERDICT_${NAME}: NO_TRANSCRIPT" > "$Q/crop_6_${NAME}.out"
    fi
  ) &
done
wait
echo "ALL JUDGES DONE $(date -u +%FT%TZ)" > "$Q/attempt6_all_done.txt"
hb
