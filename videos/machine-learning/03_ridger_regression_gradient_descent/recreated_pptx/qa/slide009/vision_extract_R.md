You are extracting precise geometry from a 4x LANCZOS-upscaled crop of a lecture-slide chart region (RIGHT chart of slide 9).
The crop image is 600x880 pixels. It was cut from the 960x540 slide frame at frame box (570,120)-(720,340) and magnified 4x.
Convert crop coordinates to frame coordinates: frame_x = 570 + crop_x/4, frame_y = 120 + crop_y/4.
Frame units are points (1 px = 1 pt) and y increases DOWNWARD.

Known elements in this crop (a scatter plot with a linear regression fit):
- A BLUE straight regression line runs through the lower-right of the crop: it enters the bottom edge near crop (386,880) and leaves through the right edge near crop (600,758). It climbs toward the right.
- A small isolated point/marker near crop (164,100) (frame (611,145)) - the outlier.
- A text label occupying crop x208..328, y356..580 (frame x622..652, y209..265).
- A saturated RED straight segment around crop x284..392, y356..580 (frame x641..668, y209..265). It may be either the shaft of a dimension arrow or a separate PCA-axis marker - report exactly what you see: does it touch the isolated point at crop (164,100)? Does it reach the blue line? Does it carry an arrowhead?
- A faint pale-red short streak near crop x88..140, y92..120 (frame x592..605, y143..150), and a small saturated RED blob at crop x120..148, y108..136 (frame x600..607, y147..154).

TASK - report ONLY what is visibly present, with numbers:
1. STROKES: enumerate every straight stroke you can see (exclude the blue regression line). For each: colour (name + hex estimate), both endpoints in crop px, length, and angle in degrees measured CLOCKWISE from the +x axis (screen convention with y down; horizontal = 0 deg, vertical = 90 deg, up-and-to-the-right = negative, down-and-to-the-right = positive).
2. ARROWHEADS: for every arrowhead / triangle / V-shaped tip you can see (small ones included): the tip point in crop px, the direction it points (unit vector, or "toward crop (x,y)"), and its colour.
3. LABEL: transcribe the exact text of the label; then estimate the baseline angle of that text in degrees CLOCKWISE from +x, and state explicitly whether the text ASCENDS left-to-right (rises toward the right) or DESCENDS left-to-right (falls toward the right).
4. PARALLEL LINE: does a stroke exist near the top-left of the crop that runs parallel to the blue regression line? If yes: colour, endpoints, angle. Does that stroke carry an arrowhead at either end? Answer explicitly.
5. SHAFT: does a red shaft run from the isolated point at crop (164,100) down toward the blue line? If yes: endpoints, angle. Does it have an arrowhead at the TOP (at the isolated point) and/or at the BOTTOM (at the blue line)? Answer explicitly for each end.
6. If an element is absent or ambiguous, say "ABSENT" or "AMBIGUOUS" - never invent it.

Output format: numbered sections 1..6, plain text, one fact per line. End with a single line: EXTRACTION DONE.
