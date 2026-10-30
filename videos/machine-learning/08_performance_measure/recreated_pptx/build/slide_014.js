const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLACK = "000000";
const WHITE = "FFFFFF";
const NODE_RED = "A00000";
const NODE_GREEN = "0E8640";
const NAVY = "1F3864";
const DARK_BLUE = "1F4E79";
const BORDER = "882433";      // dark-red panel/box borders measured on the frame
const GREEN_HDR = "375623";
const PURPLE = "5B2C86";
const FONT = "Arial";

const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";

const PX = 1 / 72;
const px = (v) => v * PX;
const rect = (x, y, w, h) => ({ x: px(x), y: px(y), w: px(w), h: px(h) });

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME (root AGENTS.md 2026-10-09 — overrides original)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 }
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 }
});
s.addText("14", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0
});
s.addText("Combine Precision and Recall in one number", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0
});

// ============================================================
// TWO PANELS (original: L x68-413, R x423-768, y113-516)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, { ...rect(68, 113, 345, 403), fill: { color: WHITE }, line: { color: BORDER, width: 1 } });
s.addShape(pptx.shapes.RECTANGLE, { ...rect(423, 113, 345, 403), fill: { color: WHITE }, line: { color: BORDER, width: 1 } });

// headers Positive / Negative (original y118-135)
const hdr = (x, label, color) => s.addText(label, {
  ...rect(x, 115, 76, 22), align: "center", valign: "middle",
  fontSize: 13, bold: true, color, fontFace: FONT, margin: 0
});
hdr(129, "Positive", RED);
hdr(307, "Negative", NODE_GREEN);
hdr(484, "Positive", RED);
hdr(662, "Negative", NODE_GREEN);

// airplane silhouettes cropped from the original frame (exact pixels)
s.addImage({ path: ASSETS + "/plane_014_L1.png", ...rect(120, 141, 89, 32) });
s.addImage({ path: ASSETS + "/plane_014_L2.png", ...rect(296, 143, 91, 30) });
s.addImage({ path: ASSETS + "/plane_014_R1.png", ...rect(476, 141, 87, 32) });
s.addImage({ path: ASSETS + "/plane_014_R2.png", ...rect(652, 143, 90, 30) });

// ============================================================
// TREE CONNECTORS (navy lines, drawn before the circles)
// ============================================================
const line = (x1, y1, x2, y2) => {
  const o = {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    line: { color: NAVY, width: 1.5 }
  };
  if (x2 < x1) o.flipH = true;
  if (y2 < y1) o.flipV = true;
  s.addShape(pptx.shapes.LINE, o);
};
// left tree: 30 -> 20(TP), 10(FN); 70 -> 59(TN), 11(FP)
line(151, 231, 105.5, 262.5);
line(151, 231, 193, 262.5);
line(331, 231, 286, 262.5);
line(331, 231, 377.5, 262.5);
// right tree: 30 -> 30(TP), 0(FN); 70 -> 0(TN), 70(FP)
line(506, 231, 460.5, 262.5);
line(506, 231, 548, 262.5);
line(687, 231, 641.5, 262.5);
line(687, 231, 733, 262.5);

// ============================================================
// TREE NODES (circles d=32px, white bold numerals) + class labels
// ============================================================
const node = (cx, cy, label, color) => {
  s.addShape(pptx.shapes.OVAL, {
    ...rect(cx - 16, cy - 16, 32, 32),
    fill: { color }, line: { color }
  });
  s.addText(label, {
    ...rect(cx - 16, cy - 16, 32, 32),
    align: "center", valign: "middle",
    fontSize: 11, bold: true, color: WHITE, fontFace: FONT, margin: 0
  });
};
const tag = (cx, label, color) => s.addText(label, {
  ...rect(cx - 20, 296, 40, 20), align: "center", valign: "middle",
  fontSize: 10, bold: true, color, fontFace: FONT, margin: 0
});
// left panel
node(151, 215, "30", NODE_RED);
node(331, 215, "70", NODE_GREEN);
node(105.5, 278.5, "20", NODE_RED);   tag(105.5, "TP", RED);
node(193, 278.5, "10", NODE_GREEN);   tag(193, "FN", NODE_GREEN);
node(286, 278.5, "59", NODE_GREEN);   tag(286, "TN", NODE_GREEN);
node(377.5, 278.5, "11", NODE_RED);   tag(377.5, "FP", RED);
// right panel
node(506, 215, "30", NODE_RED);
node(687, 215, "70", NODE_GREEN);
node(460.5, 278.5, "30", NODE_RED);   tag(460.5, "TP", RED);
node(548, 278, "0", NODE_GREEN);      tag(548, "FN", NODE_GREEN);
node(641.5, 278, "0", NODE_GREEN);    tag(641.5, "TN", NODE_GREEN);
node(733, 278.5, "70", NODE_RED);     tag(733, "FP", RED);

// ============================================================
// DESCRIPTION BOXES (original y324-395)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, { ...rect(68, 324, 345, 71), fill: { color: "E2F0D9" }, line: { color: BORDER, width: 1 } });
s.addText("Good Model:", {
  ...rect(80, 334, 250, 18), fontSize: 12, bold: true, color: GREEN_HDR, fontFace: FONT, margin: 0, valign: "middle"
});
s.addText("Properly Classifies 20 out of 30 as Positive", {
  ...rect(80, 353, 320, 18), fontSize: 10.5, color: BLACK, fontFace: FONT, margin: 0, valign: "middle"
});
s.addText("Properly Classifies 59 out of 70 as Negative", {
  ...rect(80, 370, 320, 18), fontSize: 10.5, color: BLACK, fontFace: FONT, margin: 0, valign: "middle"
});

