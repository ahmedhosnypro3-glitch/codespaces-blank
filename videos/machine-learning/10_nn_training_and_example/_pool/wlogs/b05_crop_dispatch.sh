#!/usr/bin/env bash
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
PROMPT="$NS/qa/slide010/crop_prompt_b05.txt"
run_one() {
  local crop="$1" view="$2" cap="$3" out="$4"
  timeout 540 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" analysis "$crop" \
    --view "$view" --capture "$cap" \
    -p "$(cat "$PROMPT")" --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
  echo "done $out rc=$? bytes=$(wc -c < "$out") $(date +%T)"
}
run_one "$NS/qa/slide010/crop_diagram_b05.png" \
  "Slide 010 CROP: neural-network diagram + right label columns (original slide px region x=380..960, y=40..310, 3x upscale)" \
  "1740x810 crop = 3x upscale of 580x270 region of a 960x540 lecture frame" \
  "$NS/qa/slide010/audit_crop_diagram_b05.txt" &
sleep 15
run_one "$NS/qa/slide010/crop_midlow_b05.png" \
  "Slide 010 CROP: middle equation band + derivative row + chain-rule block + right recap panel (original px region x=50..960, y=185..470, 2x upscale)" \
  "1820x570 crop = 2x upscale of 910x285 region of a 960x540 lecture frame" \
  "$NS/qa/slide010/audit_crop_midlow_b05.txt" &
wait
echo "ALL DONE $(date +%T)"
