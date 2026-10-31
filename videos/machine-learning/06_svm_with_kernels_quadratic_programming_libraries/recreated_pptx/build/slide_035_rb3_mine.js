// slide_035.js — REBUILD WAVE 3 (fix 2), built ONLY from qa/reanalysis2/slide_035_analysis.txt
// "How to Kernelize SVM": upper SVM panel, middle Remember panel, lower kernelized panel.
// Fix 2: Latin math glyphs rendered \mathbf (upright bold) so w/b/W/X are unambiguous.
// Build from project root: node <NS>/recreated_pptx/build/slide_035.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_035/");
const W = 13.33, H = 7.5;
const FONT = "Arial", MATH = "Times New Roman";

// normalized [x0,y0,x1,y1] -> inches
const R = (x0, y0, x1, y1) => ({ x: x0 * 13.33, y: y0 * 7.5, w: (x1 - x0) * 13.33, h: (y1 - y0) * 7.5 });

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (overrides spec): red frame, badge, title
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("35", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("How to Kernelize SVM", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Three panels: upper cream, middle white, lower cream (thin blue borders)
const pU = R(0.071, 0.137, 0.875, 0.387);
const pM = R(0.071, 0.394, 0.875, 0.580);
const pL = R(0.071, 0.589, 0.875, 0.837);
s.addShape(pres.shapes.RECTANGLE, { ...pU, fill: { color: "F7F7DE" }, line: { color: "0000FF", width: 1 } });
s.addShape(pres.shapes.RECTANGLE, { ...pM, fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 } });
s.addShape(pres.shapes.RECTANGLE, { ...pL, fill: { color: "F7F7DE" }, line: { color: "0000FF", width: 1 } });

// White blue-bordered boxes holding w and b equations (upper + lower)
const wB_U = R(0.090, 0.228, 0.240, 0.311), bB_U = R(0.347, 0.226, 0.736, 0.313);
const wB_L = R(0.090, 0.680, 0.240, 0.763), bB_L = R(0.347, 0.676, 0.736, 0.763);
for (const b of [wB_U, bB_U, wB_L, bB_L]) {
  s.addShape(pres.shapes.RECTANGLE, { ...b, fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 } });
}

// Peach callout boxes (upper + lower)
const cU = R(0.125, 0.324, 0.486, 0.376), cL = R(0.125, 0.774, 0.486, 0.830);
for (const c of [cU, cL]) {
  s.addShape(pres.shapes.RECTANGLE, { ...c, fill: { color: "FBE5D6" }, line: { color: "E8A87C", width: 1 } });
}
// Green highlight ovals (lower panel) — AFTER boxes/callouts, BEFORE equations/text
const lagU = R(0.098, 0.157, 0.439, 0.233), lagLbox = R(0.098, 0.611, 0.454, 0.689);
const LAG_U = { w: 2.95333, h: 0.54833 }, LAG_L = { w: 3.00667, h: 0.55667 };
const WIMG = { w: 1.235, h: 0.55333 }, B_U = { w: 4.46, h: 0.54333 }, B_L = { w: 4.82167, h: 0.54667 };
const lagLimgY = 4.5825 + (0.585 - LAG_L.h) / 2;
const bLimgX = bB_L.x + (bB_L.w - B_L.w) / 2, bLimgY = bB_L.y + (bB_L.h - B_L.h) / 2;
const ovals = [
  R(0.401, 0.617, 0.454, 0.683),  // around x_i^T x_j tail of lower Lagrangian
  R(0.521, 0.700, 0.576, 0.752),  // around first W^T X_i in lower b
  R(0.667, 0.700, 0.723, 0.752),  // around second W^T X_i in lower b
  R(0.388, 0.778, 0.431, 0.826),  // around W^T Z in lower callout
];
// oval 1 hugs the actual rendered tail of the lower Lagrangian image
ovals[0].w = 0.62;
ovals[0].x = lagLbox.x + LAG_L.w - ovals[0].w - 0.03;
ovals[0].y = lagLimgY + (LAG_L.h - ovals[0].h) / 2;
ovals[1].y = bLimgY + (B_L.h - ovals[1].h) / 2;
ovals[2].y = bLimgY + (B_L.h - ovals[2].h) / 2;
for (const o of ovals) {
  s.addShape(pres.shapes.OVAL, { x: o.x, y: o.y, w: o.w, h: o.h, fill: { color: "A6F3A6" }, line: { color: "2E9E2E", width: 1 } });
}

