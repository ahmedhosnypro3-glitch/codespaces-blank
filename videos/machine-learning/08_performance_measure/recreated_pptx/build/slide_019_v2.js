const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE = "000080";
const BLUE_MID = "0000FF";
const GREEN = "008000";
const RED_BRIGHT = "FF0000";
const ORANGE = "FFA500";
const PURPLE = "800080";
const LIGHT_PINK = "FF9999";
const LIGHT_GREEN = "99FF99";
const LIGHT_YELLOW = "FFFFE0";
const DARK_RED = "8B0000";
const GRAY = "808080";
const BLACK = "000000";
const WHITE = "FFFFFF";
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
s.addText("19", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// Title bar: blue rectangular header with white text
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.7,
  fill: { color: BLUE }, line: { color: "none" },
});
s.addText("Training Samples with Labels (Two Classes)", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.7,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});

// LEFT HALF: Positive Class and Negative Class columns
// Positive Class column - roughly x=0.6 to 3.5 in (8-28% width)
// Header area
s.addText("Positive Class", {
  x: 0.6, y: 1.2, w: 2.9, h: 0.35,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: BLUE_MID, fontFace: FONT, margin: 0,
});
s.addText('"Shoot the Enemy"', {
  x: 0.6, y: 1.55, w: 2.9, h: 0.3,
  align: "left", valign: "top",
  fontSize: 16, color: RED_BRIGHT, fontFace: FONT, margin: 0,
});
// Label header above the +1 strip (moved to right)
s.addText("Label", {
  x: 3.5, y: 1.55, w: 0.5, h: 0.3,
  align: "center", valign: "top",
  fontSize: 14, color: BLACK, fontFace: FONT, margin: 0,
});

// Positive class airplane drawings box - red border
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 1.9, w: 2.9, h: 4.9,
  fill: { color: BG }, line: { color: RED_BRIGHT, width: 1.5 },
});

// Placeholder for 6 airplane drawings - draw simple airplane shapes
for (let i = 0; i < 6; i++) {
  const py = 2.0 + i * 0.78;
  // Draw airplane shape using shapes
  // Fuselage
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 1.0, y: py + 0.15, w: 2.0, h: 0.15,
    fill: { color: GRAY }, line: { color: BLACK, width: 0.5 },
  });
  // Wings
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 0.8, y: py + 0.05, w: 2.4, h: 0.05,
    fill: { color: GRAY }, line: { color: BLACK, width: 0.5 },
  });
  // Tail
  s.addShape(pptx.shapes.TRIANGLE, {
    x: 2.9, y: py + 0.1, w: 0.3, h: 0.3,
    fill: { color: GRAY }, line: { color: BLACK, width: 0.5 },
  });
  // Skull-and-crossbones indicator (small black mark)
  s.addShape(pptx.shapes.OVAL, {
    x: 1.2, y: py + 0.08, w: 0.15, h: 0.15,
    fill: { color: BLACK }, line: { color: "none" },
  });
}

