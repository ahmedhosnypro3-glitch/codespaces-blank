#!/bin/bash
# crop-legs-016b: re-run BOTH legs on render_6.png (underline-fix rebuild).
# Payloads byte-verified from shared_patterns/judge_protocol_03.md:
#   Template A md5 9387f5fbb94ef05a31db19f1e018dde1 (4115 bytes)
#   Template B md5 481172b034aa3336f54591d4e8e4bc98 (1914 bytes, BLOCKER x2)
set -u
MODE="${1:?usage: dispatch_judge_6.sh <legA|last_bullet|full_body>}"
cd /workspaces/codespaces-blank/ai_llm_slides || exit 3
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide016
case "$MODE" in
  legA)
    exec scripts/16_vision_gate.sh timeout 1700 python3 \
      .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$Q/render_6.png" \
      videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_016.jpg \
      --view "Slide 016 recreation attempt 6 — fidelity check vs original lecture frame" \
      --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
      --thinking high --max-tokens 65536 \
      --timeout 1200 --rounds 1 --tries 1 \
      --transcript "$Q/judge_attempt_6.txt" \
      -p "$(cat "$Q/judge_prompt_6A.txt")" ;;
  *)
    case "$MODE" in
      last_bullet) DESC="the last bullet's small-text cluster: red (N)/(d), 'Large vector Length', and the black underlines beneath 'Small number of samples', 'Large vector' and 'Length'" ;;
      full_body)   DESC="the whole 12-line text block inside the white content box: title/heading lines, the blue 'Penalize large values of W' line, and all body bullets with their separators and the three black underlines" ;;
      *) echo "unknown leg $MODE" >&2; exit 2 ;;
    esac
    exec scripts/16_vision_gate.sh timeout 1700 python3 \
      .agents/skills/image-analysis/scripts/analyze_image.py comparison \
      "$Q/crop_6_${MODE}_render.png" \
      "$Q/crop_6_${MODE}_orig.png" \
      --view "Slide 016 zoomed crop ${MODE} — render vs original at matched scale (attempt 6)" \
      --capture "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: ${DESC}" \
      --thinking high --max-tokens 65536 \
      --timeout 1200 --rounds 1 --tries 1 \
      --transcript "$Q/crop_6_${MODE}_judge.txt" \
      -p "$(cat "$Q/judge_prompt_6B.txt")" ;;
esac
