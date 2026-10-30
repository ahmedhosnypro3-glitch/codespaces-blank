#!/usr/bin/env bash
# Cut leg-B crop pairs for slide 003 attempt 19 at MATCHED effective scale.
# Render: render_19.png (2001x1125, 2.0833 px per frame px).
# Original: unique_slides/slide_003.jpg (960x540 -> upscale x2.0833 LANCZOS).
set -e
B="/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$B/recreated_pptx/qa/slide003"
K=22
cut() {
  local name="$1" x0="$2" y0="$3" x1="$4" y1="$5"
  python3 - "$B" "$Q" "$K" "$name" "$x0" "$y0" "$x1" "$y1" <<'EOF'
import sys
from PIL import Image
B, Q, K, name, x0, y0, x1, y1 = sys.argv[1:9]
x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
orig = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
ren = Image.open(Q + "/render_%s.png" % K).convert("RGB")
S = ren.size[1] / 540.0
r_crop = ren.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
o_up = orig.crop((x0, y0, x1, y1)).resize((r_crop.size[0], r_crop.size[1]), Image.LANCZOS)
r_crop.save(Q + "/crop_%s_%s_render.png" % (K, name))
o_up.save(Q + "/crop_%s_%s_orig.png" % (K, name))
print("crop %-12s box=(%d,%d,%d,%d) size=%s scale=%.4f px per frame px"
      % (name, x0, y0, x1, y1, r_crop.size, S))
EOF
}
# 1. densest region: bottom design matrix + y-vector + weight vector + dim labels
cut matrix 74 320 538 520
# 2. top sample box: column headers, entries, ellipsis column, red y-labels, brackets
cut topbox 266 105 600 305
# 3. right-hand annotation boxes + bottom-right Where block
cut sideboxes 640 140 903 310
cut bottomright 538 380 903 520
echo "all leg-B crops cut for attempt $K"
