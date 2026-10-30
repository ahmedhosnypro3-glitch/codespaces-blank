const pptxgen = require("pptxgenjs");
const fs = require("fs");
const pathMod = require("path");

// ---- parameters -----------------------------------------------------------
const NUM = 5;
const TITLE = "Revision";
const FONT = "Arial";
const BG = "E8E8E8";
const RED = "C00000";
const BLACK = "000000";
const DARK_BLUE = "000080";
const DARK_GREEN = "008000";
const BLUE = "0000FF";

// Box colors from analysis
const BOX1_BG = "E6F3FF";  // light blue
const BOX1_BORDER = "000080";
const BOX2_BG = "FFFDE6";  // light yellow
const BOX2_BORDER = "000080";
const BOX3_BG = "E6FFE6";  // light green
const BOX3_BORDER = "008000";

// ---- load equation sidecars -----------------------------------------------
const assetsDir = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets/";
const eq_b_fa = JSON.parse(fs.readFileSync(assetsDir + "eq_b_fa.json", "utf8"));
const eq_c_fb = JSON.parse(fs.readFileSync(assetsDir + "eq_c_fb.json", "utf8"));
const eq_c_fa = JSON.parse(fs.readFileSync(assetsDir + "eq_c_fa.json", "utf8"));
const eq_implies = JSON.parse(fs.readFileSync(assetsDir + "eq_implies.json", "utf8"));
const eq_cond = JSON.parse(fs.readFileSync(assetsDir + "eq_cond.json", "utf8"));
const eq1c = JSON.parse(fs.readFileSync(assetsDir + "eq_01c.json", "utf8"));
const eq2a = JSON.parse(fs.readFileSync(assetsDir + "eq_02a.json", "utf8"));
const eq2b = JSON.parse(fs.readFileSync(assetsDir + "eq_02b.json", "utf8"));
const eq_sum_ai_wi = JSON.parse(fs.readFileSync(assetsDir + "eq_sum_ai_wi.json", "utf8"));
const eq_db_dwi = JSON.parse(fs.readFileSync(assetsDir + "eq_db_dwi.json", "utf8"));
const eq_b_fw = JSON.parse(fs.readFileSync(assetsDir + "eq_b_fw.json", "utf8"));
const eq_3c_fa = JSON.parse(fs.readFileSync(assetsDir + "eq_3c_fa.json", "utf8"));
const eq_3a_fb = JSON.parse(fs.readFileSync(assetsDir + "eq_3a_fb.json", "utf8"));
const eq_cond2 = JSON.parse(fs.readFileSync(assetsDir + "eq_cond2.json", "utf8"));
const eq_through = JSON.parse(fs.readFileSync(assetsDir + "eq_through.json", "utf8"));
const eq3c = JSON.parse(fs.readFileSync(assetsDir + "eq_03c.json", "utf8"));

// ---- build ----------------------------------------------------------------
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. Slide-number badge (yellow oval + centered bold numeral)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title box (house position: y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Helper to add image at baseline
const addImg = (side, x, baselineY) => {
  const y = baselineY - side.baseline_frac * side.h_in;
  s.addImage({ path: assetsDir + pathMod.basename(side.path), x, y, w: side.w_in, h: side.h_in });
  return y + side.h_in;
};

// 4. Three stacked colored boxes - adjusted to prevent overflow
const boxX = 1.0;
const boxW = 11.33;
const leftMargin = boxX + 0.2;

// Box 1: light blue (top) - reduced height
const box1Y = 1.0;
const box1H = 1.8;
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: box1Y, w: boxW, h: box1H,
  fill: { color: BOX1_BG }, line: { color: BOX1_BORDER, width: 1.5 },
});

// Box 1 content: separate pieces on line 1 WITH PROPER SPACING
let y = box1Y + 0.25;
let x = leftMargin;

// b=f(a)
addImg(eq_b_fa, x, y);
x += eq_b_fa.w_in + 0.15;

// c=f(b)
addImg(eq_c_fb, x, y);
x += eq_c_fb.w_in + 0.15;

// =>
addImg(eq_implies, x, y);
x += eq_implies.w_in + 0.15;

// c=f(a)
addImg(eq_c_fa, x, y);
x += eq_c_fa.w_in + 0.25;

// conditional text (red, italic, spaced)
s.addText("if a is changed , c will be changed accordingly)", {
  x: x, y: y - 0.1, w: 4.0, h: 0.35,
  fontSize: 16, italic: true, color: RED, fontFace: FONT, margin: 0,
});

// Line 2: chain rule equation
y += Math.max(eq_b_fa.h_in, eq_c_fb.h_in, eq_c_fa.h_in, 0.25) + 0.15;
addImg(eq1c, leftMargin, y);

// "Chain Rule" italic label - BELOW equation, centered
s.addText("Chain Rule", {
  x: leftMargin + (eq1c.w_in / 2) - 0.5, y: y + eq1c.h_in + 0.05, w: 1.5, h: 0.3,
  fontSize: 16, italic: true, color: DARK_BLUE, fontFace: FONT, margin: 0,
});

// Box 2: light yellow (middle)
const box2Y = box1Y + box1H + 0.1;
const box2H = 2.0;
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: box2Y, w: boxW, h: box2H,
  fill: { color: BOX2_BG }, line: { color: BOX2_BORDER, width: 1.5 },
});

// Box 2 content
y = box2Y + 0.2;

// Linear combination - full expanded form
addImg(eq2a, leftMargin, y);
y += eq2a.h_in + 0.1;

// Partial derivatives
addImg(eq2b, leftMargin, y);
y += eq2b.h_in + 0.1;

// Conclusion line - "Conclusion:" bold red at LEFT, separate from math
s.addText("Conclusion:", {
  x: leftMargin, y: y - 0.1, w: 1.5, h: 0.3,
  fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
});

let conc_x = leftMargin + 1.5;

// b=f(W)=
addImg(eq_b_fw, conc_x, y);
conc_x += eq_b_fw.w_in + 0.1;

// Σ a_i w_i
addImg(eq_sum_ai_wi, conc_x, y);
conc_x += eq_sum_ai_wi.w_in + 0.15;

// " then "
s.addText("then", {
  x: conc_x, y: y - 0.1, w: 0.8, h: 0.3,
  fontSize: 16, color: BLACK, fontFace: FONT, margin: 0,
});
conc_x += 0.8;

// ∂b/∂w_i = a_i
addImg(eq_db_dwi, conc_x, y);

// "One Term ONLY" blue italic at RIGHT end - SEPARATED from Conclusion
s.addText("One Term ONLY", {
  x: leftMargin + boxW - 2.0, y: y - 0.1, w: 2.0, h: 0.3,
  fontSize: 16, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});

// Box 3: light green (bottom) - ensure it fits within slide
const box3Y = box2Y + box2H + 0.1;
const box3H = 2.0;  // Reduced to prevent overflow (bottom at ~6.1, house frame at 7.35)
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: box3Y, w: boxW, h: box3H,
  fill: { color: BOX3_BG }, line: { color: BOX3_BORDER, width: 1.5 },
});

// Box 3 content
y = box3Y + 0.2;

// Line 1: c=f(a1), c=f(a2), c=f(a3)   and   a1=f(b), a2=f(b), a3=f(b)
addImg(eq_3c_fa, leftMargin, y);

let line1_x = leftMargin + eq_3c_fa.w_in + 0.15;
s.addText("and", {
  x: line1_x, y: y - 0.1, w: 0.5, h: 0.3,
  fontSize: 16, color: BLACK, fontFace: FONT, margin: 0,
});
line1_x += 0.5;
addImg(eq_3a_fb, line1_x, y);

// Line 2: c=f(b) => if b is changed... [through a1,a2,a3]
y += Math.max(eq_3c_fa.h_in, eq_3a_fb.h_in) + 0.15;
addImg(eq_cond2, leftMargin, y);  // This is "c=f(b) => if b is changed..."

let cond2_x = leftMargin + eq_cond2.w_in + 0.1;
addImg(eq_through, cond2_x, y);

// Line 3: expanded chain rule (with brackets)
y += Math.max(eq_cond2.h_in, eq_through.h_in) + 0.15;
addImg(eq3c, leftMargin, y);

// 5. Black bottom strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.05, w: W, h: 0.05,
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

pres.writeFile({
  fileName: "videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_005_recreated.pptx"
}).then(() => console.log("wrote slide_005_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });