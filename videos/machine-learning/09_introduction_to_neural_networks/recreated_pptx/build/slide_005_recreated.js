// Slide 005 — "Visualization of Single Perceptron"
//
// Geometry comes from pixel measurement of the original frame
// (unique_slides/slide_005.jpg, 960x540 => 1 original px = 1 pt = 1/72 in).
// Every element below carries its measured original-frame coordinates.
//
// House chrome (project rule, overrides the source slide): LAYOUT_WIDE,
// #E8E8E8 background, outer red frame at 0.15in inset, yellow badge with the
// printed slide number, centered title at y=0.28in.
//
// Equations follow the house math rule: matplotlib mathtext -> 600 dpi PNG ->
// addImage at px/600 in. slide_005_eq.png carries the decision equation
// (red X inside d(X), red b*1 tail, bold underlined W) and slide_005_rules.png
// carries the three blue class rules.
const pptxgen = require("pptxgenjs");

const V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks";
const B = V + "/recreated_pptx/build";
const NUM = 5;
const TITLE = "Visualization of Single Perceptron";
const W = 13.333, H = 7.5;

const SERIF = "Times New Roman";
const SANS = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// px in the original frame -> inches
const px = (v) => v / 72;

// ---------------------------------------------------------------- house chrome
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: SANS, margin: 0,
});
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: SANS, margin: 0,
});

// ------------------------------------------------------------- panel frames
// measured: top-left x82-419 y87-246, top-right x528-793 y88-246,
// banner x81-767 y254-342, diagram x227-613 y349-508, caption x629-818 y400-441
function panel(x0, y0, x1, y1) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: "FFFFFF" },
    line: { color: "C00000", width: 0.75 },
  });
}
panel(82, 87, 419, 246);
panel(528, 88, 793, 246);
panel(81, 254, 767, 342);
panel(227, 349, 613, 508);

// ------------------------------------------------------------- bracket strokes
// The originals' matrix brackets are 2px vertical strokes with no arms.
function vbar(x, y0, y1, w, color) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(x), y: px(y0), w: px(w), h: px(y1 - y0),
    fill: { color }, line: { type: "none" },
  });
}
// left panel: vector 1 brackets x116-117 / x139-140 (y121-218 / y116-223)
vbar(116, 121, 218, 2, "000000");
vbar(139, 116, 223, 2, "000000");
// left panel: augmented vector brackets x248-250 / x272-273 (y107-231)
vbar(248, 107, 231, 3, "000000");
vbar(272, 107, 231, 2, "000000");
// right panel: weight vector brackets x592-593 / x619-620 (y107-231)
vbar(592, 107, 231, 2, "000000");
vbar(619, 107, 231, 2, "000000");
// banner: rule-group brackets x544-545 / x748-750 (y263-330), muted blue-grey
vbar(544, 263, 330, 2, "9E9BB6");
vbar(748, 263, 330, 3, "9E9BB6");

// ----------------------------------------------------------- vector entries
// A matrix entry is placed by its glyph baseline in the original frame.
// Baseline rows measured from the original:
//   vector 1 (x122-135): x1 130, x2 153, "..." 175, "..." 197, xn 219
//   augmented (x256-268): 1 120(red), x1 141, x2 164, "..." 187, "..." 208, xn 229
//   weights  (x599-610): b 120(red), w1 141, w2 164, "..." 187, "..." 208, wn 229
function entry(text, x, baseline, size, color, italic) {
  s.addText(text, {
    x: px(x), y: px(baseline - size * 0.80), w: px(60), h: px(size * 1.35),
    align: "left", valign: "top",
    fontSize: size, color, fontFace: SERIF, italic: !!italic, margin: 0,
  });
}
const SZ = 18;   // entry x-height 7-8px => ~18pt serif
// vector 1
entry("x₁", 122, 130, SZ, "000000", true);
entry("x₂", 122, 153, SZ, "000000", true);
entry("…", 122, 175, SZ, "000000", true);
entry("…", 122, 197, SZ, "000000", true);
entry("xₙ", 122, 219, SZ, "000000", true);
// augmented vector (the leading 1 is red)
entry("1", 258, 120, 20, "C00000", true);
entry("x₁", 256, 141, SZ, "000000", true);
entry("x₂", 256, 164, SZ, "000000", true);
entry("…", 256, 187, SZ, "000000", true);
entry("…", 256, 208, SZ, "000000", true);
entry("xₙ", 256, 229, SZ, "000000", true);
// weight vector (the leading b is blue in the original, not red)
entry("b", 602, 120, 20, "0000FF", true);
entry("w₁", 599, 141, SZ, "000000", true);
entry("w₂", 599, 164, SZ, "000000", true);
entry("…", 599, 187, SZ, "000000", true);
entry("…", 599, 208, SZ, "000000", true);
entry("wₙ", 599, 229, SZ, "000000", true);

