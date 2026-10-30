// slide_016.js — Neural Network Model (slide 16)
// Build: NODE_PATH=$(npm root -g) node slide_016.js
// Uses patterns: house-chrome, equations-mathtext-png, highlight-box, graph-panel-generated
// Diagram pre-rendered by gen_slide_016_diagram.py (600dpi transparent PNG)

const pptxgen = require("pptxgenjs");
const fs = require("fs");

const FONT = "Arial";
const NUM = 16;
const TITLE = "Neural Network Model";
const SUBTITLE = "(How Weights of hidden layer affect Calculated Error)";

// Colors from analysis — background corrected to house rule #E8E8E8
// (analysis reported F5E8D0 beige, but measured original is gray E8E8E8)
const BG = "E8E8E8";
const TITLE_COLOR = "70302C";
const SUBTITLE_COLOR = "7C64B8";
const FRAME_COLOR = "C00000";
const BADGE_FILL = "FFF9C4";
const BADGE_LINE = "FFF9C4";
const BADGE_TEXT = "333333";

// Eq sidecars (rendered by render_eq.py)
const EQ1 = JSON.parse(fs.readFileSync("eq1_016.json"));
const EQ2 = JSON.parse(fs.readFileSync("eq2_016.json"));
const EQ3 = JSON.parse(fs.readFileSync("eq3_016.json"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: FRAME_COLOR, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_FILL }, line: { color: BADGE_LINE, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_TEXT, fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: TITLE_COLOR, fontFace: FONT, margin: 0,
});
s.addText(SUBTITLE, {
  x: 0.6, y: 0.75, w: 12.13, h: 0.5,
  align: "center", valign: "top",
  fontSize: 16, bold: true, color: SUBTITLE_COLOR, fontFace: FONT, margin: 0,
});

// ========== EMBED DIAGRAM (graph-panel-generated pattern) ==========
s.addImage({
  path: "slide_016_diagram.png",
  x: 0.5, y: 1.3, w: 12.3, h: 4.9
});

// ========== TOP BOXES: Input Sample (left) and Target Label (right) ==========
// Input Sample box - purple rounded
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1.0, w: 1.8, h: 0.4,
  fill: { color: "DDA0DD" }, line: { color: "800080", width: 1.5 },
});
s.addText("Input Sample", {
  x: 0.5, y: 1.0, w: 1.8, h: 0.4,
  align: "center", valign: "middle", fontSize: 12, bold: true, color: "800080", fontFace: FONT, margin: 0,
});

// Target Label box - purple rounded
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 11.03, y: 1.0, w: 1.8, h: 0.4,
  fill: { color: "DDA0DD" }, line: { color: "800080", width: 1.5 },
});
s.addText("Target Label", {
  x: 11.03, y: 1.0, w: 1.8, h: 0.4,
  align: "center", valign: "middle", fontSize: 12, bold: true, color: "800080", fontFace: FONT, margin: 0,
});

// ========== ERROR BAR AND CLASS LABELS (right side) ==========
// Vertical red bar with "Error Error"
s.addShape(pres.shapes.RECTANGLE, {
  x: 12.5, y: 2.0, w: 0.4, h: 3.5,
  fill: { color: "8B0000" }, line: { type: "none" },
});
s.addText("Error Error", {
  x: 12.5, y: 2.0, w: 0.4, h: 3.5,
  align: "center", valign: "middle", fontSize: 10, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});

// Class labels - green
const CLASS_Y_START = 2.0;
const CLASS_H = 1.0;
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 12.93, y: CLASS_Y_START + i * CLASS_H, w: 1.0, h: CLASS_H,
    fill: { color: "90EE90" }, line: { color: "006400", width: 1 },
  });
  s.addText(`Class ${i+1}`, {
    x: 12.93, y: CLASS_Y_START + i * CLASS_H, w: 1.0, h: CLASS_H,
    align: "center", valign: "middle", fontSize: 12, bold: true, color: "006400", fontFace: FONT, margin: 0,
  });
}

// Output labels - orange
const OUTPUT_Y_START = 3.5;
const OUTPUT_H = 0.6;
for (let i = 0; i < 3; i++) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 12.93, y: OUTPUT_Y_START + i * OUTPUT_H, w: 1.0, h: OUTPUT_H,
    fill: { color: "FFA07A" }, line: { color: "FF4500", width: 1 },
  });
  s.addText(`Output ${i+1}`, {
    x: 12.93, y: OUTPUT_Y_START + i * OUTPUT_H, w: 1.0, h: OUTPUT_H,
    align: "center", valign: "middle", fontSize: 10, bold: true, color: "FF4500", fontFace: FONT, margin: 0,
  });
}

