const pptxgen = require("pptxgenjs");

// Slide 018 — Precision and Recall of Multi-class classification
// Geometry PIL-measured from unique_slides/slide_018.jpg (960x540, 1px = 1pt = 1/72in).
// Text face measured condensed (width/cap-height consistent with Arial Narrow).

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const BADGE_Y = "FFF9C4";
const DARK = "333333";
const BLACK = "000000";
const BLUE = "0000FF";
const NARROW = "Arial Narrow";
const A = "videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/";

// measured table palette (spec hexes were qualitatively wrong here)
const PANEL_FILL = "EEFFF4";   // 238,255,244 measured interior
const PANEL_LINE = "469546";   // saturated green border
const BAND = "F2AF6A";         // highlighter band composite over green
const STRIP = "FFFF00";        // bright stroke over digits

let s = pptx.addSlide();
s.background = { color: BG };

// ---------------- HOUSE CHROME (overrides spec + judge) ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_Y }, line: { color: BADGE_Y, width: 0.5 },
});
s.addText("18", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: "Arial", margin: 0,
});
s.addText("Precision and Recall of Multi-class classification", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: RED, fontFace: NARROW, margin: 0,
});

// ---------------- CONFUSION MATRIX PANEL (green border, pale green) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.2361, y: 1.5694, w: 4.8056, h: 2.7361,
  fill: { color: PANEL_FILL }, line: { color: PANEL_LINE, width: 2 },
});

s.addText("Predicted as", {
  x: 2.8861, y: 1.614, w: 2.2, h: 0.30,
  align: "center", valign: "middle", margin: 0,
  fontSize: 18, bold: true, color: BLACK, fontFace: NARROW, lineSpacing: 18,
});
s.addText("(Positive Class)", {
  x: 2.8861, y: 1.875, w: 2.2, h: 0.26,
  align: "center", valign: "middle", margin: 0,
  fontSize: 15, color: BLACK, fontFace: NARROW, lineSpacing: 15,
});

// rotated row label "Actual" (ink x96-108, y217-264)
s.addText("Actual", {
  x: 1.0832, y: 3.2203, w: 0.667, h: 0.24,
  rotate: 270, align: "center", valign: "middle", margin: 0,
  fontSize: 19, bold: true, color: BLACK, fontFace: NARROW,
});

s.addText("Confusion Matrix", {
  x: 6.2083, y: 2.8517, w: 2.36, h: 0.38,
  align: "left", valign: "middle", margin: 0,
  fontSize: 21, color: BLUE, fontFace: NARROW,
});

// ---------------- TABLE GRID (red rules; x115-420, y158-299) -----------
function tc(t, extra) {
  return Object.assign({
    text: t, options: {
      fontSize: 19, fontFace: NARROW, color: BLACK,
      align: "center", valign: "middle",
      fill: { color: PANEL_FILL }, margin: 0,
    },
  }, extra || {});
}
let tableData = [
  [tc(""), tc("Dog"), tc("Cat"), tc("Fish"), tc("Total")],
  [tc("Dog"), tc("5"), tc("2"), tc("1"), tc("8")],
  [tc("Cat"), tc("4"), tc("6"), tc("1"), tc("11")],
  [tc("Fish"), tc("7"), tc("0"), tc("0"), tc("7")],
];
s.addTable(tableData, {
  x: 1.5972, y: 2.1944,
  colW: [0.875, 0.9167, 0.8889, 0.7917, 0.7639],
  rowH: [0.5, 0.5, 0.4583, 0.5],
  fontSize: 19, fontFace: NARROW, color: BLACK,
  border: [{ type: "solid", color: RED, width: 1.5 }],
});

// ---------------- YELLOW HIGHLIGHTER ANNOTATION (measured in original) --
// Translator's marker: translucent band across the Dog row + bright stroke
// down the Dog-column digits. Reproduced as translucent overlays on top of
// the table so the digits stay visible (they read as olive in the original).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 2.6806, y: 2.8194, w: 2.3889, h: 0.2639,
  fill: { color: BAND, transparency: 50 }, line: { type: "none" },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: 2.8194, y: 2.8194, w: 0.2222, h: 1.2083,
  fill: { color: STRIP, transparency: 72 }, line: { type: "none" },
});

// ---------------- BOTTOM COLUMNS (DOG / CAT / FISH) ---------------------
// measured: col x = 78-327, 358-607, 627-876 (w 249px); header box y321-374,
// precision box y388-427, recall box y442-472. Header text is two lines
// ("Precision and Recall" / "of <X> Class"), dark red; formulas dark red.
const LAV = "EDE7F6";
const YEL = "FFF2CC";
const ORA = "FCE4D6";
const cols = [
  { x: 1.0833, cls: "DOG",  p: "eq_018_p1_18pt", r: "eq_018_r1_18pt" },
  { x: 4.9722, cls: "CAT",  p: "eq_018_p2_18pt", r: "eq_018_r2_18pt" },
  { x: 8.7083, cls: "FISH", p: "eq_018_p3_18pt", r: "eq_018_r3_18pt" },
];
// equation PNG sidecars (600dpi, px/600 = inches)
const EQ = {
  "eq_018_p1_18pt": { w: 2.79167, h: 0.33667, bl: 0.68317 },
  "eq_018_r1_18pt": { w: 2.31167, h: 0.33667, bl: 0.68317 },
  "eq_018_p2_18pt": { w: 2.68,    h: 0.34,    bl: 0.68627 },
  "eq_018_r2_18pt": { w: 2.42167, h: 0.34,    bl: 0.68627 },
  "eq_018_p3_18pt": { w: 2.695,   h: 0.34,    bl: 0.68627 },
  "eq_018_r3_18pt": { w: 2.32833, h: 0.34,    bl: 0.68627 },
};
const INK_X = [1.1944, 5.0972, 8.8194];   // measured formula ink left edges
const BASE_P = 5.681;   // precision formula baseline (409px)
const BASE_R = 6.444;   // recall formula baseline (464px)

cols.forEach((c, i) => {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: c.x, y: 4.4583, w: 3.4583, h: 0.7361,
    fill: { color: LAV }, line: { type: "none" }, rectRadius: 0.06,
  });
  s.addText([
    { text: "Precision and Recall", options: { breakLine: true } },
    { text: "of " + c.cls + " Class" },
  ], {
    x: c.x, y: 4.4583, w: 3.4583, h: 0.7361,
    align: "center", valign: "middle", margin: 0,
    fontSize: 21, bold: true, color: RED, fontFace: NARROW, lineSpacing: 24,
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: c.x, y: 5.3889, w: 3.4583, h: 0.5417,
    fill: { color: YEL }, line: { type: "none" },
  });
  s.addShape(pptx.shapes.RECTANGLE, {
    x: c.x, y: 6.1389, w: 3.4583, h: 0.4167,
    fill: { color: ORA }, line: { type: "none" },
  });
  const pe = EQ[c.p], re = EQ[c.r];
  s.addImage({ path: A + c.p + ".png", x: INK_X[i], y: BASE_P - pe.bl * pe.h, w: pe.w, h: pe.h });
  s.addImage({ path: A + c.r + ".png", x: INK_X[i], y: BASE_R - re.bl * re.h, w: re.w, h: re.h });
});

pptx.writeFile({ fileName: "videos/machine-learning/08_performance_measure/recreated_pptx/slide_018_recreated.pptx" })
  .then((f) => console.log("wrote " + f));
