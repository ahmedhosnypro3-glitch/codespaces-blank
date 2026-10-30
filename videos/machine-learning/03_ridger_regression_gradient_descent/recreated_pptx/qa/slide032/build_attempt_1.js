// Build: slide 032 — "Convex Function, Learning Rate =0.4, Start at X=3"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// GEOMETRY SOURCE: PIL measurement of unique_slides/slide_032.jpg (960x540, 1px=1pt).
// Spec: analysis/slide_032_final.json + sibling pattern from slide_030.js / slide_031.js.
// Where spec and frame disagree, THE FRAME WINS. All frame px below are measured ink boxes.
//
// MEASURED LAYOUT (frame px, 960x540):
//   House chrome (deck standard shared_patterns/house_chrome.js):
//     canvas FFFFFF; gray panel E9E9E7 x54..903 y45..540 (no border);
//     C00000 1pt strokes LEFT x58.5 (rows46..539), RIGHT x901, BOTTOM y538.5; NO TOP STROKE;
//     badge circle d~35 centred (876,73), fill FDFD96, ring 6A5ACD 2pt, bold "32" Arial 18pt #333333.
//
//   Title (ONE line, top-left): "Convex Function,  Learning Rate =0.4,  Start at X=3"
//     runs: "Convex Function,  " C00000 | "Learning Rate =0.4,  " 008000 | "Start at X=3" 0000FF
//     measured ink x 80..815, y 63..88 (Arial bold 26pt).
//
//   Parameter table (3x2): x 76..208, y 178..251
//     label col x76..142 (green C0E0C0 / pink F0C0C0 / yellow FFFFC0), value col x142..208 white
//     rows y178..202 / 204..227 / 230..251 ; step 0.4 | initial X 3 | delta 0.1
//
//   Graph (top-right): white plot rect x 574..809, y 67..265
//     red 1pt border on LEFT x573, RIGHT x810, TOP y66; gray 1pt BOTTOM y266
//     calibration: x_data=0 -> px 630, 11.5 px/unit ; y_data=0 -> px 266, 12 px/unit
//     gray gridlines (D9D9D9 0.5pt) every 1 unit; axis lines 1pt; tick marks + labels
//     red dashed vertical at x=5 (px 687.5); blue parabola f(x)=(x-5)^2+1 (2pt)
//     green dot (5,1) at px (687.5,254) d8, green label "(5,1)"
//     red dot (2,10) at px (653,146) d8, red label "(2,10)"
//     black horizontal segment y=10 from x=2 to x=7 (px y146, x653..710)
//
//   Equation callout column (centre):
//     box1 x 398..530, y 184..212 : RED border 1.5pt, WHITE fill, mathtext equation PNG
//     "X = 5" bold red C00000, plain text y 215..230
//     box2 x 380..538, y 234..280 : GREEN fill, "f(x) Minimum value is 1.0"
//     box3 x 380..547, y 292..312 : PINK fill, "Reach Minimum after 6 Steps" purple 800080
//
//   Magenta arrow (down, from callout to table): x ~490..600, y ~306..334, real arrowhead.
//
//   Iteration table (8 rows x 7 cols): x 298..600, y 331..527
//     label col x298..355 ; 6 data cols ~40.8 wide: 355, 395.8, 436.7, 477.5, 518.3, 559.2, 600
//     8 equal rows of 24.5: 331, 355.5, 380, 404.5, 429, 453.5, 478, 502.5, 527
//     row fills (whole row, measured): Y FFFF99, Y FFFF99, P D9B8E8, P D9B8E8,
//                                      Y FFFF99, Y FFFF99, G C0E0C0, R F0C0C0
//     outer+inner borders 564BA7 (measured dark blue-violet)
//
// Laws honored: hex without '#'; fontFace explicit everywhere; margin 0; measured geometry
// over intuition; explicit lineSpacing on multi-line text; single plain-named deliverable.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = __dirname + "/../slide_032_recreated.pptx";
const px = (v) => v / 72; // frame px -> inches

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();
const ST = pptx.ShapeType;
const A = "Arial";

