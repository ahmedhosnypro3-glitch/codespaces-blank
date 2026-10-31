const pptxgen = require("pptxgenjs");

// Slide 010: Classification of "AND" Truth Table  (build v3 - wave 4)
// Geometry derived from PIL measurement of unique_slides/slide_010.jpg (960x540):
//   table box  x95-313  y138-309   plot panel x536-818 y109-368
//   nn panel   x141-500 y352-491   eq box      x576-776  y415-444
const NUM = 10;
const TITLE = 'Classification of \u201cAND\u201d Truth Table';
const FONT = "Arial";

const BG = "E8E8E8";            // house background
const DARK_RED = "C00000";      // house frame + table gridlines + plot axes + arrows
const BLACK = "000000";
const BLUE = "0000FF";          // weight labels
const NAVY = "1F3864";          // decision boundary line
const CYAN = "00FFFF";          // class-0 dots
const GREEN = "66FF00";         // class-1 dot
const CHIP_CYAN = "BAFFFF";     // O/P chips for the three 0 rows
const CHIP_GREEN = "C4EBC2";    // O/P chip for the 1 row
const PANEL_PINK = "E0BCC4";    // thin light-pink panel borders
const MAGENTA = "A03E7C";       // activation-box outline + step glyph
const SIGMA_FILL = "E4FFFB";    // summation node fill
const GRAY = "C0C0C0";          // NN connector lines
const PEACH = "F7E7D5";         // equation box fill
const PEACH_BDR = "F2B183";     // equation box border

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// HOUSE CHROME (overrides per-slide geometry: red frame 0.15in inset, yellow badge, title y=0.28)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: DARK_RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top",
  fontSize: 28, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});

// ===================== TRUTH TABLE  (orig x95-313 y138-309) =====================
const TT_X = 1.319, TT_Y = 1.917, TT_W = 3.028, TT_H = 2.375;
const COLW = TT_W / 3, ROWH = TT_H / 5;

s.addShape(pres.shapes.RECTANGLE, {
  x: TT_X, y: TT_Y, w: TT_W, h: TT_H,
  fill: { color: "FFFFFF" }, line: { color: DARK_RED, width: 1.5 },
});
const headers = ["X\u2081", "X\u2082", "O/P"];
headers.forEach((h, i) => {
  s.addText(h, {
    x: TT_X + i * COLW, y: TT_Y, w: COLW, h: ROWH, align: "center", valign: "middle",
    fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });
});
const rows = [
  { vals: ["0", "0", "0"], chip: CHIP_CYAN },
  { vals: ["0", "1", "0"], chip: CHIP_CYAN },
  { vals: ["1", "0", "0"], chip: CHIP_CYAN },
  { vals: ["1", "1", "1"], chip: CHIP_GREEN },
];
rows.forEach((row, r) => {
  const ry = TT_Y + (r + 1) * ROWH;
  for (let c = 0; c < 3; c++) {
    const cx = TT_X + c * COLW;
    s.addShape(pres.shapes.RECTANGLE, {
      x: cx, y: ry, w: COLW, h: ROWH,
      fill: { color: "FFFFFF" }, line: { color: DARK_RED, width: 0.5 },
    });
    if (c === 2) {
      const cw = COLW * 0.29, ch = ROWH * 0.77;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: cx + (COLW - cw) / 2, y: ry + (ROWH - ch) / 2, w: cw, h: ch,
        fill: { color: row.chip },
      });
    }
    s.addText(row.vals[c], {
      x: cx, y: ry, w: COLW, h: ROWH, align: "center", valign: "middle",
      fontSize: 13, color: BLACK, fontFace: FONT, margin: 0,
    });
  }
});

// ===================== DECISION-BOUNDARY PLOT  (orig x536-818 y109-368) =====================
const PL_X = 7.444, PL_Y = 1.514, PL_W = 3.914, PL_H = 3.597;
s.addShape(pres.shapes.RECTANGLE, {
  x: PL_X, y: PL_Y, w: PL_W, h: PL_H,
  fill: { color: "FFFFFF" }, line: { color: PANEL_PINK, width: 1 },
});

