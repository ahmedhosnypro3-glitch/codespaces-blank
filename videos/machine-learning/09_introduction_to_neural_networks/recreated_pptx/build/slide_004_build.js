const pptxgen = require("pptxgenjs");

// Slide 004: Problem Formulation
// Equations embedded as 600dpi mathtext PNGs (Professional Format 2D) per MISSION_PROTOCOL.
const NUM = 4;
const TITLE = "Problem Formulation";
const FONT = "Arial";
const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const GREEN = "00B050";
const BORDER_RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const PEACH = "FDEADA";
const LIGHT_GREEN = "E2EFDA";

// Equation PNG sizes (px at 600dpi -> inches = px/600), from gen_slide_004_eq.py output
const EQ = {
  error:             { w: 4.982, h: 0.790 },
  gradient_descent:  { w: 3.848, h: 0.790 },
  gradient:          { w: 3.828, h: 0.790 },
  update_batch:      { w: 6.855, h: 0.790 },
  update_online:     { w: 3.710, h: 0.790 },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
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

// 3. Slide-number badge - HOUSE CHROME LAW
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "4B0082", fontFace: FONT, margin: 0,
});

// 4. Title - HOUSE CHROME LAW
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 5. Panel 1: Define delta - square-cornered red border, white fill
const panel1_x = 0.93, panel1_y = 1.30, panel1_w = 11.2, panel1_h = 1.45;
s.addShape(pres.shapes.RECTANGLE, {
  x: panel1_x, y: panel1_y, w: panel1_w, h: panel1_h,
  fill: { color: WHITE }, line: { color: RED, width: 1 },
});