drawHouseChrome(pptx, slide, { numeral: 32 });

// ------------------------------------------------------------------ TITLE
slide.addText(
  [
    { text: "Convex Function,  ", options: { fontSize: 26, bold: true, color: "C00000", fontFace: A } },
    { text: "Learning Rate =0.4,  ", options: { fontSize: 26, bold: true, color: "008000", fontFace: A } },
    { text: "Start at X=3", options: { fontSize: 26, bold: true, color: "0000FF", fontFace: A } },
  ],
  { x: px(80), y: px(62), w: px(740), h: px(28), margin: 0, align: "left", valign: "top" }
);

// ------------------------------------------------------- PARAMETER TABLE
const paramRows = [
  { label: "step", value: "0.4", fill: "C0E0C0" },
  { label: "initial X", value: "3", fill: "F0C0C0" },
  { label: "delta", value: "0.1", fill: "FFFFC0" },
];
const pTBL = 76, pTBV = 142, pTBR = 208;
const pRowY = [178, 178 + 24.33, 178 + 48.67];
const pRowH = [24.33, 24.34, 22.99];
paramRows.forEach((row, i) => {
  const y = px(pRowY[i]), h = px(pRowH[i]);
  slide.addShape(ST.rect, { x: px(pTBL), y, w: px(pTBV - pTBL), h, fill: { color: row.fill }, line: { color: "000000", width: 0.5 } });
  slide.addText(row.label, { x: px(pTBL), y, w: px(pTBV - pTBL), h, align: "center", valign: "middle", fontSize: 12, color: "000000", fontFace: A, margin: 0 });
  slide.addShape(ST.rect, { x: px(pTBV), y, w: px(pTBR - pTBV), h, fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.5 } });
  slide.addText(row.value, { x: px(pTBV), y, w: px(pTBR - pTBV), h, align: "center", valign: "middle", fontSize: 12, color: "000000", fontFace: A, margin: 0 });
});

// ----------------------------------------------------------------- GRAPH
const GP = { x0: 574, x1: 809, y0: 67, y1: 265 };
const XC = 630, SX = 11.5;   // data x -> px
const YC = 266, SY = 12;     // data y -> px (inverted)
const mx = (v) => XC + SX * v;
const my = (v) => YC - SY * v;

// white plot background
slide.addShape(ST.rect, { x: px(GP.x0), y: px(GP.y0), w: px(GP.x1 - GP.x0), h: px(GP.y1 - GP.y0), fill: { color: "FFFFFF" }, line: { type: "none" } });

// gridlines (1 unit)
for (let k = -5; k <= 15; k++) {
  const x = mx(k);
  if (x < GP.x0 || x > GP.x1) continue;
  const major = (k === 0);
  slide.addShape(ST.line, { x: px(x), y: px(GP.y0), w: 0, h: px(GP.y1 - GP.y0),
    line: { color: major ? "000000" : "D9D9D9", width: major ? 1 : 0.5 } });
}
for (let k = 0; k <= 16; k++) {
  const y = my(k);
  if (y < GP.y0 || y > GP.y1) continue;
  const major = (k === 0);
  slide.addShape(ST.line, { x: px(GP.x0), y: px(y), w: px(GP.x1 - GP.x0), h: 0,
    line: { color: major ? "000000" : "D9D9D9", width: major ? 1 : 0.5 } });
}

// plot frame: red left/right/top, gray bottom (measured)
slide.addShape(ST.line, { x: px(573), y: px(66), w: 0, h: px(200), line: { color: "C00000", width: 1 } });
slide.addShape(ST.line, { x: px(810), y: px(66), w: 0, h: px(200), line: { color: "C00000", width: 1 } });
slide.addShape(ST.line, { x: px(GP.x0), y: px(66), w: px(GP.x1 - GP.x0), h: 0, line: { color: "C00000", width: 1 } });
slide.addShape(ST.line, { x: px(GP.x0), y: px(266), w: px(GP.x1 - GP.x0), h: 0, line: { color: "808080", width: 1 } });

