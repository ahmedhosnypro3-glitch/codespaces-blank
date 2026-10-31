const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// Slide 005 — FRESH rebuild from qa/reanalysis2/slide_005_analysis.txt ONLY.
// Spec: SLIDE_TITLE none; x^T A x 3-variable quadratic form, coefficient
// definitions, bottom matrix -> coefficient-grid diagram. House chrome mandatory.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_005.js

const NUM = 5;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx", "build", "eq_005");
const MAN = JSON.parse(fs.readFileSync(path.join(EQ, "w3_manifest.json"), "utf8"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (overrides spec) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
// House title box (spec SLIDE_TITLE: none — box kept, no text added).
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Place a rendered mathtext PNG centered in its spec box, at exact size w = px/600.
function img(name) {
  const m = MAN[name];
  s.addImage({
    path: path.join(EQ, m.image),
    x: m.x + (m.w - m.w_in) / 2,
    y: m.y + (m.h - m.h_in) / 2,
    w: m.w_in,
    h: m.h_in,
  });
}

// ---- R2 top equation block (spec sections 2/8: E1, E2, E3) ----
["w3_e1", "w3_e2", "w3_e3"].forEach(img);

// ---- R3 coefficient-definition list (six implication lines) ----
["w3_d1", "w3_d2", "w3_d3", "w3_d4", "w3_d5", "w3_d6"].forEach(img);

// ---- R4 right annotation "Three Variables Example" (italic, right-aligned) ----
s.addText("Three Variables Example", {
  x: 0.742 * W, y: 0.405 * H, w: (0.980 - 0.742) * W, h: (0.555 - 0.405) * H,
  align: "right", valign: "middle",
  fontSize: 20, italic: true, color: "000000", fontFace: "Georgia", margin: 0,
});
// ---- R5 bottom diagram ----
// left matrix header + rows
["w3_hdr", "w3_m1", "w3_m2", "w3_m3"].forEach(img);
// cell highlights: blue outline around a_11/a_12 row, red outlines around a_22 and a_32
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.115 * W, y: 0.755 * H, w: (0.230 - 0.115) * W, h: (0.795 - 0.755) * H,
  fill: { type: "none" }, line: { color: "4472C4", width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.125 * W, y: 0.815 * H, w: (0.185 - 0.125) * W, h: (0.850 - 0.815) * H,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.125 * W, y: 0.875 * H, w: (0.185 - 0.125) * W, h: (0.910 - 0.875) * H,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
// hand-drawn connector marks between left matrix and right coefficient boxes
s.addShape(pres.shapes.LINE, {
  x: 0.315 * W, y: 0.765 * H, w: (0.420 - 0.315) * W, h: (0.805 - 0.765) * H,
  line: { color: "000000", width: 1.5 },
});
s.addShape(pres.shapes.LINE, {
  x: 0.250 * W, y: 0.805 * H, w: (0.330 - 0.250) * W, h: (0.840 - 0.805) * H,
  line: { color: "000000", width: 1.5 }, flipV: true,
});
// right 3x3 coefficient grid: red-outlined white boxes, then labels
const COLS = [[0.500, 0.640], [0.640, 0.800], [0.800, 0.965]];
const ROWS = [[0.745, 0.775], [0.805, 0.835], [0.865, 0.895]];
for (let r = 0; r < 3; r++) {
  for (let c = 0; c < 3; c++) {
    s.addShape(pres.shapes.RECTANGLE, {
      x: COLS[c][0] * W, y: ROWS[r][0] * H,
      w: (COLS[c][1] - COLS[c][0]) * W, h: (ROWS[r][1] - ROWS[r][0]) * H,
      fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.25 },
    });
  }
}
["w3_b1", "w3_b2", "w3_b3", "w3_b4", "w3_b5", "w3_b6", "w3_b7", "w3_b8", "w3_b9"].forEach(img);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx", "slide_005_recreated.pptx") });
