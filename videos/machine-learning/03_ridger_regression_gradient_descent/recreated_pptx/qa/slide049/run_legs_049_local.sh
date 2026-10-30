#!/usr/bin/env bash
# Vision-judge legs for slide 049, worker fix-judge-049g (attempt 10, render_8).
# Gate law: pgrep before each call; >=8 clients -> heartbeat, sleep 240, re-probe
# (max TWO re-probes per hour) then PARK. Wall: analyzer --timeout 1200 inside
# `timeout 1700`; payload bytes unchanged from shared_patterns/judge_protocol_03.md.
# Args: <leg>  (legA | header | legend | dxi | wstack | bottom)
set -u
LEG="$1"
PROJ="/home/ahmed/Projects/ai_llm_slides"
DECK="$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide049"
SCRIPT="$PROJ/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE="$PROJ/scripts/16_vision_gate.sh"
export TMPDIR="$PROJ/scratch/tmp"; mkdir -p "$TMPDIR"
WID=s7-judge-1024
LOG="$QA/legs_049g.log"
hb(){ ( cd "$PROJ" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 49 "$WID" >/dev/null 2>&1 ); }
say(){ echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
clients(){ local n; n=$(pgrep -c -f '[a]nalyze_image\.py' 2>/dev/null) || n=0; echo "${n:-0}"; }

case "$LEG" in
  legA)
    IMG1="$DECK/recreated_pptx/qa/slide049/render_9.png"
    IMG2="$DECK/unique_slides/slide_049.jpg"
    OUT="$QA/judge_attempt_10.txt"
    PAYLOAD="$QA/judge_prompt_1.txt"
    VIEW="Slide 049 recreation attempt 10 — fidelity check vs original lecture frame"
    CAPTURE="IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame"
    ;;
  header|legend|dxi|wstack|bottom)
    IMG1="$QA/crop_9_${LEG}_render.png"
    IMG2="$QA/crop_9_${LEG}_orig.png"
    OUT="$QA/crop_9_${LEG}_judge.txt"
    PAYLOAD="$QA/crop_prompt_6_callout.txt"
    VIEW="Slide 049 zoomed crop $LEG — render vs original at matched scale (attempt 10)"
    case "$LEG" in
      header)  DESC="top blue-violet box: x1..x6 table with the red Initial column header and Initial W value row, the red REPEAT instruction, the Check classes label and its 3x3 grid" ;;
      legend)  DESC="the single-line class colour legend 'C1 positive C2 negative Zero is unaccepted' under the top box" ;;
      dxi)     DESC="the six calculation rows' d(x1..x6) labels and their stacked 2D bracketed matrices plus the arrow rows" ;;
      wstack)  DESC="the far-right result column of the six calculation rows: the 'W =' label and the stacked bracketed value column" ;;
      bottom)  DESC="the bottom-left text block: 'No change in W' with the underlined W, and 'Stop Iterations'" ;;
    esac
    CAPTURE="IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: $DESC"
    ;;
  *) echo "unknown leg $LEG" >&2; exit 2 ;;
esac

# ---- gate: probe fleet, at most TWO re-probes then park ----
for try in 0 1 2; do
  L=$(clients)
  if [ "$L" -lt 8 ]; then say "$LEG slot open clients=$L"; break; fi
  if [ "$try" = "2" ]; then say "$LEG PARKED reason=congestion clients=$L"; echo "$(date -u +%F_%H:%M) $LEG PARKED congestion clients=$L" >> "$QA/judge_status_049g.log"; exit 3; fi
  say "$LEG congested clients=$L -> heartbeat + sleep 240 (re-probe $try/2)"; hb; sleep 240
done

hb; rm -f "$OUT"
say "$LEG FIRE clients=$(clients) wall=1700 inner=1200"
( cd "$PROJ" && timeout 1700 bash "$GATE" python3 "$SCRIPT" comparison \
    "$IMG1" "$IMG2" --view "$VIEW" --capture "$CAPTURE" \
    --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
    --transcript "$OUT" -p "$(cat "$PAYLOAD")" ) > "$QA/${LEG}_049g_dispatch.log" 2>&1
rc=$?
say "$LEG EXIT rc=$rc bytes=$( [ -f "$OUT" ] && wc -c < "$OUT" || echo 0 )"
if [ -s "$OUT" ] && grep -q "FINAL VERDICT" "$OUT"; then
  v=$(grep -oE "FINAL VERDICT: (PASS|FAIL)" "$OUT" | tail -1)
  echo "$(date -u +%F_%H:%M) $LEG VERDICT $v rc=$rc" >> "$QA/judge_status_049g.log"
  say "$LEG $v"; exit 0
fi
echo "$(date -u +%F_%H:%M) $LEG NO_VERDICT rc=$rc" >> "$QA/judge_status_049g.log"
say "$LEG no usable transcript rc=$rc"; exit 1
