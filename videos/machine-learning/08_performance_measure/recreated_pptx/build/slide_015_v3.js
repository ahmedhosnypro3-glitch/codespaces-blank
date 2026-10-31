const pptxgenpkg = require("pptxgenjs");
const fs = require("fs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE = "0000FF";
const NAVY = "000080";
const GREEN = "008000";
const WHITE = "FFFFFF";
const PEACH = "FFE6CC";
const DARK_RED = "B00000";
const BRIGHT_RED = "FF0000";
const BLACK = "000000";
const FONT = "Arial";

const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
const EQ = JSON.parse(fs.readFileSync(ASSETS + "/eq_015_manifest.json", "utf8"));

const PX = 1 / 72;
const px = (v) => v * PX;

const capTop = (baselineIn, size) => baselineIn - 0.189 * size * PX;
const boxTop = (baselineIn, size) => baselineIn - 0.905 * size * PX;

function eqImg(slide, key, inkLeftIn, inkTopIn) {
  const m = EQ[key];
  const w = m.w_in;
  const h = m.h_in;
  slide.addImage({
    path: ASSETS + "/eq_015_" + key + ".png",
    x: inkLeftIn - m.ink_left_frac * w,
    y: inkTopIn - m.ink_top_frac * h,
    w: w,
    h: h
  });
  return {
    left: inkLeftIn,
    right: inkLeftIn + m.ink_w_frac * w,
    top: inkTopIn,
    bottom: inkTopIn + m.ink_h_frac * h
  };
}

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 }
});

s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 }
});
s.addText("15", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0
});

// title text only: the original has no title-bar rectangle (its title sits inside
// the slide's own outer frame), and a bar here would cross the house badge.
s.addText([
  { text: "Required to ", options: { color: DARK_RED } },
  { text: "PENALIZE", options: { color: BRIGHT_RED, underline: true } },
  { text: " small values of Precision and Recall", options: { color: DARK_RED } }
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.79,
  align: "center", valign: "bottom",
  fontSize: 19, bold: true, fontFace: FONT, margin: 0
});

// ============================================================
// REMEMBER BOX  (measured frame x 74..547, y 120..251)
// ============================================================
const RX = px(74), RY = px(120), RW = px(473), RH = px(131);
s.addShape(pptx.shapes.RECTANGLE, {
  x: RX, y: RY, w: RW, h: RH,
  fill: { color: WHITE }, line: { color: BLUE, width: 2 }
});

const TF = 18;
const rBase1 = px(146);
s.addText("Remember:", {
  x: px(93), y: boxTop(rBase1, TF), w: 3.0, h: 0.35,
  fontSize: TF, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  valign: "top"
});

const rBase2 = px(167);
s.addText([
  { text: "Ranges of Precision and Recall are ", options: { color: NAVY } },
  { text: "from 0 to 1", options: { color: BRIGHT_RED } }
], {
  x: px(93), y: boxTop(rBase2, TF), w: 6.2, h: 0.4,
  fontSize: TF, fontFace: FONT, margin: 0, valign: "top"
});

