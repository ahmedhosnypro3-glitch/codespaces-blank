const pptxgen = require("pptxgenjs");

// Slide 026 — Effect of Selecting Threshold Value on Model Performance
// Rebuilt 2026-10-31 from pool_run/image_analysis/slide_026_analysis.txt (AUTHORITATIVE)
// + PIL measurements of unique_slides/slide_026.jpg (960x540, 1px = 1pt).
// Measured geometry (frame px):
//  legend matrix: Actual x65, labels x81-91, table x91-145 y108-174, header y82-96
//  threshold box: x183-309 y109-135 "Threshold=0.7"
//  numeric matrix: labels x150-174, table x174-250 y164-222, header y140-152
//  panel x328-841 y102-194 fill ~FAFEE4; test sample white box x344-432 y128-168
//  (plane icon inside, block arrow x410-448); model box x449-570 y121-178 fill 9C0000,
//  sigmoid inside x531-565 y132-158; predicted value rounded box x576-676 y140-164
//  fill EBFFFF, grey-blue border, navy text; threshold box x691-730 y110-187;
//  class I oval x758-832 y112-140, class II x758-832 y166-194;
//  axis y433 x60-915, dotted line at 0.7 -> x652. House chrome per root AGENTS.md.

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const HILITE = "B4D36A";
const DARK = "333333";
const BLUE = "0000FF";
const WHITE = "FFFFFF";
const PANEL = "FAFEE4";
const DARKRED = "9C0000";
const GREENL = "D0F6DE";
const PINKL = "E9C8E8";
const PURPLE = "B266FF";
const PVBG = "EBFFFF";      // measured predicted-value box fill
const PVBORDER = "5F7488"; // measured grey-blue border
const PVTEXT = "11116B";   // measured navy text
const NAVY = "212121";
const FONT = "Arial";