// Equation images at exact rendered size (w = px/600 in, never rescaled)
const img = (f, x, y, w, h) => s.addImage({ path: EQ + f, x, y, w, h });
img("rb2_lag_upper.png", lagU.x, lagU.y + (lagU.h - LAG_U.h) / 2, LAG_U.w, LAG_U.h);
img("rb2_lag_lower.png", lagLbox.x, lagLimgY, LAG_L.w, LAG_L.h);
img("rb2_w.png", wB_U.x + (wB_U.w - WIMG.w) / 2, wB_U.y + (wB_U.h - WIMG.h) / 2, WIMG.w, WIMG.h);
img("rb2_w.png", wB_L.x + (wB_L.w - WIMG.w) / 2, wB_L.y + (wB_L.h - WIMG.h) / 2, WIMG.w, WIMG.h);
img("rb2_b_upper.png", bB_U.x + (bB_U.w - B_U.w) / 2, bB_U.y + (bB_U.h - B_U.h) / 2, B_U.w, B_U.h);
img("rb2_b_lower.png", bLimgX, bLimgY, B_L.w, B_L.h);
const idb = R(0.281, 0.467, 0.590, 0.515);
img("rb2_ident.png", idb.x + (idb.w - 2.375) / 2, idb.y + (idb.h - 0.33833) / 2, 2.375, 0.33833);
// Middle panel: "Remember :" header (blue bold italic)
s.addText("Remember :", {
  x: 1.07973, y: 2.98, w: 3.0, h: 0.24, align: "left", valign: "middle",
  fontSize: 12, bold: true, italic: true, color: "0000FF", fontFace: FONT, margin: 0,
});