// Red/pink +1 label strip at right edge of positive column
s.addShape(pptx.shapes.RECTANGLE, {
  x: 3.5, y: 1.9, w: 0.5, h: 4.9,
  fill: { color: LIGHT_PINK }, line: { color: RED_BRIGHT, width: 1 },
});
for (let i = 0; i < 6; i++) {
  const py = 2.0 + i * 0.78;
  s.addText("+1", {
    x: 3.5, y: py + 0.09, w: 0.5, h: 0.6,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// Negative Class column - roughly x=4.2 to 7.0 in (35-55% width)
s.addText("Negative Class", {
  x: 4.2, y: 1.2, w: 2.8, h: 0.35,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});
s.addText('"Safe"', {
  x: 4.2, y: 1.55, w: 2.8, h: 0.3,
  align: "left", valign: "top",
  fontSize: 16, color: GREEN, fontFace: FONT, margin: 0,
});
// Label header above the -1 strip
s.addText("Label", {
  x: 7.0, y: 1.55, w: 0.5, h: 0.3,
  align: "center", valign: "top",
  fontSize: 14, color: BLACK, fontFace: FONT, margin: 0,
});

// Negative class airplane drawings box - green border
s.addShape(pptx.shapes.RECTANGLE, {
  x: 4.2, y: 1.9, w: 2.8, h: 4.9,
  fill: { color: BG }, line: { color: GREEN, width: 1.5 },
});

for (let i = 0; i < 6; i++) {
  const py = 2.0 + i * 0.78;
  // Draw airplane shape (passenger style - no skull)
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 4.6, y: py + 0.15, w: 2.0, h: 0.15,
    fill: { color: GRAY }, line: { color: BLACK, width: 0.5 },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 4.4, y: py + 0.05, w: 2.4, h: 0.05,
    fill: { color: GRAY }, line: { color: BLACK, width: 0.5 },
  });
  s.addShape(pptx.shapes.TRIANGLE, {
    x: 6.5, y: py + 0.1, w: 0.3, h: 0.3,
    fill: { color: GRAY }, line: { color: BLACK, width: 0.5 },
  });
  // Window line
  s.addShape(pptx.shapes.RECTANGLE, {
    x: 4.8, y: py + 0.15, w: 1.5, h: 0.03,
    fill: { color: BLACK }, line: { color: "none" },
  });
}

// Green -1 label strip at right edge of negative column
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.0, y: 1.9, w: 0.5, h: 4.9,
  fill: { color: LIGHT_GREEN }, line: { color: GREEN, width: 1 },
});
for (let i = 0; i < 6; i++) {
  const py = 2.0 + i * 0.78;
  s.addText("-1", {
    x: 7.0, y: py + 0.09, w: 0.5, h: 0.6,
    align: "center", valign: "middle",
    fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
}

// RIGHT HALF: Three stacked panels
// Panel 1: Activation Function (top-right, y=1.2 to 2.5, x=7.7 to 12.8)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.7, y: 1.2, w: 5.1, h: 1.3,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Activation Function", {
  x: 7.9, y: 1.25, w: 4.7, h: 0.35,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: BLUE_MID, fontFace: FONT, margin: 0,
});
s.addText("Bi-polar step (-1 , +1)", {
  x: 7.9, y: 1.6, w: 4.7, h: 0.25,
  align: "left", valign: "top",
  fontSize: 14, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText('Threshold at "zero"', {
  x: 7.9, y: 1.85, w: 4.7, h: 0.25,
  align: "left", valign: "top",
  fontSize: 14, color: BLACK, fontFace: FONT, margin: 0,
});
// Step function graph - draw as shape
// Horizontal at y=-1, vertical at x=0, horizontal at y=+1
s.addShape(pptx.shapes.RECTANGLE, {
  x: 11.5, y: 1.5, w: 1.2, h: 0.8,
  fill: { color: WHITE }, line: { color: PURPLE, width: 2 },
});
// Step function: line from left at y=bottom (y=-1) to middle, up, then right at top (y=+1)
const stepY1 = 1.5 + 0.7;  // -1 position
const stepY2 = 1.5 + 0.1;  // +1 position
const stepXmid = 11.5 + 0.6;  // middle x
// Left horizontal (-1)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 11.6, y: stepY1, w: 0.5, h: 0.03,
  fill: { color: PURPLE }, line: { color: "none" },
});
// Vertical transition
s.addShape(pptx.shapes.RECTANGLE, {
  x: stepXmid - 0.015, y: stepY2, w: 0.03, h: stepY1 - stepY2,
  fill: { color: PURPLE }, line: { color: "none" },
});
// Right horizontal (+1)
s.addShape(pptx.shapes.RECTANGLE, {
  x: stepXmid, y: stepY2, w: 0.5, h: 0.03,
  fill: { color: PURPLE }, line: { color: "none" },
});

// Panel 2: Training (middle-right, y=2.7 to 4.8)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.7, y: 2.7, w: 5.1, h: 2.1,
  fill: { color: LIGHT_YELLOW }, line: { color: BLACK, width: 1 },
});
s.addText("Training", {
  x: 7.9, y: 2.75, w: 4.7, h: 0.35,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: RED_BRIGHT, fontFace: FONT, margin: 0,
});
// Flowchart: Input Sample -> Model -> Predicted Class -> LOSS <- Label of Input Sample
// Input Sample
s.addShape(pptx.shapes.RECTANGLE, {
  x: 8.0, y: 3.2, w: 1.0, h: 0.4,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Input\nSample", {
  x: 8.0, y: 3.2, w: 1.0, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});
