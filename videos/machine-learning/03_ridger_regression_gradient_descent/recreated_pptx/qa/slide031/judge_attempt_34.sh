#!/usr/bin/env bash
# Attempt 34 judge legs for slide 031: probe + Template A + 3x Template B crops.
# Payloads byte-for-byte from shared_patterns/judge_protocol_03.md (payload_A_32.txt
# == Template A body verified byte-identical; payload_B_33.txt == Template B NNN->031).
# Run one leg per invocation: $1 = probe|A|topblock|graph|table
set -u
cd /home/ahmed/Projects/ai_llm_slides
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
B=videos/machine-learning/03_ridger_regression_gradient_descent
Q=$B/recreated_pptx/qa/slide031
LEG=${1:?leg: probe|A|topblock|graph|table}
payload_B() { sed -n '117p' $B/shared_patterns/judge_protocol_03.md | sed -e 's/^  -p "//' -e 's/"$//' -e 's/slide NNN/slide 031/'; }
gate() {
  local n; n=$(pgrep -c -f analyze_image.py)
  if [ "$n" -ge 8 ]; then echo "GATE SATURATED ($n >= 8) before $1" >&2; exit 42; fi
  if [ "$n" -gt 0 ]; then echo "note: $n foreign gate process(es) present before $1" >&2; fi
}
case $LEG in
probe)
  gate $LEG
  scripts/16_vision_gate.sh timeout 150 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py analysis \
    $Q/render_34.png \
    --view "Slide 031 recreation attempt 34 — probe" \
    --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
    --timeout 120 --rounds 1 --tries 1 \
    --transcript $Q/probe_34.txt
  ;;
A)
  gate $LEG
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/render_34.png \
    $B/unique_slides/slide_031.jpg \
    --view "Slide 031 recreation — fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript $Q/judge_attempt_34.txt \
    -p "$(cat $Q/payload_A_32.txt)"
  ;;
topblock|graph|table)
  gate $LEG
  case $LEG in
    topblock) DESC="title lines, parameter table, formula box, annotation box";;
    graph)    DESC="plot box of f(x)=(x-5)^2+1: blue parabola, black chord, red+green points, tick grid";;
    table)    DESC="main density table, 8 rows x 1 label col + 16 data cols, y~350-530";;
  esac
  scripts/16_vision_gate.sh timeout 1700 python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $Q/crop_34_${LEG}_render.png \
    $Q/crop_34_${LEG}_orig.png \
    --view "Slide 031 zoomed crop ${LEG} — render vs original at matched scale (attempt 34)" \
    --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
    --thinking high --max-tokens 65536 \
    --timeout 600 --rounds 1 --tries 1 \
    --transcript $Q/crop_34_${LEG}_judge.txt \
    -p "$(payload_B)"
  ;;
*)
  echo "unknown leg $LEG" >&2; exit 1;;
esac
