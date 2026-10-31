// slide_028.js — FRESH REBUILD (rb4) from qa/reanalysis2/slide_028_analysis.txt only.
// Spec coords [x0,y0,x1,y1] normalized -> inches: x*13.33, y*7.5, w=(x1-x0)*13.33, h=(y1-y0)*7.5.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_028.js
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = NS + "/recreated_pptx/build/eq_028/";
const man = JSON.parse(fs.readFileSync(EQ + "manifest_rb4.json", "utf8"));
const W = 13.33, H = 7.5, FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" }; // house rule

// House chrome (overrides spec): outer red frame + badge. Spec has NO title -> no title text.
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("28", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
// House title box (spec has no printed title -> empty text, chrome geometry only)
s.addText("", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Spec coords are normalized to the original 960x540 capture whose red frame is
// [0.054,0.065,0.852,0.856]; map that frame onto the house frame
// [0.011,0.02,0.989,0.98] so panels/glyphs match the original relative to it.
const FX0 = 0.054, FY0 = 0.065, FX1 = 0.852, FY1 = 0.856;
const SX = (0.989 - 0.011) / (FX1 - FX0), SY = (0.980 - 0.020) / (FY1 - FY0);
function box(x0, y0, x1, y1) {
  const nx0 = 0.011 + (x0 - FX0) * SX, nx1 = 0.011 + (x1 - FX0) * SX;
  const ny0 = 0.020 + (y0 - FY0) * SY, ny1 = 0.020 + (y1 - FY0) * SY;
  return { x: nx0 * W, y: ny0 * H, w: (nx1 - nx0) * W, h: (ny1 - ny0) * H };
}
// (black letterbox band and cursor stroke are capture artifacts: omitted)

// Upper blue panel [0.065,0.152,0.783,0.411], white fill
s.addShape(pres.shapes.RECTANGLE, Object.assign(
  box(0.065, 0.152, 0.783, 0.411),
  { fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 } }));
// Lower blue panel [0.065,0.426,0.833,0.843], white fill
s.addShape(pres.shapes.RECTANGLE, Object.assign(
  box(0.065, 0.426, 0.833, 0.843),
  { fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1.5 } }));

// Peach rounded chip behind "a^T b + 1" [0.069,0.246,0.136,0.309]
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(
  box(0.069, 0.246, 0.136, 0.309),
  { fill: { color: "FFE4C4" }, line: { color: "DDDDDD", width: 0.5 }, adj: 0.25 }));

// Red hollow left-pointing arrows (outline only)
function larrow(x0, y0, x1, y1) {
  s.addShape(pres.shapes.LEFT_ARROW, Object.assign(
    box(x0, y0, x1, y1),
    { fill: { type: "none" }, line: { color: "FF0033", width: 1.5 } }));
}
larrow(0.654, 0.754, 0.691, 0.780); // beside the = 144 sum
larrow(0.350, 0.796, 0.386, 0.822); // beside the bottom-left computation

// Equation PNGs at exact size (w_in = px/600, h_in = px/600), left-aligned,
// vertically centered within each spec box.
function eq(name) {
  const m = man[name];
  const b = box(m.box[0], m.box[1], m.box[2], m.box[3]);
  s.addImage({
    path: EQ + m.file,
    x: b.x, y: b.y + Math.max(0, (b.h - m.h_in) / 2),
    w: m.w_in, h: m.h_in,
  });
}
// Upper panel content
eq("chip");   // a^T b + 1 (red, on peach chip)
eq("sq");     // ^2 =
eq("arow");   // red alpha row vector
eq("bcol");   // blue beta 6-line column with ^T
eq("eq");     // = phi(a)^T phi(b)
eq("where");  // Where: phi(x) = (x1 x2)^T
eq("arrow");  // red =>
eq("phicol"); // black phi(x) 6-line column
// Lower panel content
eq("a");      // a = (1 2)^T red bold
eq("b");      // b = (3 4)^T blue bold
eq("leq");    // phi(a)^T phi(b) =
eq("row");    // red numeric row (1^2, 2^2, ...)
eq("bcol2");  // blue numeric 6-line column with ^T
eq("prod");   // = red product row
eq("numcol"); // blue (9, 16, 12sqrt2, ...)
eq("sum");    // = 9+64+48+6+16+1 = 144
eq("bot");    // |a^T b+1|^2 = (1+3+2*4+1)^2 = 12^2 = 144

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_028_recreated.pptx") })
  .then(() => console.log("wrote slide_028_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