const px = (v) => v / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME (root AGENTS.md 2026-10-09 — overrides everything)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("26", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// LEFT BLOCK — legend matrix, threshold box, numeric matrix
// ============================================================
function matrix2(xPx, yPx, o, cells, hl) {
  const x = px(xPx), y = px(yPx);
  const actW = px(o.actW), rowW = px(o.rowW);
  const cellW = px(o.cellW), cellH = px(o.cellH);
  const headH = px(o.headH), colH = px(o.colH);
  const tx = x + actW + rowW;
  const ty = y + headH + colH;
  s.addText("Predicted as", {
    x: tx, y: y, w: cellW * 2, h: headH,
    fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false,
  });
  s.addText("P", { x: tx, y: y + headH, w: cellW, h: colH, fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
  s.addText("N", { x: tx + cellW, y: y + headH, w: cellW, h: colH, fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
  s.addText("Actual", { x: x, y: ty, w: actW, h: cellH * 2, fontSize: 8, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270, wrap: false });
  s.addText("P", { x: x + actW, y: ty, w: rowW, h: cellH, fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
  s.addText("N", { x: x + actW, y: ty + cellH, w: rowW, h: cellH, fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
  s.addShape(pptx.shapes.RECTANGLE, { x: tx, y: ty, w: cellW * 2, h: cellH * 2, fill: { type: "none" }, line: { color: RED, width: 1.25 } });
  s.addShape(pptx.shapes.LINE, { x: tx + cellW, y: ty, w: 0, h: cellH * 2, line: { color: RED, width: 0.75 } });
  s.addShape(pptx.shapes.LINE, { x: tx, y: ty + cellH, w: cellW * 2, h: 0, line: { color: RED, width: 0.75 } });
  const pos = [[0, 0], [1, 0], [0, 1], [1, 1]];
  cells.forEach((c, i) => {
    const cx = tx + pos[i][0] * cellW;
    const cy = ty + pos[i][1] * cellH;
    const isHl = hl && hl[i];
    s.addShape(pptx.shapes.RECTANGLE, {
      x: cx, y: cy, w: cellW, h: cellH,
      fill: { color: isHl ? HILITE : WHITE }, line: { type: "none" },
    });
    s.addText(c.text, {
      x: cx, y: cy, w: cellW, h: cellH,
      fontSize: o.valSize, bold: true, color: c.color || NAVY, fontFace: FONT,
      align: "center", valign: "middle", margin: 0, wrap: false,
    });
  });
}

// Legend matrix (TP/FN/FP/TN; TP & TN green): table x91-145 y108-174
matrix2(65, 82, { actW: 16, rowW: 10, cellW: 27, cellH: 33, headH: 14, colH: 12, valSize: 11 }, [
  { text: "TP" }, { text: "FN" }, { text: "FP" }, { text: "TN" },
], [true, false, false, true]);

// Threshold callout: red-bordered white box x183-309 y109-135
const tbX = px(183), tbY = px(109), tbW = px(126), tbH = px(26);
s.addShape(pptx.shapes.RECTANGLE, { x: tbX, y: tbY, w: tbW, h: tbH, fill: { color: WHITE }, line: { color: RED, width: 1.25 } });
s.addText("Threshold=0.7", { x: tbX, y: tbY, w: tbW, h: tbH, fontSize: 11, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });

// Numeric matrix (3 blue / 2 red / 0 black / 6 red): table x174-250 y164-222
matrix2(150, 140, { actW: 14, rowW: 10, cellW: 38, cellH: 29, headH: 12, colH: 12, valSize: 14 }, [
  { text: "3", color: BLUE }, { text: "2", color: RED },
  { text: "0", color: NAVY }, { text: "6", color: RED },
], null);

// ============================================================
// PIPELINE PANEL — x328-841 y102-194, light yellow, red border
// ============================================================
const pnX = px(328), pnY = px(102), pnW = px(841 - 328), pnH = px(194 - 102);
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: pnX, y: pnY, w: pnW, h: pnH, fill: { color: PANEL }, line: { color: RED, width: 1 }, adj: 0.12 });

const fy = px(152); // flow vertical center

function redArrow(x0, y0, lenPx) {
  const aw = px(lenPx || 16);
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: y0 - px(1.5), w: Math.max(aw - px(8), px(2)), h: px(3), fill: { color: RED }, line: { type: "none" } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x0 + aw - px(9), y: y0 - px(6), w: px(9), h: px(12), fill: { color: RED }, line: { type: "none" }, rotate: 90 });
}

// ---- side-view propeller plane, nose right, optional rotation (deg, clockwise) ----
function drawPlane(cxPx, cyPx, grey, dot, scale, rotDeg) {
  const cx = px(cxPx), cy = px(cyPx), u = px(1) * (scale || 1);
  const th = (rotDeg || 0) * Math.PI / 180;
  const cos = Math.cos(th), sin = Math.sin(th);
  const edge = grey ? "616161" : NAVY;
  const fillC = grey ? "BDBDBD" : WHITE;
  // place a part with local center (lx,ly) and local size (w,h) units, rotated about (cx,cy)
  function part(shape, lx, ly, w, h, opts) {
    const rx = lx * cos - ly * sin, ry = lx * sin + ly * cos;
    s.addShape(shape, Object.assign({
      x: cx + rx * u - (w * u) / 2, y: cy + ry * u - (h * u) / 2,
      w: w * u, h: h * u,
      rotate: (opts && opts.ownRotate ? opts.ownRotate : 0) + (rotDeg || 0),
    }, opts));
  }
  part(pptx.shapes.ISOSCELES_TRIANGLE, -16, -6, 8, 10, { ownRotate: 180, fill: { color: fillC }, line: { color: edge, width: 1 } }); // tail fin
  part(pptx.shapes.ISOSCELES_TRIANGLE, -16, 4, 6, 4, { fill: { color: fillC }, line: { color: edge, width: 1 } }); // stabilizer
  part(pptx.shapes.OVAL, 0, 0, 40, 5, { fill: { color: fillC }, line: { color: edge, width: 1.25 } }); // fuselage
  part(pptx.shapes.OVAL, 8.5, -3.75, 7, 4.5, { fill: { color: fillC }, line: { color: edge, width: 1 } }); // cockpit
  part(pptx.shapes.ISOSCELES_TRIANGLE, 0.5, -8.5, 15, 13, { ownRotate: 180, fill: { color: fillC }, line: { color: edge, width: 1 } }); // main wing
  part(pptx.shapes.ISOSCELES_TRIANGLE, 0, 5.5, 10, 6, { fill: { color: fillC }, line: { color: edge, width: 1 } }); // lower wing
  part(pptx.shapes.LINE, 21, 0, 0.2, 16, { line: { color: edge, width: 1.5 } }); // propeller blade
  part(pptx.shapes.OVAL, 21, 0, 3, 3, { fill: { color: edge }, line: { type: "none" } }); // hub
  if (dot) part(pptx.shapes.OVAL, 27, -4.5, 7, 7, { fill: { color: dot }, line: { type: "none" } });
}

// Test Sample: white box x344-432 y128-168 with plane icon inside; block arrow to Model
const tsX = px(344), tsY = px(128), tsW = px(88), tsH = px(40);
s.addText("Test Sample", { x: tsX, y: px(108), w: tsW, h: px(16), fontSize: 11, bold: true, color: NAVY, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
s.addShape(pptx.shapes.RECTANGLE, { x: tsX, y: tsY, w: tsW, h: tsH, fill: { color: WHITE }, line: { color: RED, width: 1 } });
drawPlane(376, 150, false, null, 0.55, 0);
s.addShape(pptx.shapes.RIGHT_ARROW, { x: px(410), y: px(143), w: px(38), h: px(18), fill: { color: RED }, line: { type: "none" }, adj: 0.55 });

// Model box (dark red) x449-570 y121-178
const mdX = px(449), mdY = px(121), mdW = px(121), mdH = px(57);
s.addShape(pptx.shapes.RECTANGLE, { x: mdX, y: mdY, w: mdW, h: mdH, fill: { color: DARKRED }, line: { type: "none" } });
s.addText("Model", { x: mdX + px(3), y: mdY + px(5), w: px(76), h: px(22), fontSize: 15, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
s.addText("[Any value] \u2192 (0,+\u221E)", { x: mdX + px(3), y: mdY + px(30), w: px(76), h: px(20), fontSize: 7, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
// purple sigmoid INSIDE right part of model box: x529-563, y132-158
for (let i = 0; i <= 16; i++) {
  const t = i / 16, t2 = (i + 1) / 16;
  const x0 = 529 + t * 34, x1 = 529 + t2 * 34;
  const y0 = 158 - Math.sin(t * Math.PI) * 26, y1 = 158 - Math.sin(t2 * Math.PI) * 26;
  s.addShape(pptx.shapes.LINE, {
    x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
    w: Math.abs(px(x1) - px(x0)) + 0.005, h: Math.abs(px(y1) - px(y0)) + 0.005,
    flipV: y1 < y0,
    line: { color: PURPLE, width: 1.5 },
  });
}

redArrow(px(572), fy, 8);

// Predicted Value: rounded light-cyan box with grey-blue border, navy text; x576-676 y140-164
const pvX = px(576), pvW = px(100);
s.addText("Predicted Value", { x: pvX, y: px(108), w: pvW, h: px(16), fontSize: 11, bold: true, color: NAVY, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: pvX, y: px(140), w: pvW, h: px(24), fill: { color: PVBG }, line: { color: PVBORDER, width: 1.25 }, adj: 0.3 });
s.addText("(0 ... 1)", { x: pvX, y: px(140), w: pvW, h: px(24), fontSize: 11, bold: true, color: PVTEXT, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });

redArrow(px(678), fy, 12);

// Threshold box (vertical, white fill red border) x691-730 y110-187, stacked labels inside
const thX = px(691), thY = px(110), thW = px(39), thH = px(77);
s.addShape(pptx.shapes.RECTANGLE, { x: thX, y: thY, w: thW, h: thH, fill: { color: WHITE }, line: { color: RED, width: 1.25 } });
s.addText("Threshold", { x: thX, y: thY + px(10), w: thW, h: px(18), fontSize: 7.5, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: true });
s.addText("(e.g. 0.5)", { x: thX, y: thY + px(36), w: thW, h: px(16), fontSize: 7.5, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: true });

// red fork arrows Threshold -> Class I / Class II
s.addShape(pptx.shapes.LINE, { x: thX + thW + px(2), y: fy - px(22), w: px(22), h: px(16), flipV: true, line: { color: RED, width: 1.5, endArrowType: "triangle" } });
s.addShape(pptx.shapes.LINE, { x: thX + thW + px(2), y: fy + px(6), w: px(22), h: px(16), line: { color: RED, width: 1.5, endArrowType: "triangle" } });

// Class I (green) / Class II (lavender) ovals x758-832
const clsW = px(74), clsH = px(28);
const ciX = px(758), ciY = px(112);
s.addShape(pptx.shapes.OVAL, { x: ciX, y: ciY, w: clsW, h: clsH, fill: { color: GREENL }, line: { color: RED, width: 1 } });
s.addText("Class I", { x: ciX, y: ciY, w: clsW, h: clsH, fontSize: 11, bold: true, color: NAVY, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
const ciiY = px(166);
s.addShape(pptx.shapes.OVAL, { x: ciX, y: ciiY, w: clsW, h: clsH, fill: { color: PINKL }, line: { color: RED, width: 1 } });
s.addText("Class II", { x: ciX, y: ciiY, w: clsW, h: clsH, fontSize: 11, bold: true, color: NAVY, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });

// ============================================================
// BOTTOM — airplane scatter + red axis
// ============================================================
// PIL-measured plane centers (frame px), varied rotations like the hand-drawn
// original. 2 grey-shaded; red dots on left-of-line planes, blue dots on
// right-of-line planes. No X marks exist in the original.
const planes = [
  { x: 125, y: 255, dot: "FF0000", s: 0.95, r: -12 },
  { x: 345, y: 260, grey: true, s: 1.0, r: 8 },
  { x: 860, y: 255, grey: true, dot: "0000FF", s: 1.25, r: -6 },
  { x: 235, y: 310, dot: "FF0000", s: 1.0, r: 14 },
  { x: 340, y: 307, s: 0.9, r: -18 },
  { x: 480, y: 307, dot: "FF0000", s: 1.05, r: 5 },
  { x: 640, y: 310, dot: "0000FF", s: 1.1, r: -8 },
  { x: 815, y: 310, s: 1.0, r: 12 },
  { x: 130, y: 367, dot: "FF0000", s: 0.8, r: -5 },
  { x: 330, y: 345, s: 0.9, r: 18 },
  { x: 485, y: 365, s: 1.0, r: -14 },
  { x: 645, y: 375, dot: "0000FF", s: 1.05, r: 7 },
  { x: 835, y: 382, s: 1.25, r: -10 },
];
for (const p of planes) drawPlane(p.x, p.y, p.grey, p.dot, p.s, p.r);

// Vertical dotted blue threshold line at 0.7 of the axis, y210..430
const axL = px(85), axR = px(895), axY = px(433);
const thrX = axL + (axR - axL) * 0.7;
for (let yy = 210; yy < 430; yy += 7) {
  s.addShape(pptx.shapes.LINE, { x: thrX, y: px(yy), w: 0, h: px(4), line: { color: BLUE, width: 1, dashType: "dash" } });
}

// Horizontal red axis y433 x60-915 with right arrowhead
const axL2 = px(60), axR2 = px(915);
s.addShape(pptx.shapes.LINE, { x: axL2, y: axY, w: axR2 - axL2 - px(10), h: 0, line: { color: RED, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: axR2 - px(10), y: axY - px(5), w: px(10), h: px(10), fill: { color: RED }, line: { type: "none" }, rotate: 90 });

// Tick labels 0.0 / 0.5 / 1.0 bold red below axis
const ticks = [
  { label: "0.0", x: axL },
  { label: "0.5", x: axL + (axR - axL) * 0.5 },
  { label: "1.0", x: axR },
];
for (const t of ticks) {
  s.addShape(pptx.shapes.LINE, { x: t.x, y: axY, w: 0, h: px(8), line: { color: RED, width: 1.5 } });
  s.addText(t.label, { x: t.x - px(14), y: px(445), w: px(28), h: px(18), fontSize: 12, bold: true, color: RED, fontFace: FONT, align: "center", margin: 0, wrap: false });
}
// minor ticks at 0.1 steps
for (const pos of [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]) {
  const x = axL + (axR - axL) * pos;
  s.addShape(pptx.shapes.LINE, { x: x, y: axY, w: 0, h: px(5), line: { color: RED, width: 1 } });
}

// ============================================================
// OUTPUT
// ============================================================
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_026_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