// measured axis geometry (orig px): vertical axis x=618, y 125->330 ; horizontal y=330, x 618->796
const AX = 8.581, AY0 = 4.583, AY1 = 1.736, AX1 = 11.055;
s.addShape(pres.shapes.LINE, {
  x: AX, y: AY1, w: 0.001, h: AY0 - AY1,
  line: { color: DARK_RED, width: 2.25, endArrow: "triangle", endArrowSize: "lg" },
});
s.addShape(pres.shapes.LINE, {
  x: AX, y: AY0, w: AX1 - AX, h: 0.001,
  line: { color: DARK_RED, width: 2.25, endArrow: "triangle", endArrowSize: "lg" },
});

// red intercept labels: "2" left of the y-axis at the boundary intercept; "1.2" below the x-axis
s.addText("2", {
  x: AX - 0.44, y: 2.76, w: 0.32, h: 0.25, align: "right", valign: "middle",
  fontSize: 12, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});
s.addText("1.2", {
  x: AX + (10.08 - 8.581) - 0.22, y: 4.80, w: 0.44, h: 0.22,
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});
// red italic x1 at the far right end of the horizontal axis, just under the arrow tip
s.addText("x\u2081", {
  x: AX1 - 0.32, y: 4.74, w: 0.40, h: 0.26, align: "right", valign: "middle",
  fontSize: 14, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});

// decision boundary: navy line from (orig 597,170) to (orig 732,348)
s.addShape(pres.shapes.LINE, {
  x: 8.288, y: 2.361, w: 10.163 - 8.288, h: 4.833 - 2.361,
  line: { color: NAVY, width: 3 },
});

// data points at the measured pixel centres: cyan (0,0) (0,1) (1,0), green (1,1)
const DOT = 0.25;
const dots = [
  { x: 8.581, y: 4.583, c: CYAN },
  { x: 8.581, y: 3.583, c: CYAN },
  { x: 9.707, y: 4.556, c: CYAN },
  { x: 9.720, y: 3.583, c: GREEN },
];
dots.forEach(d => {
  s.addShape(pres.shapes.OVAL, {
    x: d.x - DOT / 2, y: d.y - DOT / 2, w: DOT, h: DOT, fill: { color: d.c },
  });
});

// ===================== NEURAL-NETWORK PANEL  (orig x141-500 y352-491) =====================
const NN_X = 1.958, NN_Y = 4.889, NN_W = 4.986, NN_H = 1.930;
s.addShape(pres.shapes.RECTANGLE, {
  x: NN_X, y: NN_Y, w: NN_W, h: NN_H,
  fill: { color: "FFFFFF" }, line: { color: PANEL_PINK, width: 1 },
});

// three input rows (measured y centres): x1 -5 @372, x2 -3 @425, bias 1 6 @467
const rowY = [5.167, 5.903, 6.489];
const SIG_CX = 4.403, SIG_CY = 5.847, SIG_R = 0.26;

const inputs = [
  { label: "x\u2081", weight: "-5", lc: BLACK, wc: BLUE },
  { label: "x\u2082", weight: "-3", lc: BLACK, wc: BLUE },
  { label: "1", weight: "6", lc: DARK_RED, wc: BLUE },
];
inputs.forEach((inp, i) => {
  const y = rowY[i];
  s.addText(inp.label, {
    x: 2.05, y: y - 0.13, w: 0.50, h: 0.26, align: "right", valign: "middle",
    fontSize: 13, bold: true, color: inp.lc, fontFace: FONT, margin: 0,
  });
  s.addText(inp.weight, {
    x: 2.889, y: y - 0.13, w: 0.42, h: 0.26, align: "left", valign: "middle",
    fontSize: 13, bold: true, color: inp.wc, fontFace: FONT, margin: 0,
  });
  // thin light-grey connector converging into the summation node
  s.addShape(pres.shapes.LINE, {
    x: 3.31, y: y, w: (SIG_CX - SIG_R) - 3.31, h: SIG_CY - y,
    line: { color: GRAY, width: 1 },
  });
});

