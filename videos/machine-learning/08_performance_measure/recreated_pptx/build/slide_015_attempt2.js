const pptxgenpkg = require("pptxgenjs");
const fs = require("fs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLUE = "0000FF";
const GREEN = "008000";
const WHITE = "FFFFFF";
const PEACH = "F6E1C6";
const DARK_RED = "8B0000";
const BLACK = "000000";
const TITLE_FONT = "Times New Roman";
const FONT = "Arial";

const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
const EQ = JSON.parse(fs.readFileSync(ASSETS + "/eq_015_manifest.json", "utf8"));

const PX = 1 / 72;
const px = (v) => v * PX;

// text metrics helpers (Arial): cap top sits 0.189em below the box top,
// the baseline sits 0.905em below it.
const capTop = (baselineIn, size) => baselineIn - 0.189 * size * PX;
const boxTop = (baselineIn, size) => baselineIn - 0.905 * size * PX;

// place a rendered equation so its ink box lands on the requested rectangle
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

// dark-red header bar around the title
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  fill: { color: BG }, line: { color: DARK_RED, width: 1.5 }
});

// title (original ~19px, serif, PENALIZE underlined in red)
s.addText([
  { text: "Required to ", options: { color: DARK_RED } },
  { text: "PENALIZE", options: { color: "FF0000", underline: true } },
  { text: " small values of Precision and Recall", options: { color: DARK_RED } }
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "middle",
  fontSize: 19, bold: true, fontFace: TITLE_FONT, margin: 0
});

// ============================================================
// REMEMBER BOX  (original x 74..547, y 120..251)
// ============================================================
const RX = px(74), RY = px(120), RW = px(473), RH = px(131);
s.addShape(pptx.shapes.RECTANGLE, {
  x: RX, y: RY, w: RW, h: RH,
  fill: { color: WHITE }, line: { color: BLUE, width: 2 }
});

const TF = 18;                       // remember-box text size (measured)
const rBase1 = px(146);              // baseline of "Remember:"
s.addText("Remember:", {
  x: px(93), y: boxTop(rBase1, TF), w: 3.0, h: 0.35,
  fontSize: TF, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  valign: "top"
});

const rBase2 = px(167);              // baseline of the range line
s.addText([
  { text: "Ranges of ", options: { color: BLACK } },
  { text: "Precision", options: { color: BLUE } },
  { text: " and ", options: { color: BLACK } },
  { text: "Recall", options: { color: BLUE } },
  { text: " are ", options: { color: BLACK } },
  { text: "from 0 to 1", options: { color: "FF0000" } }
], {
  x: px(93), y: boxTop(rBase2, TF), w: 6.2, h: 0.4,
  fontSize: TF, fontFace: FONT, margin: 0, valign: "top"
});

