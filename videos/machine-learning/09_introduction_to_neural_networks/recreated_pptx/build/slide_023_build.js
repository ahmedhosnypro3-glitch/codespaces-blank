const pptxgen = require("pptxgenjs");

// Slide 023: Derivatives of some Activation Functions
const NUM = 23;
const TITLE = "Derivatives of some Activation Functions";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000FF";
const BORDER_RED = "8B0000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const BADGE_OUTLINE = "4B0082";
const BADGE_NUM = "4B0082";
const YELLOW = "FFF9C4";

// Additional colors from validation
const PEACH = "FDE9E0";
const PEACH_BORDER = "E06666";
const CREAM = "FFFDE0";
const CREAM_BORDER = "9999FF";
const BLUE_VIOLET = "6666CC";
const GREEN = "008000";
const RED_ACCENT = "CC0000";

function c(hex) { return "#" + hex; }

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Bottom black bar - from validation analysis
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { color: "none" },
});

// 3. Inner blue-violet frame
s.addShape(pres.shapes.RECTANGLE, {
  x: 1.0, y: 1.5, w: W - 2.0, h: H - 3.0,
  fill: { type: "none" },
  line: { color: BLUE_VIOLET, width: 1 },
});

// 4. Slide-number badge - HOUSE CHROME LAW (yellow circle at 12.48, 0.30, 0.5x0.5)
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: BADGE_NUM, fontFace: FONT, margin: 0,
});

// 5. Title box - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 6. Row data: [y_pos, left_box_x, left_box_w, right_box_x, right_box_w, left_content, right_content, is_piecewise]
// All measurements converted from percentage positions to inches (13.33" wide)
const rows = [
  // Row 1: Uni-polar
  {
    y: 1.95,
    left: { x: 1.13, w: 5.1, h: 0.9 },   // 8.5%-45.5% of 13.33
    center: { x: 6.67, w: 1.07, h: 0.9 }, // 50%-58%
    right: { x: 8.60, w: 3.6, h: 0.9 },   // 64.5%-91.5%
    leftEq: "eq_s023_unipolar.png",
    rightEq: "eq_s023_step_deriv.png",
    leftFunc: "f(x) = Uni-polar Unit Step",
    rightFunc: "f'(x)",
    leftPiecewise: true,
    rightPiecewise: true,
  },
  // Row 2: Bi-polar
  {
    y: 3.07,
    left: { x: 1.13, w: 5.1, h: 0.9 },
    center: { x: 6.67, w: 1.07, h: 0.9 },
    right: { x: 8.60, w: 3.6, h: 0.9 },
    leftEq: "eq_s023_bipolar.png",
    rightEq: "eq_s023_step_deriv.png",
    leftFunc: "f(x) = Bi-polar Unit Step",
    rightFunc: "f'(x)",
    leftPiecewise: true,
    rightPiecewise: true,
  },
  // Row 3: Sigmoid
  {
    y: 4.20,
    left: { x: 1.13, w: 3.83, h: 0.75 }, // 8.5%-34%
    center: { x: 6.67, w: 1.07, h: 0.75 },
    right: { x: 8.60, w: 3.6, h: 0.75 },
    leftEq: "eq_s023_sigmoid.png",
    rightEq: "eq_s023_sigmoid_deriv.png",
    leftFunc: "f(x) = Sigmoid(x)",
    rightFunc: "f'(x) = f(x)(1-f(x))",
    leftPiecewise: false,
    rightPiecewise: false,
  },
  // Row 4: tanh
  {
    y: 5.33,
    left: { x: 1.13, w: 3.83, h: 0.75 },
    center: { x: 6.67, w: 1.07, h: 0.75 },
    right: { x: 8.60, w: 3.6, h: 0.75 },
    leftEq: "eq_s023_tanh.png",
    rightEq: "eq_s023_tanh_deriv.png",
    leftFunc: "f(x) = tanh(x)",
    rightFunc: "f'(x) = 1-f(x)^2",
    leftPiecewise: false,
    rightPiecewise: false,
  },
  // Row 5: arctan
  {
    y: 6.40,
    left: { x: 1.13, w: 2.27, h: 0.75 }, // 8.5%-24.5%
    center: { x: 6.67, w: 1.07, h: 0.75 },
    right: { x: 8.60, w: 1.67, h: 0.75 }, // 64.5%-77%
    leftEq: "eq_s023_arctan.png",
    rightEq: "eq_s023_arctan_deriv.png",
    leftFunc: "f(x) = tan^{-1}(x)",
    rightFunc: "f'(x) = 1/(x^2+1)",
    leftPiecewise: false,
    rightPiecewise: false,
  },
];

const BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/";

rows.forEach(row => {
  // Left box
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: row.left.x, y: row.y, w: row.left.w, h: row.left.h,
    fill: { color: PEACH }, line: { color: PEACH_BORDER, width: 1 },
  });

  // Left equation image (piecewise or full equation)
  s.addImage({
    path: BUILD_DIR + row.leftEq,
    x: row.left.x + 0.1, y: row.y + 0.1,
    w: row.left.w - 0.2,
  });

  // Center: "Derivative" + double arrow
  s.addText("Derivative", {
    x: row.center.x, y: row.y, w: row.center.w, h: 0.35,
    align: "center", valign: "top",
    fontSize: 16, bold: false, italic: true, color: RED_ACCENT, fontFace: "Times New Roman", margin: 0,
  });
  s.addText("\u21d2", {  // ⇒
    x: row.center.x, y: row.y + 0.3, w: row.center.w, h: 0.4,
    align: "center", valign: "top",
    fontSize: 28, bold: false, color: RED_ACCENT, fontFace: "Times New Roman", margin: 0,
  });

  // Right box
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: row.right.x, y: row.y, w: row.right.w, h: row.right.h,
    fill: { color: CREAM }, line: { color: CREAM_BORDER, width: 1 },
  });

  // Right equation image
  s.addImage({
    path: BUILD_DIR + row.rightEq,
    x: row.right.x + 0.1, y: row.y + 0.1,
    w: row.right.w - 0.2,
  });
});

pres.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_023_recreated.pptx"
}).then(() => console.log("wrote slide_023_recreated.pptx"));