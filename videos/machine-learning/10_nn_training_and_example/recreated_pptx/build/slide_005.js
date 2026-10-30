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
const GREEN = "008000";

// Box colors from analysis
const BOX1_BG = "E6F3FF";  // light blue
const BOX1_BORDER = "000080";
const BOX2_BG = "FFFDE6";  // light yellow
const BOX2_BORDER = "000080";
const BOX3_BG = "E6FFE6";  // light green
const BOX3_BORDER = "008000";

// ---- load equation sidecars -----------------------------------------------
const assetsDir = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets/";

// Split eq_02a into two parts: first part (b=f(W)=w1a1+...) and trailing (=Σ)
const eq2a_first = JSON.parse(fs.readFileSync(assetsDir + "eq_2a_fixed.json", "utf8")); // first part with baseline dots
const eq2a_trailing = JSON.parse(fs.readFileSync(assetsDir + "eq_sum_wi_ai.json", "utf8")); // = Σ w_i a_i
const eq2b = JSON.parse(fs.readFileSync(assetsDir + "eq_02b.json", "utf8"));  // partial derivatives
const eq2c = JSON.parse(fs.readFileSync(assetsDir + "eq_02c.json", "utf8"));  // conclusion

const eq3a1 = JSON.parse(fs.readFileSync(assetsDir + "eq_03a1.json", "utf8")); // c=f(a1), c=f(a2), c=f(a3)
const eq3a2 = JSON.parse(fs.readFileSync(assetsDir + "eq_03a2.json", "utf8")); // and a1=f(b), a2=f(b), a3=f(b)
const eq_cfb_implies = JSON.parse(fs.readFileSync(assetsDir + "eq_cfb_implies.json", "utf8")); // c=f(b) =>
const eq_cond2 = JSON.parse(fs.readFileSync(assetsDir + "eq_cond2_fixed.json", "utf8")); // if b is changed...
const eq_through = JSON.parse(fs.readFileSync(assetsDir + "eq_through_fixed.json", "utf8")); // [through a1,a2,a3]
const eq3c = JSON.parse(fs.readFileSync(assetsDir + "eq_3c_full.json", "utf8")); // full bracketed expansion

const eq_b_fa = JSON.parse(fs.readFileSync(assetsDir + "eq_b_fa.json", "utf8"));
const eq_c_fb = JSON.parse(fs.readFileSync(assetsDir + "eq_c_fb.json", "utf8"));
const eq_c_fa = JSON.parse(fs.readFileSync(assetsDir + "eq_c_fa.json", "utf8"));
const eq_implies = JSON.parse(fs.readFileSync(assetsDir + "eq_implies.json", "utf8"));
const eq_cond = JSON.parse(fs.readFileSync(assetsDir + "eq_cond_fixed.json", "utf8"));
const eq1c = JSON.parse(fs.readFileSync(assetsDir + "eq_01c.json", "utf8"));

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

// 4. Three stacked colored boxes
const boxX = 1.0;
const boxW = 11.33;
const leftMargin = boxX + 0.2;

// Box 1: light blue (top)
const box1Y = 0.8;
const box1H = 1.5;
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: box1Y, w: boxW, h: box1H,
  fill: { color: BOX1_BG }, line: { color: BOX1_BORDER, width: 1.5 },
});

// Box 1 content: split pieces on line 1
let y = box1Y + 0.25;
let x = leftMargin;

// b=f(a)
addImg(eq_b_fa, x, y);
x += eq_b_fa.w_in + 0.15;

// c=f(b)
addImg(eq_c_fb, x, y);
x += eq_c_fb.w_in + 0.05;

// =>
addImg(eq_implies, x, y);
x += eq_implies.w_in + 0.05;

// c=f(a)
addImg(eq_c_fa, x, y);
x += eq_c_fa.w_in + 0.15;

// conditional text (fixed: includes closing paren, no cedilla)
addImg(eq_cond, x, y);

// Line 2: chain rule equation
y += Math.max(eq_b_fa.h_in, eq_c_fb.h_in, eq_c_fa.h_in, eq_cond.h_in) + 0.15;
addImg(eq1c, leftMargin, y);

// "Chain Rule" italic label - INLINE to the RIGHT of equation, black/dark
s.addText("Chain Rule", {
  x: leftMargin + eq1c.w_in + 0.15, y: y - 0.1, w: 1.5, h: 0.3,
  fontSize: 16, italic: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Box 2: light yellow (middle) - taller for expanded linear combination
const box2Y = box1Y + box1H + 0.1;
const box2H = 2.5;
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: box2Y, w: boxW, h: box2H,
  fill: { color: BOX2_BG }, line: { color: BOX2_BORDER, width: 1.5 },
});

// Box 2 content
y = box2Y + 0.25;

// Linear combination: first part + trailing "= Σ w_i a_i" on SAME line
addImg(eq2a_first, leftMargin, y);
let lin2_x = leftMargin + eq2a_first.w_in + 0.05;
addImg(eq2a_trailing, lin2_x, y);
y += Math.max(eq2a_first.h_in, eq2a_trailing.h_in) + 0.1;

// Partial derivatives
addImg(eq2b, leftMargin, y);
y += eq2b.h_in + 0.1;

// Conclusion line
addImg(eq2c, leftMargin, y);

// "Conclusion:" bold red at LEFT (on new line below eq2c)
y += eq2c.h_in + 0.1;
s.addText("Conclusion:", {
  x: leftMargin, y: y - 0.1, w: 1.5, h: 0.3,
  fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// "One Term ONLY" blue italic at RIGHT end
s.addText("One Term ONLY", {
  x: leftMargin + boxW - 1.8, y: y - 0.1, w: 1.8, h: 0.3,
  fontSize: 16, italic: true, color: BLUE, fontFace: FONT, margin: 0,
});

// Box 3: light green (bottom) - must end before house frame bottom (y=7.35)
const box3Y = box2Y + box2H + 0.1;
const box3H = 2.75;  // enough for 4 lines
s.addShape(pres.shapes.RECTANGLE, {
  x: boxX, y: box3Y, w: boxW, h: box3H,
  fill: { color: BOX3_BG }, line: { color: BOX3_BORDER, width: 1.5 },
});

// Box 3 content
y = box3Y + 0.2;

// Line 1: c=f(a1), c=f(a2), c=f(a3)
addImg(eq3a1, leftMargin, y);
y += eq3a1.h_in + 0.1;

// Line 2: and a1=f(b), a2=f(b), a3=f(b)
addImg(eq3a2, leftMargin, y);
y += eq3a2.h_in + 0.1;

// Line 3: c=f(b) => if b is changed... [through a1,a2,a3]
// Need: c=f(b) => [from eq_cfb_implies] + conditional [eq_cond2] + [through...] [eq_through]
let cond_x = leftMargin;
addImg(eq_cfb_implies, cond_x, y);
cond_x += eq_cfb_implies.w_in + 0.1;
addImg(eq_cond2, cond_x, y);
cond_x += eq_cond2.w_in + 0.1;
addImg(eq_through, cond_x, y);

y += Math.max(eq_cfb_implies.h_in, eq_cond2.h_in, eq_through.h_in) + 0.1;

// Line 4: full bracketed chain rule expansion
addImg(eq3c, leftMargin, y);

// 5. Black bottom strip
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.05, w: W, h: 0.05,
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

pres.writeFile({
  fileName: "videos/machine-learning/10_nn_training_and_example/recreated_pptx/slide_005_recreated.pptx"
}).then(() => console.log("wrote slide_005_recreated.pptx"))
  .catch(e => { console.error(e); process.exit(1); });