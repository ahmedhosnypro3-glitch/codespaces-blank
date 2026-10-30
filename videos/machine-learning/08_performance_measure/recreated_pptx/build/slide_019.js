// Slide 019 rebuild attempt 4 — Training Samples with Labels (Two Classes)
// Frame-vs-spec deviations (measured from unique_slides/slide_019.jpg, 960x540, 1px=1pt):
//  - 5 positive planes / 5x "+1" (pink strip), 6 negative planes / 6x "-1" (green strip)
//  - "Positive Class" + "Shoot the Enemy" RED (spec said blue header; frame wins)
//  - Model caption verbatim drift item: [Any value] → (-1 , +1)  (parens + arrow, not brackets/->)
//  - Flow arrows point LEFT->RIGHT (RIGHT_ARROW), Training and Evaluation
//  - LOSS circle pale peach F4A460 (was saturated orange)
//  - house chrome per root AGENTS.md (red frame, yellow badge "19", title box y0.28)
const pptxgen = require("pptxgenjs");
const path = require("path");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";        // house frame
const YELLOW = "FFF9C4";     // badge
const DARK = "333333";
const TXT_RED = "C02828";    // positive class text
const TXT_GREEN = "1E8A3C";  // negative class text
const DARK_RED = "8B0000";   // plane-box borders / Model boxes
const PINK = "F8DBDD";       // +1 strip fill
const GREEN_FILL = "E4FFEE"; // -1 strip fill
const MAROON = "A01818";     // +1 text
const TEAL = "12694E";       // -1 text
const BLUE = "20409B";       // activation border / heading
const PURPLE = "6A3FB5";     // bi-polar step line
const PEACH = "F4A460";      // LOSS circle
const CREAM = "FBFEE3";      // training/eval panel fill
const ORANGE = "E8A33D";     // training/eval border
const NAVY = "2E2A6E";       // title text
const BLUE_TXT = "0000CC";   // (+1, -1) values
const BLACK = "000000";
const WHITE = "FFFFFF";
const GRAY_LINE = "C8C8C8";
const FONT = "Arial";

const ASSETS = path.join(__dirname, "assets");
const AIR_ENEMY = path.join(ASSETS, "eq_019_airplane_enemy.png");
const AIR_SAFE = path.join(ASSETS, "eq_019_airplane_safe.png");
const STEP_ICON = path.join(ASSETS, "eq_019_step_icon.png");
const STEP_SMALL = path.join(ASSETS, "eq_019_step_small.png");
const AIR_W = 745 / 600, AIR_H = 672 / 600;
const STEP_W = 849 / 600, STEP_H = 528 / 600;
const STEP_S_W = 477 / 600, STEP_S_H = 477 / 600;

const P = 1 / 72; // frame px -> inches

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});
// title box (house geometry); original banner is light fill, blue border, navy text
// drawn BEFORE the badge so its fill can never cover the badge numeral
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 11.8, h: 0.62,
  fill: { color: WHITE }, line: { color: BLUE, width: 1.5 },
});
s.addText("Training Samples with Labels (Two Classes)", {
  x: 0.6, y: 0.28, w: 11.8, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 22, bold: true, color: NAVY, fontFace: FONT, margin: 0,
});
// Slide number badge: yellow circle at top-right (drawn after title so numeral stays visible)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("19", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// ---- samples panel (gray panel x69..557 y92..509 in frame px) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 69 * P, y: 92 * P, w: 488 * P, h: 417 * P,
  fill: { color: WHITE }, line: { color: GRAY_LINE, width: 1 },
});

