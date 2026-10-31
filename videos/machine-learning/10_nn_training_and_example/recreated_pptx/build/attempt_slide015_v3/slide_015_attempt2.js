// slide_015_attempt2.js v3 — error-bar caption fixed: 3 words "Error Error Error" (PIL-measured), caption as 600dpi PNG
// Build: NODE_PATH=$(npm root -g) node slide_015_attempt2.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const FONT = "Arial";
const NUM = 15;
const TITLE = "Neural Network Model";
const SUBTITLE = "(Weights of hidden layer AFFECT Calculated Error)";

const BG = "E8E8E8";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// house chrome
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3, fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText(String(NUM), { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0 });
s.addText(TITLE, { x: 0.6, y: 0.28, w: 12.13, h: 0.5, align: "center", valign: "top", fontSize: 24, bold: true, color: "70302C", fontFace: FONT, margin: 0 });
s.addText(SUBTITLE, { x: 0.6, y: 0.75, w: 12.13, h: 0.45, align: "center", valign: "top", fontSize: 15, bold: true, color: "7C64B8", fontFace: FONT, margin: 0 });

// network diagram (v2, canvas == placement, no stretch)
s.addImage({ path: "slide_015_diagram_v2.png", x: 0.5, y: 1.3, w: 12.3, h: 4.4 });

// Input Sample / Target Label boxes (measured: 0.89..1.79 / 11.36..12.25, y 1.33..1.74)
for (const [bx, label] of [[0.89, "Input Sample"], [11.36, "Target Label"]]) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: bx, y: 1.33, w: 0.9, h: 0.41, fill: { color: "DDA0DD" }, line: { color: "800080", width: 1.5 } });
  s.addText(label, { x: bx, y: 1.33, w: 0.9, h: 0.41, align: "center", valign: "middle", fontSize: 9, bold: true, color: "800080", fontFace: FONT, margin: 0 });
}

// error bar (measured x 10.96..11.26, y 2.08..5.04)
s.addShape(pres.shapes.RECTANGLE, { x: 10.96, y: 2.08, w: 0.31, h: 2.96, fill: { color: "8B0000" }, line: { type: "none" } });
// caption "Error Error Error": three words, PIL-measured clusters inside the bar.
// Rendered as one 600dpi PNG (canvas == bar size) for per-word placement control.
s.addImage({ path: "errcap_015.png", x: 10.96, y: 2.08, w: 0.31, h: 2.96 });

// Class labels: plain green text (measured x 11.39..12.25, rows y~2.53/3.53/4.66)
for (const [cy, lab] of [[2.53, "Class 1"], [3.53, "Class 2"], [4.66, "Class m"]]) {
  s.addText(lab, { x: 11.39, y: cy - 0.1, w: 0.86, h: 0.2, align: "left", valign: "middle", fontSize: 9, bold: true, color: "006400", fontFace: FONT, margin: 0 });
}
// annotation row (measured y 5.70..6.14): 5 boxes
const ANN_Y = 5.70, ANN_H = 0.42;
const ann = [
  [0.96, 1.42, 'For Layer "j"', "FFFFFF", "000000", "C00000"],
  [3.00, 1.22, "Previous Layer (l)", "BBDEFB", "0000FF", "000000"],
  [5.31, 1.26, "Current Layer (You are here)", "C8E6C9", "008000", "000000"],
  [7.68, 1.01, "Next Layer (K)", "FFE6CC", "FF8C00", "000000"],
];
for (const [bx, bw, txt, fill, line, tcol] of ann) {
  s.addShape(pres.shapes.RECTANGLE, { x: bx, y: ANN_Y, w: bw, h: ANN_H, fill: { color: fill }, line: { color: line, width: 1.2 } });
  s.addText(txt, { x: bx, y: ANN_Y, w: bw, h: ANN_H, align: "center", valign: "middle", fontSize: 8, bold: true, color: tcol, fontFace: FONT, margin: 0.03 });
}
// up-arrow labels above boxes 2-4
for (const [bx, lab] of [[3.0, "i"], [5.31, "j"], [7.68, "k"]]) {
  s.addText("↑ " + lab, { x: bx, y: ANN_Y - 0.28, w: 1.0, h: 0.26, align: "center", valign: "bottom", fontSize: 12, color: "000000", fontFace: FONT, margin: 0 });
}
// note box (measured x 8.99..12.4, y 5.78..6.14)
s.addShape(pres.shapes.RECTANGLE, { x: 8.99, y: 5.78, w: 3.41, h: 0.36, fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 } });
s.addText('Note: Layer "j" is NOT Output Layer', { x: 8.99, y: 5.78, w: 3.41, h: 0.36, align: "center", valign: "middle", fontSize: 9, bold: true, color: "FF0000", fontFace: FONT, margin: 0.03 });

// equation band: full-width tan panel (measured x 0.83..12.49, y 6.0..7.15)
s.addShape(pres.shapes.RECTANGLE, { x: 0.83, y: 6.0, w: 11.66, h: 1.15, fill: { color: "F5E6D3" }, line: { color: "D8CBB8", width: 0.75 } });
// white eq boxes (measured left 1.01..3.54 y 6.14..7.07 ; right 8.79..12.38 y 6.25..6.97)
s.addShape(pres.shapes.RECTANGLE, { x: 1.01, y: 6.14, w: 2.53, h: 0.93, fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });
s.addShape(pres.shapes.RECTANGLE, { x: 8.79, y: 6.25, w: 3.59, h: 0.72, fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });

const E1 = JSON.parse(fs.readFileSync("eq1_015_v2.json"));
const E2 = JSON.parse(fs.readFileSync("eq2_015_v2.json"));
const E3 = JSON.parse(fs.readFileSync("eq3_015_v2.json"));
s.addImage({ path: E1.path, x: 1.16, y: 6.21, w: E1.w_in, h: E1.h_in });
s.addImage({ path: E2.path, x: 1.16, y: 6.58, w: E2.w_in, h: E2.h_in });
s.addImage({ path: E3.path, x: 8.93, y: 6.42, w: E3.w_in, h: E3.h_in });
s.addText("X X X", { x: 10.45, y: 6.42, w: 1.6, h: 0.4, align: "left", valign: "middle", fontSize: 14, bold: true, color: "FF0000", fontFace: FONT, margin: 0 });

pres.writeFile({ fileName: "slide_015_attempt2.pptx" })
  .then(() => console.log("wrote slide_015_attempt2.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