// Mapping line (verbatim): Mapping Instead of using X_i (of dimension d) use φ(X_i) (with higher dimension )
s.addText([
  { text: "Mapping", options: { fontSize: 13, bold: true, italic: true, color: "FF0000", fontFace: FONT, margin: 0 } },
  { text: " Instead of using ", options: { fontSize: 12, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "X", options: { fontSize: 12, bold: true, color: "0000FF", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, bold: true, color: "0000FF", fontFace: MATH, subscript: true, margin: 0 } },
  { text: " (of dimension ", options: { fontSize: 12, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "d", options: { fontSize: 12, bold: true, italic: true, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: ") use ", options: { fontSize: 12, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "φ(X", options: { fontSize: 12, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, color: "FF0000", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ") (with higher dimension )", options: { fontSize: 12, italic: true, color: "FF0000", fontFace: FONT, margin: 0 } },
], { x: 1.07973, y: 3.2475, w: 8.34258, h: 0.24, align: "left", valign: "middle", margin: 0 });
// Kernelization line (verbatim): Kernelization Instead of using φ(X_i), φ(X_j) use K(X_i^T, X_j^T) (Where K is one of kernel functions)
s.addText([
  { text: "Kernelization", options: { fontSize: 13, bold: true, italic: true, color: "FF0000", fontFace: FONT, margin: 0 } },
  { text: " Instead of using ", options: { fontSize: 12, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "φ(X", options: { fontSize: 12, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, color: "FF0000", fontFace: MATH, subscript: true, margin: 0 } },
  { text: "), φ(X", options: { fontSize: 12, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: "j", options: { fontSize: 12, color: "FF0000", fontFace: MATH, subscript: true, margin: 0 } },
  { text: ") use ", options: { fontSize: 12, color: "000000", fontFace: FONT, margin: 0 } },
  { text: "K(X", options: { fontSize: 12, bold: true, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: "i", options: { fontSize: 12, bold: true, color: "FF0000", fontFace: MATH, subscript: true, margin: 0 } },
  { text: "T", options: { fontSize: 12, bold: true, color: "FF0000", fontFace: MATH, superscript: true, margin: 0 } },
  { text: ", X", options: { fontSize: 12, bold: true, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: "j", options: { fontSize: 12, bold: true, color: "FF0000", fontFace: MATH, subscript: true, margin: 0 } },
  { text: "T", options: { fontSize: 12, bold: true, color: "FF0000", fontFace: MATH, superscript: true, margin: 0 } },
  { text: ")", options: { fontSize: 12, bold: true, color: "FF0000", fontFace: MATH, margin: 0 } },
  { text: " (Where ", options: { fontSize: 12, italic: true, color: "0000FF", fontFace: FONT, margin: 0 } },
  { text: "K", options: { fontSize: 12, italic: true, color: "0000FF", fontFace: MATH, margin: 0 } },
  { text: " is one of kernel functions)", options: { fontSize: 12, italic: true, color: "0000FF", fontFace: FONT, margin: 0 } },
], { x: 1.07973, y: 3.99, w: 9.76024, h: 0.24, align: "left", valign: "middle", margin: 0 });
// Callout texts: "Class of vector Z ⇒ sign(W^T Z + b)" (upper: black/green/red/blue; lower: red/black)
const callout = (c, runs) => s.addText(runs, {
  x: c.x, y: c.y, w: c.w, h: c.h, align: "center", valign: "middle", margin: 0,
});
callout(cU, [
  { text: "Class of vector ", options: { fontSize: 13, color: "000000", fontFace: MATH } },
  { text: "Z", options: { fontSize: 13, bold: true, color: "2E9E2E", fontFace: MATH } },
  { text: " ⇒ ", options: { fontSize: 13, color: "FF0000", fontFace: MATH } },
  { text: "sign(", options: { fontSize: 13, italic: true, color: "FF0000", fontFace: MATH } },
  { text: "W", options: { fontSize: 13, color: "0000FF", fontFace: MATH } },
  { text: "T", options: { fontSize: 13, color: "0000FF", fontFace: MATH, superscript: true } },
  { text: " Z + b)", options: { fontSize: 13, color: "0000FF", fontFace: MATH } },
]);
callout(cL, [
  { text: "Class of vector ", options: { fontSize: 13, color: "FF0000", fontFace: MATH } },
  { text: "Z", options: { fontSize: 13, bold: true, color: "FF0000", fontFace: MATH } },
  { text: " ⇒ ", options: { fontSize: 13, color: "FF0000", fontFace: MATH } },
  { text: "sign(", options: { fontSize: 13, italic: true, color: "000000", fontFace: MATH } },
  { text: "W", options: { fontSize: 13, color: "000000", fontFace: MATH } },
  { text: "T", options: { fontSize: 13, color: "000000", fontFace: MATH, superscript: true } },
  { text: " Z + b)", options: { fontSize: 13, color: "000000", fontFace: MATH } },
]);

// Faint gray hairline near top-right edge
const hl = R(0.860, 0.060, 0.925, 0.070);
s.addShape(pres.shapes.RECTANGLE, { x: hl.x, y: hl.y + hl.h / 2, w: hl.w, h: 0.02, fill: { color: "D9D9D9" }, line: { type: "none" } });

// Mouse-pointer cursor over the lower b equation
const cur = R(0.590, 0.715, 0.606, 0.748);
s.addShape(pres.shapes.ISOSCELES_TRIANGLE, { x: cur.x, y: cur.y, w: cur.w, h: cur.h, fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 } });

// Black overlay strip along the bottom-left edge of the capture
const blk = R(0.042, 0.856, 0.500, 1.000);
s.addShape(pres.shapes.RECTANGLE, { ...blk, fill: { color: "000000" }, line: { type: "none" } });

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_035_recreated.pptx") })
  .then(() => console.log("wrote slide_035_recreated.pptx"))
  .catch(err => console.error(err));