// tick marks + labels
const xticks = [-5, 0, 5, 10, 15];
const yticks = [0, 5, 10, 15];
xticks.forEach((v) => {
  const x = mx(v);
  slide.addShape(ST.line, { x: px(x), y: px(267), w: 0, h: px(6), line: { color: "000000", width: 1 } });
  slide.addText(String(v), { x: px(x - 12), y: px(276), w: px(24), h: px(14), align: "center", valign: "top", fontSize: 9, color: "000000", fontFace: A, margin: 0 });
});
yticks.forEach((v) => {
  const y = my(v);
  slide.addShape(ST.line, { x: px(567), y: px(y), w: px(6), h: 0, line: { color: "000000", width: 1 } });
  slide.addText(String(v), { x: px(536), y: px(y - 7), w: px(28), h: px(14), align: "right", valign: "middle", fontSize: 9, color: "000000", fontFace: A, margin: 0 });
});
slide.addText("x", { x: px(806), y: px(276), w: px(16), h: px(14), align: "left", valign: "top", fontSize: 10, bold: true, color: "000000", fontFace: A, margin: 0 });
slide.addText("f(x)", { x: px(536), y: px(64), w: px(36), h: px(16), align: "right", valign: "middle", fontSize: 10, bold: true, color: "000000", fontFace: A, margin: 0 });

// red dashed vertical at x=5
for (let y = GP.y0 + 3; y < GP.y1 - 3; y += 8) {
  slide.addShape(ST.line, { x: px(687.5), y: px(y), w: 0, h: px(4), line: { color: "FF0000", width: 1 } });
}

// blue parabola f(x)=(x-5)^2+1 — ONE smooth analytic curve, dense sampling
{
  const N = 600;
  let prev = null;
  for (let i = 0; i <= N; i++) {
    const xv = -5 + 20 * i / N;
    const yv = Math.pow(xv - 5, 2) + 1;
    const X = mx(xv), Y = my(yv);
    const Yc = Math.max(Y, GP.y0);
    if (prev !== null && Y >= GP.y0 - 40 && Y <= GP.y1 + 4) {
      slide.addShape(ST.line, {
        x: Math.min(prev.x, X), y: Math.min(prev.yc, Yc),
        w: Math.abs(X - prev.x), h: Math.abs(Yc - prev.yc),
        line: { color: "0000FF", width: 2 },
        flipV: (Y - prev.y) * (X - prev.x) < 0,
      });
    }
    prev = { x: X, yc: Yc, y: Y };
  }
}

// markers
slide.addShape(ST.ellipse, { x: px(683.5), y: px(250), w: px(8), h: px(8), fill: { color: "008000" }, line: { color: "008000", width: 1 } });
slide.addText("(5,1)", { x: px(652), y: px(226), w: px(40), h: px(14), align: "center", valign: "bottom", fontSize: 11, bold: true, color: "008000", fontFace: A, margin: 0 });

slide.addShape(ST.ellipse, { x: px(649), y: px(142), w: px(8), h: px(8), fill: { color: "FF0000" }, line: { color: "FF0000", width: 1 } });
slide.addText("(2,10)", { x: px(618), y: px(124), w: px(50), h: px(14), align: "center", valign: "bottom", fontSize: 11, bold: true, color: "FF0000", fontFace: A, margin: 0 });

// black horizontal segment at y=10 from x=2 to x=7
slide.addShape(ST.line, { x: px(653), y: px(146), w: px(710 - 653), h: 0, line: { color: "000000", width: 2 } });

// --------------------------------------------------- EQUATION CALLOUTS
// box 1: equation, red border, white fill
slide.addShape(ST.rect, { x: px(398), y: px(184), w: px(132), h: px(28), fill: { color: "FFFFFF" }, line: { color: "FF0000", width: 1.5 } });
const eq = require("./assets/eq_032_main.json");
const eqX = px(398 + (132 - eq.w_in * 72) / 2);
const eqY = px(184 + (28 - eq.h_in * 72) / 2);
slide.addImage({ path: ASSET_DIR + "/eq_032_main.png", x: eqX, y: eqY, w: eq.w_in, h: eq.h_in });

