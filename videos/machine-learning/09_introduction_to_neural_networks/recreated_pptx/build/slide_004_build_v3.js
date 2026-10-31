const pptxgen = require("pptxgenjs");

// Slide 004 "Problem Formulation" — wave-4 rejudge rebuild.
// Geometry/fills re-measured from unique_slides/slide_004.jpg with PIL (see qa/slide004/REJUDGE_MEASUREMENTS.md).
const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const OUT = BUILD + "/slide_004_recreated.pptx";

const FONT = "Arial";
const BG = "E8E8E8";
const FRAME_RED = "C00000";
const RED = "FF0000";
const BLACK = "000000";
const GREEN = "00B050";
const BLUE = "0000FF";
const P2_FILL = "FEFFE8";   // cream  (measured mode 254,255,232)
const P3_FILL = "EADBC8";   // tan    (measured mode 234,219,200)
const MINT = "DFFFEE";      // left bottom box fill (measured mode 223,255,238)
const PALE_YELLOW = "F6FCB4"; // right bottom box fill (measured mode 246,252,182)
const BOX_GREEN = "5B8C3E"; // bottom box borders (measured ~8A9D59 blurred)

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// ---- house chrome (founder house rule, never tuned) ----
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3, fill: { type: "none" }, line: { color: FRAME_RED, width: 1.5 } });
s.addShape(pres.shapes.RECTANGLE, { x: 0.555, y: 7.18, w: 12.22, h: 0.32, fill: { color: BLACK } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText("4", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "4B0082", fontFace: FONT, margin: 0 });
s.addText("Problem Formulation", { x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "top", fontSize: 30, bold: true, color: FRAME_RED, fontFace: FONT, margin: 0 });

// ---- three stacked panels, all x 0.82..12.52, y per original ----
const PX = 0.82, PW = 11.70;
s.addShape(pres.shapes.RECTANGLE, { x: PX, y: 1.417, w: PW, h: 1.389, fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: PX, y: 3.042, w: PW, h: 1.514, fill: { color: P2_FILL }, line: { color: RED, width: 1.5 }, rectRadius: 0.05 });
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: PX, y: 4.889, w: PW, h: 2.278, fill: { color: P3_FILL }, line: { color: RED, width: 1.5 }, rectRadius: 0.05 });

const TX = 0.95; // panel 1/2 text left edge (measured text x 0.944)

// PANEL 1
s.addText([
  { text: "Define ", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 12, fontFace: FONT, subscript: true } },
  { text: " as:", options: { color: BLACK, bold: true, fontSize: 16, fontFace: FONT } },
], { x: TX, y: 1.53, w: PW - 0.3, h: 0.28, align: "left", valign: "top", margin: 0 });

