// Slide 049 — machine-learning lecture 03 (03_ridger_regression_gradient_descent)
// "Iteration 2" — built from measured frame unique_slides/slide_049.jpg (960x540, 1px=1pt)
// plus the content spec analysis/slide_049_final.json.
//
// MEASURED GEOMETRY (frame px), banked from PIL measurement 2026-10-23
// (scratch/meas049.py, scratch/rlscan_049.py, scratch/zoom.py, scratch/lines.py):
//   chrome        : panel x54..903 y45..540; C00000 strokes L58.5 / R901 / B538.5 (NO top);
//                   badge centre (876,73) d35
//   top box       : x68..720 y54..130, BLUE-VIOLET 2px border, WHITE interior
//   data table    : 6 num cols x89..103,111..125,133..148,155..171,178..193,201..215
//                   (pitch 21.2); header row y64..73; data rows y77..125
//   "Initial" hdr : x239..253 y58..73 (RED)
//   "Initial W=.." : x257..423 (dark)
//   "REPEAT ..."  : RED, x420..535 y61..74
//   "Check classes of" : x550..624 y86..98
//   3x3 grid      : cols x640..656, 663..678, 686..701; rows y71..84, 86..104, 106..118
//   title         : "Ugmented Vectors (from Top)" BLUE-VIOLET x82..215 y146..159
//   aug table     : cols x89..211 y162..230 (6 cols pitch ~21, 5 rows)
//   class labels  : C1 x88..134 RED / C2 x152..202 BLUE, y230..244
//   RED box       : x84..214 y277..305, red fill + one white text line
//   "No change in W": x77..156 y350..370 (black, plain)
//   red "=>"-glyph: x84..122 y375..394 ; "Stop Iterations": x76..205 y375..394
//   calc table    : x273..852, rules y140/205/271/337/403/469/527, WHITE interior
//                   per row: d(xN) x283..336 | matrix x350..437 | "=> Keep same Weight"
//                   x508..622 | W-vector x708..757

const pptxgenpkg = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";  // 13.333 x 7.5 in
const s = pptx.addSlide();

drawHouseChrome(pptx, s, { numeral: "49" });

const FONT = "Arial";
const BLACK = "000000";
const RED = "FF0000";
const BLUE = "0000FF";
const VIOLET = "6A5ACD";   // measured blue-violet (box border, left heading, ring family)
const RULE = "C1C1C9";     // measured calc-table rule
const WHITE = "FFFFFF";

// frame px -> inches (absolute frame coords: 960x540 == 13.333x7.5in)
function fx(px) { return px / 72; }
function fy(px) { return px / 72; }
function fw(px) { return px / 72; }
function fh(px) { return px / 72; }

function cell(text, o) {
  return { text: text, options: Object.assign({
    fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle", margin: 0,
  }, o || {}) };
}
// parenthesised numeric cell (spec: "Column/vector numerals are parenthesized in tables")
function pc(v, o) { return cell("(" + v + ")", o); }

// ---------------- 1. TOP BLUE-VIOLET BOX (white interior) ----------------
s.addShape(pptx.ShapeType.rect, {
  x: fx(68), y: fy(54), w: fw(720 - 68), h: fh(130 - 54),
  fill: { color: WHITE }, line: { color: VIOLET, width: 1.5 },
});

// ---------------- 2. TOP DATA TABLE (x1..x6) ----------------
const TBL_X = 89, TBL_W = 21.2;
const tblRows = [
  [cell("x1"), cell("x2"), cell("x3"), cell("x4"), cell("x5"), cell("x6")],
  [pc("1"), pc("2"), pc("1"), pc("5"), pc("6"), pc("6")],
  [pc("1"), pc("1"), pc("2"), pc("4"), pc("5"), pc("6")],
  [pc("1"), pc("1"), pc("2"), pc("4"), pc("5"), pc("6")],
];
s.addTable(tblRows, {
  x: fx(TBL_X), y: fy(64), w: fw(TBL_W * 6),
  colW: [fw(TBL_W), fw(TBL_W), fw(TBL_W), fw(TBL_W), fw(TBL_W), fw(TBL_W)],
  rowH: [fh(14), fh(15), fh(15), fh(14)],
  fontFace: FONT, margin: 0, border: { type: "none" },
});