// "X = 5" bold red
slide.addText("X = 5", { x: px(398), y: px(217), w: px(120), h: px(24), align: "left", valign: "middle", fontSize: 20, bold: true, color: "C00000", fontFace: A, margin: 0, lineSpacing: 22 });

// box 2: green fill, "f(x) Minimum value is 1.0"
slide.addShape(ST.rect, { x: px(380), y: px(234), w: px(158), h: px(46), fill: { color: "C0E0C0" }, line: { type: "none" } });
slide.addText([
  { text: "f(x) ", options: { fontSize: 13, color: "000000", fontFace: A } },
  { text: "Minimum value is ", options: { fontSize: 13, color: "800080", fontFace: A } },
  { text: "1.0", options: { fontSize: 13, bold: true, color: "0000FF", fontFace: A } },
], { x: px(384), y: px(258), w: px(150), h: px(20), align: "left", valign: "middle", margin: 0, lineSpacing: 15 });

// box 3: pink fill, "Reach Minimum after 6 Steps"
slide.addShape(ST.rect, { x: px(380), y: px(292), w: px(167), h: px(20), fill: { color: "F0C0C0" }, line: { type: "none" } });
slide.addText("Reach Minimum after 6 Steps", { x: px(384), y: px(294), w: px(160), h: px(16), align: "left", valign: "middle", fontSize: 13, bold: true, color: "800080", fontFace: A, margin: 0, lineSpacing: 15 });

// ------------------------------------------------------------ ARROW
slide.addShape(ST.downArrow, { x: px(540), y: px(300), w: px(28), h: px(34), fill: { color: "C000C0" }, line: { color: "C000C0", width: 0.5 } });

// --------------------------------------------------- ITERATION TABLE
const rowLabels = ["x", "f(x)", "x-delta", "f(x-delta)", "x+delta", "f(x+delta)", "slope", "next x"];
const rowData = [
  ["3", "3.4", "3.8", "4.2", "4.6", "5"],
  ["5", "3.56", "2.44", "1.64", "1.16", "1"],
  ["2.9", "3.3", "3.7", "4.1", "4.5", "4.9"],
  ["5.41", "3.89", "2.69", "1.81", "1.25", "1.01"],
  ["3.1", "3.5", "3.9", "4.3", "4.7", "5.1"],
  ["4.61", "3.25", "2.21", "1.49", "1.09", "1.01"],
  ["-8", "-6.4", "-4.8", "-3.2", "-1.6", "0"],
  ["3.4", "3.8", "4.2", "4.6", "5", "stop"],
];
const rowFills = ["FFFF99", "FFFF99", "D9B8E8", "D9B8E8", "FFFF99", "FFFF99", "C0E0C0", "F0C0C0"];
const colX = [298, 355, 395.8, 436.7, 477.5, 518.3, 559.2, 600];
const rowY = [331, 355.5, 380, 404.5, 429, 453.5, 478, 502.5, 527];
const BORDER = "564BA7";

for (let r = 0; r < 8; r++) {
  const fill = rowFills[r];
  for (let c = 0; c < 7; c++) {
    const x0 = colX[c], x1 = colX[c + 1], y0 = rowY[r], y1 = rowY[r + 1];
    slide.addShape(ST.rect, { x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0), fill: { color: fill }, line: { color: BORDER, width: 0.5 } });
    const isLabel = c === 0;
    const txt = isLabel ? rowLabels[r] : rowData[r][c - 1];
    const isStop = !isLabel && r === 7 && c === 6;
    slide.addText(txt, {
      x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
      align: isLabel ? "left" : "center", valign: "middle",
      fontSize: 9, bold: isLabel || isStop, color: isStop ? "C00000" : "000000",
      fontFace: A, margin: 0, lineSpacing: 11,
    });
  }
}

pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
