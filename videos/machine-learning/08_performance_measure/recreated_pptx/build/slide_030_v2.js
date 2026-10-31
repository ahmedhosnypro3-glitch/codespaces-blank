const pptxgenpkg = require("pptxgenjs");

// Slide 30 — "ROC Curve for Same Model -different thresholds" (fresh rebuild, agent-s30-fresh).
// Original frame 960x540 px; 1px = 1pt = 1/72 in. Geometry PIL-measured from
// unique_slides/slide_030.jpg:
//   outer RED rect x[59,900] y[48,516] (right/bottom edges JPEG-washed)
//   blue verticals x=342 (left block), x=643 & x=895 (right column y[80,388])
//   blue horizontals y=162, y=288, y=401 spanning left block x[59,635]
//   matrix panels (pink, red border): p1 x[60,341] y[48,159], p2 x[60,341] y[167,283]
//   ROC plot panel x[641,895] y[81,387] (asset roc_030_v2.png, 254x306 px)
//   title box x[353,622] y[426,474] pink fill blue outline
//   bottom-right cell x[641,895] y[403,507]: formula box + legend (green x[811,879] y[460,497])
// Drift items (pool_run/spec_gaps.md slide_030): 2D stacked fractions
//   TPR = TP/(TP+FN) and FPR = FP/(FP+TN) -> eq_030_v2_*.png (600dpi, colored per
//   pool_run/image_analysis/slide_030_analysis.txt: TPR red #C00000, FPR blue #1F497D).
// House chrome (root AGENTS.md 2026-10-09) drawn LAST, overrides per-slide geometry.

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";
const ASSETS = NS + "/recreated_pptx/build/assets";
const BG = "E8E8E8", RED = "C00000", DBLUE = "0000CC", INK = "000000";
const PINK = "FBD5D5", GREEN = "92D050", GREY = "F2F2F2", BADGE = "FFF9C4", NUM = "333333";
const FPRBLUE = "1F497D", PURE_RED = "FF0000", AXBLUE = "0000FF";
const FONT = "Arial";

const X = (px) => px / 72, Y = (px) => px / 72, W = (px) => px / 72, H = (px) => px / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE red frame (root AGENTS.md 2026-10-09) drawn FIRST, fill = bg gray ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 }
});

// --- outer red content rect x[59,900] y[48,516] (fill white) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(59), y: Y(48), w: W(900 - 59), h: H(516 - 48),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 }
});

// --- blue structural lines ---
// vertical x=342 across left block; x=643 is the right column's left edge (plot/cell outline)
s.addShape(pptx.shapes.LINE, { x: X(342), y: Y(48), w: 0, h: H(516 - 48), line: { color: DBLUE, width: 1.25 } });
// horizontals y=162, y=288, y=401 across the left block x[59,635]
for (const gy of [162, 288, 401]) {
  s.addShape(pptx.shapes.LINE, { x: X(59), y: Y(gy), w: W(635 - 59), h: 0, line: { color: DBLUE, width: 1.25 } });
}

// --- confusion matrix panels (pink fill, red border) ---
function matrixPanel(py, hgt, header, cells, tpr, fpr) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: X(60), y: Y(py), w: W(341 - 60), h: H(hgt),
    fill: { color: PINK }, line: { color: RED, width: 1.5 }
  });
  s.addText(header, {
    x: X(68), y: Y(py + 5), w: W(172 - 68) + 0.6, h: H(24),
    fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0
  });
  const tx = 113, ty = py === 48 ? 92 : 206;
  s.addTable(
    [
      [{ text: " ", options: { fill: { color: PINK }, fontSize: 11 } },
       { text: "Predicted as", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center", colspan: 2 } }],
      [{ text: "Actual", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } },
       { text: "P", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } },
       { text: "N", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } }],
      [{ text: "P", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } },
       { text: cells[0], options: { fill: { color: PINK }, fontSize: 13, color: RED, fontFace: FONT, align: "center", bold: true } },
       { text: cells[1], options: { fill: { color: PINK }, fontSize: 13, color: INK, fontFace: FONT, align: "center" } }],
      [{ text: "N", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } },
       { text: cells[2], options: { fill: { color: PINK }, fontSize: 13, color: RED, fontFace: FONT, align: "center", bold: true } },
       { text: cells[3], options: { fill: { color: PINK }, fontSize: 13, color: INK, fontFace: FONT, align: "center", bold: true } }],
    ],
    {
      x: X(tx), y: Y(ty), w: W(225 - tx), h: H((py === 48 ? 157 : 273) - ty),
      border: { type: "solid", pt: 1, color: RED },
      colW: [W(40), W(40), W(40)],
      rowH: [H(18), H(16), H(24), H(24)],
      margin: 0.02, valign: "middle",
    }
  );
  // worked metrics to the right of the matrix: TPR red, FPR blue (image-analysis source of truth)
  s.addText([
    { text: tpr, options: { fontSize: 10.5, color: RED, fontFace: FONT, bold: true, breakLine: true } },
    { text: fpr, options: { fontSize: 10.5, color: FPRBLUE, fontFace: FONT, bold: true, breakLine: true } },
  ], {
    x: X(232), y: Y(py === 48 ? 108 : 220), w: W(339 - 232), h: H(44),
    fontFace: FONT, margin: 0, lineSpacing: 15
  });
}

matrixPanel(48, 159 - 48, "Threshold=0.0", ["5", "0", "6", "0"],
  "TPR=5/(5+0)=1", "FPR=6/(6+0)=1");
matrixPanel(167, 283 - 167, "Threshold=0.1", ["5", "0", "4", "2"],
  "TPR=5/(5+0)=1", "FPR=4/(4+2)=0.66");

// --- ROC plot panel (generated image, whole panel baked) ---
s.addImage({ path: ASSETS + "/roc_030_v2.png", x: X(641), y: Y(81), w: W(254), h: H(306) });

// --- title box (lower-middle cell, pink fill, blue outline) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(353), y: Y(426), w: W(622 - 353), h: H(474 - 426),
  fill: { color: PINK }, line: { color: DBLUE, width: 1.25 }
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: X(358), y: Y(428), w: W(612 - 358), h: H(470 - 428),
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: RED, fontFace: FONT, margin: 0, lineSpacing: 15
});

// --- bottom-right cell: pink fill, blue outline, formula box + legend ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(641), y: Y(403), w: W(895 - 641), h: H(507 - 403),
  fill: { color: PINK }, line: { color: DBLUE, width: 1.25 }
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(649), y: Y(415), w: W(752 - 649), h: H(500 - 415),
  fill: { color: PINK }, line: { color: DBLUE, width: 1.25 }
});
// drift equations as professional 2D fractions (600dpi PNG, exact size)
s.addImage({ path: ASSETS + "/eq_030_v2_tpr.png", x: X(656), y: Y(424), w: 728 / 600, h: 230 / 600 });
s.addImage({ path: ASSETS + "/eq_030_v2_fpr.png", x: X(656), y: Y(462), w: 725 / 600, h: 230 / 600 });

// legend 2x2 confusion-matrix key at x[784,869] y[440,500]; TP/TN green #92D050, FN/FP grey #F2F2F2
s.addTable(
  [
    [{ text: " ", options: { fill: { color: PINK }, fontSize: 9 } },
     { text: "Predicted as", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK }, colspan: 2 } }],
    [{ text: "Actual", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } },
     { text: "P", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } },
     { text: "N", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } }],
    [{ text: "P", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } },
     { text: "TP", options: { fontSize: 10, bold: true, color: INK, fontFace: FONT, align: "center", fill: { color: GREEN } } },
     { text: "FN", options: { fontSize: 10, bold: true, color: INK, fontFace: FONT, align: "center", fill: { color: GREY } } }],
    [{ text: "N", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } },
     { text: "FP", options: { fontSize: 10, bold: true, color: INK, fontFace: FONT, align: "center", fill: { color: GREY } } },
     { text: "TN", options: { fontSize: 10, bold: true, color: INK, fontFace: FONT, align: "center", fill: { color: GREEN } } }],
  ],
  {
    x: X(784), y: Y(440), w: W(869 - 784), h: H(500 - 440),
    border: { type: "solid", pt: 0.75, color: INK },
    colW: [W(22), W(31), W(31)],
    rowH: [H(12), H(11), H(18), H(18)],
    margin: 0.01, valign: "middle",
  }
);

// --- HOUSE badge + title drawn LAST so no content occludes them ---
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("30", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.28, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: RED, fontFace: FONT, margin: 0
});

const outPath = NS + "/recreated_pptx/slide_030_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