s.addText([
  { text: "If X \u2208 ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "class I", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: " and ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "misclassified as ", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "Class II", options: { color: BLUE, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: " then ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true } },
  { text: " will be ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "<0", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " \u21D2 ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 12, fontFace: FONT, subscript: true } },
  { text: " = -1", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: " \u21D2 ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 12, fontFace: FONT, subscript: true } },
  { text: " >0", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
], { x: TX, y: 1.89, w: PW - 0.3, h: 0.3, align: "left", valign: "top", margin: 0 });

s.addText([
  { text: "If X \u2208 ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "class II", options: { color: BLUE, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: " and ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "misclassified as ", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "Class I", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: " then ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true } },
  { text: " will be ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: ">0", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT } },
  { text: " \u21D2 ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 12, fontFace: FONT, subscript: true } },
  { text: " = +1", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: " \u21D2 ", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
  { text: "d(X)", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "\u03B4", options: { color: GREEN, bold: true, fontSize: 16, fontFace: FONT, italic: true } },
  { text: "i", options: { color: GREEN, bold: true, fontSize: 12, fontFace: FONT, subscript: true } },
  { text: " >0", options: { color: BLACK, fontSize: 16, fontFace: FONT } },
], { x: TX, y: 2.24, w: PW - 0.3, h: 0.3, align: "left", valign: "top", margin: 0 });

// PANEL 2 - Redefine Error function (cream)
s.addText("Redefine Error function as:", { x: TX, y: 3.18, w: PW - 0.3, h: 0.3, align: "left", valign: "top", fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0 });
// Error equation: ink placed at x 1.14, y 3.51 (measured); PNG ink bbox (23,44)-(2977,430), scale 0.936
s.addImage({ path: BUILD + "/eq_error.png", x: 1.104, y: 3.441, w: 4.664, h: 0.740 });
s.addText("\u21D2 (W\u1D40X\u1D62) takes positive and negative values and \u03B4\u1D62 has the same sign",
  { x: 5.88, y: 3.52, w: 6.3, h: 0.5, align: "left", valign: "top", fontSize: 14, italic: true, color: BLACK, fontFace: FONT, margin: 0 });
s.addText([
  { text: "Summation is always ", options: { color: BLACK, fontSize: 14, fontFace: FONT, italic: true } },
  { text: "positive", options: { color: RED, bold: true, fontSize: 14, fontFace: FONT, italic: true } },
], { x: TX, y: 4.10, w: PW - 0.3, h: 0.3, align: "left", valign: "top", margin: 0 });

// PANEL 3 - Gradient descent update (tan)
s.addText([
  { text: "Minimize the Error using ", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true, underline: true } },
  { text: "Gradient Descent", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT, italic: true, underline: true } },
  { text: " with step ", options: { color: BLACK, fontSize: 16, fontFace: FONT, italic: true, underline: true } },
  { text: "\u03B7", options: { color: RED, bold: true, fontSize: 16, fontFace: FONT, italic: true, underline: true } },
], { x: 1.15, y: 4.86, w: 7.2, h: 0.3, align: "left", valign: "top", margin: 0 });

// Gradient-descent update equation: ink x 1.15, y 5.42 (measured); ink bbox (23,117)-(2291,357), scale 0.926
s.addImage({ path: BUILD + "/eq_gradient_descent.png", x: 1.114, y: 5.239, w: 3.563, h: 0.732 });
s.addText("where", { x: 4.90, y: 5.50, w: 1.55, h: 0.35, align: "center", valign: "top", fontSize: 16, bold: true, color: BLACK, fontFace: FONT, margin: 0 });
// Gradient equation: ink x 7.11, y 5.42 (measured); ink bbox (17,51)-(2286,422), scale 0.915
s.addImage({ path: BUILD + "/eq_gradient.png", x: 7.084, y: 5.342, w: 3.503, h: 0.723 });

// ---- bottom row: two boxes + caption + arrow (measured y 6.15..6.93) ----
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1.10, y: 6.15, w: 5.63, h: 0.78, fill: { color: MINT }, line: { color: BOX_GREEN, width: 1.5 }, rectRadius: 0.04 });
// batch update: ink x 1.17, y 6.29 (measured); ink bbox (23,44)-(4102,430), scale 0.544
s.addImage({ path: BUILD + "/eq_update_batch.png", x: 1.149, y: 6.250, w: 3.731, h: 0.430 });

// center caption (single line, red, centered in the gap at x 6.79..9.00)
s.addText("Update after each sample", { x: 6.70, y: 6.24, w: 2.25, h: 0.3, align: "center", valign: "middle", fontSize: 11, color: RED, fontFace: FONT, margin: 0 });
s.addText("\u25BC", { x: 6.70, y: 6.50, w: 2.25, h: 0.3, align: "center", valign: "top", fontSize: 11, color: BLACK, fontFace: FONT, margin: 0 });

s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.00, y: 6.15, w: 3.33, h: 0.78, fill: { color: PALE_YELLOW }, line: { color: BOX_GREEN, width: 1.5 }, rectRadius: 0.04 });
// online update: ink x 9.16, y 6.32 (measured); ink bbox (23,128)-(2214,340), scale 0.778
s.addImage({ path: BUILD + "/eq_update_online.png", x: 9.130, y: 6.209, w: 2.885, h: 0.614 });

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));