// summation node: light-cyan filled circle with black Sigma glyph
s.addShape(pres.shapes.OVAL, {
  x: SIG_CX - SIG_R, y: SIG_CY - SIG_R, w: SIG_R * 2, h: SIG_R * 2,
  fill: { color: SIGMA_FILL }, line: { color: "8FD4CE", width: 1 },
});
s.addText("\u03a3", {
  x: SIG_CX - SIG_R, y: SIG_CY - SIG_R, w: SIG_R * 2, h: SIG_R * 2,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// red arrow Sigma -> activation box (orig x337-356)
s.addShape(pres.shapes.LINE, {
  x: SIG_CX + SIG_R + 0.02, y: 5.847, w: 0.24, h: 0.001,
  line: { color: DARK_RED, width: 1.5, endArrow: "triangle", endArrowSize: "med" },
});

// activation box (orig x356-402 y406-433) with a magenta step glyph inside
const AB_X = 4.944, AB_Y = 5.639, AB_W = 0.639, AB_H = 0.375;
s.addShape(pres.shapes.RECTANGLE, {
  x: AB_X, y: AB_Y, w: AB_W, h: AB_H,
  fill: { type: "none" }, line: { color: MAGENTA, width: 1.5 },
});
const stepX = AB_X + 0.12, stepY = AB_Y + 0.07;
s.addShape(pres.shapes.LINE, {
  x: stepX, y: stepY + 0.12, w: 0.17, h: 0,
  line: { color: MAGENTA, width: 1.5 },
});
s.addShape(pres.shapes.LINE, {
  x: stepX + 0.17, y: stepY + 0.12, w: 0, h: -0.12,
  line: { color: MAGENTA, width: 1.5 },
});
s.addShape(pres.shapes.LINE, {
  x: stepX + 0.17, y: stepY, w: 0.17, h: 0,
  line: { color: MAGENTA, width: 1.5 },
});

// threshold rule block, above/right of the activation box (orig x366-420, lines at y377 and y392)
const RULE_X = 5.083, RULE_W = 0.78;
s.addText([
  { text: ">0 ", options: { color: BLACK } },
  { text: "\u21d2 1", options: { color: DARK_RED } },
], {
  x: RULE_X, y: 5.10, w: RULE_W, h: 0.26, align: "left", valign: "middle",
  fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "<0 ", options: { color: BLACK } },
  { text: "\u21d2 0", options: { color: DARK_RED } },
], {
  x: RULE_X, y: 5.31, w: RULE_W, h: 0.26, align: "left", valign: "middle",
  fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
});

// red arrow activation box -> O/P (orig x403-463)
s.addShape(pres.shapes.LINE, {
  x: AB_X + AB_W + 0.02, y: 5.847, w: 6.431 - (AB_X + AB_W + 0.02), h: 0.001,
  line: { color: DARK_RED, width: 1.5, endArrow: "triangle", endArrowSize: "med" },
});
s.addText("O/P", {
  x: 6.55, y: 5.717, w: 0.42, h: 0.26, align: "left", valign: "middle",
  fontSize: 13, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// ===================== EQUATION BOX  (orig x576-776 y415-444) =====================
const EQ_X = 8.000, EQ_Y = 5.764, EQ_W = 2.778, EQ_H = 0.403;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: EQ_X, y: EQ_Y, w: EQ_W, h: EQ_H,
  fill: { color: PEACH }, line: { color: PEACH_BDR, width: 1 },
});
const eqImg = {
  path: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_010_eq.png",
  w_in: 2.45, h_in: 2.45 * (0.25333 / 2.66333),
};
s.addImage({
  path: eqImg.path,
  x: EQ_X + (EQ_W - eqImg.w_in) / 2, y: EQ_Y + (EQ_H - eqImg.h_in) / 2,
  w: eqImg.w_in, h: eqImg.h_in,
});

const out = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_010_recreated.pptx";
pres.writeFile({ fileName: out }).then(() => console.log("wrote " + out));
