const pptxgen = require("pptxgenjs");
const fs = require("fs");

const FONT = "Arial";
const NUM = 7;
const TITLE = "Neural Network Model";

// Colors
const BG = "F5E8D3";
const TITLE_COLOR = "C0392B";
const SUBTITLE_COLOR = "2980B9";
const FRAME_COLOR = "C00000";
const BADGE_FILL = "FFF9C4";
const BADGE_LINE = "FFF9C4";
const BADGE_TEXT = "333333";

// Eq sidecars (12pt, rendered by render_eq.py)
const EQ1 = JSON.parse(fs.readFileSync("eq1.json"));   // Net_j = Σ (w_ji O_i)
const EQ2 = JSON.parse(fs.readFileSync("eq2.json"));   // O_j = f(Net_j) = 1/(1+e^-Net_j)
const EQ3 = JSON.parse(fs.readFileSync("eq3.json"));   // E = 1/2 Σ (t_j - O_j)^2

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// ========== HOUSE CHROME (mandated template) ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: FRAME_COLOR, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_FILL }, line: { color: BADGE_LINE, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_TEXT, fontFace: FONT, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: TITLE_COLOR, fontFace: FONT, margin: 0,
});
// Subtitle with AFFECTS underlined (original underlines it)
s.addText(
  [
    { text: "(Weights of Output Layer ", options: { underline: false } },
    { text: "AFFECTS", options: { underline: true } },
    { text: " Calculated Error)", options: { underline: false } },
  ],
  {
    x: 0.6, y: 0.78, w: 12.13, h: 0.4,
    align: "center", valign: "top",
    fontSize: 16, bold: true, color: SUBTITLE_COLOR, fontFace: FONT, margin: 0,
  }
);

// ========== EMBED DIAGRAM ==========
// Diagram: 12.3 x 4.85in at slide x=0.5, y=1.20 -> bottom 6.05 (inside frame)
s.addImage({
  path: "slide_007_diagram.png",
  x: 0.5, y: 1.20, w: 12.3, h: 4.85
});

// ========== BOTTOM ANNOTATION PANELS ==========
// Inner frame bottom: 7.35in. Panels: y 6.15..7.30, clear of diagram (ends 6.05)
const BOX_Y = 6.15;
const BOX_H = 1.15;
const GAP = 0.15;
const B1_X = 0.5, B1_W = 3.0;
const B2_X = B1_X + B1_W + GAP, B2_W = 2.9;
const B3_X = B2_X + B2_W + GAP, B3_W = 3.2;
const B4_X = B3_X + B3_W + GAP, B4_W = 2.88;  // right edge 12.93 < 13.03 ✓

// ---- Panel 1: For Layer "j" + two equations (no collision: header, eq1, eq2 stacked) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: B1_X, y: BOX_Y, w: B1_W, h: BOX_H,
  fill: { color: "FDF2E9" }, line: { color: "BF8F00", width: 1 },
});
s.addText('For Layer "j"', {
  x: B1_X, y: BOX_Y, w: B1_W, h: 0.22,
  align: "left", valign: "top", fontSize: 11, bold: true, italic: true,
  color: TITLE_COLOR, fontFace: FONT, margin: 0.08,
});
// Eq1 baseline 6.6317in (top 6.42); Eq2 baseline 7.08in (top 6.78).
// Header band ends 6.37; eq1 bottom 6.703; eq2 bottom 7.27; panel bottom 7.30.
s.addImage({ path: "eq1.png", x: B1_X + 0.15, y: 6.6317 - EQ1.baseline_frac * EQ1.h_in, w: EQ1.w_in, h: EQ1.h_in });
s.addImage({ path: "eq2.png", x: B1_X + 0.15, y: 7.08 - EQ2.baseline_frac * EQ2.h_in, w: EQ2.w_in, h: EQ2.h_in });

// ---- Panel 2: Previous Layer Layer (0) with BOXED arrow containing "i" ----
s.addShape(pres.shapes.RECTANGLE, {
  x: B2_X, y: BOX_Y, w: B2_W, h: BOX_H,
  fill: { color: "FDF2E9" }, line: { color: "BF8F00", width: 1 },
});
// Boxed arrow outline containing the letter "i" (matches original)
s.addShape(pres.shapes.RECTANGLE, {
  x: B2_X + B2_W / 2 - 0.14, y: BOX_Y + 0.05, w: 0.28, h: 0.22,
  fill: { type: "none" }, line: { color: "2980B9", width: 1.25 },
});
s.addText("i", {
  x: B2_X + B2_W / 2 - 0.14, y: BOX_Y + 0.04, w: 0.28, h: 0.24,
  align: "center", valign: "middle", fontSize: 11, bold: true,
  color: "2980B9", fontFace: FONT, margin: 0,
});
s.addText("Previous Layer Layer (0)", {
  x: B2_X, y: BOX_Y + 0.42, w: B2_W, h: 0.3,
  align: "center", valign: "middle", fontSize: 11, bold: true, italic: true,
  color: TITLE_COLOR, fontFace: FONT, margin: 0.08,
});

// ---- Panel 3: Current Layer is Output Layer (You are here) with BOXED arrow "j" ----
s.addShape(pres.shapes.RECTANGLE, {
  x: B3_X, y: BOX_Y, w: B3_W, h: BOX_H,
  fill: { color: "D5F5E3" }, line: { color: "BF8F00", width: 1 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: B3_X + B3_W / 2 - 0.14, y: BOX_Y + 0.05, w: 0.28, h: 0.22,
  fill: { type: "none" }, line: { color: "27AE60", width: 1.25 },
});
s.addText("j", {
  x: B3_X + B3_W / 2 - 0.14, y: BOX_Y + 0.04, w: 0.28, h: 0.24,
  align: "center", valign: "middle", fontSize: 11, bold: true,
  color: "27AE60", fontFace: FONT, margin: 0,
});
s.addText("Current Layer is Output Layer (You are here)", {
  x: B3_X, y: BOX_Y + 0.42, w: B3_W, h: 0.3,
  align: "center", valign: "middle", fontSize: 11, bold: true, italic: true,
  color: TITLE_COLOR, fontFace: FONT, margin: 0.08,
});

// ---- Panel 4: If Layer "j" is Output Layer: + Eq3 ----
s.addShape(pres.shapes.RECTANGLE, {
  x: B4_X, y: BOX_Y, w: B4_W, h: BOX_H,
  fill: { color: "FDF2E9" }, line: { color: "BF8F00", width: 1 },
});
s.addText('If Layer "j" is Output Layer:', {
  x: B4_X, y: BOX_Y, w: B4_W, h: 0.22,
  align: "left", valign: "top", fontSize: 11, bold: true, italic: true,
  color: TITLE_COLOR, fontFace: FONT, margin: 0.08,
});
s.addImage({ path: "eq3.png", x: B4_X + 0.15, y: 6.90 - EQ3.baseline_frac * EQ3.h_in, w: EQ3.w_in, h: EQ3.h_in });

// ========== WRITE ==========
pres.writeFile({ fileName: "slide_007_recreated.pptx" })
  .then(() => console.log("wrote slide_007_recreated.pptx"))
  .catch(err => { console.error(err); process.exit(1); });