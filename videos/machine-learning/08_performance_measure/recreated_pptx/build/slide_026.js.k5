const pptxgen = require("pptxgenjs");

// Slide 026 — Effect of Selecting Threshold Value on Model Performance
// Rebuilt 2026-10-30 from pool_run/image_analysis/slide_026_analysis.txt (fresh read,
// AUTHORITATIVE) + PIL measurements of unique_slides/slide_026.jpg (960x540, 1px = 1pt).
// Frame-derived values: pipeline panel x=328..841px y=102..194px; dotted line x~630px;
// axis y~433px x 85..895px; planes/dots measured below. House chrome per root AGENTS.md.

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";      // house frame + original accents (#CC0000 family)
const YELLOW = "FFF9C4";   // house badge
const HILITE = "B4D36A";   // TP/TN highlight cells (judge+frame: green, not yellow)
const DARK = "333333";
const BLUE = "0000FF";     // dotted line + "3" + blue dots (fresh analysis)
const WHITE = "FFFFFF";
const PANEL = "FFFFF0";    // light-yellow flowchart container (fresh analysis)
const DARKRED = "9F0000";  // measured model box median (159,0,3)
const GREENL = "D0F6DE";   // measured Class I oval (208,246,223)
const PINKL = "E9C8E8";    // Class II oval — lavender/purple (measured 236,201,230)
const GREY = "808080";     // shaded planes
const BLACK = "212121";
const FONT = "Arial";

const px = (v) => v / 72;   // 960x540 frame px == pt == in*72

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
// Fresh analysis (px): legend header x60 y85; table x65 y95 w80 h45;
// threshold callout x185 y100 w100 h30; matrix2 header x155 y125;
// table2 x155 y145 w95 h55.
// ============================================================
const cellW = px(42), cellH = px(27), headH = px(16), labelW = px(24);

