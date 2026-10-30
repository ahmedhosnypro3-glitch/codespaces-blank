#!/usr/bin/env bash
# Vision-judge legs for slide 050, attempt 14 (6-item fix-cycle re-cert on render_14;
# matched-coord crops via cut_crops_050_v11.py 14). legA = full-slide Template A
# (judge_payload_6.txt, verbatim substring of shared_patterns/judge_protocol_03.md);
# crop legs = Template B (judge_payload_B_6.txt) over crop_15_* pairs.
# Gate law: pgrep before each call; >=8 -> exit 3 (heartbeat + re-probe outside).
# Args: <leg>  (legA | mathzone | tableeq | chart | caption)
set -u
LEG="${1:?leg required}"
PROJ="/home/ahmed/Projects/ai_llm_slides"
DECK="$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide050"
SCRIPT="$PROJ/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE="$PROJ/scripts/16_vision_gate.sh"
export TMPDIR="$PROJ/scratch/tmp"; mkdir -p "$TMPDIR"
ATT=15
LOG="$QA/legs_050_a15.log"

case "$LEG" in
  legA)
    IMG1="$QA/render_15.png"
    IMG2="$DECK/unique_slides/slide_050.jpg"
    OUT="$QA/judge_attempt_15.txt"
    PAYLOAD="$QA/judge_payload_6.txt"
    VIEW="Slide 050 recreation attempt 14 — fidelity check vs original lecture frame"
    CAPTURE="IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame"
    INNER=1200
    ;;
  mathzone|tableeq|chart|caption)
    IMG1="$QA/crop_15_${LEG}_render.png"
    IMG2="$QA/crop_15_${LEG}_orig.png"
    OUT="$QA/crop_15_${LEG}_judge.txt"
    PAYLOAD="$QA/judge_payload_B_6.txt"
    VIEW="Slide 050 zoomed crop ${LEG} — render vs original at matched scale (attempt ${ATT})"
    case "$LEG" in
      mathzone)  DESC="the math zone inside the navy top box: 'Initial W' with underlined W and its tall bracketed 3-row column (4 / -2 / -2), the dark underlined 'Step η = 1' text, the red 'REPEAT using Step' line, the 'Check classes of' label with Z1 Z2 Z3 subscripts over three small bracketed 3-value columns, and the key line 'C1 positive C2 negative Zero is unaccepted'" ;;
      tableeq)   DESC="the whole navy box: left six-column x1..x6 data table with bracketed single digits and red C1 / blue C2 class tags, the math zone (Initial W 3-row bracket column, dark underlined 'Step η = 1', red 'REPEAT using Step', Check-classes Z columns), and the caption box 'Augmented Vectors ( from Top )' with six tall bracketed 3-row vector columns and red/blue class tags" ;;
      chart)     DESC="the scatter chart: red border, faint gridlines, three blue squares, three magenta diamonds, two red downward triangles, the red decision line running top-left to bottom-right with a '+ve' annotation and two small red arrows, x tick labels 0..8 and y tick labels 7..0" ;;
      caption)   DESC="the strip under the navy box where the Initial-W bracket column's bottom meets the key caption line 'C1 positive  C2 negative  Zero is unaccepted' (C1 red, C2 blue, Zero green)" ;;
    esac
    CAPTURE="IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}"
    INNER=600
    ;;
  *) echo "unknown leg $LEG" >&2; exit 2 ;;
esac

L=$(pgrep -c -f '[a]nalyze_image\.py' 2>/dev/null) || L=0
echo "[gate law] fleet analyze_image.py procs = $L -> $(date -u +%H:%M:%S)" >> "$LOG"
if [ "${L:-0}" -ge 8 ]; then
  echo "$(date -u +%F_%H:%M) $LEG PARKED congestion clients=$L" >> "$QA/judge_status_050.log"
  exit 3
fi

rm -f "$OUT"
echo "$LEG FIRE clients=$L wall=1700 inner=$INNER" >> "$LOG"
( cd "$PROJ" && timeout 1700 bash "$GATE" python3 "$SCRIPT" comparison \
    "$IMG1" "$IMG2" --view "$VIEW" --capture "$CAPTURE" \
    --thinking high --max-tokens 65536 --timeout "$INNER" --rounds 1 --tries 1 \
    --transcript "$OUT" -p "$(cat "$PAYLOAD")" ) > "$QA/${LEG}_a15_dispatch.log" 2>&1