// Positive Class header (red) + motto
s.addText("Positive Class", {
  x: 75 * P, y: 95 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("\u201CShoot the Enemy\u201D", {
  x: 75 * P, y: 114 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 247 * P, y: 138 * P, w: 0.6, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
// positive plane box (white, dark-red border) x80..239 y137..505
s.addShape(pptx.shapes.RECTANGLE, {
  x: 80 * P, y: 137 * P, w: 159 * P, h: 368 * P,
  fill: { color: WHITE }, line: { color: DARK_RED, width: 2 },
});
// 5 enemy planes, band centers ~197,265,325,387,454 px
const posY = [197, 265, 325, 387, 454];
for (const cy of posY) {
  s.addImage({ path: AIR_ENEMY, x: 80 * P + (159 * P - AIR_W) / 2, y: cy * P - AIR_H / 2, w: AIR_W, h: AIR_H });
}
// +1 strip x247..289 y161..493 (pink)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 247 * P, y: 161 * P, w: 42 * P, h: 332 * P,
  fill: { color: PINK }, line: { color: TXT_RED, width: 1 },
});
for (const cy of [195, 257, 318, 380, 441]) {
  s.addText("+1", {
    x: 247 * P, y: (cy - 9) * P, w: 42 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: MAROON, fontFace: FONT, margin: 0,
  });
}

// Negative Class header (green) + motto
s.addText("Negative Class", {
  x: 330 * P, y: 95 * P, w: 2.6, h: 0.26,
  fontSize: 14, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("\u201CSafe\u201D", {
  x: 330 * P, y: 114 * P, w: 2.6, h: 0.24,
  fontSize: 12, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
s.addText("Label", {
  x: 498 * P, y: 138 * P, w: 0.6, h: 0.2,
  align: "center", fontSize: 10, bold: true, color: TXT_GREEN, fontFace: FONT, margin: 0,
});
// negative plane box x330..484 y136..505 (dark-red border per frame pixels)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 330 * P, y: 136 * P, w: 154 * P, h: 369 * P,
  fill: { color: WHITE }, line: { color: DARK_RED, width: 2 },
});
// 6 safe planes, band centers ~185,236,291,339,395,455 px
const negY = [185, 236, 291, 339, 395, 455];
for (const cy of negY) {
  s.addImage({ path: AIR_SAFE, x: 330 * P + (154 * P - AIR_W) / 2, y: cy * P - AIR_H / 2, w: AIR_W, h: AIR_H });
}
// -1 strip x498..540 y161..499 (pale green)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 498 * P, y: 161 * P, w: 42 * P, h: 338 * P,
  fill: { color: GREEN_FILL }, line: { color: TXT_GREEN, width: 1 },
});
for (const cy of [176, 238, 283, 336, 398, 460]) {
  s.addText("-1", {
    x: 498 * P, y: (cy - 9) * P, w: 42 * P, h: 18 * P,
    align: "center", valign: "middle",
    fontSize: 12, bold: true, color: TEAL, fontFace: FONT, margin: 0,
  });
}

// ---- right column ----
// Activation Function box x660..944 y78..218, white fill, blue border
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 78 * P, w: 284 * P, h: 140 * P,
  fill: { color: WHITE }, line: { color: BLUE, width: 1.5 },
});
s.addText("Activation Function", {
  x: 672 * P, y: 86 * P, w: 3.4, h: 0.24,
  fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Bi-polar step (-1 , +1)", {
  x: 672 * P, y: 112 * P, w: 3.4, h: 0.22,
  fontSize: 11, color: PURPLE, fontFace: FONT, margin: 0,
});
s.addText("Threshold at \u201Czero\u201D", {
  x: 672 * P, y: 136 * P, w: 3.4, h: 0.22,
  fontSize: 11, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addImage({ path: STEP_ICON, x: 868 * P, y: 96 * P, w: STEP_W * 0.75, h: STEP_H * 0.75 });

// Training: heading + pale-yellow panel x660..944 y240..330
s.addText("Training", {
  x: 700 * P, y: 222 * P, w: 2.0, h: 0.26,
  align: "center", fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 240 * P, w: 284 * P, h: 90 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const ty = 250 * P; // flow row top
// Input Sample
s.addShape(pptx.shapes.RECTANGLE, {
  x: 666 * P, y: ty, w: 60 * P, h: 52 * P,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Input\nSample", {
  x: 666 * P, y: ty, w: 60 * P, h: 52 * P,
  align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0, lineSpacing: 11,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 728 * P, y: ty + 17 * P, w: 12 * P, h: 16 * P, fill: { color: BLACK } });
// Model box (dark red) with verbatim drift caption
s.addShape(pptx.shapes.RECTANGLE, {
  x: 742 * P, y: ty - 4 * P, w: 96 * P, h: 60 * P,
  fill: { color: DARK_RED },
});
s.addText("Model", {
  x: 742 * P, y: ty, w: 96 * P, h: 20 * P,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 742 * P, y: ty + 22 * P, w: 96 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: WHITE, fontFace: FONT, margin: 0,
});
s.addImage({ path: STEP_SMALL, x: 826 * P, y: ty + 2 * P, w: STEP_S_W * 0.5, h: STEP_S_H * 0.5 });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 840 * P, y: ty + 17 * P, w: 10 * P, h: 16 * P, fill: { color: BLACK } });
// Predicted Class
s.addShape(pptx.shapes.RECTANGLE, {
  x: 852 * P, y: ty, w: 48 * P, h: 52 * P,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted\nClass", {
  x: 852 * P, y: ty, w: 48 * P, h: 52 * P,
  align: "center", valign: "middle",
  fontSize: 8, color: BLACK, fontFace: FONT, margin: 0, lineSpacing: 10,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 902 * P, y: ty + 17 * P, w: 8 * P, h: 16 * P, fill: { color: BLACK } });
// LOSS circle (pale peach)
s.addShape(pptx.shapes.OVAL, {
  x: 912 * P, y: ty + 6 * P, w: 30 * P, h: 30 * P,
  fill: { color: PEACH }, line: { color: BLACK, width: 1 },
});
s.addText("LOSS", {
  x: 912 * P, y: ty + 6 * P, w: 30 * P, h: 30 * P,
  align: "center", valign: "middle",
  fontSize: 7, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// Label of Input Sample (+1, -1) below the flow row, inside panel
s.addText("Label of Input Sample", {
  x: 846 * P, y: ty + 54 * P, w: 96 * P, h: 12 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("(+1, -1)", {
  x: 846 * P, y: ty + 66 * P, w: 96 * P, h: 14 * P,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

// Evaluation: heading + pale-yellow panel x660..944 y380..497
s.addText("Evaluation", {
  x: 700 * P, y: 377 * P, w: 2.0, h: 0.26,
  align: "center", fontSize: 14, bold: true, color: TXT_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 660 * P, y: 392 * P, w: 284 * P, h: 100 * P,
  fill: { color: CREAM }, line: { color: ORANGE, width: 1 },
});
const ey = 406 * P; // flow row top
// Test Sample
s.addShape(pptx.shapes.RECTANGLE, {
  x: 666 * P, y: ey, w: 60 * P, h: 52 * P,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Test\nSample", {
  x: 666 * P, y: ey, w: 60 * P, h: 52 * P,
  align: "center", valign: "middle",
  fontSize: 9, color: BLACK, fontFace: FONT, margin: 0, lineSpacing: 11,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 728 * P, y: ey + 17 * P, w: 12 * P, h: 16 * P, fill: { color: BLACK } });
// Model box
s.addShape(pptx.shapes.RECTANGLE, {
  x: 742 * P, y: ey - 4 * P, w: 96 * P, h: 60 * P,
  fill: { color: DARK_RED },
});
s.addText("Model", {
  x: 742 * P, y: ey, w: 96 * P, h: 20 * P,
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: WHITE, fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (-1 , +1)", {
  x: 742 * P, y: ey + 22 * P, w: 96 * P, h: 16 * P,
  align: "center", valign: "middle",
  fontSize: 7, color: WHITE, fontFace: FONT, margin: 0,
});
s.addImage({ path: STEP_SMALL, x: 826 * P, y: ey + 2 * P, w: STEP_S_W * 0.5, h: STEP_S_H * 0.5 });
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 840 * P, y: ey + 17 * P, w: 10 * P, h: 16 * P, fill: { color: BLACK } });
// Predicted Class
s.addShape(pptx.shapes.RECTANGLE, {
  x: 852 * P, y: ey, w: 48 * P, h: 52 * P,
  fill: { color: WHITE }, line: { color: BLACK, width: 1 },
});
s.addText("Predicted\nClass", {
  x: 852 * P, y: ey, w: 48 * P, h: 52 * P,
  align: "center", valign: "middle",
  fontSize: 8, color: BLACK, fontFace: FONT, margin: 0, lineSpacing: 10,
});
s.addShape(pptx.shapes.RIGHT_ARROW, { x: 902 * P, y: ey + 17 * P, w: 8 * P, h: 16 * P, fill: { color: BLACK } });
// (+1, -1) blue bold at right end
s.addText("(+1, -1)", {
  x: 912 * P, y: ey + 9 * P, w: 30 * P, h: 34 * P,
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_019_recreated.pptx"
}).then(() => console.log("done"));
