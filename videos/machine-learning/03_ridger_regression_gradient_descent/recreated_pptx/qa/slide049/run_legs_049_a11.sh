#!/usr/bin/env bash
# Vision-judge legs for slide 049, attempt 11 (rebuild render_10).
# legA = full-slide Template A (judge_prompt_1.txt, byte-identical to
# shared_patterns/judge_protocol_03.md); crop legs = Template B
# (crop_prompt_6_callout.txt) over crop_10_* pairs cut from render_10.
# Gate law: pgrep before each call; >=8 -> exit 3 (heartbeat + re-probe outside).
# Args: <leg>  (legA | top_band | aug_box | legend | calc_rows | iter_stop)
set -u
LEG="${1:?leg required}"
PROJ="/home/ahmed/Projects/ai_llm_slides"
DECK="$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide049"
SCRIPT="$PROJ/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE="$PROJ/scripts/16_vision_gate.sh"
export TMPDIR="$PROJ/scratch/tmp"; mkdir -p "$TMPDIR"
ATT=11
LOG="$QA/legs_049_a11.log"

case "$LEG" in
  legA)
    IMG1="$QA/render_10.png"
    IMG2="$DECK/unique_slides/slide_049.jpg"
    OUT="$QA/judge_attempt_11.txt"
    PAYLOAD="$QA/judge_prompt_1.txt"
    VIEW="Slide 049 recreation attempt 11 — fidelity check vs original lecture frame"
    CAPTURE="IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame"
    INNER=1200
    ;;
  top_band|aug_box|legend|calc_rows|iter_stop)
    IMG1="$QA/crop_10_${LEG}_render.png"
    IMG2="$QA/crop_10_${LEG}_orig.png"
    OUT="$QA/crop_10_${LEG}_judge.txt"
    PAYLOAD="$QA/crop_prompt_6_callout.txt"
    VIEW="Slide 049 zoomed crop ${LEG} — render vs original at matched scale (attempt ${ATT})"
    case "$LEG" in
      top_band)  DESC="top box region: six-column x1..x6 table with bracketed 2-value stacks and a third value row, the dark underlined 'Initial W' label with its stacked bracket column to its left, the red 'REPEAT using Step eta = 1' line, the 'Check classes of' label and its Z1 Z2 Z3 3x3 grid" ;;
      aug_box)   DESC="the augmented-vectors box: violet title line, six 3-row bracketed vector columns with a digit triplet above each, red C1 and dark C2 class tags" ;;
      legend)    DESC="the single-line class legend 'C1 positive C2 negative Zero is unaccepted' with colored C1/C2/Zero tokens" ;;
      calc_rows) DESC="the right calculation panel: six rows d(x1)..d(x6), each with a bare 3-digit row, a tall bracketed 3-value column, an equals sign, a result value, a red double arrow, the 'Keep same Weight' verdict, and a 'W =' bracketed column" ;;
      iter_stop) DESC="the bottom-left block: red 'Iteration 2' box, 'No change in W' with underlined W, red 'Stop' plus 'Iterations'" ;;
    esac
    CAPTURE="IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}"
    INNER=600
    ;;
  *) echo "unknown leg $LEG" >&2; exit 2 ;;
esac

L=$(pgrep -c -f '[a]nalyze_image\.py' 2>/dev/null) || L=0
echo "[gate law] fleet analyze_image.py procs = $L -> $(date -u +%H:%M:%S)" >> "$LOG"
if [ "${L:-0}" -ge 8 ]; then
  echo "$(date -u +%F_%H:%M) $LEG PARKED congestion clients=$L" >> "$QA/judge_status_049g.log"
  exit 3
fi

rm -f "$OUT"
echo "$LEG FIRE clients=$L wall=1700 inner=$INNER" >> "$LOG"
( cd "$PROJ" && timeout 1700 bash "$GATE" python3 "$SCRIPT" comparison \
    "$IMG1" "$IMG2" --view "$VIEW" --capture "$CAPTURE" \
    --thinking high --max-tokens 65536 --timeout "$INNER" --rounds 1 --tries 1 \
    --transcript "$OUT" -p "$(cat "$PAYLOAD")" ) > "$QA/${LEG}_a11_dispatch.log" 2>&1
rc=$?
say_bytes=$( [ -f "$OUT" ] && wc -c < "$OUT" || echo 0 )
echo "$LEG EXIT rc=$rc bytes=$say_bytes $(date -u +%H:%M:%S)" >> "$LOG"
if [ -s "$OUT" ] && grep -q "FINAL VERDICT" "$OUT"; then
  v=$(grep -oE "FINAL VERDICT: (PASS|FAIL)" "$OUT" | tail -1)
  echo "$(date -u +%F_%H:%M) $LEG VERDICT $v rc=$rc" >> "$QA/judge_status_049g.log"
  exit 0
fi
echo "$(date -u +%F_%H:%M) $LEG NO_VERDICT rc=$rc" >> "$QA/judge_status_049g.log"
exit 1
