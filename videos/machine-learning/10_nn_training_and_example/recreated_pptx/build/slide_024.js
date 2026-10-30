const pptxgen = require("pptxgenjs");

const FONT = "Arial";
const NUM = 24;
const TITLE = "Stopping Criteria";

const BG = "E8E8E8";         // House background
const RED = "C00000";        // Red for frames, title, status
const BLACK = "000000";      // Body text
const BLUE = "0000FF";       // Blue highlight
const YELLOW_BG = "FFFF00";  // Yellow text highlight
const BADGE_FILL = "FFD966"; // Badge fill (from analysis)
const BADGE_LINE = "000000"; // Badge outline
const BADGE_TEXT = "000000"; // Badge text
const PANEL_FILL = "FFFFFF"; // Panel fill
const PANEL_BORDER = "C00000"; // Panel border

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// ========== HOUSE CHROME ==========
// 1. Outer red frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_FILL }, line: { color: BADGE_LINE, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_TEXT, fontFace: FONT, margin: 0,
});

// 3. Title box (house position: y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 38, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ========== TOP PANEL ==========
const panelX = 0.6;
const panelW = 12.13;
const panelGap = 0.15; // gap between panels

// Top panel position and size
const topPanelY = 1.0;
const topPanelH = 2.6;

s.addShape(pres.shapes.RECTANGLE, {
  x: panelX, y: topPanelY, w: panelW, h: topPanelH,
  fill: { color: PANEL_FILL }, line: { color: PANEL_BORDER, width: 1.5 },
});

// Top panel content: 4 lines
const textX = panelX + 0.3;
const textW = panelW - 0.6;
const lineH = 0.45;
let y = topPanelY + 0.2;

// Line 1: [1] Total Error = zero (Theoretical)
s.addText("[1] Total Error = zero ", {
  x: textX, y: y, w: textW, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});
// Yellow highlight on "(Theoretical)"
s.addText("(Theoretical)", {
  x: textX + 3.5, y: y, w: 1.8, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
  fill: { color: YELLOW_BG },
});

// Line 2: [2] Total Error < certain value (Threshold)
y += lineH;
s.addText("[2] Total Error < certain value (Threshold)", {
  x: textX, y: y, w: textW, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});

// Line 3: [3] Percentage Change of Weights is less than certain value (Threshold)
y += lineH;
s.addText("[3] Percentage Change of Weights is less than certain value (Threshold)", {
  x: textX, y: y, w: textW, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});

// Line 4: [4] Reach Maximum number of iterations (Epochs) without satisfying [2] or [3]
y += lineH;
s.addText("[4] Reach Maximum number of iterations ", {
  x: textX, y: y, w: textW, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});
// Blue highlight on "(Epochs)"
s.addText("(Epochs)", {
  x: textX + 4.5, y: y, w: 1.2, h: lineH,
  fontSize: 19, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText(" without satisfying [2] or [3]", {
  x: textX + 5.7, y: y, w: textW - 5.7, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});

// ========== BOTTOM PANEL ==========
const bottomPanelY = topPanelY + topPanelH + panelGap;
const bottomPanelH = 3.0;

s.addShape(pres.shapes.RECTANGLE, {
  x: panelX, y: bottomPanelY, w: panelW, h: bottomPanelH,
  fill: { color: PANEL_FILL }, line: { color: PANEL_BORDER, width: 1.5 },
});

let by = bottomPanelY + 0.2;

// Status line (red)
s.addText("Stopping is due to reaching Maximum number of iterations = Training is FAILED", {
  x: textX, y: by, w: textW, h: lineH,
  fontSize: 19, bold: true, color: RED, fontFace: FONT, margin: 0,
});

by += lineH;

// Subheading "Expected Reasons:" (red)
s.addText("Expected Reasons:", {
  x: textX, y: by, w: textW, h: lineH,
  fontSize: 19, bold: true, color: RED, fontFace: FONT, margin: 0,
});

by += lineH;

// Reason 1: [1] The defined Maximum Number of Epochs is small. Try to increase the limit
s.addText("[1] The defined Maximum Number of ", {
  x: textX, y: by, w: textW, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("Epochs", {
  x: textX + 4.0, y: by, w: 1.0, h: lineH,
  fontSize: 19, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText(" is small. Try to increase the limit", {
  x: textX + 5.0, y: by, w: textW - 5.0, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});

by += lineH;

// Reason 2: [2] Under-fitting (Training samples are not adequate). Try to provide more training samples
s.addText("[2] Under-fitting (Training samples are not adequate). Try to provide more training samples", {
  x: textX, y: by, w: textW, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});

by += lineH;

// Reason 3: [3] Model Design is not suitable to training data. Try to add more nodes in hidden layer or add more hidden Layers
s.addText("[3] Model Design is not suitable to training data. Try to add more nodes in ", {
  x: textX, y: by, w: textW, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("hidden layer", {
  x: textX + 5.0, y: by, w: 1.5, h: lineH,
  fontSize: 19, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText(" or add more hidden Layers", {
  x: textX + 6.5, y: by, w: textW - 6.5, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});

by += lineH;

// Reason 4: [4] Data is NOT separable by Neural Network. Try Another Models (e.g. SVM with Kernels)
s.addText("[4] Data is ", {
  x: textX, y: by, w: textW, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("NOT", {
  x: textX + 1.0, y: by, w: 0.7, h: lineH,
  fontSize: 19, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText(" separable by ", {
  x: textX + 1.7, y: by, w: 2.0, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("Neural Network", {
  x: textX + 3.7, y: by, w: 2.2, h: lineH,
  fontSize: 19, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText(". Try Another Models ", {
  x: textX + 5.9, y: by, w: 2.5, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(e.g. SVM with Kernels)", {
  x: textX + 8.4, y: by, w: 2.5, h: lineH,
  fontSize: 19, color: BLACK, fontFace: FONT, margin: 0,
  fill: { color: YELLOW_BG },
});

pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_024_recreated.pptx"
}).then(() => console.log("wrote slide_024_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });
