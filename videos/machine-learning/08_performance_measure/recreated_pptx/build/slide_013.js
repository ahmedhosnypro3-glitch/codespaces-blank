const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", YELLOW = "FFF9C4", INK = "333333";
const FONT = "Arial";
const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets";
const P = (px) => px / 72; // original frame 960x540, 1px = 1pt = 1/72 in

let s = pptx.addSlide();
s.background = { color: BG };

// House frame
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
// Badge "13"
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("13", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
// Title
s.addText("Combine Precision and Recall in one number", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "middle",
  fontSize: 33, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- Diagram container: red border x68-413 y113-324 ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(68), y: P(113), w: P(345), h: P(211),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 },
});

// Section headers
s.addText("Positive", {
  x: P(120), y: P(118), w: P(90), h: P(22), align: "center",
  fontSize: 15, bold: true, color: "A52A2A", fontFace: FONT, margin: 0,
});
s.addText("Negative", {
  x: P(290), y: P(118), w: P(90), h: P(22), align: "center",
  fontSize: 15, bold: true, color: "2E7D32", fontFace: FONT, margin: 0,
});

// Airplane icons above parent nodes (parent centers x150.5 and x331.5, y215.5)
s.addImage({ path: `${ASSETS}/airplane_013.png`, x: P(150.5) - P(85) / 2, y: P(146), w: P(85), h: P(52) });
s.addImage({ path: `${ASSETS}/airplane_013.png`, x: P(331.5) - P(85) / 2, y: P(146), w: P(85), h: P(52) });

// Parent nodes: 30 dark red (c 150.5,215.5 d33), 70 dark green (c 331.5,215 d33)
function node(cx, cy, d, fill, label) {
  s.addShape(pptx.shapes.OVAL, {
    x: P(cx) - P(d) / 2, y: P(cy) - P(d) / 2, w: P(d), h: P(d),
    fill: { color: fill }, line: { color: fill, width: 1 },
  });
  s.addText(label, {
    x: P(cx) - P(d) / 2, y: P(cy) - P(d) / 2, w: P(d), h: P(d),
    align: "center", valign: "middle",
    fontSize: 14, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
}
node(150.5, 215.5, 33, "8B0000", "30");
node(331.5, 215, 33, "006400", "70");
// Children: 20 red c(105,278); 10 green c(193,278); 59 green c(286,278); 11 red c(377,278.5)
node(105, 278, 32, "E00000", "20");
node(193, 278, 32, "00B050", "10");
node(286, 278, 32, "00B050", "59");
node(377, 278.5, 32, "E00000", "11");

// Short blue parent->child connectors with arrowheads at the child circle edge (drawn on top of nodes)
// pptxgenjs LINE renders the bbox TL->BR diagonal by default; down-left strokes need flipH
function arrow(x1, y1, r1, x2, y2, r2) {
  const dx = x2 - x1, dy = y2 - y1;
  const len = Math.hypot(dx, dy);
  const ux = dx / len, uy = dy / len;
  const sx = x1 + ux * (r1 - 2), sy = y1 + uy * (r1 - 2);
  const ex = x2 - ux * (r2 + 1), ey = y2 - uy * (r2 + 1);
  const opts = {
    x: P(Math.min(sx, ex)), y: P(Math.min(sy, ey)),
    w: P(Math.abs(ex - sx)), h: P(Math.abs(ey - sy)),
    line: { color: "0000FF", width: 1.5, endArrowType: "triangle" },
  };
  if (dx < 0) opts.flipH = true;
  s.addShape(pptx.shapes.LINE, opts);
}
arrow(150.5, 215.5, 16.5, 105, 278, 16);
arrow(150.5, 215.5, 16.5, 193, 278, 16);
arrow(331.5, 215, 16.5, 286, 278, 16);
arrow(331.5, 215, 16.5, 377, 278.5, 16);

// Leaf captions TP/FN/TN/FP in red below children
function caption(cx, label) {
  s.addText(label, {
    x: P(cx) - P(29), y: P(296), w: P(58), h: P(20), align: "center",
    fontSize: 13, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
}
caption(105, "TP"); caption(193, "FN"); caption(286, "TN"); caption(377, "FP");



// ---- Top-right formula boxes ----
// Precision: x749-897 y124-166 yellow rounded; Recall: x748-896 y184-227 blue rounded
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(749), y: P(124), w: P(148), h: P(42),
  fill: { color: "FFF2CC" }, line: { color: "BF9000", width: 1 }, round: 0.08,
});
s.addText("Precision =", {
  x: P(752), y: P(136), w: P(82), h: P(20), valign: "middle",
  fontSize: 12, color: TEXT, fontFace: FONT, margin: 0,
});
s.addImage({ path: `${ASSETS}/eq_013_prec.png`, x: P(836), y: P(133), w: 0.65833, h: 0.33 });

s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: P(748), y: P(184), w: P(148), h: P(43),
  fill: { color: "CFE2F3" }, line: { color: "2E75B6", width: 1 }, round: 0.08,
});
s.addText("Recall =", {
  x: P(752), y: P(196), w: P(72), h: P(20), valign: "middle",
  fontSize: 12, color: TEXT, fontFace: FONT, margin: 0,
});
s.addImage({ path: `${ASSETS}/eq_013_rec.png`, x: P(826), y: P(193), w: 0.68333, h: 0.33 });

// ---- Good Model box: green border x68-413 y329-395, light green fill ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(76), y: P(334), w: P(304), h: P(58),
  fill: { color: "FFFFFF" }, line: { color: "008000", width: 1.5 },
});
s.addText("Good Model:", {
  x: P(84), y: P(337), w: P(160), h: P(17),
  fontSize: 14, bold: true, color: "008000", fontFace: FONT, margin: 0,
});
s.addText("Properly Classifies 20 out of 30 as Positive", {
  x: P(84), y: P(355), w: P(290), h: P(15),
  fontSize: 13, color: TEXT, fontFace: FONT, margin: 0,
});
s.addText("Properly Classifies 59 out of 70 as Negative", {
  x: P(84), y: P(372), w: P(290), h: P(15),
  fontSize: 13, color: TEXT, fontFace: FONT, margin: 0,
});

// ---- Bottom calculation boxes x70-908; P y398-426 yellow, R y434-466 blue, A y477-509 blue ----
function calcBox(y, h, fill) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(76), y: P(y), w: P(275), h: P(h),
    fill: { color: fill }, line: { color: "BFBFBF", width: 0.5 },
  });
}
function calcLine(y, h, label, result) {
  s.addText([
    { text: label, options: { fontSize: 13, color: TEXT, fontFace: FONT } },
    { text: result, options: { fontSize: 13, color: "000060", fontFace: FONT, bold: true } },
  ], {
    x: P(88), y: P(y), w: P(255), h: P(h), valign: "middle", margin: 0,
  });
}
calcBox(398, 28, "FFF2CC");
calcLine(400, 24, "Precision= 20/(20+11) ", "=64.5%");
calcBox(434, 32, "CFE2F3");
calcLine(436, 28, "Recall= 20/(20+10) ", "=66.6%");
calcBox(477, 32, "CFE2F3");
calcLine(479, 28, "Average= 68.7%+60% ", "=65.55%");

const outPath = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_013_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done"));
