const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE_HEAD = "0000FF";
const BLUE_PANEL_B = "0000CC";
const GREEN = "00CC00";
const RED_BRIGHT = "FF0000";
const ORANGE = "FFA500";
const PURPLE = "800080";
const LIGHT_PINK = "FF9999";
const LIGHT_GREEN = "99FF99";
const LIGHT_YELLOW = "FFFFE0";
const DARK_RED = "A00000";
const CRIMSON = "C00000";
const GRAY = "808080";
const BLACK = "000000";
const WHITE = "FFFFFF";
const CREAM = "FFFFE0";
const LAVENDER = "E6C8E6";
const TAN = "F5CBA7";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// House frame: red rectangle at 0.15 inset from every edge
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});

// Slide number badge: yellow circle at top-right
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("20", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// Title box at y=0.28
s.addText("Training Samples with Labels (Two Classes)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.7,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: BLUE_HEAD, fontFace: FONT, margin: 0,
});

// LEFT REGION: light-blue filled panel enclosing both class columns
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.05, w: 7.15, h: 5.1,
  fill: { color: "DCE6F1" }, line: { color: BLUE_PANEL_B, width: 1 },
});

// Positive Class column: x=0.6..3.5
s.addText("Positive Class", {
  x: 0.6, y: 1.2, w: 2.0, h: 0.35,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: CRIMSON, fontFace: FONT, margin: 0,
});
s.addText('"Shoot the Enemy"', {
  x: 2.3, y: 1.28, w: 1.3, h: 0.3,
  align: "left", valign: "top",
  fontSize: 14, color: CRIMSON, fontFace: FONT, margin: 0,
});
// Label header to the right of the caption line, above the +1 strip
s.addText("Label", {
  x: 3.55, y: 1.28, w: 0.45, h: 0.3,
  align: "center", valign: "top",
  fontSize: 14, color: CRIMSON, fontFace: FONT, margin: 0,
});

// Positive class airplane box - red border, on panel bg
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 2.1, w: 2.9, h: 3.9,
  fill: { color: WHITE }, line: { color: RED_BRIGHT, width: 1.5 },
});

// Enemy airplane drawing (larger, with fuselage/wings/windows)
function drawEnemyPlane(slide, cx, cy, w) {
  const h = w * 0.42;
  // Fuselage (horizontal body)
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: cx - w/2, y: cy - h*0.10, w: w, h: h*0.20,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, adjustValue: 0.5,
  });
  // Nose / cockpit
  slide.addShape(pptx.shapes.OVAL, {
    x: cx + w/2 - h*0.22, y: cy - h*0.10, w: h*0.22, h: h*0.20,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 },
  });
  // Propeller
  slide.addShape(pptx.shapes.LINE, { x: cx + w/2, y: cy - h*0.30, w: 0, h: h*0.60, line: { color: GRAY, width: 1.5 } });
  slide.addShape(pptx.shapes.LINE, { x: cx + w/2 - h*0.08, y: cy, w: h*0.16, h: 0, line: { color: GRAY, width: 1 } });
  // Main wings (swept back)
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx + w*0.16, y: cy + h*0.06, w: w*0.20, h: h*0.42,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 210,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx + w*0.16, y: cy - h*0.48, w: w*0.20, h: h*0.42,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 150,
  });
  // Tail wings
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w*0.42, y: cy + h*0.06, w: w*0.18, h: h*0.36,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 195,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w*0.42, y: cy - h*0.42, w: w*0.18, h: h*0.36,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 165,
  });
  // Windows: three small circles on fuselage
  for (let i = 0; i < 3; i++) {
    slide.addShape(pptx.shapes.OVAL, {
      x: cx + w*0.08 + i * w*0.10, y: cy - h*0.045, w: h*0.09, h: h*0.09,
      fill: { color: WHITE }, line: { color: GRAY, width: 0.75 },
    });
  }
  // Skull-and-crossbones mark (red dot cluster near nose)
  slide.addShape(pptx.shapes.OVAL, {
    x: cx + w*0.26, y: cy - h*0.09, w: h*0.18, h: h*0.18,
    fill: { color: RED_BRIGHT }, line: { color: BLACK, width: 0.5 },
  });
  slide.addShape(pptx.shapes.LINE, { x: cx + w*0.26, y: cy, w: h*0.18, h: 0, line: { color: WHITE, width: 1 } });
  slide.addShape(pptx.shapes.LINE, { x: cx + w*0.26 + h*0.09, y: cy - h*0.09, w: 0, h: h*0.18, line: { color: WHITE, width: 1 } });
}

