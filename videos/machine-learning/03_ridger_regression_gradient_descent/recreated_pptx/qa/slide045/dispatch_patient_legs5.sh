#!/usr/bin/env bash
# Slide 045 PATIENT lane: ONE leg at a time. Usage:
#   bash dispatch_leg.sh <leg>     # leg = templateA | calcs | toppanel | augtable
# Pre-checks the fleet (<8) BEFORE launching; refuses if congested.
set -u
export TMPDIR="/workspaces/codespaces-blank/ai_llm_slides/scratch/tmp"
ROOT="/workspaces/codespaces-blank/ai_llm_slides"
VIDEO="machine-learning/03_ridger_regression_gradient_descent"
Q="$ROOT/videos/$VIDEO/recreated_pptx/qa/slide045"
LEG="${1:-}"

if [ -z "$LEG" ]; then echo "USAGE: bash dispatch_leg.sh <templateA|calcs|toppanel|augtable>"; exit 2; fi

C=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0)
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) leg=$LEG fleet=$C"
if [ "$C" -ge 8 ]; then
  echo "REFUSED: fleet $C >= 8 — do not dump into a congested gateway"
  exit 3
fi

GATE="$ROOT/scripts/16_vision_gate.sh"
ANAL="$ROOT/.agents/skills/image-analysis/scripts/analyze_image.py"
RENDER="$Q/render_1.png"
ORIG="$ROOT/videos/$VIDEO/unique_slides/slide_045.jpg"

case "$LEG" in
  templateA)
    TS="$Q/judge_patient_legs5_templateA.txt"
    timeout 1700 bash "$GATE" python3 "$ANAL" comparison \
      "$RENDER" "$ORIG" \
      --view "Slide 045 recreation — fidelity check vs original lecture frame" \
      --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
      --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
      --transcript "$TS" \
      -p "$(cat "$Q/judge_prompt_1.txt")"
    rc=$?
    ;;
  calcs|toppanel|augtable)
    TS="$Q/crop_${LEG}_judge_patient_legs5.txt"
    case "$LEG" in
      calcs)    DESC="calculation panel: six ruled rows of dotted-product arithmetic with two bracket column vectors per row" ;;
      toppanel) DESC="top worked-example panel: data table x1..x6, Initial W bracket vector, Step eta, check-classes matrix and pointer arrow" ;;
      augtable) DESC="augmented vectors table with class row" ;;
    esac
    timeout 1700 bash "$GATE" python3 "$ANAL" comparison \
      "$Q/crop_1_r2_${LEG}_render.png" "$Q/crop_1_r2_${LEG}_orig.png" \
      --view "Slide 045 zoomed crop ${LEG} — render vs original at matched scale (patient legs5)" \
      --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
      --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
      --transcript "$TS" \
      -p "$(cat "$Q/crop_prompt_1_r2_${LEG}.txt")"
    rc=$?
    ;;
  *)
    echo "UNKNOWN LEG: $LEG"; exit 2 ;;
esac

echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) leg=$LEG rc=$rc transcript=$TS"
if [ -f "$TS" ]; then
  echo "transcript bytes=$(wc -c < "$TS")"
  if grep -q "FINAL VERDICT" "$TS"; then
    echo "FINAL VERDICT PRESENT:"
    grep -A2 "FINAL VERDICT" "$TS" | head -6
  else
    echo "NO FINAL VERDICT in transcript (not evidence)"
  fi
else
  echo "NO TRANSCRIPT FILE PRODUCED"
fi
exit $rc
