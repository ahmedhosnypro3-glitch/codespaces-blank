#!/bin/bash
# Slide 28 spatial-map extraction via small-crop vision calls (2x upscale).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
TOOL=/home/codespace/.agents/skills/image-analysis/analyze_image/analyze_image.py
LOG=$NS/_pool/storm_log/s028_cropmap.log
: > "$LOG"

run () {
  local name="$1" img="$2" prompt="$3"
  echo "=== $name $(date -Is) ===" >> "$LOG"
  timeout 300 python3 "$TOOL" analysis "$img" --timeout 240 --rounds 1 --tries 1 \
    -p "$prompt" >> "$LOG" 2>&1
  echo "--- exit=$? $(date -Is) ---" >> "$LOG"
}

run diag "$NS/_pool/crops028/diag.png" \
"This image is a 1060x294 crop of a 960x540 slide, upscaled 2x from source region x=395..925, y=45..192. Give exact pixel coordinates IN THIS IMAGE for: (1) every text label with its exact string and bounding box, (2) every node circle with center x,y, radius, and fill color, (3) every connecting edge or arrow line with endpoints, (4) any label like Input, Output, Target, X1, X2, Bias, eta=5. Be exhaustive and terse; output a plain list."

run topbox "$NS/_pool/crops028/topbox.png" \
"This image is a 710x180 crop of a 960x540 slide, upscaled 2x from source region x=40..395, y=68..158. It shows a red-bordered box containing two equations. (1) Give the bbox in THIS image of the red box border. (2) Give the exact equation text of each of the two lines with proper sub/superscripts, and the bbox of each line in THIS image. (3) State the font color of each line."

run leftcol "$NS/_pool/crops028/leftcol.png" \
"This image is a 790x704 crop of a 960x540 slide, upscaled 2x from source region x=45..440, y=188..540. List every text line from TOP to BOTTOM: exact string, bbox in THIS image, and text color. Also list every rectangular box outline with its bbox. Be exhaustive."

run rightcol "$NS/_pool/crops028/rightcol.png" \
"This image is a 990x704 crop of a 960x540 slide, upscaled 2x from source region x=430..925, y=188..540. List every text line from TOP to BOTTOM: exact string, bbox in THIS image, and text color. Also list every rectangular box outline with its bbox. Be exhaustive."

echo "ALL DONE $(date -Is)" >> "$LOG"