for (let i = 0; i < 5; i++) {
  const py = 2.42 + i * 0.75;
  drawEnemyPlane(s, 1.85, py, 1.7);
}

// +1 label strip at right edge of positive column
s.addShape(pptx.shapes.RECTANGLE, {
  x: 3.5, y: 2.1, w: 0.5, h: 3.9,
  fill: { color: LIGHT_PINK }, line: { color: RED_BRIGHT, width: 1 },
});
for (let i = 0; i < 5; i++) {
  const py = 2.35 + i * 0.75;
  s.addText("+1", {
    x: 3.5, y: py, w: 0.5, h: 0.6,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Negative Class column: x=4.2..7.0
s.addText("Negative Class", {
  x: 4.2, y: 1.2, w: 1.9, h: 0.35,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});
s.addText('"Safe"', {
  x: 5.8, y: 1.28, w: 0.9, h: 0.3,
  align: "left", valign: "top",
  fontSize: 14, color: GREEN, fontFace: FONT, margin: 0,
});
// Label header to the right of the caption line, above the 0 strip
s.addText("Label", {
  x: 7.05, y: 1.28, w: 0.45, h: 0.3,
  align: "center", valign: "top",
  fontSize: 14, color: GREEN, fontFace: FONT, margin: 0,
});

// Negative class airplane box - green border
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.2, y: 2.1, w: 2.8, h: 3.9,
  fill: { color: WHITE }, line: { color: GREEN, width: 1.5 },
});

// Safe (civilian) airplane drawing - same outline, no skull mark
function drawSafePlane(slide, cx, cy, w) {
  const h = w * 0.42;
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: cx - w/2, y: cy - h*0.10, w: w, h: h*0.20,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, adjustValue: 0.5,
  });
  slide.addShape(pptx.shapes.OVAL, {
    x: cx + w/2 - h*0.22, y: cy - h*0.10, w: h*0.22, h: h*0.20,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 },
  });
  slide.addShape(pptx.shapes.LINE, { x: cx + w/2, y: cy - h*0.30, w: 0, h: h*0.60, line: { color: GRAY, width: 1.5 } });
  slide.addShape(pptx.shapes.LINE, { x: cx + w/2 - h*0.08, y: cy, w: h*0.16, h: 0, line: { color: GRAY, width: 1 } });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx + w*0.16, y: cy + h*0.06, w: w*0.20, h: h*0.42,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 210,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx + w*0.16, y: cy - h*0.48, w: w*0.20, h: h*0.42,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 150,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w*0.42, y: cy + h*0.06, w: w*0.18, h: h*0.36,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 195,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w*0.42, y: cy - h*0.42, w: w*0.18, h: h*0.36,
    fill: { color: WHITE }, line: { color: GRAY, width: 1.25 }, rotate: 165,
  });
  for (let i = 0; i < 3; i++) {
    slide.addShape(pptx.shapes.OVAL, {
      x: cx + w*0.08 + i * w*0.10, y: cy - h*0.045, w: h*0.09, h: h*0.09,
      fill: { color: WHITE }, line: { color: GRAY, width: 0.75 },
    });
  }
}

for (let i = 0; i < 5; i++) {
  const py = 2.42 + i * 0.75;
  drawSafePlane(s, 5.35, py, 1.7);
}

// 0 label strip at right edge of negative column
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.0, y: 2.1, w: 0.5, h: 3.9,
  fill: { color: LIGHT_GREEN }, line: { color: GREEN, width: 1 },
});
for (let i = 0; i < 5; i++) {
  const py = 2.35 + i * 0.75;
  s.addText("0", {
    x: 7.0, y: py, w: 0.5, h: 0.6,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// RIGHT HALF
// Panel 1: Activation Function -- white rect with BLUE border, icon = lavender circle w/ sigmoid curve
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.7, y: 1.05, w: 5.1, h: 1.5,
  fill: { color: WHITE }, line: { color: BLUE_PANEL_B, width: 1.25 },
});
s.addText("Activation Function", {
  x: 7.9, y: 1.1, w: 3.2, h: 0.35,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
});
s.addText("Sigmoid function (0,+1)", {
  x: 7.9, y: 1.45, w: 3.2, h: 0.3,
  align: "left", valign: "top",
  fontSize: 14, color: "0000FF", fontFace: FONT, margin: 0,
});
s.addText('Threshold at "0.5"', {
  x: 7.9, y: 1.75, w: 3.2, h: 0.3,
  align: "left", valign: "top",
  fontSize: 14, bold: true, color: CRIMSON, fontFace: FONT, margin: 0,
});
// Icon: lavender circle containing sigmoid curve + axes
s.addShape(pptx.shapes.OVAL, {
  x: 11.6, y: 1.2, w: 1.05, h: 1.05,
  fill: { color: LAVENDER }, line: { color: PURPLE, width: 1.5 },
});
// axes inside the circle
s.addShape(pptx.shapes.LINE, { x: 11.75, y: 1.7, w: 0.75, h: 0, line: { color: PURPLE, width: 1 } });
s.addShape(pptx.shapes.LINE, { x: 12.12, y: 1.32, w: 0, h: 0.78, line: { color: PURPLE, width: 1 } });
// sigmoid curve inside the circle
(function () {
  const steps = 30;
  let px = null, py = null;
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps - 0.5) * 8;
    const sig = 1 / (1 + Math.exp(-t));
    const x = 11.78 + (i / steps) * 0.70;
    const y = 2.18 - sig * 0.72;
    if (px !== null) s.addShape(pptx.shapes.LINE, { x: px, y: py, w: x - px, h: y - py, line: { color: PURPLE, width: 1.5 } });
    px = x; py = y;
  }
})();

// Panel 2: Training -- heading ABOVE the cream rounded panel
s.addText("Training", {
  x: 7.7, y: 2.62, w: 5.1, h: 0.35,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: CRIMSON, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 7.7, y: 3.0, w: 5.1, h: 1.9,
  fill: { color: CREAM }, line: { color: DARK_RED, width: 1.25 }, adjustValue: 0.06,
});

// Flow: Input Sample -> Model -> Predicted Class -> LOSS; Label(+1,0) feeds into LOSS
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.85, y: 3.55, w: 0.85, h: 0.4,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Input\nSample", {
  x: 7.85, y: 3.55, w: 0.85, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// arrow right
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 8.72, y: 3.62, w: 0.25, h: 0.26, fill: { color: WHITE }, line: { color: CRIMSON, width: 1 } });
// Model box
s.addShape(pptx.shapes.RECTANGLE, {
  x: 9.0, y: 3.35, w: 1.75, h: 0.75,
  fill: { color: DARK_RED }, line: { color: "800000", width: 1 },
});
s.addText("Model", {
  x: 9.0, y: 3.42, w: 1.75, h: 0.22,
  align: "center", valign: "top",
  fontSize: 12, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("(Any value) (0, +1)", {
  x: 9.0, y: 3.66, w: 1.75, h: 0.22,
  align: "center", valign: "top",
  fontSize: 9, color: "FFFF00", fontFace: FONT, margin: 0,
});
// sigmoid icon in model box (small lavender circle, upper-right of the box)
s.addShape(pptx.shapes.OVAL, {
  x: 10.4, y: 3.4, w: 0.42, h: 0.42,
  fill: { color: LAVENDER }, line: { color: PURPLE, width: 1 },
});
// cross-axes inside the circle
s.addShape(pptx.shapes.LINE, { x: 10.45, y: 3.61, w: 0.32, h: 0, line: { color: PURPLE, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: 10.61, y: 3.45, w: 0, h: 0.33, line: { color: PURPLE, width: 0.75 } });
(function () {
  const steps = 16;
  let px = null, py = null;
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps - 0.5) * 8;
    const sig = 1 / (1 + Math.exp(-t));
    const x = 10.44 + (i / steps) * 0.33;
    const y = 3.78 - sig * 0.32;
    if (px !== null) s.addShape(pptx.shapes.LINE, { x: px, y: py, w: x - px, h: y - py, line: { color: PURPLE, width: 0.75 } });
    px = x; py = y;
  }
})();
// arrow right
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 10.78, y: 3.62, w: 0.25, h: 0.26, fill: { color: WHITE }, line: { color: CRIMSON, width: 1 } });
// Predicted Class
s.addShape(pptx.shapes.RECTANGLE, {
  x: 11.06, y: 3.55, w: 0.85, h: 0.4,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted\nClass", {
  x: 11.06, y: 3.55, w: 0.85, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// arrow right
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 11.93, y: 3.62, w: 0.25, h: 0.26, fill: { color: WHITE }, line: { color: CRIMSON, width: 1 } });
// LOSS circle (tan fill, crimson text)
s.addShape(pptx.shapes.OVAL, {
  x: 12.2, y: 3.45, w: 0.55, h: 0.55,
  fill: { color: TAN }, line: { color: ORANGE, width: 1.5 },
});
s.addText("LOSS", {
  x: 12.2, y: 3.45, w: 0.55, h: 0.55,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: CRIMSON, fontFace: FONT, margin: 0,
});
// Label of Input Sample (three stacked lines) feeding the LOSS from below-left
s.addText("Label of\nInput\nSample", {
  x: 11.15, y: 4.15, w: 0.95, h: 0.6,
  align: "center", valign: "top",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0, lineSpacing: 13,
});
s.addText("(+1, 0)", {
  x: 11.55, y: 4.62, w: 0.6, h: 0.22,
  align: "left", valign: "top",
  fontSize: 10, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
});
// arrow from the label block up to the LOSS circle
s.addShape(pptx.shapes.LINE, { x: 12.4, y: 4.02, w: 0, h: 0.33, line: { color: CRIMSON, width: 1, endArrowType: "triangle" }, flipV: true });