let y = panel1_y + 0.08;
s.addText([
  { text: "Define ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 12, fontFace: FONT, subscript: true } },
  { text: " as:", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
], {
  x: panel1_x + 0.2, y: y, w: panel1_w - 0.4, h: 0.35,
  align: "left", valign: "top", margin: 0,
});
y += 0.35;

// Conditional line 1
s.addText([
  { text: "If X \u2208 ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "class I", options: { color: RED, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
  { text: " and ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "misclassified as ", options: { color: BLACK, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "Class II", options: { color: BLUE, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
  { text: " then ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, fontSize: 14, fontFace: FONT, italic: true } },
  { text: " will be ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "<0", options: { color: RED, bold: true, fontSize: 14, fontFace: FONT } },
  { text: " \u21D2 ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 10, fontFace: FONT, subscript: true } },
  { text: " = -1", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: " \u21D2 ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 10, fontFace: FONT, subscript: true } },
  { text: " >0", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
], {
  x: panel1_x + 0.2, y: y, w: panel1_w - 0.4, h: 0.4,
  align: "left", valign: "top", margin: 0,
});
y += 0.35;

// Conditional line 2
s.addText([
  { text: "If X \u2208 ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "class II", options: { color: BLUE, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
  { text: " and ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "misclassified as ", options: { color: BLACK, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "Class I", options: { color: RED, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
  { text: " then ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, fontSize: 14, fontFace: FONT, italic: true } },
  { text: " will be ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: ">0", options: { color: RED, bold: true, fontSize: 14, fontFace: FONT } },
  { text: " \u21D2 ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 10, fontFace: FONT, subscript: true } },
  { text: " = +1", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: " \u21D2 ", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 10, fontFace: FONT, subscript: true } },
  { text: " >0", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
], {
  x: panel1_x + 0.2, y: y, w: panel1_w - 0.4, h: 0.4,
  align: "left", valign: "top", margin: 0,
});

// 6. Panel 2: Redefine Error function - rounded red border, white fill
const panel2_x = 0.93, panel2_y = 2.90, panel2_w = 11.47, panel2_h = 1.55;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: panel2_x, y: panel2_y, w: panel2_w, h: panel2_h,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

y = panel2_y + 0.08;
s.addText("Redefine Error function as:", {
  x: panel2_x + 0.2, y: y, w: panel2_w - 0.4, h: 0.32,
  align: "left", valign: "top",
  fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
y += 0.34;

// Error equation as 2D PNG (eq_error.png: 4.982 x 0.790 in) scaled to fit
const eq_err_scale = 0.75; // scale factor to fit panel
const eq_err_w = EQ.error.w * eq_err_scale;
const eq_err_h = EQ.error.h * eq_err_scale;
s.addImage({
  path: BUILD + "/eq_error.png",
  x: panel2_x + 0.25, y: y, w: eq_err_w, h: eq_err_h,
});
// implication clause to the right of the equation
s.addText("\u21D2 (W\u1D40X\u1D62) takes positive and negative values and \u03B4\u1D62 has the same sign", {
  x: panel2_x + 0.25 + eq_err_w + 0.15, y: y + 0.1, w: panel2_w - 0.4 - eq_err_w - 0.3, h: 0.5,
  align: "left", valign: "top",
  fontSize: 12, color: BLACK, fontFace: FONT, italic: true, margin: 0,
});
y += eq_err_h + 0.02;

s.addText([
  { text: "Summation is always ", options: { color: BLACK, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "positive", options: { color: RED, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
], {
  x: panel2_x + 0.2, y: panel2_y + panel2_h - 0.35, w: panel2_w - 0.4, h: 0.3,
  align: "left", valign: "top", margin: 0,
});

// 7. Panel 3: Gradient descent update - rounded red border, peach fill
const panel3_x = 0.93, panel3_y = 4.60, panel3_w = 11.47, panel3_h = 2.35;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: panel3_x, y: panel3_y, w: panel3_w, h: panel3_h,
  fill: { color: PEACH }, line: { color: RED, width: 1.5 },
});

y = panel3_y + 0.08;
s.addText([
  { text: "Minimize the Error using ", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true, underline: true } },
  { text: "Gradient Descent", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT, italic: true, underline: true } },
  { text: " with step ", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true, underline: true } },
  { text: "\u03B7", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT, italic: true, underline: true } },
], {
  x: panel3_x + 0.2, y: y, w: panel3_w - 0.4, h: 0.4,
  align: "left", valign: "top", margin: 0,
});
y += 0.42;

// Gradient descent update as 2D PNG (eq_gradient_descent.png: 3.848 x 0.790 in)
const eq_gd_scale = 0.72;
const eq_gd_w = EQ.gradient_descent.w * eq_gd_scale;
const eq_gd_h = EQ.gradient_descent.h * eq_gd_scale;
s.addImage({
  path: BUILD + "/eq_gradient_descent.png",
  x: panel3_x + 0.25, y: y, w: eq_gd_w, h: eq_gd_h,
});
// "where" beside the equation
s.addText("where", {
  x: panel3_x + 0.25 + eq_gd_w + 0.2, y: y + 0.15, w: 0.8, h: 0.35,
  align: "left", valign: "top",
  fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
// gradient equation as 2D PNG (eq_gradient.png: 3.828 x 0.790 in)
const eq_g_scale = 0.72;
const eq_g_w = EQ.gradient.w * eq_g_scale;
const eq_g_h = EQ.gradient.h * eq_g_scale;
s.addImage({
  path: BUILD + "/eq_gradient.png",
  x: panel3_x + 0.25 + eq_gd_w + 1.0, y: y, w: eq_g_w, h: eq_g_h,
});
y += eq_gd_h + 0.02;

// Bottom row: two green boxes with caption and arrow between
const green_box_y = panel3_y + panel3_h - 0.78;
const green_box_h = 0.72;
const green_box_w = 4.4;
const gap = 0.55;

// Left green box: batch update as 2D PNG
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: panel3_x + 0.2, y: green_box_y, w: green_box_w, h: green_box_h,
  fill: { color: LIGHT_GREEN }, line: { color: GREEN, width: 1.5 },
});
const eq_b_scale = Math.min(0.62, (green_box_w - 0.2) / EQ.update_batch.w);
const eq_b_w = EQ.update_batch.w * eq_b_scale;
const eq_b_h = EQ.update_batch.h * eq_b_scale;
s.addImage({
  path: BUILD + "/eq_update_batch.png",
  x: panel3_x + 0.2 + (green_box_w - eq_b_w) / 2, y: green_box_y + (green_box_h - eq_b_h) / 2, 
  w: eq_b_w, h: eq_b_h,
});

// Center caption and arrow
s.addText("Update after each sample", {
  x: panel3_x + 0.2 + green_box_w + 0.05, y: green_box_y + 0.08, w: gap, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 11, color: RED, fontFace: FONT, margin: 0,
});
s.addShape(pres.shapes.LINE, {
  x: panel3_x + 0.2 + green_box_w + 0.05 + gap - 0.05, y: green_box_y + 0.45,
  w: -(gap - 0.1), h: 0,
  line: { color: RED, width: 2, endArrowType: "triangle" },
});

// Right green box: online update as 2D PNG
const right_box_x = panel3_x + 0.2 + green_box_w + gap + 0.1;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: right_box_x, y: green_box_y, w: green_box_w, h: green_box_h,
  fill: { color: LIGHT_GREEN }, line: { color: GREEN, width: 1.5 },
});
const eq_o_scale = Math.min(0.62, (green_box_w - 0.2) / EQ.update_online.w);
const eq_o_w = EQ.update_online.w * eq_o_scale;
const eq_o_h = EQ.update_online.h * eq_o_scale;
s.addImage({
  path: BUILD + "/eq_update_online.png",
  x: right_box_x + (green_box_w - eq_o_w) / 2, y: green_box_y + (green_box_h - eq_o_h) / 2,
  w: eq_o_w, h: eq_o_h,
});

pres.writeFile({ 
  fileName: BUILD + "/slide_004_recreated.pptx" 
}).then(() => console.log("wrote slide_004_recreated.pptx"));