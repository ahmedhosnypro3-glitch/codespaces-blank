const pptxgen = require("pptxgenjs");

// Slide 019: Sigmoid, tanh, tan, and arctan Function Graphs
const NUM = 19;
const TITLE = "Sigmoid, tanh, tan, and tan\u207B\u00B9 Function Graphs";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE_BORDER = "0000CC";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const PEACH = "FCE4D6";
const PEACH_BORDER = "E6B8A2";
const GRAY = "D9D9D9";
const GRAY_BORDER = "A6A6A6";
const DARK_GRAY = "404040";
const LIGHT_GRAY = "BFBFBF";
const RED_CURVE = "E06666";

// Equation sizes from render_eq.py output
const EQ = {
  sigmoid: { w_in: 3.31167, h_in: 0.59, baseline_frac: 0.64689 },
  tanh:    { w_in: 2.75167, h_in: 0.595, baseline_frac: 0.65546 },
  tan:     { w_in: 1.47833, h_in: 0.24833, baseline_frac: 0.81208 },
  arctan:  { w_in: 1.74667, h_in: 0.29167, baseline_frac: 0.84 },
};

// Graph panel positions and sizes (inches, measured from 960x540 frame: 1px = 1pt = 1/72in)
// Panel specs from vision analysis:
// top-left (sigmoid):    x=11%-43%, y=11%-44% -> x=[0.15,0.57], y=[0.08,0.33] of 13.33x7.5
// top-right (tanh):      x=52%-84%, y=11%-44% -> x=[0.69,1.12], y=[0.08,0.33]
// bottom-left (tan):     x=11%-43%, y=55%-88% -> x=[0.15,0.57], y=[0.41,0.66]
// bottom-right (arctan): x=52%-84%, y=55%-88% -> x=[0.69,1.12], y=[0.41,0.66]
// House frame inset: 0.15in from edges. Inner content area: x=[0.15,13.18], y=[0.15,7.35]
// Scale percentages to inner area: 13.33-0.3=13.03 wide, 7.5-0.3=7.2 tall
// x% = 0.15 + x% * 13.03, y% = 0.15 + y% * 7.2

const PANEL_W = 4.17;  // ~32% of 13.03
const PANEL_H = 2.38;  // ~33% of 7.2
const PANEL_GAP_X = 0.25;
const PANEL_GAP_Y = 0.25;

const PANEL_TL = { x: 0.15 + 0.11 * 13.03, y: 0.15 + 0.11 * 7.2, w: PANEL_W, h: PANEL_H };
const PANEL_TR = { x: 0.15 + 0.52 * 13.03, y: 0.15 + 0.11 * 7.2, w: PANEL_W, h: PANEL_H };
const PANEL_BL = { x: 0.15 + 0.11 * 13.03, y: 0.15 + 0.55 * 7.2, w: PANEL_W, h: PANEL_H };
const PANEL_BR = { x: 0.15 + 0.52 * 13.03, y: 0.15 + 0.55 * 7.2, w: PANEL_W, h: PANEL_H };

const CAPTION_H = 0.45;
const CAPTION_GAP = 0.10;
const ARROW_Y = PANEL_BL.y + PANEL_H / 2;  // vertically centered on bottom row

const BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const GRAPH_DIR = BUILD_DIR + "/graphs_slide_019";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. Bottom black bar (video player overlay artifact in original)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { color: "none" },
});

// 3. Slide-number badge - HOUSE CHROME LAW (yellow oval at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// 4. Title - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
// The source slide has no title; we add the inferred title per validation
// Use a smaller font since it's not original content
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 20, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 5. Four graph panels with blue borders
const panelStyle = {
  fill: { color: GRAY }, line: { color: BLUE_BORDER, width: 1.5 },
};

s.addShape(pres.shapes.RECTANGLE, { ...panelStyle, ...PANEL_TL });
s.addShape(pres.shapes.RECTANGLE, { ...panelStyle, ...PANEL_TR });
s.addShape(pres.shapes.RECTANGLE, { ...panelStyle, ...PANEL_BL });
s.addShape(pres.shapes.RECTANGLE, { ...panelStyle, ...PANEL_BR });

// 6. Embed generated graph PNGs inside panels (exact panel size)
s.addImage({ path: GRAPH_DIR + "/graph_sigmoid.png", ...PANEL_TL });
s.addImage({ path: GRAPH_DIR + "/graph_tanh.png", ...PANEL_TR });
s.addImage({ path: GRAPH_DIR + "/graph_tan.png", ...PANEL_BL });
s.addImage({ path: GRAPH_DIR + "/graph_arctan.png", ...PANEL_BR });

// 7. Formula caption boxes below each panel
// Peach rounded rect for sigmoid, tanh, arctan; gray for tan
const captionPeach = {
  fill: { color: PEACH }, line: { color: PEACH_BORDER, width: 1 },
};
const captionGray = {
  fill: { color: GRAY }, line: { color: GRAY_BORDER, width: 1 },
};

const capW = PANEL_W * 0.85;
const capX_offset = PANEL_W * 0.075;

