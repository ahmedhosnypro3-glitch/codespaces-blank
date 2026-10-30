// Slide 23: Back Propagation Flowchart — attempt 3 (judge fixes applied)
// Pattern: house-chrome + curved-arrows-custgeom
// Judge fixes: add PickFirst box, correct colors (green/pink per vision analysis), fix arrows, remove thick black artifacts

const pptxgen = require("pptxgenjs");
const PptxGenJS = pptxgen.default || pptxgen;
const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED_FRAME = "C00000";
const YELLOW_BADGE = "FFFFA2";
const BADGE_TEXT = "333333";
const FONT = "Arial";

// VISION ANALYSIS COLORS (not washed-out JPEG pixels)
const PALE_PURPLE = "DDA0DD";   // Initialization, PickFirst again
const LIGHT_GREEN = "90EE90";   // Pick Training Sample
const PALE_YELLOW = "FFFFE0";   // Go Forward, Go Backward
const ORANGE = "F4A460";        // Decision diamonds
const BRIGHT_GREEN = "00FF00";  // Stop
const PINK_RED = "FFB6C1";      // Stop with FAIL
const DARK_RED = "8B0000";      // Arrows/text
const CREAM_TXT = "4A1015";     // text inside colored boxes (dark for contrast)

let s = pptx.addSlide();
s.background = { color: BG };

// ===== HOUSE CHROME =====
s.addShape(pptx.ShapeType.rect, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2, line: { color: RED_FRAME, width: 1.5 },
});
s.addShape(pptx.ShapeType.ellipse, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW_BADGE }, line: { color: YELLOW_BADGE, width: 0.5 },
});
s.addText("23", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_TEXT, fontFace: FONT, margin: 0,
});

// ===== SLIDE 23 CONTENT =====
const CX = W / 2;                 // 6.665
const BW = 4.0, BH = 0.45;        // box width/height
const BWX = CX - BW / 2;          // box left x
const DW = 2.7, DH = 0.55;        // diamond width/height
const DWX = CX - DW / 2;          // diamond left x

const Y1 = 0.95, Y2 = 1.60, Y3 = 2.25, Y4 = 2.90;
const YD1 = 3.55;                 // Last Sample diamond
const YD2 = 4.25;                 // Stop criteria diamond
const YBR = 5.10;                 // branch row: Stop (right), PickFirst (left)
const YD3 = 5.10;                 // Max Iter diamond
const Y6 = 5.80;                  // Stop with FAIL
const GAPV = 0.20;

function box(x, y, fill, text, fs = 10) {
  s.addShape(pptx.ShapeType.roundRect, {
    x, y, w: BW, h: BH,
    fill: { color: fill }, line: { color: DARK_RED, width: 1 },
  });
  s.addText(text, {
    x, y, w: BW, h: BH,
    align: "center", valign: "middle",
    fontSize: fs, color: CREAM_TXT, fontFace: FONT, margin: 0,
  });
}
function dia(x, y, fill, text, fs = 9) {
  s.addShape(pptx.ShapeType.diamond, {
    x, y, w: DW, h: DH,
    fill: { color: fill }, line: { color: DARK_RED, width: 1 },
  });
  s.addText(text, {
    x, y, w: DW, h: DH,
    align: "center", valign: "middle",
    fontSize: fs, color: CREAM_TXT, fontFace: FONT, margin: 0,
  });
}
function vArrow(x, y, h) {
  s.addShape(pptx.ShapeType.downArrow, {
    x, y, w: 0.15, h, fill: { color: DARK_RED }, line: { color: DARK_RED, width: 0 },
  });
}
function hArrow(x, y, w, flipH = false) {
  s.addShape(pptx.ShapeType.leftArrow, {
    x, y, w, h: 0.15, fill: { color: DARK_RED }, line: { color: DARK_RED, width: 0 }, flipH,
  });
}
function label(text, x, y, w = 0.4, fs = 8) {
  s.addText(text, {
    x, y, w, h: 0.2, fontSize: fs, bold: true, color: DARK_RED, fontFace: FONT, margin: 0,
  });
}

