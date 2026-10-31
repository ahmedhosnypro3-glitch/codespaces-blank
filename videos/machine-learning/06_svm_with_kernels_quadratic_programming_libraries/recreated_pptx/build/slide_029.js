// slide_029.js — REBUILD WAVE 3 from qa/reanalysis2/slide_029_analysis.txt ONLY.
// Spec coords [x0,y0,x1,y1] normalized -> inches: x*13.33, y*7.5.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_029.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = NS + "/recreated_pptx/build/eq_029_v2/";
const man = JSON.parse(fs.readFileSync(EQ + "manifest.json", "utf8"));
const W = 13.33, H = 7.5;
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House chrome (overrides spec): red frame, badge, title box
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("29", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Radial Basis Function (RBF) Kernel", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.45,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

function box(x0, y0, x1, y1, fill, line, lw) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: x0 * W, y: y0 * H, w: (x1 - x0) * W, h: (y1 - y0) * H,
    fill: { color: fill }, line: { color: line, width: lw || 1 },
  });
}
// Left column: three purple-bordered white boxes (spec section 4)
box(0.081, 0.167, 0.510, 0.230, "FFFFFF", "3333CC", 1);
box(0.081, 0.259, 0.510, 0.333, "FFFFFF", "3333CC", 1);
box(0.081, 0.369, 0.510, 0.794, "FFFFFF", "3333CC", 1);
// Right panel: red border, white fill; inner purple box around e^x series
box(0.524, 0.163, 0.871, 0.644, "FFFFFF", "CC0000", 1.5);
box(0.527, 0.219, 0.865, 0.291, "FFFFFF", "3333CC", 1);
// Yellow rounded highlights behind the phi labels
for (const b of [[0.182, 0.467, 0.251, 0.520], [0.332, 0.594, 0.397, 0.650]]) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: b[0] * W, y: b[1] * H, w: (b[2] - b[0]) * W, h: (b[3] - b[1]) * H,
    fill: { color: "FFFF99" }, line: { type: "none" }, adj: 0.3,
  });
}
// Small white pen-cursor glyph with dark outline (spec IMAGERY)
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: 0.288 * W, y: 0.641 * H, w: (0.305 - 0.288) * W, h: (0.672 - 0.641) * H,
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 }, rotate: 225,
});
// Black player/crop band across the bottom (spec section 4), drawn last
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.038 * W, y: 0.852 * H, w: (0.921 - 0.038) * W, h: (1.000 - 0.852) * H,
  fill: { color: "000000" }, line: { type: "none" },
});
// Equation PNGs at exact size (w = px/600 in, never rescaled), left-aligned
// at x0, vertically centered in the spec band [y0,y1].
function eq(name, x0, y0, x1, y1) {
  const m = man[name];
  const bh = (y1 - y0) * H;
  s.addImage({ path: EQ + m.file, x: x0 * W, y: y0 * H + Math.max(0, (bh - m.h_in) / 2), w: m.w_in, h: m.h_in });
}
eq("e1", 0.090, 0.167, 0.510, 0.230);     // RBF identity, box 1 (centered in box)
eq("e2", 0.086, 0.259, 0.510, 0.333);     // Taylor series of e^{ab}, box 2 (in box)
eq("e3_eq", 0.090, 0.393, 0.127, 0.426);  // "e^{ab} =" lead-in, box 3
eq("e3_row", 0.130, 0.389, 0.365, 0.444); // bracketed row vector
eq("e3_col", 0.400, 0.395, 0.505, 0.785); // bracketed column vector
eq("e4", 0.533, 0.231, 0.859, 0.281);     // e^x series, inner box
eq("e5", 0.533, 0.311, 0.854, 0.365);     // e^3 series line
eq("phi_a", 0.182, 0.467, 0.251, 0.520);  // phi(a)^T on yellow highlight
eq("phi_b", 0.332, 0.594, 0.397, 0.650);  // phi(b) on yellow highlight

// Right panel heading (dark red bold, spec section 2 HEADER)
s.addText("Taylor series expansion of (x)", {
  x: 0.534 * W, y: 0.174 * H, w: (0.729 - 0.534) * W, h: (0.200 - 0.174) * H,
  align: "left", valign: "middle",
  fontSize: 11, bold: true, color: "990000", fontFace: FONT, margin: 0,
});

// Approximation list: 7 rows in [0.533,0.381,0.761,0.619], pitch 0.034
// label (left) | blue => arrow at x~0.645 | dark-red bold value at x~0.665
const rows = [
  ["Approx. to 4 terms", "13", false],
  ["Approx. to 5 terms", "16.375", false],
  ["Approx. to 6 terms", "18.4", false],
  ["Approx. to 7 terms", "19.413", false],
  ["Approx. to 8 terms", "19.84", false],
  ["Approx. to 9 terms", "19.8420.01", false],
  ["Actual Value", "20.086", true],
];
rows.forEach((r, i) => {
  const y = (0.381 + i * 0.034) * H, h = 0.030 * H;
  s.addText(r[0], {
    x: 0.533 * W, y: y, w: (0.640 - 0.533) * W, h: h,
    align: "left", valign: "middle", fontSize: 10, bold: r[2],
    color: "000000", fontFace: FONT, margin: 0,
  });
  s.addText("\u21D2", {
    x: 0.645 * W, y: y, w: (0.662 - 0.645) * W, h: h,
    align: "center", valign: "middle", fontSize: 10, bold: true,
    color: "3333CC", fontFace: FONT, margin: 0,
  });
  s.addText(r[1], {
    x: 0.665 * W, y: y, w: (0.761 - 0.665) * W, h: h,
    align: "left", valign: "middle", fontSize: 10, bold: true,
    color: "990000", fontFace: FONT, margin: 0,
  });
});

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_029_recreated.pptx") })
  .then(() => console.log("wrote slide_029_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