// "Initial" header of the 7th column (RED)
s.addText("Initial", {
  x: fx(233), y: fy(64), w: fw(24), h: fh(14),
  fontFace: FONT, fontSize: 11, color: RED, align: "left", valign: "middle", margin: 0,
});
// "Initial W = [4, -2]" — first data row, x257..423
s.addText([
  { text: "Initial ", options: { color: BLACK } },
  { text: "W", options: { color: BLACK, italic: true } },
  { text: " = [4, -2]", options: { color: BLACK } },
], {
  x: fx(257), y: fy(64), w: fw(170), h: fh(15),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// ---------------- 3. REPEAT instruction (RED, x420..535 y61..74) ----------------
s.addText("REPEAT using Step \u03b7 = 1", {
  x: fx(420), y: fy(58), w: fw(120), h: fh(18),
  fontFace: FONT, fontSize: 11, color: RED, bold: true,
  align: "left", valign: "middle", margin: 0,
});

// ---------------- 4. "Check classes of" + 3x3 grid ----------------
// measured: single line x542..624 y86..96 (needs w>=90 or 11pt wraps to 2 lines)
s.addText("Check classes of", {
  x: fx(548), y: fy(85), w: fw(92), h: fh(14),
  fontFace: FONT, fontSize: 10, color: BLACK, align: "left", valign: "middle", margin: 0,
});
s.addTable([
  [cell("Z1"), cell("Z1"), cell("Z1")],
  [pc("0"), pc("7"), pc("3")],
  [pc("0"), pc("6"), pc("2")],
], {
  x: fx(636), y: fy(69), w: fw(70),
  colW: [fw(23.3), fw(23.3), fw(23.4)],
  rowH: [fh(15), fh(19), fh(14)],
  fontFace: FONT, margin: 0, border: { type: "none" },
});

// ---------------- 5. colour legend ----------------
// measured: single line x245..544 y110..124 (~15px glyphs) — 15pt
s.addText([
  { text: "C1 positive", options: { color: RED } },
  { text: "  ", options: { color: BLACK } },
  { text: "C2 negative", options: { color: BLUE } },
  { text: "  ", options: { color: BLACK } },
  { text: "Zero is unaccepted", options: { color: BLACK } },
], {
  x: fx(245), y: fy(109), w: fw(305), h: fh(18),
  fontFace: FONT, fontSize: 15, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// ---------------- 6. Ugmented Vectors title + table ----------------
// measured: title x82..219 y148..159 (~12px glyphs) — 12pt
s.addText("Ugmented Vectors (from Top)", {
  x: fx(82), y: fy(146), w: fw(158), h: fh(15),
  fontFace: FONT, fontSize: 12, color: VIOLET, align: "left", valign: "middle", margin: 0,
});
const AW = 21;
s.addTable([
  [cell("x1"), cell("x2"), cell("x3"), cell("x4"), cell("x5"), cell("x6")],
  [pc("1"), pc("1"), pc("1"), pc("1"), pc("1"), pc("1")],
  [pc("1"), pc("2"), pc("1"), pc("5"), pc("6"), pc("6")],
  [pc("1"), pc("1"), pc("2"), pc("4"), pc("5"), pc("6")],
  [pc("1"), pc("1"), pc("2"), pc("4"), pc("5"), pc("6")],
], {
  x: fx(89), y: fy(162), w: fw(AW * 6),
  colW: [fw(AW), fw(AW), fw(AW), fw(AW), fw(AW), fw(AW)],
  rowH: [fh(14), fh(14), fh(14), fh(14), fh(13)],
  fontFace: FONT, margin: 0, border: { type: "none" },
});
[["C1", 88, RED], ["C1", 109, RED], ["C1", 130, RED],
 ["C2", 151, BLUE], ["C2", 172, BLUE], ["C2", 193, BLUE]].forEach(function (c) {
  s.addText(c[0], {
    x: fx(c[1]), y: fy(230), w: fw(21), h: fh(15),
    fontFace: FONT, fontSize: 11, color: c[2], bold: true, align: "center", valign: "middle", margin: 0,
  });
});

// ---------------- 7. RED BOX "Iteration 2" ----------------
// measured box x84..213 y278..304; white text x99..199 y283..298 (~16px glyphs) -> 21pt bold
s.addShape(pptx.ShapeType.rect, {
  x: fx(84), y: fy(278), w: fw(129), h: fh(26),
  fill: { color: RED }, line: { color: RED, width: 1 },
});
s.addText("Iteration 2", {
  x: fx(84), y: fy(278), w: fw(129), h: fh(26),
  fontFace: FONT, fontSize: 21, color: WHITE, bold: true, align: "center", valign: "middle", margin: 0,
});

// ---------------- 8. "No change in W" (W underlined) / "Stop Iterations" ----------------
// measured line1 x78..216 y351..370: "No change in " x78..188 + underlined W x200..216 (rule y366..367)
// measured line2: RED "Stop" x85..123 y375..394  +  dark "Iterations" x127..208 y375..394
// glyph height ~16px in both lines -> 20pt
s.addText("No change in ", {
  x: fx(78), y: fy(349), w: fw(120), h: fh(22),
  fontFace: FONT, fontSize: 20, color: BLACK, align: "left", valign: "middle", margin: 0,
});
s.addText("W", {
  x: fx(198), y: fy(349), w: fw(20), h: fh(22),
  fontFace: FONT, fontSize: 20, color: BLACK, underline: true,
  align: "left", valign: "middle", margin: 0,
});
s.addText("Stop", {
  x: fx(85), y: fy(374), w: fw(42), h: fh(22),
  fontFace: FONT, fontSize: 20, color: RED, align: "left", valign: "middle", margin: 0,
});
s.addText("Iterations", {
  x: fx(127), y: fy(374), w: fw(90), h: fh(22),
  fontFace: FONT, fontSize: 20, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// ---------------- 9. SIX CALCULATION ROWS (table x273..852) ----------------
const CALC = [
  { y: 140, lbl: "d(x1)", m: "[1, 1, 1, 5]", res: "[-1, 3]" },
  { y: 205, lbl: "d(x2)", m: "[1, 2, 1, 5]", res: "[-1, 2]" },
  { y: 271, lbl: "d(x3)", m: "[1, 1, 2, 5]", res: "[-1, 2]" },
  { y: 337, lbl: "d(x4)", m: "[1, 5, 4, 5]", res: "[-1, -4]" },
  { y: 403, lbl: "d(x5)", m: "[1, 6, 5, 5]", res: "[-1, -6]" },
  { y: 469, lbl: "d(x6)", m: "[1, 6, 6, 5]", res: "[-1, -7]" },
];
CALC.forEach(function (r) {
  const ry = r.y + 18;                    // measured text-line centre offset inside the row
  s.addShape(pptx.ShapeType.line, {
    x: fx(273), y: fy(r.y), w: fw(852 - 273), h: 0,
    line: { color: RULE, width: 1 },
  });
  // d(xN) label + matrix, single text line centred on the row's text line
  s.addText([
    { text: r.lbl + " = ", options: { fontFace: FONT, fontSize: 12, color: BLACK } },
    { text: r.m, options: { fontFace: FONT, fontSize: 12, color: BLACK } },
    { text: "  ", options: { fontFace: FONT, fontSize: 12, color: BLACK } },
    { text: r.res, options: { fontFace: FONT, fontSize: 12, color: BLACK } },
  ], {
    x: fx(283), y: fy(ry), w: fw(160), h: fh(18),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });
  s.addText("\u21d2 Keep same Weight", {
    x: fx(508), y: fy(ry), w: fw(120), h: fh(18),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "left", valign: "middle", margin: 0,
  });
  s.addText([
    { text: "5", options: { breakLine: true } },
    { text: "-1", options: { breakLine: true } },
    { text: "-1", options: {} },
  ], {
    x: fx(708), y: fy(ry - 2), w: fw(50), h: fh(50),
    fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle",
    lineSpacing: 17, margin: 0,
  });
});
s.addShape(pptx.ShapeType.line, {
  x: fx(273), y: fy(527), w: fw(852 - 273), h: 0,
  line: { color: RULE, width: 1 },
});

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_049_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