// Top-left caption (sigmoid)
const capTL_y = PANEL_TL.y + PANEL_H + CAPTION_GAP;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: PANEL_TL.x + capX_offset, y: capTL_y, w: capW, h: CAPTION_H,
  ...captionPeach,
});
s.addImage({
  path: BUILD_DIR + "/eq_sigmoid.png",
  x: PANEL_TL.x + capX_offset + (capW - EQ.sigmoid.w_in) / 2,
  y: capTL_y + (CAPTION_H - EQ.sigmoid.h_in) / 2,
  w: EQ.sigmoid.w_in, h: EQ.sigmoid.h_in,
});

// Top-right caption (tanh)
const capTR_y = PANEL_TR.y + PANEL_H + CAPTION_GAP;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: PANEL_TR.x + capX_offset, y: capTR_y, w: capW, h: CAPTION_H,
  ...captionPeach,
});
s.addImage({
  path: BUILD_DIR + "/eq_tanh.png",
  x: PANEL_TR.x + capX_offset + (capW - EQ.tanh.w_in) / 2,
  y: capTR_y + (CAPTION_H - EQ.tanh.h_in) / 2,
  w: EQ.tanh.w_in, h: EQ.tanh.h_in,
});

// Bottom-left caption (tan)
const capBL_y = PANEL_BL.y + PANEL_H + CAPTION_GAP;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: PANEL_BL.x + capX_offset, y: capBL_y, w: capW, h: CAPTION_H,
  ...captionGray,
});
s.addImage({
  path: BUILD_DIR + "/eq_tan.png",
  x: PANEL_BL.x + capX_offset + (capW - EQ.tan.w_in) / 2,
  y: capBL_y + (CAPTION_H - EQ.tan.h_in) / 2,
  w: EQ.tan.w_in, h: EQ.tan.h_in,
});

// Bottom-right caption (arctan)
const capBR_y = PANEL_BR.y + PANEL_H + CAPTION_GAP;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: PANEL_BR.x + capX_offset, y: capBR_y, w: capW, h: CAPTION_H,
  ...captionPeach,
});
s.addImage({
  path: BUILD_DIR + "/eq_arctan.png",
  x: PANEL_BR.x + capX_offset + (capW - EQ.arctan.w_in) / 2,
  y: capBR_y + (CAPTION_H - EQ.arctan.h_in) / 2,
  w: EQ.arctan.w_in, h: EQ.arctan.h_in,
});

// 8. Red hollow block arrow between bottom panels
const arrow_x = PANEL_BL.x + PANEL_W + PANEL_GAP_X / 2;
const arrow_y = ARROW_Y - 0.15;
const arrow_w = PANEL_GAP_X * 0.8;
const arrow_h = 0.3;
// Use a block arrow shape
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: arrow_x, y: arrow_y, w: arrow_w, h: arrow_h,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

// 9. In-plot title for arctan: "Inverse Tangent Graph" - native text positioned
// This goes inside the bottom-right panel, upper-left area
s.addText("Inverse Tangent Graph", {
  x: PANEL_BR.x + 0.1, y: PANEL_BR.y + 0.08, w: 2.0, h: 0.3,
  align: "left", valign: "top",
  fontSize: 8, color: DARK_GRAY, fontFace: FONT, margin: 0,
});

// 10. Legend for sigmoid panel: "sig(x) = 1/(1+e^-x)" in upper-left of panel
s.addText("sig(x) = 1/(1+e^-x)", {
  x: PANEL_TL.x + 0.15, y: PANEL_TL.y + 0.1, w: 2.0, h: 0.3,
  align: "left", valign: "top",
  fontSize: 8, color: RED_CURVE, fontFace: FONT, margin: 0,
});

// 11. Axis labels (small text, sans-serif)
// sigmoid y-axis label "sig(x)" at top of y-axis (left of panel)
s.addText("sig(x)", {
  x: PANEL_TL.x + 0.05, y: PANEL_TL.y + 0.05, w: 0.5, h: 0.2,
  align: "center", valign: "bottom",
  fontSize: 7, color: DARK_GRAY, fontFace: FONT, margin: 0,
  rotate: -90,
});
// tanh y-axis label "tanh x"
s.addText("tanh x", {
  x: PANEL_TR.x + 0.05, y: PANEL_TR.y + 0.05, w: 0.5, h: 0.2,
  align: "center", valign: "bottom",
  fontSize: 7, color: DARK_GRAY, fontFace: FONT, margin: 0,
  rotate: -90,
});
// tan y-axis label "tan x"
s.addText("tan x", {
  x: PANEL_BL.x + 0.05, y: PANEL_BL.y + 0.05, w: 0.5, h: 0.2,
  align: "center", valign: "bottom",
  fontSize: 7, color: DARK_GRAY, fontFace: FONT, margin: 0,
  rotate: -90,
});

// 12. X-axis tick labels for sigmoid: -8, -6, -4, -2, 2, 4, 6, 8
// These are small, placed below the panel (but inside the border in original)
// We'll place them as text on the panel bottom edge area
// Given the complexity and small size, these may be skipped as they're in the graph PNG
// The graph PNGs already have them rendered

// Write the pptx
const outPptx = BUILD_DIR + "/slide_019_recreated.pptx";
pres.writeFile({ fileName: outPptx }).then(() => console.log("wrote " + outPptx));