// ------------------------------------------------- vector labels and arrows
// "X =" appears twice: x87-113 (baseline 171) and x219-245 (baseline 171)
function vecLabel(x, baseline) {
  s.addText("X =", {
    x: px(x), y: px(baseline - 19), w: px(40), h: px(30),
    align: "left", valign: "top",
    fontSize: 21, color: "000000", fontFace: SERIF, bold: true, italic: true,
    margin: 0,
  });
}
vecLabel(87, 171);
vecLabel(219, 171);
// red double arrow between vector 1 and the augmented vector (x178-194, y161-170)
s.addText("⇒", {
  x: px(176), y: px(158), w: px(22), h: px(18),
  align: "center", valign: "middle",
  fontSize: 20, bold: true, color: "C00000", fontFace: SERIF, margin: 0,
});
// "Augmented Vector" blue italic, x298-406 y161-175 (baseline 171)
s.addText("Augmented Vector", {
  x: px(298), y: px(161 - 16), w: px(115), h: px(24),
  align: "left", valign: "top",
  fontSize: 16, color: "0000FF", fontFace: SERIF, italic: true, margin: 0,
});
// "W" red + "=" black in the right panel (W x560-575 y159-174, = x578-589)
s.addText("W", {
  x: px(559), y: px(159 - 19), w: px(20), h: px(26),
  align: "left", valign: "top",
  fontSize: 22, color: "C00000", fontFace: SERIF, bold: true, italic: true,
  margin: 0,
});
s.addText("=", {
  x: px(578), y: px(159 - 17), w: px(16), h: px(24),
  align: "left", valign: "top",
  fontSize: 21, color: "000000", fontFace: SERIF, margin: 0,
});
// "Model Weights" blue italic, x670-761 y161-174 (baseline 171)
s.addText("Model Weights", {
  x: px(670), y: px(161 - 16), w: px(100), h: px(24),
  align: "left", valign: "top",
  fontSize: 16, color: "0000FF", fontFace: SERIF, italic: true, margin: 0,
});

// ------------------------------------------------------------ banner assets
// equation PNG spans original x84-526, y279-310
s.addImage({
  path: B + "/slide_005_eq.png",
  x: px(84), y: px(279), w: px(442), h: px(31),
});
// rules PNG spans original x555-745, y264-328
s.addImage({
  path: B + "/slide_005_rules.png",
  x: px(555), y: px(264), w: px(190), h: px(64),
});

// --------------------------------------------------------- bottom diagram
// the perceptron schematic is generated by slide_005_graph.py and spans
// original x227-614, y349-508
s.addImage({
  path: B + "/slide_005_graph.png",
  x: px(227), y: px(349), w: px(387), h: px(159),
});

// ------------------------------------------------------------------ caption
// beige box x629-818 y400-441; two bold brown lines
s.addShape(pres.shapes.RECTANGLE, {
  x: px(629), y: px(400), w: px(189), h: px(41),
  fill: { color: "E1E6C6" }, line: { type: "none" },
});
s.addText("Binary Classification", {
  x: px(629), y: px(401), w: px(189), h: px(18),
  align: "center", valign: "top",
  fontSize: 13, bold: true, color: "663311", fontFace: SANS, margin: 0,
});
s.addText("(2 Classes)", {
  x: px(629), y: px(417), w: px(189), h: px(18),
  align: "center", valign: "top",
  fontSize: 13, bold: true, color: "663311", fontFace: SANS, margin: 0,
});

pres.writeFile({ fileName: B + "/slide_005_recreated.pptx" })
  .then(() => console.log("wrote " + B + "/slide_005_recreated.pptx"));