const rBase3 = px(211);
const rTop3 = px(189);
s.addText("Using", {
  x: px(93), y: boxTop(rBase3, TF), w: 0.9, h: 0.35,
  fontSize: TF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "frac1_prec", px(145), rTop3);
s.addText("and", {
  x: px(243), y: boxTop(rBase3, TF), w: 0.55, h: 0.35,
  fontSize: TF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "frac1_rec", px(291), rTop3);
s.addText("+", {
  x: px(333), y: boxTop(rBase3, TF), w: 0.3, h: 0.35,
  fontSize: TF, color: BLACK, fontFace: FONT, margin: 0, valign: "top"
});

// ============================================================
// GRAPH PANEL  (measured frame x 661..859, y 97..273)
// generated matplotlib plot: red y=1/x, ticks x -6..6 / y -3..3, yellow oval
// ============================================================
s.addImage({
  path: ASSETS + "/eq_015_graph_v2.png",
  x: px(661), y: px(97), w: px(198), h: px(176)
});

// ============================================================
// BOTTOM BLUE PANEL  (measured frame x 63..871, y 286..501)
// ============================================================
const BX = px(63), BY = px(286), BW = px(808), BH = px(215);
s.addShape(pptx.shapes.RECTANGLE, {
  x: BX, y: BY, w: BW, h: BH,
  fill: { color: WHITE }, line: { color: BLUE, width: 2 }
});

const BF = 15;

// line 1: As Precision/Recall Decreases => Value of (1/Precision) and (1/Recall) Increases
const bBase1 = px(311);
const bTop1 = px(296);
s.addText([
  { text: "As ", options: { color: BLACK } },
  { text: "Precision/Recall", options: { color: BLACK, bold: true } },
  { text: " ", options: { color: BLACK } },
  { text: "Decreases", options: { color: BLACK, underline: true } },
  { text: " ", options: { color: BLACK } },
  { text: "\u21d2", options: { color: BRIGHT_RED } },
  { text: " Value of ", options: { color: BLACK } }
], {
  x: px(85), y: boxTop(bBase1, BF), w: 4.2, h: 0.35,
  fontSize: BF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "paren_prec", px(372), bTop1);
s.addText("and", {
  x: px(530), y: boxTop(bBase1, BF), w: 0.5, h: 0.35,
  fontSize: BF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "paren_rec", px(590), bTop1);
s.addText("Increases", {
  x: px(680), y: boxTop(bBase1, BF), w: 1.4, h: 0.35,
  fontSize: BF, bold: true, color: GREEN, fontFace: FONT, margin: 0, valign: "top"
});

// line 2: Define: 1/F1 = 1/Precision + 1/Recall => F1 increases as both Precision and Recall are high values
const bBase2 = px(376);
const bTop2 = px(360);
s.addText("Define:", {
  x: px(83), y: boxTop(bBase2, BF), w: 1.0, h: 0.35,
  fontSize: BF, bold: true, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "frac1_f1", px(150), bTop2);
s.addText("=", {
  x: px(190), y: boxTop(bBase2, BF), w: 0.3, h: 0.35,
  fontSize: BF, color: BLACK, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "frac1_prec", px(208), bTop2);
s.addText("+", {
  x: px(296), y: boxTop(bBase2, BF), w: 0.3, h: 0.35,
  fontSize: BF, color: BLACK, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "frac1_rec", px(314), bTop2);
s.addText("\u21d2", {
  x: px(400), y: boxTop(bBase2, BF), w: 0.3, h: 0.35,
  fontSize: BF, color: BRIGHT_RED, fontFace: FONT, margin: 0, valign: "top"
});
s.addText([
  { text: "F1", options: { color: BLACK, bold: true } },
  { text: " increases as both ", options: { color: BLACK } },
  { text: "Precision", options: { color: BRIGHT_RED } },
  { text: " and ", options: { color: BLACK } },
  { text: "Recall", options: { color: BRIGHT_RED } },
  { text: " are high values", options: { color: BLACK } }
], {
  x: px(432), y: boxTop(bBase2, BF), w: 6.2, h: 0.35,
  fontSize: BF, fontFace: FONT, margin: 0, valign: "top"
});

// line 3: F1 Range is from 0 to 0.5 => Normalize
const CF = 18;
const bBase3 = px(462);
s.addText([
  { text: "F1", options: { color: BLUE, bold: true } },
  { text: " Range is ", options: { color: BLACK } },
  { text: "from 0 to 0.5", options: { color: BRIGHT_RED, bold: true } },
  { text: " ", options: { color: BLACK } },
  { text: "\u21d2", options: { color: BRIGHT_RED } },
  { text: " ", options: { color: BLACK } },
  { text: "Normalize", options: { color: BRIGHT_RED, bold: true, italic: true } }
], {
  x: px(102), y: boxTop(bBase3, CF), w: 6.5, h: 0.4,
  fontSize: CF, fontFace: FONT, margin: 0, valign: "top"
});

// ============================================================
// ORANGE NORMALIZED-EQUATION BOX (measured frame x 549..863, y 419..493)
// single line: 1/F1 = 0.5 x (1/Precision + 1/Recall)
// ============================================================
const OX = px(549), OY = px(419), OW = px(314), OH = px(73);
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: OX, y: OY, w: OW, h: OH,
  fill: { color: PEACH }, line: { color: BRIGHT_RED, width: 1.5, dashType: "dash" }
});

const OF = 16;
const oBase = px(457);
const oInkTop = px(433);
eqImg(s, "frac1_f1_sm", px(560), oInkTop);
s.addText("=", {
  x: px(596), y: boxTop(oBase, OF), w: 0.3, h: 0.3,
  fontSize: OF, color: BLACK, fontFace: FONT, margin: 0, valign: "top"
});
s.addText("0.5", {
  x: px(614), y: boxTop(oBase, OF), w: 0.5, h: 0.3,
  fontSize: OF, color: BRIGHT_RED, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "paren_sum", px(668), oInkTop);

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_015_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
