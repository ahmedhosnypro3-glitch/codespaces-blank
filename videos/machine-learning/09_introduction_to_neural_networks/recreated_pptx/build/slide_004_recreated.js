const pptxgen = require("pptxgenjs");

// Slide 004: Problem Formulation
// Original panel measurements (from PIL analysis of 960x540 @ 72dpi):
// House frame: x=1.097in, y=0.597in from image top-left
// Panel 1: y=1.43in to 2.79in (height 1.36in), x=1.097in to 9.19in
// Panel 2: y=3.04in to 4.54in (height 1.50in), x=1.097in to 9.19in  
// Panel 3: y=4.65in to 7.08in (height 2.43in), x=1.097in to 9.19in
// For recreation: house frame at 0.15in inset, panels at x=0.6, w=12.13
// Panel positions relative to house frame (0.15, 0.15):
// Panel 1: y = 1.43 - 0.597 + 0.15 = 0.983in -> use 0.98
// Panel 2: y = 3.04 - 0.597 + 0.15 = 2.593in -> use 2.60
// Panel 3: y = 4.65 - 0.597 + 0.15 = 4.203in -> use 4.20

const NUM = 4;
const TITLE = "Problem Formulation";
const FONT = "Arial";

const BG = "E8E8E8";
const BORDER_RED = "8B0000";
const BLACK = "000000";
const RED = "FF0000";
const DARK_RED = "C00000";
const GREEN = "00B050";
const BLUE = "0000FF";
const PEACH = "FDEADA";
const LIGHT_GREEN = "E2EFDA";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Bottom black bar - video player overlay
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
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 4. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
});

// Panel common: x=0.6, w=12.13 (house frame content area)
const PANEL_X = 0.6;
const PANEL_W = 12.13;

// ============================================================
// PANEL 1: Define δᵢ (y=0.98, height=1.36)
// ============================================================
const P1_Y = 0.98;
const P1_H = 1.36;

// Panel 1 background - white with red square-cornered border
s.addShape(pres.shapes.RECTANGLE, {
  x: PANEL_X, y: P1_Y, w: PANEL_W, h: P1_H,
  fill: { color: WHITE },
  line: { color: DARK_RED, width: 1.5 },
});

