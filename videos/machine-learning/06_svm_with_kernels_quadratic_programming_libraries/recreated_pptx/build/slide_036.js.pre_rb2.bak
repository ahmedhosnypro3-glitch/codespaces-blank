const pptxgen = require("pptxgenjs");
const fs = require("fs");

// Slide 036 — FRESH rebuild (wave 3) from qa/reanalysis2/slide_036_analysis.txt ONLY.
// Spec: "How to Kernelize SVM" — two white/blue panels with primal vs kernelized
// dual equations (2-D mathtext PNGs), center "Kernelize using" + K(a,b)=(a^T b)^2
// boxes with red down arrow, two peach class-of-vector boxes.
// Run: cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_036.js

const NUM = 36;
const FONT = "Arial";
const W = 13.33, H = 7.5;
const BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = BASE + "/recreated_pptx/build/eq_036/";
const OUT = BASE + "/recreated_pptx/slide_036_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// ---- house chrome (mandatory, overrides spec geometry) ----
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("How to Kernelize SVM", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---- helpers ----
const X = n => n * 13.33, Y = n => n * 7.5;
function box(x0, y0, x1, y1, fill, line, shape) {
  s.addShape(shape || pres.shapes.RECTANGLE, {
    x: X(x0), y: Y(y0), w: X(x1 - x0), h: Y(y1 - y0),
    fill: { color: fill }, line: { color: line, width: 1.25 },
  });
}
function img(name, x, y) {
  const m = JSON.parse(fs.readFileSync(EQ + name + ".png.json"));
  s.addImage({ path: EQ + name + ".png", x, y, w: m.w_in, h: m.h_in });
  return m;
}
function imgIn(name, x0n, y0n, wN, hN) { // centered inside a normalized box
  const m = JSON.parse(fs.readFileSync(EQ + name + ".png.json"));
  s.addImage({
    path: EQ + name + ".png",
    x: X(x0n) + (X(wN) - m.w_in) / 2, y: Y(y0n) + (Y(hN) - m.h_in) / 2,
    w: m.w_in, h: m.h_in,
  });
  return m;
}
// wide text box at spec y (lesson from slide 001 judge FAIL: never narrow boxes)
function cline(ynorm, text, size, color, extra) {
  s.addText(text, {
    x: 0.6, y: Y(ynorm), w: 12.13, h: 0.42,
    align: "center", valign: "top", fontSize: size, color, fontFace: FONT,
    margin: 0, ...(extra || {}),
  });
}

// ---- header: "Example: Quadratic Kernel" rounded label [0.06,0.08,0.32,0.14] ----
box(0.06, 0.08, 0.32, 0.14, "FFFFFF", "3333CC", pres.shapes.ROUNDED_RECTANGLE);
s.addText("Example: Quadratic Kernel", {
  x: X(0.06), y: Y(0.085), w: X(0.26), h: Y(0.05),
  align: "center", valign: "middle",
  fontSize: 12, italic: true, color: "0000FF", fontFace: FONT, margin: 0,
});

// ---- top panel [0.05,0.23,0.96,0.46] + bottom panel [0.05,0.59,0.96,0.87] ----
box(0.05, 0.23, 0.96, 0.46, "FFFFFF", "3333CC");
box(0.05, 0.59, 0.96, 0.87, "FFFFFF", "3333CC");
// ---- peach class-of-vector boxes (drawn before the white center boxes) ----
box(0.12, 0.47, 0.88, 0.51, "FFDAB9", "800000");
box(0.12, 0.83, 0.88, 0.87, "FFDAB9", "800000");

// ---- center: "Kernelize using" box + kernel equation box + red down arrow ----
box(0.28, 0.47, 0.42, 0.54, "FFFFFF", "800000");
s.addText("Kernelize using", {
  x: X(0.28), y: Y(0.47), w: X(0.14), h: Y(0.07),
  align: "center", valign: "middle",
  fontSize: 12, color: "FF0000", fontFace: FONT, margin: 0,
});
box(0.59, 0.48, 0.71, 0.54, "FFFFFF", "800000");
imgIn("f36_kern", 0.59, 0.48, 0.12, 0.06);
s.addShape(pres.shapes.DOWN_ARROW, {
  x: X(0.43), y: Y(0.48), w: X(0.04), h: Y(0.10),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0.5 },
});

// ---- top panel equations (spec boxes [0.08,0.24,0.92,0.31] / [0.08|0.38,0.32,...]) ----
img("f36_lag_top", X(0.08), 1.80);
img("f36_w", X(0.08), 2.42);
const bTop = JSON.parse(fs.readFileSync(EQ + "f36_b_top.png.json"));
img("f36_b_top", X(0.38), 2.42 + (0.50 - bTop.h_in) / 2);

// ---- bottom panel: green highlight on the squared kernel term, then equations ----
const lagBot = JSON.parse(fs.readFileSync(EQ + "f36_lag_bot.png.json"));
const lagBotX = X(0.08), lagBotY = 4.50;
const TAIL_W = 1.1667, PAD = 8 / 600; // tail seg [X_i^T X_j]^2 width at 24pt, render PAD_PX
const tailX0 = lagBot.w_in - PAD - TAIL_W;
s.addShape(pres.shapes.RECTANGLE, {
  x: lagBotX + tailX0 - 0.03, y: lagBotY, w: TAIL_W + 0.06, h: lagBot.h_in,
  fill: { color: "90EE90" }, line: { color: "90EE90", width: 0 },
});
img("f36_lag_bot", lagBotX, lagBotY);
img("f36_w", X(0.08), 5.325);
const bBot = JSON.parse(fs.readFileSync(EQ + "f36_b_bot.png.json"));
img("f36_b_bot", X(0.38), 5.325 + (0.50 - bBot.h_in) / 2);

// ---- class-of-vector lines inside the peach boxes ----
imgIn("f36_cls_top", 0.12, 0.47, 0.76, 0.04);
imgIn("f36_cls_bot", 0.12, 0.83, 0.76, 0.04);

pres.writeFile({ fileName: OUT })
  .then(() => console.log("wrote " + OUT))
  .catch(e => { console.error(e); process.exit(1); });