s.addShape(pptx.shapes.RECTANGLE, { ...rect(423, 324, 345, 71), fill: { color: "F9E4CF" }, line: { color: BORDER, width: 1 } });
s.addText("Actually:", {
  ...rect(429, 334, 250, 18), fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0, valign: "middle"
});
s.addText([
  { text: "This is ", options: { color: BLACK } },
  { text: "Not a Model", options: { color: RED, bold: true } },
  { text: ":", options: { color: BLACK } }
], {
  ...rect(429, 353, 320, 18), fontSize: 10.5, fontFace: FONT, margin: 0, valign: "middle"
});
s.addText("It classifies ALL Samples as Positive", {
  ...rect(429, 370, 320, 18), fontSize: 10.5, color: BLACK, fontFace: FONT, margin: 0, valign: "middle"
});

// ============================================================
// EQUATION ROWS (gray strip y396-516, three white rows per panel)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, { ...rect(68, 396, 345, 120), fill: { color: "E8E8E8" } });
s.addShape(pptx.shapes.RECTANGLE, { ...rect(423, 396, 345, 120), fill: { color: "E8E8E8" } });
const eqRow = (x, y, h) =>
  s.addShape(pptx.shapes.RECTANGLE, { ...rect(x, y, 345, h), fill: { color: WHITE }, line: { color: "BFBFBF", width: 0.75 } });
eqRow(68, 401, 23); eqRow(68, 440, 24); eqRow(68, 482, 28);
eqRow(423, 401, 23); eqRow(423, 440, 24); eqRow(423, 482, 28);

const eqText = (x, y, h, text) => s.addText(text, {
  ...rect(x, y, 330, h), fontSize: 11, color: BLACK, fontFace: FONT, margin: 0, valign: "middle"
});
eqText(92, 401, 23, "Precision= 20/(20+11) =64.5%");
eqText(92, 440, 24, "Recall= 20/(20+10) =66.6%");
eqText(92, 482, 28, "Average= 64.5%+66.6% =65.55%");
eqText(448, 401, 23, "Precision= 30/(30+70) =30.3%");
eqText(448, 440, 24, "Recall= 30/(30+0) =100%");
eqText(448, 482, 28, "Average= 30.3%+100% =65%");

// ============================================================
// BLUE REFERENCE FORMULA BOXES (original x749-896; box1 y122-168, box2 y168-228)
// stacked 2D fractions TP/(TP+FP) and TP/(TP+FN)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, { ...rect(749, 122, 147, 46), fill: { color: "FDFBCB" }, line: { color: NAVY, width: 1 } });
s.addText("Precision =", {
  ...rect(756, 127, 62, 14), fontSize: 10, bold: true, color: DARK_BLUE, fontFace: FONT, margin: 0, valign: "middle"
});
s.addText("TP", {
  ...rect(826, 126, 44, 12), align: "center", fontSize: 10, color: DARK_BLUE, fontFace: FONT, margin: 0, valign: "middle"
});
s.addShape(pptx.shapes.RECTANGLE, { ...rect(822, 140, 52, 2), fill: { color: DARK_BLUE } });
s.addText("TP+FP", {
  ...rect(822, 143, 52, 13), align: "center", fontSize: 10, color: DARK_BLUE, fontFace: FONT, margin: 0, valign: "middle"
});

s.addShape(pptx.shapes.RECTANGLE, { ...rect(749, 168, 147, 60), fill: { color: "D3FFFE" }, line: { color: NAVY, width: 1 } });
s.addText("Recall =", {
  ...rect(756, 180, 62, 14), fontSize: 10, bold: true, color: DARK_BLUE, fontFace: FONT, margin: 0, valign: "middle"
});
s.addText("TP", {
  ...rect(826, 182, 44, 12), align: "center", fontSize: 10, color: DARK_BLUE, fontFace: FONT, margin: 0, valign: "middle"
});
s.addShape(pptx.shapes.RECTANGLE, { ...rect(822, 198, 52, 2), fill: { color: DARK_BLUE } });
s.addText("TP+FN", {
  ...rect(822, 201, 52, 13), align: "center", fontSize: 10, color: DARK_BLUE, fontFace: FONT, margin: 0, valign: "middle"
});

// ============================================================
// CONCLUSION BOX (original x737-895, y430-484)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, { ...rect(737, 430, 158, 54), fill: { color: "F9DCFA" }, line: { color: "7030A0", width: 1 } });
s.addText("Conclusion:", {
  ...rect(745, 433, 145, 13), fontSize: 11, bold: true, color: PURPLE, fontFace: FONT, margin: 0, valign: "middle"
});
s.addText("Average", {
  ...rect(745, 449, 145, 13), fontSize: 10, bold: true, italic: true, color: PURPLE, fontFace: FONT, margin: 0, valign: "middle"
});
s.addText("is NOT good idea", {
  ...rect(745, 465, 145, 14), fontSize: 10, bold: true, color: BLACK, fontFace: FONT, margin: 0, valign: "middle"
});

const outFile = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_014_recreated.pptx";
pptx.writeFile({ fileName: outFile }).then(() => console.log("done"));