box(BWX, Y1, PALE_PURPLE, "Initialization (Random Weights)");
box(BWX, Y2, LIGHT_GREEN, "Pick Training Sample, and Corresponding Label");
box(BWX, Y3, PALE_YELLOW, "Go Forward, Calculate Output");
box(BWX, Y4, PALE_YELLOW, "Go Backward, Update weights");
dia(DWX, YD1, ORANGE, "Last Sample ?");
dia(DWX, YD2, ORANGE, "Stop criteria is reached");

vArrow(CX - 0.075, Y1 + BH, GAPV);
vArrow(CX - 0.075, Y2 + BH, GAPV);
vArrow(CX - 0.075, Y3 + BH, GAPV);
vArrow(CX - 0.075, Y4 + BH, GAPV);
vArrow(CX - 0.075, YD1 + DH, GAPV);
vArrow(CX - 0.075, YD2 + DH, GAPV);

box(BWX + 2.6, YBR, BRIGHT_GREEN, "Stop", 11);
box(BWX - 2.4, YBR, PALE_PURPLE, "Pick First Sample again");
box(BWX - 2.4, Y6, PINK_RED, "Stop with FAIL", 10);
dia(DWX - 2.4, YD3, ORANGE, "Max Iteration Is reached");

s.addShape(pptx.ShapeType.custGeom, {
  x: 0, y: 0, w: W, h: H,
  line: { color: DARK_RED, width: 1.5 },
  points: [
    { x: DWX + DW, y: YD1 + DH / 2, moveTo: true },
    { x: BWX - 0.15, y: Y2 + BH / 2,
      curve: { type: "cubic", x1: DWX + DW + 1.2, y1: YD1 + DH / 2, x2: BWX - 1.0, y2: Y2 + BH / 2 } },
  ],
});
s.addShape(pptx.ShapeType.triangle, {
  x: BWX - 0.12, y: Y2 + BH / 2 - 0.06, w: 0.12, h: 0.12,
  fill: { color: DARK_RED }, line: { color: DARK_RED, width: 0 }, flipH: true,
});
label("NO", DWX + DW + 0.08, YD1 + DH / 2 - 0.08);

label("Yes", DWX + DW + 0.08, YD2 + DH / 2 - 0.08);
hArrow(DWX + DW + 0.12, YD2 + DH / 2 - 0.075, 2.1);
label("NO", DWX - 0.6, YD2 + DH / 2 - 0.08);
hArrow(DWX - 2.4 + DW + 0.12, YD2 + DH / 2 - 0.075, 1.2, true);
label("Yes", DWX - 2.4 + DW / 2 - 0.15, YD3 + DH + 0.02);
vArrow(DWX - 2.4 + DW / 2 - 0.075, YD3 + DH, Y6 - YD3 - DH);
label("NO", DWX - 2.4 - 0.55, YD3 + DH / 2 - 0.08);
hArrow(DWX - 2.4 - 0.12 - 0.15, YD3 + DH / 2 - 0.075, 0.15, true);

s.addShape(pptx.ShapeType.custGeom, {
  x: 0, y: 0, w: W, h: H,
  line: { color: DARK_RED, width: 1.5 },
  points: [
    { x: BWX - 2.4 + 1.7, y: YBR + BH / 2, moveTo: true },
    { x: BWX - 0.15, y: Y3 + BH / 2,
      curve: { type: "cubic", x1: BWX - 2.4 + 1.7 + 0.8, y1: YBR + BH / 2 - 0.3, x2: BWX - 0.8, y2: Y3 + BH / 2 - 0.3 } },
  ],
});
s.addShape(pptx.ShapeType.triangle, {
  x: BWX - 0.12, y: Y3 + BH / 2 - 0.06, w: 0.12, h: 0.12,
  fill: { color: DARK_RED }, line: { color: DARK_RED, width: 0 }, flipH: true,
});

const outPath = "videos/machine-learning/10_nn_training_and_example/recreated_pptx/slide_023_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));