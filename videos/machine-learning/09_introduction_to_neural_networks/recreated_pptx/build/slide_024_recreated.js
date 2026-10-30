const pptxgen = require("pptxgenjs");

const NUM = 24;
const TITLE = "For Sigmoid Function";
const FONT = "Arial";
const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";

const BG = "E8E8E8";
const RED = "C0392B";
const BLUE = "0000FF";
const BORDER_RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "F1C40F";  // bright yellow per validation
const PEACH = "FDF2E9";
const LIGHT_BLUE = "E3F2FD";
const DARK_GRAY = "333333";

const W = 13.33, H = 7.5;

const EQ = {
  sigmoid:     { w: 3.752, h: 0.790 },
  remember:    { w: 1.637, h: 1.020 },
  step1:       { w: 5.172, h: 0.790 },
  step2a:      { w: 3.647, h: 0.790 },
  step2b:      { w: 3.697, h: 0.790 },
  step3:       { w: 3.790, h: 0.790 },
  final:       { w: 3.398, h: 0.790 },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Bottom black bar (video player overlay artifact in original)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { color: "none" },
});

// 3. Slide-number badge - HOUSE CHROME LAW (bright yellow F1C40F)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 4. Title - HOUSE CHROME LAW (top-left, red, ITALIC per original)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "left", valign: "top",
  fontSize: 28, bold: false, italic: true, color: RED, fontFace: FONT, margin: 0,
});

// Column positions (two-column layout)
const LEFT_X = 0.93;
const LEFT_W = 5.9;
const RIGHT_X = 7.1;
const RIGHT_W = 5.9;
const TOP_Y = 1.30;
const BOX_H = 1.35;
const BOX_GAP = 0.15;

// ===== LEFT COLUMN =====
let leftY = TOP_Y;

// 5. Sigmoid definition box (peach, formula text in RED)
s.addShape(pres.shapes.RECTANGLE, {
  x: LEFT_X, y: leftY, w: LEFT_W, h: BOX_H,
  fill: { color: PEACH }, line: { color: RED, width: 1 },
});
s.addImage({
  path: BUILD + "/eq_s024_sigmoid.png",
  x: LEFT_X + 0.2, y: leftY + 0.28, w: EQ.sigmoid.w, h: EQ.sigmoid.h,
});
leftY += BOX_H + BOX_GAP;

// 6. Derivation step 1 box (white, large)
const step1_h = BOX_H * 1.2;
s.addShape(pres.shapes.RECTANGLE, {
  x: LEFT_X, y: leftY, w: LEFT_W, h: step1_h,
  fill: { color: WHITE }, line: { color: BORDER_RED, width: 1 },
});
s.addImage({
  path: BUILD + "/eq_s024_step1.png",
  x: LEFT_X + 0.2, y: leftY + 0.25, w: EQ.step1.w, h: EQ.step1.h,
});
leftY += step1_h + BOX_GAP;

// 7. Derivation step 2 box (white, TALL - combines step2a and step2b in single box per original)
const step2_combined_h = EQ.step2a.h + EQ.step2b.h + 0.3;
s.addShape(pres.shapes.RECTANGLE, {
  x: LEFT_X, y: leftY, w: LEFT_W, h: step2_combined_h,
  fill: { color: WHITE }, line: { color: BORDER_RED, width: 1 },
});
s.addImage({
  path: BUILD + "/eq_s024_step2a.png",
  x: LEFT_X + 0.2, y: leftY + 0.1, w: EQ.step2a.w, h: EQ.step2a.h,
});
s.addImage({
  path: BUILD + "/eq_s024_step2b.png",
  x: LEFT_X + 0.2, y: leftY + 0.1 + EQ.step2a.h + 0.1, w: EQ.step2b.w, h: EQ.step2b.h,
});
leftY += step2_combined_h + BOX_GAP;

