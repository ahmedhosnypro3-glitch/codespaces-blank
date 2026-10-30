// slide_009.js — Build "Gradient Descent" slide for 10_nn_training_and_example
// Run from project root: node videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_009.js
// Geometry measured from unique_slides/slide_009.jpg (qa/slide009/measure*.py).
// Equations: 600dpi mathtext PNGs (eq_slide_009/render_all.py) at exact px/600 size.

const pptxgen = require("pptxgenjs");
const FONT = "Arial";
const NUM = "9";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ===== HOUSE CHROME (machine-learning family — overrides per-slide spec) =====
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

// ===== content-area constants (measured) =====
const B = "videos/machine-learning/10_nn_training_and_example/recreated_pptx/build";
const WHITE = "FFFFFF", RED = "FF0000", REDD = "C00000", BLUE = "0000FF";
const GREEN = "008000", BLK = "000000";

function eq(name, x, y, w, h) {
  s.addImage({ path: `${B}/eq_slide_009/${name}.png`, x, y, w, h });
}
function box(x, y, w, h, fill, lineColor, lw) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill }, line: { color: lineColor, width: lw },
  });
}

// ===== 1. TOP-LEFT UPDATE-EQUATION BOX (red border, white fill) =====
// measured: left border x=0.92, right border x=4.64, rows 1.35..2.87
box(0.90, 1.05, 3.75, 1.85, WHITE, RED, 1.5);
eq("eq1", 1.00, 1.28, 1.99167, 0.32833);   // W^Updated = W^old - eta dE/dW
eq("eq2", 1.00, 1.70, 1.82833, 0.31333);   // W^Updated = W^old + Delta
s.addText("Where", {
  x: 1.00, y: 2.16, w: 0.58, h: 0.26,
  align: "left", valign: "middle",
  fontSize: 14, italic: true, color: RED, fontFace: FONT, margin: 0,
});
eq("eq3", 1.62, 2.14, 0.92167, 0.28);      // Delta = -eta dE/dW

// ===== 2. NEURAL-NETWORK DIAGRAM (generated image on beige panel) =====
// measured beige region: x 5.33..10.00, y 0.70..2.67
s.addImage({ path: `${B}/assets/diagram_009.png`, x: 5.33, y: 0.70, w: 4.67, h: 1.97 });

// ===== 3. ERROR PANEL (far top-right) =====
// measured red bar: x 11.11..11.28, y 0.86..2.55
s.addShape(pres.shapes.RECTANGLE, {
  x: 11.11, y: 0.86, w: 0.17, h: 1.69, fill: { color: RED }, line: { type: "none" },
});
const errLetters = ["E", "r", "r", "o", "r"];
for (let i = 0; i < errLetters.length; i++) {
  s.addText(errLetters[i], {
    x: 11.115, y: 1.22 + i * 0.13, w: 0.16, h: 0.13,
    align: "center", valign: "middle",
    fontSize: 8, bold: true, color: WHITE, fontFace: FONT, margin: 0,
  });
}
const errClasses = ["Error Class 1", "Error Class 2", "Error Class m"];
for (let i = 0; i < errClasses.length; i++) {
  s.addText(errClasses[i], {
    x: 11.36, y: 0.94 + i * 0.60, w: 1.15, h: 0.28,
    align: "left", valign: "middle",
    fontSize: 10, color: GREEN, fontFace: FONT, margin: 0,
  });
}

// ===== 4. MIDDLE EQUATION STRIP (white box, red border) =====
// measured bottom border row 302 = 4.19in, width 0.89..12.52
box(0.89, 3.45, 11.63, 0.75, WHITE, REDD, 1.5);
eq("eq4", 0.95, 3.60, 1.42667, 0.42167);    // E = 1/2 sum_j (t_j - O_j)^2
s.addText("For Sigmoid Activation", {
  x: 4.70, y: 3.72, w: 1.58, h: 0.22,
  align: "left", valign: "middle",
  fontSize: 11, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});
eq("eq5", 6.35, 3.68, 1.89833, 0.265);      // O_j = f(Net_j) = 1/(1+e^-Net_j)
eq("eq6", 10.05, 3.62, 1.36833, 0.39333);   // Net_j = sum_i (w_ji O_i)

// ===== 5. DERIVATIVE BOXES ROW (three white boxes, blue borders) =====
box(0.90, 4.40, 2.85, 0.62, WHITE, BLUE, 1.5);
eq("eq7", 1.67, 4.57, 1.31167, 0.28167);    // dE/dO_j = -(t_j - O_j)
box(5.05, 4.40, 2.60, 0.62, WHITE, BLUE, 1.5);
eq("eq8", 5.61, 4.55, 1.48167, 0.32);       // dO_j/dNet_j = O_j(1-O_j)
box(10.43, 4.40, 2.09, 0.62, WHITE, BLUE, 1.5);
eq("eq9", 11.09, 4.55, 0.78167, 0.31833);   // dNet_j/dW_ji = O_i

// ===== 6. CHAIN-RULE BOX (bottom-left, white, red border) =====
// measured: right border col 678 = 9.42in, bottom border row 453 = 6.29in
box(0.90, 5.30, 8.53, 1.05, WHITE, RED, 1.5);
eq("eq10b", 1.10, 5.42, 2.34833, 0.43833);  // dE/dW_ji = dE/dO_j * dO_j/dNet_j * dNet_j/dW_ji
eq("eq11b", 1.10, 5.90, 3.23, 0.29167);     // = -(t_j - O_j) * O_j(1-O_j) * O_i
// small grey stylus icon near the box's right side
s.addShape(pres.shapes.RECTANGLE, {
  x: 8.62, y: 5.94, w: 0.52, h: 0.09, rotate: 330,
  fill: { color: "808080" }, line: { color: "808080", width: 0.5 },
});

// ===== 7. SUMMARY DERIVATIVES BOX (bottom-right, pale yellow, blue border) =====
box(10.35, 5.30, 2.17, 1.45, "FFFFE0", BLUE, 1.5);
eq("eq12", 10.72, 5.42, 1.31167, 0.28167);
eq("eq13", 10.62, 5.82, 1.48167, 0.32);
eq("eq14", 10.97, 6.22, 0.78167, 0.31833);

// ===== 8. FOOTER BAR (bottom edge) =====
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.05, w: W, h: 0.05, fill: { color: BLK }, line: { type: "none" },
});

// Write output — single-version deliverable
const outPath = "videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_009_recreated.pptx";
pres.writeFile({ fileName: outPath })
  .then(() => console.log("wrote " + outPath))
  .catch(e => { console.error(e); process.exit(1); });
