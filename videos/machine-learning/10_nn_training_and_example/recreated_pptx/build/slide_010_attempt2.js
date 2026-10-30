// slide_010_attempt2.js — rebuild of slide 10 per b05 fresh audit + validated final.
// Layout mirrors certified slide_009.js geometry; slide-10 adds the delta rule band.
// Run from project root: NODE_PATH=$(npm root -g) node videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_010_attempt2.js
const pptxgen = require("pptxgenjs");
const FONT = "Arial";
const NUM = "10";
const B = "videos/machine-learning/10_nn_training_and_example/recreated_pptx/build";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ===== HOUSE CHROME (machine-learning family) =====
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(NUM, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Gradient Descent", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

const WHITE = "FFFFFF", RED = "FF0000", REDD = "C00000", BLUE = "0000FF";
const BLK = "000000", GREEN = "008000";
const EQ = require("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/eq_slide_010b/sidecars.json");
function eq(name, x, y) {
  const e = EQ[name];
  s.addImage({ path: `${B}/eq_slide_010b/${name}.png`, x, y, w: e.w_in, h: e.h_in });
}
function box(x, y, w, h, fill, lineColor, lw) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill }, line: { color: lineColor, width: lw },
  });
}
function txt(str, x, y, w, h, size, color, opts) {
  s.addText(str, Object.assign({
    x, y, w, h, align: "left", valign: "middle",
    fontSize: size, color, fontFace: FONT, margin: 0,
  }, opts || {}));
}

// ===== 1. TOP-LEFT UPDATE-EQUATION BOX (red border, white fill) =====
box(0.90, 1.05, 3.75, 1.85, WHITE, RED, 1.5);
eq("eq1", 1.00, 1.28);
eq("eq2", 1.00, 1.70);
txt("Where", 1.00, 2.16, 0.58, 0.26, 14, RED, { italic: true, bold: true });
eq("eq3", 1.62, 2.14);

// ===== 2. NEURAL-NETWORK DIAGRAM (generated raster on beige panel) =====
s.addImage({ path: `${B}/assets/diagram_010.png`, x: 5.32, y: 0.75, w: 5.65, h: 2.10 });

// ===== 3. ERROR STRIP (red vertical bar, white vertical text) + Class labels =====
s.addShape(pres.shapes.RECTANGLE, {
  x: 10.86, y: 0.86, w: 0.17, h: 1.69, fill: { color: RED }, line: { type: "none" },
});
const errLetters = ["E", "r", "r", "o", "r"];
for (let i = 0; i < errLetters.length; i++) {
  txt(errLetters[i], 10.865, 1.22 + i * 0.13, 0.16, 0.13, 8, WHITE,
      { align: "center", bold: true });
}
const cls = ["Class 1", "Class 2", "Class m"];
for (let i = 0; i < 3; i++) {
  txt(cls[i], 11.12, 0.94 + i * 0.60, 1.30, 0.28, 10, GREEN);
}

// ===== 4. MIDDLE EQUATION STRIP (white box, red border) =====
box(0.89, 3.45, 11.63, 0.75, WHITE, REDD, 1.5);
eq("eq4", 0.95, 3.60);
txt("For Sigmoid Activation", 4.70, 3.72, 1.58, 0.22, 11, "1F3F9E",
    { italic: true, bold: true });
eq("eq5", 6.35, 3.68);
eq("eq6", 10.05, 3.62);

// ===== 5. DERIVATIVE BOXES ROW (white boxes, blue borders) =====
box(0.90, 4.40, 2.85, 0.62, WHITE, BLUE, 1.5);
box(5.05, 4.40, 2.60, 0.62, WHITE, BLUE, 1.5);
box(10.43, 4.40, 2.09, 0.62, WHITE, BLUE, 1.5);
eq("eq7", 1.66, 4.57);
eq("eq8", 5.60, 4.55);
eq("eq9", 11.07, 4.55);

// ===== 6. CHAIN-RULE BOX (bottom-left, white, red border, highlights) =====
box(0.90, 5.15, 8.60, 1.60, WHITE, RED, 1.5);
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.30, y: 5.22, w: 1.60, h: 0.42, fill: { color: "B0E0E6" }, line: { type: "none" },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.00, y: 5.62, w: 3.50, h: 0.34, fill: { color: "90EE90" }, line: { type: "none" },
});
eq("eq10", 1.05, 5.27);
eq("eq11", 1.05, 5.68);
txt("Where", 1.05, 6.00, 0.60, 0.26, 13, RED, { italic: true, bold: true });
eq("eq12", 1.70, 5.98);

// ===== 7. SUMMARY BOX (bottom-right, pale yellow, blue border) =====
box(10.35, 5.15, 2.17, 1.60, "FFFFE0", BLUE, 1.5);
eq("eq7", 10.66, 5.30);
eq("eq8", 10.68, 5.75);
eq("eq9", 11.07, 6.20);

// ===== 8. BOTTOM DELTA-RULE STRIP =====
box(0.30, 6.88, 12.73, 0.42, WHITE, BLK, 1);
s.addShape(pres.shapes.RECTANGLE, {
  x: 3.02, y: 6.93, w: 3.90, h: 0.32, fill: { color: "90EE90" }, line: { type: "none" },
});
eq("eq13", 0.45, 6.94);
txt("Where", 2.45, 6.96, 0.55, 0.26, 12, REDD, { italic: true, bold: true });
eq("eq14", 3.05, 6.98);

// ===== 9. FOOTER BAR =====
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.05, w: W, h: 0.05, fill: { color: BLK }, line: { type: "none" },
});

const outPath = "videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_010_attempt2.pptx";
pres.writeFile({ fileName: outPath })
  .then(() => console.log("wrote " + outPath))
  .catch(e => { console.error(e); process.exit(1); });