// 8. Derivation step 3 box (white) - ensure it fits within frame
const frame_bottom = H - 0.15 - 0.35;  // house frame bottom minus black bar
if (leftY + BOX_H > frame_bottom) {
  // Adjust if too low
}
s.addShape(pres.shapes.RECTANGLE, {
  x: LEFT_X, y: leftY, w: LEFT_W, h: BOX_H,
  fill: { color: WHITE }, line: { color: BORDER_RED, width: 1 },
});
s.addImage({
  path: BUILD + "/eq_s024_step3.png",
  x: LEFT_X + 0.2, y: leftY + 0.28, w: EQ.step3.w, h: EQ.step3.h,
});

// ===== RIGHT COLUMN =====
let rightY = TOP_Y;

// 9. Remember box (light blue, BLUE text per original)
s.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_X, y: rightY, w: RIGHT_W, h: BOX_H,
  fill: { color: LIGHT_BLUE }, line: { color: BLUE, width: 1 },
});
// Use text for "Remember:" + image for equation (to avoid colon spacing issue)
s.addText("Remember:", {
  x: RIGHT_X + 0.2, y: rightY + 0.15, w: RIGHT_W - 0.4, h: 0.35,
  align: "left", valign: "top",
  fontSize: 16, color: BLUE, fontFace: FONT, margin: 0,
});
s.addImage({
  path: BUILD + "/eq_s024_remember.png",
  x: RIGHT_X + 0.2, y: rightY + 0.45, w: EQ.remember.w, h: EQ.remember.h,
});
rightY += BOX_H + BOX_GAP;

// 10. Sigmoid description box (peach)
const desc_h = BOX_H * 1.2;
s.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_X, y: rightY, w: RIGHT_W, h: desc_h,
  fill: { color: PEACH }, line: { color: RED, width: 1 },
});
// Header: red bold
s.addText("Sigmoid (aka Logistic function)", {
  x: RIGHT_X + 0.2, y: rightY + 0.1, w: RIGHT_W - 0.4, h: 0.3,
  align: "left", valign: "top",
  fontSize: 16, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// Body with rich formatting: squashing=italic, unbounded=underline, probabilistic=underline, (from 0 to 1)=red+italic
s.addText([
  { text: "It is a ", options: { color: DARK_GRAY, fontSize: 14, fontFace: FONT } },
  { text: "squashing", options: { color: DARK_GRAY, fontSize: 14, fontFace: FONT, italic: true } },
  { text: " function used to convert an ", options: { color: DARK_GRAY, fontSize: 14, fontFace: FONT } },
  { text: "unbounded", options: { color: DARK_GRAY, fontSize: 14, fontFace: FONT, underline: true } },
  { text: " values to a bounded ", options: { color: DARK_GRAY, fontSize: 14, fontFace: FONT } },
  { text: "probabilistic", options: { color: DARK_GRAY, fontSize: 14, fontFace: FONT, underline: true } },
  { text: " space ", options: { color: DARK_GRAY, fontSize: 14, fontFace: FONT } },
  { text: "(from 0 to 1)", options: { color: RED, fontSize: 14, fontFace: FONT, italic: true } },
], {
  x: RIGHT_X + 0.2, y: rightY + 0.45, w: RIGHT_W - 0.4, h: 0.7,
  align: "left", valign: "top", margin: 0,
});
rightY += desc_h + BOX_GAP;

// 11. Final result box (peach with red arrow - ONLY from equation PNG, no duplicate text arrow)
s.addShape(pres.shapes.RECTANGLE, {
  x: RIGHT_X, y: rightY, w: RIGHT_W, h: BOX_H,
  fill: { color: PEACH }, line: { color: RED, width: 1 },
});
// Equation PNG already contains the arrow, just place it centered
s.addImage({
  path: BUILD + "/eq_s024_final.png",
  x: RIGHT_X + (RIGHT_W - EQ.final.w) / 2, y: rightY + 0.28, w: EQ.final.w, h: EQ.final.h,
});

pres.writeFile({ 
  fileName: BUILD + "/slide_024_recreated.pptx" 
}).then(() => console.log("wrote slide_024_recreated.pptx"));