// Arrow to Model
s.addShape(pptx.shapes.LEFT_ARROW, {
  x: 9.0, y: 3.25, w: 0.3, h: 0.3,
  fill: { color: BLACK },
});
// Model box (dark red) - WIDER to fit "Model" text
s.addShape(pptx.shapes.RECTANGLE, {
  x: 9.3, y: 3.1, w: 1.6, h: 0.7,
  fill: { color: DARK_RED },
});
s.addText("Model", {
  x: 9.3, y: 3.12, w: 1.6, h: 0.25,
  align: "center", valign: "top",
  fontSize: 12, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("[Any value] -> [-1 , +1]", {
  x: 9.3, y: 3.35, w: 1.6, h: 0.25,
  align: "center", valign: "top",
  fontSize: 9, color: WHITE, fontFace: FONT, margin: 0,
});
// Step icon in model (purple circle with step)
s.addShape(pptx.shapes.OVAL, {
  x: 10.2, y: 3.15, w: 0.6, h: 0.6,
  fill: { color: WHITE }, line: { color: PURPLE, width: 2 },
});
// Draw step inside the circle
const icx = 10.5, icy = 3.45;
s.addShape(pptx.shapes.RECTANGLE, {
  x: icx - 0.2, y: icy + 0.15, w: 0.2, h: 0.02,
  fill: { color: PURPLE }, line: { color: "none" },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: icx - 0.01, y: icy - 0.15, w: 0.02, h: 0.3,
  fill: { color: PURPLE }, line: { color: "none" },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: icx, y: icy - 0.15, w: 0.2, h: 0.02,
  fill: { color: PURPLE }, line: { color: "none" },
});
// Arrow to Predicted Class
s.addShape(pptx.shapes.LEFT_ARROW, {
  x: 10.9, y: 3.3, w: 0.3, h: 0.3,
  fill: { color: BLACK },
});
// Predicted Class
s.addShape(pptx.shapes.RECTANGLE, {
  x: 11.2, y: 3.2, w: 1.2, h: 0.4,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted\nClass", {
  x: 11.2, y: 3.2, w: 1.2, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});
// Arrow to LOSS
s.addShape(pptx.shapes.LEFT_ARROW, {
  x: 12.4, y: 3.3, w: 0.3, h: 0.3,
  fill: { color: BLACK },
});
// LOSS circle (orange)
s.addShape(pptx.shapes.OVAL, {
  x: 12.7, y: 3.2, w: 0.6, h: 0.6,
  fill: { color: ORANGE }, line: { color: BLACK, width: 1 },
});
s.addText("LOSS", {
  x: 12.7, y: 3.2, w: 0.6, h: 0.6,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// Label of Input Sample below
s.addText("Label of\nInput Sample", {
  x: 12.7, y: 3.85, w: 0.6, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, -1)", {
  x: 12.7, y: 4.1, w: 0.6, h: 0.3,
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Panel 3: Evaluation (bottom-right, y=5.0 to 7.0)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 7.7, y: 5.0, w: 5.1, h: 2.0,
  fill: { color: LIGHT_YELLOW }, line: { color: BLACK, width: 1 },
});
s.addText("Evaluation", {
  x: 7.9, y: 5.05, w: 4.7, h: 0.35,
  align: "left", valign: "top",
  fontSize: 18, bold: true, color: RED_BRIGHT, fontFace: FONT, margin: 0,
});
// Flowchart: Test Sample -> Model -> Predicted Class -> (+1, -1)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 8.0, y: 5.5, w: 1.0, h: 0.4,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Test\nSample", {
  x: 8.0, y: 5.5, w: 1.0, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});
// Arrow to Model
s.addShape(pptx.shapes.LEFT_ARROW, {
  x: 9.0, y: 5.55, w: 0.3, h: 0.3,
  fill: { color: BLACK },
});
// Model box
s.addShape(pptx.shapes.RECTANGLE, {
  x: 9.3, y: 5.4, w: 1.6, h: 0.7,
  fill: { color: DARK_RED },
});
s.addText("Model", {
  x: 9.3, y: 5.42, w: 1.6, h: 0.25,
  align: "center", valign: "top",
  fontSize: 12, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("[Any value] -> [-1 , +1]", {
  x: 9.3, y: 5.65, w: 1.6, h: 0.25,
  align: "center", valign: "top",
  fontSize: 9, color: WHITE, fontFace: FONT, margin: 0,
});
// Step icon in model
s.addShape(pptx.shapes.OVAL, {
  x: 10.2, y: 5.45, w: 0.6, h: 0.6,
  fill: { color: WHITE }, line: { color: PURPLE, width: 2 },
});
const icx2 = 10.5, icy2 = 5.75;
s.addShape(pptx.shapes.RECTANGLE, {
  x: icx2 - 0.2, y: icy2 + 0.15, w: 0.2, h: 0.02,
  fill: { color: PURPLE }, line: { color: "none" },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: icx2 - 0.01, y: icy2 - 0.15, w: 0.02, h: 0.3,
  fill: { color: PURPLE }, line: { color: "none" },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: icx2, y: icy2 - 0.15, w: 0.2, h: 0.02,
  fill: { color: PURPLE }, line: { color: "none" },
});
// Arrow to Predicted Class
s.addShape(pptx.shapes.LEFT_ARROW, {
  x: 10.9, y: 5.6, w: 0.3, h: 0.3,
  fill: { color: BLACK },
});
// Predicted Class
s.addShape(pptx.shapes.RECTANGLE, {
  x: 11.2, y: 5.5, w: 1.2, h: 0.4,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted\nClass", {
  x: 11.2, y: 5.5, w: 1.2, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 11, color: BLACK, fontFace: FONT, margin: 0,
});
// Arrow to (+1, -1)
s.addShape(pptx.shapes.LEFT_ARROW, {
  x: 12.4, y: 5.6, w: 0.3, h: 0.3,
  fill: { color: BLACK },
});
// Blue (+1, -1) text WITH COMMA
s.addText("(+1, -1)", {
  x: 12.7, y: 5.5, w: 0.6, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: BLUE_MID, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_019_recreated.pptx"
}).then(() => console.log("done"));