// Panel 1 heading
s.addText([
  { text: "Define ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "δᵢ", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " as:", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
], {
  x: PANEL_X + 0.1, y: P1_Y + 0.08, w: PANEL_W - 0.2, h: 0.3,
  align: "left", valign: "top", margin: 0,
});

// Line 1 - larger font to fill panel
s.addText([
  { text: "If X ∈ ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "class I", options: { color: RED, bold: true, italic: true, fontSize: 16, fontFace: FONT } },
  { text: " and misclassified as ", options: { color: BLACK, italic: true, fontSize: 16, fontFace: FONT } },
  { text: "Class II", options: { color: BLUE, bold: true, italic: true, fontSize: 16, fontFace: FONT } },
  { text: " then d(X) will be ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "<0", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " ⇒ ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "δᵢ", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " = -1", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: " ⇒ ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, italic: true, fontSize: 16, fontFace: FONT } },
  { text: "δᵢ", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " >0", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
], {
  x: PANEL_X + 0.1, y: P1_Y + 0.3, w: PANEL_W - 0.2, h: 0.45,
  align: "left", valign: "top", margin: 0,
});

// Line 2 - larger font
s.addText([
  { text: "If X ∈ ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "class II", options: { color: BLUE, bold: true, italic: true, fontSize: 16, fontFace: FONT } },
  { text: " and misclassified as ", options: { color: BLACK, italic: true, fontSize: 16, fontFace: FONT } },
  { text: "Class I", options: { color: RED, bold: true, italic: true, fontSize: 16, fontFace: FONT } },
  { text: " then d(X) will be ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: ">0", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " ⇒ ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "δᵢ", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " = +1", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: " ⇒ ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, italic: true, fontSize: 16, fontFace: FONT } },
  { text: "δᵢ", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " >0", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
], {
  x: PANEL_X + 0.1, y: P1_Y + 0.75, w: PANEL_W - 0.2, h: 0.45,
  align: "left", valign: "top", margin: 0,
});

// ============================================================
// PANEL 2: Redefine Error function (y=2.60, height=1.50)
// ============================================================
const P2_Y = 2.60;
const P2_H = 1.50;

// Panel 2 background - white with red rounded border
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: PANEL_X, y: P2_Y, w: PANEL_W, h: P2_H,
  fill: { color: WHITE },
  line: { color: DARK_RED, width: 1.5 },
});

// Panel 2 heading
s.addText("Redefine Error function as:", {
  x: PANEL_X + 0.1, y: P2_Y + 0.08, w: PANEL_W - 0.2, h: 0.3,
  align: "left", valign: "top",
  fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Equation: Error = Σ δᵢ WᵀXᵢ with subscript "all misclassified vectors (i)"
s.addImage({
  path: "equations_slide004/eq4_error.png",
  x: PANEL_X + 0.1, y: P2_Y + 0.25, w: 2.17667, h: 0.385,
});

// Subscript "all misclassified vectors (i)" in small red italic under sigma
s.addText("all misclassified vectors (i)", {
  x: PANEL_X + 0.3, y: P2_Y + 0.65, w: 2.5, h: 0.2,
  align: "center", valign: "top",
  fontSize: 10, italic: true, color: RED, fontFace: FONT, margin: 0,
});

// Explanation text - larger
s.addText("(WᵀXᵢ) takes positive and negative values and δᵢ has the same sign", {
  x: PANEL_X + 2.5, y: P2_Y + 0.28, w: PANEL_W - 2.6, h: 0.35,
  align: "left", valign: "top",
  fontSize: 16, italic: true, color: BLACK, fontFace: FONT, margin: 0,
});

// "Summation is always positive" - larger
s.addText([
  { text: "Summation is always ", options: { color: BLACK, italic: true, fontSize: 16, fontFace: FONT } },
  { text: "positive", options: { color: RED, bold: true, italic: true, fontSize: 16, fontFace: FONT } },
], {
  x: PANEL_X + 0.1, y: P2_Y + 1.1, w: PANEL_W - 0.2, h: 0.25,
  align: "left", valign: "top", margin: 0,
});

// ============================================================
// PANEL 3: Gradient Descent Update (y=4.20, height=2.43)
// ============================================================
const P3_Y = 4.20;
const P3_H = 2.43;

// Panel 3 background - peach with red rounded border
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: PANEL_X, y: P3_Y, w: PANEL_W, h: P3_H,
  fill: { color: PEACH },
  line: { color: DARK_RED, width: 1.5 },
});

// Heading: Minimize the Error using Gradient Descent with step η
// "Minimize the Error using" is underlined, rest is not
s.addText([
  { text: "Minimize the Error using", options: { color: BLACK, italic: true, underline: true, fontSize: 16, fontFace: FONT } },
  { text: " Gradient Descent", options: { color: RED, bold: true, italic: true, fontSize: 16, fontFace: FONT } },
  { text: " with step ", options: { color: BLACK, italic: true, fontSize: 16, fontFace: FONT } },
  { text: "η", options: { color: RED, bold: true, italic: true, fontSize: 16, fontFace: FONT } },
], {
  x: PANEL_X + 0.1, y: P3_Y + 0.08, w: PANEL_W - 0.2, h: 0.35,
  align: "left", valign: "top", margin: 0,
});

// Equation 1: W^(updated) = W^old - η ∂Error/∂W where ∂Error/∂W = Σ δᵢ Xᵢ
// Place both equations on same line with "where" inline
s.addImage({
  path: "equations_slide004/eq7_update1.png",
  x: PANEL_X + 0.1, y: P3_Y + 0.45, w: 3.15667, h: 0.39167,
});

// "where" bold black - INLINE after first equation
s.addText("where", {
  x: PANEL_X + 3.4, y: P3_Y + 0.5, w: 0.7, h: 0.3,
  align: "left", valign: "top",
  fontSize: 14, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Equation 2: ∂Error/∂W = Σ δᵢ Xᵢ (with subscript "misclassified vectors")
s.addImage({
  path: "equations_slide004/eq8_gradient.png",
  x: PANEL_X + 4.1, y: P3_Y + 0.5, w: 1.53167, h: 0.37167,
});

// Subscript "misclassified vectors" in small red italic
s.addText("misclassified vectors", {
  x: PANEL_X + 4.3, y: P3_Y + 0.9, w: 2.0, h: 0.2,
  align: "center", valign: "top",
  fontSize: 10, italic: true, color: RED, fontFace: FONT, margin: 0,
});

// ============================================================
// BOTTOM ROW: Two green boxes with caption and arrow
// ============================================================
// Green boxes should be fully INSIDE panel 3
const GREEN_Y = P3_Y + 1.5;
const GREEN_H = 0.7;  // Tighter fit
const GREEN_W = (PANEL_W - 1.2) / 2; // With wider gap

// Left green box - fully inside panel
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: PANEL_X + 0.15, y: GREEN_Y, w: GREEN_W, h: GREEN_H,
  fill: { color: LIGHT_GREEN },
  line: { color: GREEN, width: 1.5 },
});
s.addImage({
  path: "equations_slide004/eq9_update2.png",
  x: PANEL_X + 0.2, y: GREEN_Y + 0.05, w: 2.97833, h: 0.34833,
});
// Subscript "misclassified vectors ONLY (i)" in small red italic
s.addText("misclassified vectors ONLY (i)", {
  x: PANEL_X + 0.2, y: GREEN_Y + 0.4, w: GREEN_W - 0.1, h: 0.2,
  align: "center", valign: "top",
  fontSize: 10, italic: true, color: RED, fontFace: FONT, margin: 0,
});

// Center caption and arrow
const CAPTION_X = PANEL_X + 0.15 + GREEN_W + 0.05;
const CAPTION_W = 1.0;
s.addText("Update after each sample", {
  x: CAPTION_X, y: GREEN_Y + 0.1, w: CAPTION_W, h: 0.4,
  align: "center", valign: "middle",
  fontSize: 12, bold: false, color: RED, fontFace: FONT, margin: 0,
});
// Arrow pointing left - LINE with endArrow
s.addShape(pres.shapes.LINE, {
  x: CAPTION_X + CAPTION_W / 2 + 0.1, y: GREEN_Y + 0.3, w: -0.2, h: 0,
  line: { color: RED, width: 2, endArrow: "triangle", endArrowSize: "med" },
});

// Right green box - fully inside panel
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: CAPTION_X + CAPTION_W + 0.05, y: GREEN_Y, w: GREEN_W, h: GREEN_H,
  fill: { color: LIGHT_GREEN },
  line: { color: GREEN, width: 1.5 },
});
s.addImage({
  path: "equations_slide004/eq10_update3.png",
  x: CAPTION_X + CAPTION_W + 0.15, y: GREEN_Y + 0.05, w: 2.73833, h: 0.315,
});

// Write output
const outputPath = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/slide_004_recreated.pptx";
pres.writeFile({ fileName: outputPath }).then(() => console.log("wrote " + outputPath)).catch(e => console.error(e));

// Debug: check images were added
setTimeout(() => {
  const zip = require('adm-zip');
  const pptx = new zip(outputPath);
  const slideXml = pptx.readAsText('ppt/slides/slide1.xml');
  console.log('Has a:pic:', slideXml.includes('a:pic') || slideXml.includes('p:pic'));
  const blips = slideXml.match(/<a:blip[^>]*r:embed="([^"]+)"[^>]*>/g);
  console.log('Image embeds:', blips);
}, 1000);