// ========== BOTTOM ANNOTATION BOXES ==========
const BOX_Y = 6.4;
const BOX_H = 1.0;
const GAP = 0.15;
// 6 boxes: 3 layer boxes + note box + 2 equation boxes
// Total inner width = 12.53in; 5 gaps @ 0.15 = 0.75; 6 boxes = 11.78 / 6 = ~1.96 each
const B1_X = 0.5, B1_W = 2.0;
const B2_X = B1_X + B1_W + GAP, B2_W = 2.0;
const B3_X = B2_X + B2_W + GAP, B3_W = 2.0;
const B4_X = B3_X + B3_W + GAP, B4_W = 2.0;
const B5_X = B4_X + B4_W + GAP, B5_W = 2.6;
const B6_X = B5_X + B5_W + GAP, B6_W = 2.6;

// Box 1: Previous Layer (l) with up arrow "i" - blue
s.addShape(pres.shapes.RECTANGLE, {
  x: B1_X, y: BOX_Y, w: B1_W, h: BOX_H,
  fill: { color: "E6F3FF" }, line: { color: "0000FF", width: 1 },
});
s.addText('Previous Layer (l)', {
  x: B1_X, y: BOX_Y + 0.35, w: B1_W, h: 0.3,
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0.08,
});
s.addText("↑ i", { x: B1_X, y: BOX_Y + 0.02, w: B1_W, h: 0.3, align: "center", valign: "bottom", fontSize: 14, color: "000000", fontFace: FONT, margin: 0 });

// Box 2: Current Layer (You are here) - green
s.addShape(pres.shapes.RECTANGLE, {
  x: B2_X, y: BOX_Y, w: B2_W, h: BOX_H,
  fill: { color: "E6FFE6" }, line: { color: "008000", width: 1 },
});
s.addText('Current Layer (You are here)', {
  x: B2_X, y: BOX_Y + 0.35, w: B2_W, h: 0.3,
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0.08,
});
s.addText("↑ j", { x: B2_X, y: BOX_Y + 0.02, w: B2_W, h: 0.3, align: "center", valign: "bottom", fontSize: 14, color: "000000", fontFace: FONT, margin: 0 });

// Box 3: Next Layer (K) - orange
s.addShape(pres.shapes.RECTANGLE, {
  x: B3_X, y: BOX_Y, w: B3_W, h: BOX_H,
  fill: { color: "FFE6CC" }, line: { color: "FF8C00", width: 1 },
});
s.addText('Next Layer (K)', {
  x: B3_X, y: BOX_Y + 0.35, w: B3_W, h: 0.3,
  align: "center", valign: "middle", fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0.08,
});
s.addText("↑ k", { x: B3_X, y: BOX_Y + 0.02, w: B3_W, h: 0.3, align: "center", valign: "bottom", fontSize: 14, color: "000000", fontFace: FONT, margin: 0 });

// Box 4: Note: Layer "j" is NOT Output Layer - white with red border
s.addShape(pres.shapes.RECTANGLE, {
  x: B4_X, y: BOX_Y, w: B4_W, h: BOX_H,
  fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 },
});
s.addText('Note: Layer "j" is NOT Output Layer', {
  x: B4_X, y: BOX_Y + 0.35, w: B4_W, h: 0.3,
  align: "center", valign: "middle", fontSize: 10, bold: true, color: "FF0000", fontFace: FONT, margin: 0.08,
});

// Box 5: Equation box bottom-left with header "For Layer \"j\"" and two equations
s.addShape(pres.shapes.RECTANGLE, {
  x: B5_X, y: BOX_Y, w: B5_W, h: BOX_H,
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});
s.addText('For Layer "j"', {
  x: B5_X, y: BOX_Y, w: B5_W, h: 0.25,
  align: "left", valign: "top", fontSize: 11, bold: true, color: "000000", fontFace: FONT, margin: 0.08,
});
s.addImage({ path: "eq1_016.png", x: B5_X + 0.15, y: BOX_Y + 0.3 - EQ1.baseline_frac * EQ1.h_in, w: EQ1.w_in, h: EQ1.h_in });
s.addImage({ path: "eq2_016.png", x: B5_X + 0.15, y: BOX_Y + 0.6 - EQ2.baseline_frac * EQ2.h_in, w: EQ2.w_in, h: EQ2.h_in });

// Box 6: Equation box bottom-right with error formula and three red X marks
s.addShape(pres.shapes.RECTANGLE, {
  x: B6_X, y: BOX_Y, w: B6_W, h: BOX_H,
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});
s.addImage({ path: "eq3_016.png", x: B6_X + 0.1, y: BOX_Y + 0.2 - EQ3.baseline_frac * EQ3.h_in, w: EQ3.w_in, h: EQ3.h_in });

// ========== WRITE ==========
pres.writeFile({ fileName: "slide_016_recreated.pptx" })
  .then(() => console.log("wrote slide_016_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });