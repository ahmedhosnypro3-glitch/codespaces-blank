const pptxgen = require("pptxgenjs");
const PptxGenJS = pptxgen.default || pptxgen;
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const BADGE_OUTLINE = "FFF9C4";
const BADGE_TEXT = "333333";
const TEXT = "000000";
const PURPLE = "8E44AD";
const BLUE = "3498DB";
const GREEN = "2ECC71";
const DARK_GRAY = "2C3E50";
const WHITE = "FFFFFF";
const BEIGE = "E8E0D0";
const BLACK = "000000";
const GREY = "BFBFBF";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ===== HOUSE CHROME =====
s.addShape(pptx.ShapeType.rect, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.ShapeType.ellipse, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: BADGE_OUTLINE, width: 1.5 },
});
s.addText("8", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_TEXT, fontFace: FONT, margin: 0,
});
s.addShape(pptx.ShapeType.rect, {
  x: 0, y: H - 0.05, w: W, h: 0.05, fill: { color: BLACK },
});

// ===== SLIDE 8 CONTENT =====
// Beige panel: x=4.85-10.59in, y=1.24-2.92in
const boxX = 4.85;
const boxY = 1.24;
const boxW = 5.74;
const boxH = 1.68;
s.addShape(pptx.ShapeType.rect, {
  x: boxX, y: boxY, w: boxW, h: boxH, fill: { color: BEIGE },
});

// -------------------------------------------------------------
// LAYER 1 (leftmost): purple input dots at x=5.60in
// 4 dots at y=1.24, 1.80, 2.40, plus one at 1.55 (5 total per judge)
const inputX = 5.60;
const inputYs = [1.28, 1.58, 1.84, 2.16, 2.42];

// -------------------------------------------------------------
// LAYER 2: grey/blue Sigma circles at x=5.78-5.95in with red arrows
const sigma1X = 5.78;
const sigma1Ys = [1.24, 1.80, 2.40];

// -------------------------------------------------------------
// LAYER 3: blue Sigma nodes at x=6.80in
const hiddenX = 6.80;
const hiddenYStart = boxY + 0.16;
const hiddenYStep = (boxH - 0.32) / 2;

// -------------------------------------------------------------
// LAYER 4: green Sigma nodes at x=8.72in
const outputX = 8.72;
const outputYStart = boxY + 0.16;
const outputYStep = (boxH - 0.32) / 2;

// -------------------------------------------------------------
// FORWARD CONNECTIONS (purple mesh): input -> sigma1 -> hidden -> output
for (let i = 0; i < 5; i++) {
  const iy = inputYs[i];
  for (let a = 0; a < 3; a++) {
    const ay = sigma1Ys[a];
    s.addShape(pptx.ShapeType.line, {
      x: inputX + 0.06, y: iy, w: sigma1X - inputX - 0.06, h: ay - iy,
      line: { color: PURPLE, width: 0.75 },
    });
  }
}

for (let a = 0; a < 3; a++) {
  const ay = sigma1Ys[a];
  for (let h = 0; h < 3; h++) {
    const hy = hiddenYStart + h * hiddenYStep;
    s.addShape(pptx.ShapeType.line, {
      x: sigma1X + 0.09, y: ay, w: hiddenX - sigma1X - 0.09, h: hy - ay,
      line: { color: PURPLE, width: 0.75 },
    });
  }
}

for (let h = 0; h < 3; h++) {
  const hy = hiddenYStart + h * hiddenYStep;
  for (let o = 0; o < 3; o++) {
    const oy = outputYStart + o * outputYStep;
    s.addShape(pptx.ShapeType.line, {
      x: hiddenX + 0.175, y: hy, w: outputX - hiddenX - 0.175, h: oy - hy,
      line: { color: PURPLE, width: 0.75 },
    });
  }
}

// -------------------------------------------------------------
// RED BACK-PROPAGATION LINES (output -> hidden, thin red)
// Vertical red column at x=8.53in from hidden-layer top to bottom
s.addShape(pptx.ShapeType.line, {
  x: 8.53, y: hiddenYStart, w: 0, h: (boxH - 0.32),
  line: { color: RED, width: 1.25 },
});
// Red vertical column at x=7.20in (left of blue layer, bias/back-prop)
s.addShape(pptx.ShapeType.line, {
  x: 7.20, y: 1.12, w: 0, h: 1.30,
  line: { color: RED, width: 1.25 },
});
// Red vertical column at x=7.73in
s.addShape(pptx.ShapeType.line, {
  x: 7.73, y: 1.11, w: 0, h: 1.33,
  line: { color: RED, width: 1.25 },
});

// -------------------------------------------------------------
// INPUT DOTS (5 purple dots)
for (let i = 0; i < 5; i++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: inputX, y: inputYs[i], w: 0.11, h: 0.11, fill: { color: PURPLE },
  });
}

// -------------------------------------------------------------
// LAYER 2: grey Sigma circles with RED arrows to blue layer
for (let a = 0; a < 3; a++) {
  const ay = sigma1Ys[a];
  s.addShape(pptx.ShapeType.ellipse, {
    x: sigma1X, y: ay, w: 0.18, h: 0.18, fill: { color: GREY },
  });
  s.addText("Σ", {
    x: sigma1X, y: ay, w: 0.18, h: 0.18,
    align: "center", valign: "middle", fontSize: 9, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
  // Red arrow from this Sigma node to the blue hidden layer
  s.addShape(pptx.ShapeType.rightArrow, {
    x: sigma1X + 0.19, y: ay + 0.03, w: hiddenX - sigma1X - 0.20, h: 0.06,
    fill: { color: RED },
  });
}

// -------------------------------------------------------------
// HIDDEN NODES (blue circles with sigma)
for (let h = 0; h < 3; h++) {
  const hy = hiddenYStart + h * hiddenYStep;
  s.addShape(pptx.ShapeType.ellipse, {
    x: hiddenX, y: hy, w: 0.35, h: 0.35, fill: { color: BLUE },
  });
  s.addText("Σ", {
    x: hiddenX, y: hy, w: 0.35, h: 0.35,
    align: "center", valign: "middle", fontSize: 16, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  });
  s.addText("Net", { x: hiddenX - 0.6, y: hy - 0.1, w: 0.5, h: 0.2, fontSize: 10, color: DARK_GRAY, fontFace: FONT, margin: 0 });
  s.addText("O",   { x: hiddenX - 0.6, y: hy + 0.05, w: 0.5, h: 0.2, fontSize: 10, color: DARK_GRAY, fontFace: FONT, margin: 0 });
  s.addText("w",   { x: hiddenX - 0.6, y: hy + 0.2, w: 0.5, h: 0.2, fontSize: 10, color: DARK_GRAY, fontFace: FONT, margin: 0 });
}

// -------------------------------------------------------------
// OUTPUT NODES (green circles with sigma) + small green square glyphs
for (let o = 0; o < 3; o++) {
  const oy = outputYStart + o * outputYStep;
  s.addShape(pptx.ShapeType.ellipse, {
    x: outputX, y: oy, w: 0.35, h: 0.35, fill: { color: GREEN },
  });
  s.addText("Σ", {
    x: outputX, y: oy, w: 0.35, h: 0.35,
    align: "center", valign: "middle", fontSize: 16, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  });
  s.addText("Net", { x: outputX + 0.4, y: oy - 0.1, w: 0.5, h: 0.2, fontSize: 10, color: DARK_GRAY, fontFace: FONT, margin: 0 });
  s.addText("O",   { x: outputX + 0.4, y: oy + 0.05, w: 0.5, h: 0.2, fontSize: 10, color: DARK_GRAY, fontFace: FONT, margin: 0 });
  s.addText("w",   { x: outputX + 0.4, y: oy + 0.2, w: 0.5, h: 0.2, fontSize: 10, color: DARK_GRAY, fontFace: FONT, margin: 0 });
  
  // Small green SQUARE glyph adjacent to the node (measured x=8.66-8.72, y=2.70-2.88)
  s.addShape(pptx.ShapeType.rect, {
    x: outputX - 0.06, y: oy + 0.18, w: 0.10, h: 0.10, fill: { color: GREEN },
  });

  const outputLabels = ["Output 1", "Output 2", "Output m"];
  s.addText(outputLabels[o], {
    x: outputX + 0.55, y: oy, w: 1.2, h: 0.35,
    align: "left", valign: "middle", fontSize: 12, color: DARK_GRAY, fontFace: FONT, margin: 0,
  });
}

// Small red square glyphs near the connection columns
const redSquareSpots = [[7.18, 1.22], [7.26, 1.69], [7.25, 2.29], [7.66, 1.26], [7.72, 1.76], [7.66, 2.44]];
for (const [rx, ry] of redSquareSpots) {
  s.addShape(pptx.ShapeType.rect, {
    x: rx, y: ry, w: 0.09, h: 0.09, fill: { color: RED },
  });
}

// -------------------------------------------------------------
// YELLOW AUXILIARY NODES (3 dots at top: x=8.01/8.85/9.33in, y=1.00-1.25in)
const yellowXs = [8.01, 8.85, 9.33];
const yellowY = 1.00;
for (let j = 0; j < 3; j++) {
  s.addShape(pptx.ShapeType.ellipse, {
    x: yellowXs[j], y: yellowY, w: 0.17, h: 0.17, fill: { color: YELLOW },
  });
  // small w_j label beside each
  s.addText("w_j", {
    x: yellowXs[j] + 0.18, y: yellowY + 0.01, w: 0.35, h: 0.16,
    fontSize: 8, color: DARK_GRAY, fontFace: FONT, margin: 0,
  });
}

// -------------------------------------------------------------
// FEEDBACK ARROWS: curved arrows at TOP of diagram (y=0.73-1.08in)
for (let a = 0; a < 4; a++) {
  const arrowX = hiddenX + a * (outputX - hiddenX) / 3.5;
  s.addShape(pptx.ShapeType.curvedUpArrow, {
    x: arrowX, y: 0.73, w: 0.6, h: 0.35,
    line: { color: BLACK, width: 1.5 },
  });
}

// -------------------------------------------------------------
// "Multi Bias" at bottom-left INSIDE panel (dot at x=5.05in)
s.addShape(pptx.ShapeType.ellipse, {
  x: 5.05, y: 2.80, w: 0.12, h: 0.12, fill: { color: PURPLE },
});
s.addText("Multi Bias", {
  x: 5.20, y: 2.78, w: 1.2, h: 0.22, fontSize: 10, color: DARK_GRAY, fontFace: FONT, margin: 0,
});

// -------------------------------------------------------------
// BOTTOM: staggered grey up-arrow (x=6.96), purple "1" (x=7.51), green up-arrow
s.addShape(pptx.ShapeType.upArrow, {
  x: 6.88, y: 2.70, w: 0.16, h: 0.22, fill: { color: GREY },
});
s.addShape(pptx.ShapeType.ellipse, {
  x: 7.46, y: 2.78, w: 0.16, h: 0.16, fill: { color: PURPLE },
});
s.addText("1", {
  x: 7.46, y: 2.78, w: 0.16, h: 0.16,
  align: "center", valign: "middle", fontSize: 9, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addShape(pptx.ShapeType.upArrow, {
  x: 8.66, y: 2.92, w: 0.16, h: 0.22, fill: { color: GREEN },
});

// -------------------------------------------------------------
// RED "ERROR" BAR
const errorBarX = 10.64;
const errorBarW = 0.15;
const errorBarY = 0.99;
const errorBarH = 1.69;
s.addShape(pptx.ShapeType.rect, {
  x: errorBarX, y: errorBarY, w: errorBarW, h: errorBarH, fill: { color: RED },
});
// WHITE "Error" vertical text at x=10.70in (inside the bar)
const errorLetters = ["E", "r", "r", "o", "r"];
for (let i = 0; i < errorLetters.length; i++) {
  s.addText(errorLetters[i], {
    x: 10.68, y: errorBarY + 0.45 + i * 0.13,
    w: 0.10, h: 0.13,
    fontSize: 8, bold: true, color: WHITE, fontFace: FONT, margin: 0, align: "center",
  });
}

// -------------------------------------------------------------
// CLASS LABELS (GREEN) at x=10.94in
const classLabels = ["Class 1", "Class 2", "Class m"];
for (let i = 0; i < 3; i++) {
  const labelY = 1.22 + i * 0.63;
  s.addText(classLabels[i], {
    x: 10.94, y: labelY, w: 1.3, h: 0.30,
    align: "left", valign: "middle", fontSize: 11, color: GREEN, fontFace: FONT, margin: 0,
  });
}

// -------------------------------------------------------------
// EQUATION: 2D stacked fraction PNG (0.358 x 0.367 in) at x=11.87in
const eqX = 11.87;
const eqY = 0.74;
s.addImage({
  path: "videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets/eq_008_1.png",
  x: eqX, y: eqY, w: 0.358, h: 0.367,
});

// Large red question mark at x=12.15-12.29in, y=1.58-1.86in
s.addText("?", {
  x: 12.13, y: 1.50, w: 0.45, h: 0.45,
  fontSize: 26, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Output file
const outPath = "videos/machine-learning/10_nn_training_and_example/recreated_pptx/slide_008_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));