function matrix(xPx, yPx, cells, hl) {
  const x = px(xPx), y = px(yPx);
  s.addText("Predicted as", {
    x: x + labelW, y: y, w: cellW * 2, h: headH,
    fontSize: 10, bold: true, color: RED, fontFace: FONT, align: "center", margin: 0,
  });
  s.addText("P", { x: x + labelW, y: y + headH, w: cellW, h: cellH, fontSize: 10, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText("N", { x: x + labelW + cellW, y: y + headH, w: cellW, h: cellH, fontSize: 10, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText("Actual", { x: x, y: y + headH, w: labelW, h: cellH * 2, fontSize: 9, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, rotate: 270 });
  s.addText("P", { x: x, y: y + headH, w: labelW, h: cellH, fontSize: 10, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  s.addText("N", { x: x, y: y + headH + cellH, w: labelW, h: cellH, fontSize: 10, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
  // red-bordered frame
  s.addShape(pptx.shapes.RECTANGLE, { x: x + labelW, y: y + headH, w: cellW * 2, h: cellH * 2, fill: { type: "none" }, line: { color: RED, width: 1.25 } });
  const pos = [[0, 0], [1, 0], [0, 1], [1, 1]];
  cells.forEach((c, i) => {
    const cx = x + labelW + pos[i][0] * cellW;
    const cy = y + headH + pos[i][1] * cellH;
    const isHl = hl && hl[i];
    s.addShape(pptx.shapes.RECTANGLE, {
      x: cx, y: cy, w: cellW, h: cellH,
      fill: { color: isHl ? HILITE : WHITE }, line: { color: RED, width: 0.5 },
    });
    s.addText(c.text, {
      x: cx, y: cy, w: cellW, h: cellH,
      fontSize: 12, bold: true, color: c.color || BLACK, fontFace: FONT,
      align: "center", valign: "middle", margin: 0,
    });
  });
}

// Legend matrix: TP (yellow), FN / FP, TN (yellow) — fresh analysis
// original: header y~90-100, table y~105-178, x 65..145
matrix(65, 90, [
  { text: "TP" }, { text: "FN" }, { text: "FP" }, { text: "TN" },
], [true, false, false, true]);

// Threshold callout: x185 y100 w100 h30, red bold text in red-bordered box
const tbX = px(185), tbY = px(108), tbW = px(100), tbH = px(30);
s.addShape(pptx.shapes.RECTANGLE, { x: tbX, y: tbY, w: tbW, h: tbH, fill: { color: WHITE }, line: { color: RED, width: 1.25 } });
s.addText("Threshold=0.7", { x: tbX, y: tbY, w: tbW, h: tbH, fontSize: 12, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// Numeric matrix: header x155 y125, table x155 y145; values 3(blue) 2(red) / 0(black) 6(red)
// original: header y~125-136, table y~137-209
matrix(155, 124, [
  { text: "3", color: BLUE }, { text: "2", color: RED },
  { text: "0", color: BLACK }, { text: "6", color: RED },
], null);

// ============================================================
// PIPELINE PANEL — measured x=328..841px, y=102..194px, light yellow, red border
// ============================================================
const pnX = px(328), pnY = px(102), pnW = px(841 - 328), pnH = px(194 - 102);
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, { x: pnX, y: pnY, w: pnW, h: pnH, fill: { color: PANEL }, line: { color: RED, width: 1 }, adj: 0.12 });

const fy = px(152);            // flow vertical center ~ y152px
const bh = px(24);             // box height

// Test Sample box (label x420 y110) with small airplane sketch inside
const tsX = px(392), tsW = px(92);
s.addText("Test Sample", { x: tsX, y: px(106), w: tsW, h: px(16), fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: tsX, y: fy - bh / 2, w: tsW, h: bh, fill: { color: WHITE }, line: { color: RED, width: 1 } });
// airplane sketch at right side of the box (dark, clearly visible)
const apx = tsX + tsW - px(14), apy = fy;
const au = px(1);
s.addShape(pptx.shapes.OVAL, { x: apx - 8 * au, y: apy - 1.5 * au, w: 16 * au, h: 3 * au, fill: { color: WHITE }, line: { color: BLACK, width: 1.25 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: apx - 1 * au, y: apy - 8 * au, w: 6 * au, h: 7 * au, fill: { color: WHITE }, line: { color: BLACK, width: 1 }, rotate: 180 });
s.addShape(pptx.shapes.LINE, { x: apx - 8 * au, y: apy - 1 * au, w: 0, h: -4 * au, line: { color: BLACK, width: 1.25 } });

// red arrow Test Sample -> Model
function redArrow(x0, y0) {
  const aw = px(16);
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: y0 - px(1), w: aw, h: px(2), fill: { color: RED }, line: { type: "none" } });
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: x0 + aw - px(4), y: y0 - px(4), w: px(6), h: px(8), fill: { color: RED }, line: { type: "none" }, rotate: 90 });
}
redArrow(tsX + tsW + px(2), fy);

// Model box (measured dark red 9F0000) x~449..568 y121..178
const mdX = px(449), mdW = px(119), mdH = px(57);
s.addShape(pptx.shapes.RECTANGLE, { x: mdX, y: px(121), w: mdW, h: mdH, fill: { color: DARKRED }, line: { type: "none" } });
s.addText("Model", { x: mdX, y: px(127), w: mdW, h: px(24), fontSize: 16, bold: true, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
s.addText("[Any value] \u2192 (0, +\u221E)", { x: mdX, y: px(153), w: mdW, h: px(18), fontSize: 9, color: WHITE, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
// small purple sigmoid curve inside model box right side (measured purple x528-565 y126-167)
for (let i = 0; i <= 12; i++) {
  const t = i / 12, sx0 = mdX + px(79) + t * px(36), sy0 = px(167) - Math.sin(t * Math.PI) * px(38) * (0.55 + 0.45 * Math.sin(t * Math.PI));
  const t2 = Math.min(1, t + 0.08), sx1 = mdX + px(79) + t2 * px(36), sy1 = px(167) - Math.sin(t2 * Math.PI) * px(38) * (0.55 + 0.45 * Math.sin(t2 * Math.PI));
  s.addShape(pptx.shapes.LINE, { x: Math.min(sx0, sx1), y: Math.min(sy0, sy1), w: Math.abs(sx1 - sx0) + 0.01, h: Math.abs(sy1 - sy0), line: { color: "B266FF", width: 1.5 } });
}

// red arrow Model -> Predicted Value
redArrow(mdX + mdW + px(2), fy);

// Predicted Value label (x555 y110) + box (white fill per frame)
const pvX = px(588), pvW = px(88);
s.addText("Predicted Value", { x: pvX, y: px(106), w: pvW, h: px(16), fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", margin: 0 });
s.addShape(pptx.shapes.RECTANGLE, { x: pvX, y: fy - bh / 2, w: pvW, h: bh, fill: { color: WHITE }, line: { color: RED, width: 1 } });
s.addText("(0 ... 1)", { x: pvX, y: fy - bh / 2, w: pvW, h: bh, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// red arrow Predicted Value -> Threshold
redArrow(pvX + pvW + px(2), fy);

// Threshold box (white fill, red border per frame) x~690..732 y112..186
const thX = px(690), thW = px(42);
s.addShape(pptx.shapes.RECTANGLE, { x: thX, y: px(112), w: thW, h: px(74), fill: { color: WHITE }, line: { color: RED, width: 1.25 } });
s.addText("Threshold", { x: thX - px(4), y: px(122), w: thW + px(8), h: px(20), fontSize: 10, bold: true, color: RED, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });
s.addText("(e.g. 0.5)", { x: thX - px(4), y: px(150), w: thW + px(8), h: px(16), fontSize: 9, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0, wrap: false });

// red fork arrows Threshold -> Class I / Class II
s.addShape(pptx.shapes.LINE, { x: thX + thW + px(2), y: fy - px(6), w: px(18), h: -px(16), line: { color: RED, width: 1.5, endArrowType: "triangle" } });
s.addShape(pptx.shapes.LINE, { x: thX + thW + px(2), y: fy + px(6), w: px(18), h: px(16), line: { color: RED, width: 1.5, endArrowType: "triangle" } });

// Class I oval (light green, x~758..832 y~112..140) and Class II oval (pink, y~166..194)
const clsW = px(74), clsH = px(28);
const ciX = px(758), ciY = px(112);
s.addShape(pptx.shapes.OVAL, { x: ciX, y: ciY, w: clsW, h: clsH, fill: { color: GREENL }, line: { color: RED, width: 1 } });
s.addText("Class I", { x: ciX, y: ciY, w: clsW, h: clsH, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });
const ciiX = px(758), ciiY = px(166);
s.addShape(pptx.shapes.OVAL, { x: ciiX, y: ciiY, w: clsW, h: clsH, fill: { color: PINKL }, line: { color: RED, width: 1 } });
s.addText("Class II", { x: ciiX, y: ciiY, w: clsW, h: clsH, fontSize: 11, bold: true, color: BLACK, fontFace: FONT, align: "center", valign: "middle", margin: 0 });

// ============================================================
// BOTTOM — airplane scatter (PIL-measured from frame) + red axis
// Axis: y~433px, x 85..895px; dotted threshold line x~630px (0.7 of axis);
// tick labels 0.0/0.5/1.0 bold red below axis.
// ============================================================
function drawPlane(cxPx, cyPx, grey, dot) {
  // side-view line-drawing airplane, ~30x18px at frame scale (1px=1pt)
  const cx = px(cxPx), cy = px(cyPx), u = px(1);
  const edge = grey ? "616161" : BLACK;
  const fillC = grey ? "BDBDBD" : WHITE;
  // fuselage: long thin body
  s.addShape(pptx.shapes.OVAL, {
    x: cx - 15 * u, y: cy - 1.5 * u, w: 30 * u, h: 3 * u,
    fill: { color: fillC }, line: { color: edge, width: 1 },
  });
  // nose
  s.addShape(pptx.shapes.OVAL, { x: cx + 13 * u, y: cy - 1.5 * u, w: 4 * u, h: 3 * u, fill: { color: fillC }, line: { color: edge, width: 1 } });
  // main wing (swept up triangle)
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 3 * u, y: cy - 12 * u, w: 10 * u, h: 11 * u,
    fill: { color: fillC }, line: { color: edge, width: 1 }, rotate: 180,
  });
  // tail wing
  s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - 14 * u, y: cy - 7 * u, w: 6 * u, h: 6 * u,
    fill: { color: fillC }, line: { color: edge, width: 1 }, rotate: 180,
  });
  // tail fin
  s.addShape(pptx.shapes.LINE, { x: cx - 14 * u, y: cy - 3 * u, w: 0, h: -5 * u, line: { color: edge, width: 1 } });
  if (dot) {
    s.addShape(pptx.shapes.OVAL, {
      x: cx + 15 * u, y: cy - 4 * u, w: 7 * u, h: 7 * u,
      fill: { color: dot }, line: { type: "none" },
    });
  }
}

// PIL-measured plane centers (frame px). 2 grey-shaded, 4 red dots left of
// the dotted line, 2 blue dots right of it (fresh analysis: 11 planes,
// 9 white + 2 grey; frame shows the same scatter).
const planes = [
  { x: 125, y: 255, dot: "FF0000" },
  { x: 345, y: 260, grey: true },
  { x: 860, y: 255, grey: true, dot: "0000FF" },
  { x: 235, y: 310, dot: "FF0000" },
  { x: 340, y: 307 },
  { x: 480, y: 307, dot: "FF0000" },
  { x: 640, y: 310, dot: "0000FF" },
  { x: 815, y: 310 },
  { x: 130, y: 367, dot: "FF0000" },
  { x: 330, y: 345 },
  { x: 485, y: 365 },
  { x: 645, y: 375, dot: "0000FF" },
  { x: 835, y: 382 },
];
for (const p of planes) drawPlane(p.x, p.y, p.grey, p.dot);

// Vertical dotted blue threshold line at 0.7 of the axis, from y210 to axis
const axL = px(85), axR = px(895), axY = px(433);
const thrX = axL + (axR - axL) * 0.7;
for (let yy = 210; yy < 430; yy += 7) {
  s.addShape(pptx.shapes.LINE, { x: thrX, y: px(yy), w: 0, h: px(4), line: { color: BLUE, width: 1, dashType: "dash" } });
}

// Horizontal red axis y~433px with right arrowhead; minor ticks each 0.1
const axL2 = px(60), axR2 = px(915);
s.addShape(pptx.shapes.LINE, { x: axL2, y: axY, w: axR2 - axL2 - px(10), h: 0, line: { color: RED, width: 2 } });
s.addShape(pptx.shapes.ISOSCELES_TRIANGLE, { x: axR2 - px(10), y: axY - px(5), w: px(10), h: px(10), fill: { color: RED }, line: { type: "none" }, rotate: 90 });

// Tick labels 0.0 / 0.5 / 1.0 bold red below axis (fresh analysis y~460)
const ticks = [
  { label: "0.0", x: axL },
  { label: "0.5", x: axL + (axR - axL) * 0.5 },
  { label: "1.0", x: axR },
];
for (const t of ticks) {
  s.addShape(pptx.shapes.LINE, { x: t.x, y: axY, w: 0, h: px(8), line: { color: RED, width: 1.5 } });
  s.addText(t.label, { x: t.x - px(14), y: px(445), w: px(28), h: px(18), fontSize: 12, bold: true, color: RED, fontFace: FONT, align: "center", margin: 0 });
}
// minor ticks at 0.1..0.4, 0.6..0.9 (measured x 164,242,321,399,478,...)
for (const pos of [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]) {
  const x = axL + (axR - axL) * pos;
  s.addShape(pptx.shapes.LINE, { x: x, y: axY, w: 0, h: px(5), line: { color: RED, width: 1 } });
}

// ============================================================
// OUTPUT
// ============================================================
const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_026_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
