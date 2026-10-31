// slide_033.js — attempt b17c
// "Initialized weights" / "Updated weights (after iteration # 10)" (badge 33)
// Geometry measured from unique_slides/slide_033.jpg (960x540 px; 1px = 1pt; PX = 13.33/960).
// Structure derived from the certified sibling recreated_pptx/build/slide_032.js.
// House chrome: bg E8E8E8, red frame 0.15in inset (C00000 1.5pt), yellow badge 33.
const pptxgen = require("pptxgenjs");
const VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example";
const PX = 13.33 / 960;
const px = v => +(v * PX).toFixed(4);
const FONT = "Arial";
const BLACK = "000000", BLUE = "0000FF", RED = "C00000";
const GREEN = "008000", NAVY = "000080", MAGENTA = "A000A0";
const YELLOW = "FFFF99", PEACH = "F8CBAD", CYAN = "4FB3B0", CREAM = "FAFCE2";
const GRAY = "A6A6A6";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ========== HOUSE CHROME ==========
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("33", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ========== HELPERS (all coords in source px) ==========
function txt(str, x, y, w, h, size, color, bold, align, italic) {
  s.addText(str, {
    x: px(x), y: px(y), w: px(w), h: px(h), align: align || "left",
    valign: "middle", fontSize: size, bold: !!bold, italic: !!italic,
    color, fontFace: FONT, margin: 0,
  });
}
function utxt(str, x, y, w, h, size, color, align, italic) {
  s.addText(str, {
    x: px(x), y: px(y), w: px(w), h: px(h), align: align || "left",
    valign: "middle", fontSize: size, bold: true, italic: !!italic,
    underline: true, color, fontFace: FONT, margin: 0,
  });
}
function node(cx, cy, r, fill) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - r), y: px(cy - r), w: px(2 * r), h: px(2 * r),
    fill: { color: fill }, line: { color: BLACK, width: 1 },
  });
}
function dot(cx, cy, fill) {
  s.addShape(pres.shapes.OVAL, {
    x: px(cx - 3), y: px(cy - 3), w: px(6), h: px(6),
    fill: { color: fill }, line: { color: fill, width: 0.5 },
  });
}
function conn(x1, y1, x2, y2, color, w) {
  s.addShape(pres.shapes.LINE, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    line: { color, width: w || 0.75 },
  });
}

// ========== MEASURED GEOMETRY (source px, from slide_033.jpg masks) ==========
// Panel A: y 89..285 (h196). Panel B: y 330..524 (h194). Panel x 101..824.
// Layer labels: Input y~102-117, Output y~101-116, Target y~105-119 (all bold italic underlined).
//    Input x[128..169], Output x[578..639], Target x[718..771]
// Nodes: hidden yellow FFFF99 r15 at x347: y124/181/237 ; output peach r13.5 at x551: y156/216
//        input black r6 at x189: y144/208 ; bias cyan r7: x190 y249 and x347 y274
// Target block: cream rounded rect x[640..790]; row1 y[140..170], row2 y[200..229]
//        cols at x676(left "O" values), x755(right "t" values) between black parens at x668..x784
// Double arrow: red LEFT_RIGHT_ARROW x[710..744] y[177..192]
// Weight label colors: in->hidden GREEN 008000, bias->hidden NAVY 000080,
//        hidden->output RED C00000 (top) / MAGENTA A000A0 (bottom), bias->output BLUE 0000FF
const PANELS = [
  { y0: 89, outFan: RED, inW: GREEN, biasW: NAVY, b2o: BLUE },
  { y0: 330, outFan: MAGENTA, inW: GREEN, biasW: NAVY, b2o: BLUE },
];
function drawPanel(p, header, inW, outW, target) {
  // panel border (no fill, C00000 1.5pt) — measured x101..824
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(101), y: px(p.y0), w: px(723), h: px(196),
    fill: { type: "none" }, line: { color: RED, width: 1.5 },
  });
  // red italic bold header, left-aligned at x111 (measured y 68..89 / 311..324 → y0-21 centered)
  txt(header, px(111), px(p.y0 - 21), px(300), px(16), 12, RED, true, "left", true);

  // ---- layer column labels (bold italic underlined) ----
  utxt("Input", px(128), px(p.y0 + 12), px(48), px(15), 10, BLUE);
  utxt("Output", px(578), px(p.y0 + 11), px(62), px(15), 10, BLUE);
  utxt("Target", px(718), px(p.y0 + 15), px(54), px(15), 10, BLACK);

  const HX = 347;              // hidden column x
  const INX = 189, INY1 = 144, INY2 = 208, BIAS = 249;
  const HY = [124, 181, 237];  // hidden node y
  const OY = [156, 216];       // output node y
  const OX = 551;

  // ---- input side: bracket vector x1=1, x2=5 ; black nodes ; bias ----
  txt("x\u2081", px(104), px(p.y0 + 51), px(22), px(15), 11, BLUE, true, "left", true);
  txt("x\u2082", px(104), px(p.y0 + 107), px(22), px(15), 11, BLUE, true, "left", true);
  txt("[", px(128), px(p.y0 + 48), px(12), px(22), 20, BLACK, true, "center");
  txt("1", px(138), px(p.y0 + 56), px(14), px(16), 12, BLACK, true, "center");
  txt("5", px(138), px(p.y0 + 112), px(14), px(16), 12, BLACK, true, "center");
  txt("]", px(148), px(p.y0 + 48), px(12), px(22), 20, BLACK, true, "center");
  node(INX, p.y0 + INY1 - p.y0, 6, BLACK);
  node(INX, INY1, 6, BLACK);
  node(INX, INY2, 6, BLACK);
  dot(199, INY1, RED); dot(199, INY2, RED);
  node(190, BIAS, 7, CYAN);
  txt("Bias", px(156), px(p.y0 + 168), px(38), px(14), 9, BLUE, true, "left", true);

  // ---- hidden nodes (numbered 3,4,5) with O labels ----
  HY.forEach((y, i) => {
    node(HX, y, 15, YELLOW);
    txt(String(3 + i), px(HX - 8), px(y - 8), px(16), px(16), 11, BLACK, true, "center");
    txt("O\u208" + (3 + i), px(HX - 4), px(y - 26), px(26), px(14), 10, BLUE, true, "center", true);
    dot(HX + 19, y, RED);
  });
  // hidden bias
  node(HX, 274, 7, CYAN);
  txt("Bias", px(300), px(p.y0 + 180), px(38), px(14), 9, BLUE, true, "left", true);

  // ---- output nodes 6,7 ----
  OY.forEach((y, i) => {
    node(OX, y, 13, PEACH);
    txt(String(6 + i), px(OX - 8), px(y - 8), px(16), px(16), 11, BLACK, true, "center");
    txt("O\u208" + (6 + i), px(OX - 9), px(y - 22), px(26), px(14), 10, BLUE, true, "center", true);
    dot(OX + 19, y, RED);
  });
  utxt("\u03b7 = 5", px(654), px(p.y0 + 172), px(52), px(16), 12, RED);