// "Using 1/Precision and 1/Recall" - fractions are stacked (2D)
const rBase3 = px(211);
const rTop3 = px(189);
s.addText("Using", {
  x: px(93), y: boxTop(rBase3, TF), w: 0.9, h: 0.35,
  fontSize: TF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "frac1_prec", px(145), rTop3 * PX);
s.addText("and", {
  x: px(243), y: boxTop(rBase3, TF), w: 0.55, h: 0.35,
  fontSize: TF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "frac1_rec", px(291), rTop3 * PX);

// ============================================================
// GRAPH PANEL  (original x 660..859, y 96..274)
// ============================================================
s.addImage({
  path: ASSETS + "/eq_015_graph.png",
  x: px(660), y: px(96), w: px(199), h: px(178)
});

// ============================================================
// BOTTOM BLUE PANEL  (original x 63..871, y 286..501)
// ============================================================
const BX = px(63), BY = px(286), BW = px(808), BH = px(215);
s.addShape(pptx.shapes.RECTANGLE, {
  x: BX, y: BY, w: BW, h: BH,
  fill: { color: WHITE }, line: { color: BLUE, width: 2 }
});

const BF = 15;                        // bottom-panel text size (measured)
const bBase1 = px(311);
const bTop1 = px(296);
s.addText([
  { text: "As ", options: { color: BLACK } },
  { text: "Precision/Recall", options: { color: BLUE, bold: true } },
  { text: " Decreases ", options: { color: BLACK } },
  { text: "\u21d2 Value of ", options: { color: BLACK } }
], {
  x: px(85), y: boxTop(bBase1, BF), w: 4.0, h: 0.35,
  fontSize: BF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "paren_prec", px(372), bTop1 * PX);
s.addText("and", {
  x: px(530), y: boxTop(bBase1, BF), w: 0.5, h: 0.35,
  fontSize: BF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "paren_rec", px(590), bTop1 * PX);
s.addText("Increases", {
  x: px(670), y: boxTop(bBase1, BF), w: 1.4, h: 0.35,
  fontSize: BF, color: GREEN, fontFace: FONT, margin: 0, valign: "top"
});

// line 2
const bBase2 = px(376);
const bTop2 = px(360);
s.addText("Define:", {
  x: px(83), y: boxTop(bBase2, BF), w: 1.0, h: 0.35,
  fontSize: BF, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "frac1_f1", px(150), bTop2 * PX);
s.addText("=", {
  x: px(176), y: boxTop(bBase2, BF), w: 0.3, h: 0.35,
  fontSize: BF, color: BLACK, fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "paren_sum", px(186), bTop2 * PX);
s.addText([
  { text: "\u21d2 ", options: { color: BLACK } },
  { text: "F1", options: { color: BLUE, bold: true } },
  { text: " ", options: { color: BLACK } },
  { text: "increases", options: { color: GREEN } },
  { text: " as both ", options: { color: BLACK } },
  { text: "Precision", options: { color: BLUE, bold: true } },
  { text: " and ", options: { color: BLACK } },
  { text: "Recall", options: { color: BLUE, bold: true } },
  { text: " are high values", options: { color: BLACK } }
], {
  x: px(426), y: boxTop(bBase2, BF), w: 6.0, h: 0.35,
  fontSize: BF, fontFace: FONT, margin: 0, valign: "top"
});

// line 3
const CF = 18;
const bBase3 = px(462);
s.addText([
  { text: "F1", options: { color: BLUE, bold: true } },
  { text: " Range is ", options: { color: BLACK } },
  { text: "from 0 to 0.5", options: { color: "FF0000", bold: true } },
  { text: " \u21d2 ", options: { color: BLACK } },
  { text: "Normalize", options: { color: BLACK, bold: true, italic: true } }
], {
  x: px(102), y: boxTop(bBase3, CF), w: 6.5, h: 0.4,
  fontSize: CF, fontFace: FONT, margin: 0, valign: "top"
});

// ============================================================
// ORANGE NORMALIZED-EQUATION BOX (original x 549..863, y 419..492)
// ============================================================
const OX = px(549), OY = px(419), OW = px(314), OH = px(73);
s.addShape(pptx.shapes.RECTANGLE, {
  x: OX, y: OY, w: OW, h: OH,
  fill: { color: PEACH }, line: { color: "FF0000", width: 1.5, dashType: "dash" }
});

const OF = 16;
const oBase = px(457);
const oInkTop = px(433);
eqImg(s, "frac1_f1_sm", px(560), oInkTop * PX);
s.addText("=", {
  x: px(596), y: boxTop(oBase, OF), w: 0.3, h: 0.3,
  fontSize: OF, color: BLACK, fontFace: FONT, margin: 0, valign: "top"
});
s.addText("0.5", {
  x: px(624), y: boxTop(oBase, OF), w: 0.5, h: 0.3,
  fontSize: OF, color: "FF0000", fontFace: FONT, margin: 0, valign: "top"
});
eqImg(s, "paren_sum", px(672), oInkTop * PX);

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_015_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