// Panel 3: Evaluation -- heading ABOVE the cream rounded panel
s.addText("Evaluation", {
  x: 7.7, y: 4.95, w: 5.1, h: 0.35,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: CRIMSON, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 7.7, y: 5.3, w: 5.1, h: 1.85,
  fill: { color: CREAM }, line: { color: DARK_RED, width: 1.25 }, adjustValue: 0.06,
});

s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.85, y: 5.85, w: 0.85, h: 0.4,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Test\nSample", {
  x: 7.85, y: 5.85, w: 0.85, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 8.72, y: 5.92, w: 0.25, h: 0.26, fill: { color: WHITE }, line: { color: CRIMSON, width: 1 } });
// Model box
s.addShape(pptx.shapes.RECTANGLE, {
  x: 9.0, y: 5.7, w: 1.75, h: 0.75,
  fill: { color: DARK_RED }, line: { color: "800000", width: 1 },
});
s.addText("Model", {
  x: 9.0, y: 5.77, w: 1.75, h: 0.22,
  align: "center", valign: "top",
  fontSize: 12, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("(Any value) (0, +1)", {
  x: 9.0, y: 6.01, w: 1.75, h: 0.22,
  align: "center", valign: "top",
  fontSize: 9, color: "FFFF00", fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.OVAL, {
  x: 10.4, y: 5.75, w: 0.42, h: 0.42,
  fill: { color: LAVENDER }, line: { color: PURPLE, width: 1 },
});
// cross-axes inside the circle
s.addShape(pptx.shapes.LINE, { x: 10.45, y: 5.96, w: 0.32, h: 0, line: { color: PURPLE, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: 10.61, y: 5.80, w: 0, h: 0.33, line: { color: PURPLE, width: 0.75 } });
(function () {
  const steps = 16;
  let px = null, py = null;
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps - 0.5) * 8;
    const sig = 1 / (1 + Math.exp(-t));
    const x = 10.44 + (i / steps) * 0.33;
    const y = 6.13 - sig * 0.32;
    if (px !== null) s.addShape(pptx.shapes.LINE, { x: px, y: py, w: x - px, h: y - py, line: { color: PURPLE, width: 0.75 } });
    px = x; py = y;
  }
})();
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 10.78, y: 5.92, w: 0.25, h: 0.26, fill: { color: WHITE }, line: { color: CRIMSON, width: 1 } });
// Predicted Class
s.addShape(pptx.shapes.RECTANGLE, {
  x: 11.06, y: 5.85, w: 0.85, h: 0.4,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted\nClass", {
  x: 11.06, y: 5.85, w: 0.85, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 11.93, y: 5.92, w: 0.25, h: 0.26, fill: { color: WHITE }, line: { color: CRIMSON, width: 1 } });
// Blue (+1, 0) inside the panel
s.addText("(+1, 0)", {
  x: 12.2, y: 5.92, w: 0.55, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_020_recreated.pptx"
}).then(() => console.log("done"));