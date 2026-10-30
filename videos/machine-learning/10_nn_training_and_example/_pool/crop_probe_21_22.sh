#!/usr/bin/env bash
# Crop-pair vision probes for originals 21 (center node) and 22 (diagram).
# Runs through the mandatory _pool/vision_gate.sh, <=2 concurrent, banked to files.
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example || exit 1
AI=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py

./_pool/vision_gate.sh timeout 540 python3 "$AI" \
  analysis qa/slide021/rejudge/orig_center_zoom.png \
  --view "ZOOMED crop of slide 21 original: center (hidden) neuron region of the backprop diagram" \
  --capture "4x upscaled crop (880x760px) of unique_slides/slide_021.jpg box (280,100)-(500,290) in 960x540 frame" \
  -p "Describe EVERY visible element in this crop precisely: each circle (fill color, outline color, approx center and radius in crop px), each dot, each text label (exact characters incl. sub/superscripts, color, italic?, approx position in crop px), each arrow (direction, start/end, color), and the hollow arrow if present with its label. State explicitly which labels touch the CENTER circle and on which side (above/below/left/right)." \
  --timeout 420 --rounds 1 --tries 1 > qa/slide021/rejudge/crop_center_analysis.txt 2>&1 &
P1=$!
sleep 15
./_pool/vision_gate.sh timeout 540 python3 "$AI" \
  analysis qa/slide022/rejudge/orig_diagram_zoom.png \
  --view "ZOOMED crop of slide 22 original: full neural-network diagram region" \
  --capture "2.5x upscaled crop (1400x500px) of unique_slides/slide_022.jpg box (0,60)-(560,260) in 960x540 frame" \
  -p "Describe the diagram in this crop exhaustively: number of node columns and rows; each node circle (fill color, outline, center+radius in crop px, symbol inside e.g. Sigma); every arrow (count, direction, color, which nodes it connects); every text label (exact chars incl. subscripts, color, position in crop px) — layer captions, Net/O labels, weight labels w_*, Output/Target labels, Error label, Neural Net caption; any small square icons. Also state the diagram bounding box in the crop and its relation to the step boxes below." \
  --timeout 420 --rounds 1 --tries 1 > qa/slide022/rejudge/crop_diagram_analysis.txt 2>&1 &
P2=$!
wait $P1 $P2
echo "crop probes done rc=$? $(date +%F\ %T)"
