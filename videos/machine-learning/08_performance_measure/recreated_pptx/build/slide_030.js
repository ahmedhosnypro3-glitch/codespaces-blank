const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";
const ASSETS = NS + "/recreated_pptx/build/assets";
const BG = "E8E8E8", RED = "C00000", BLUE = "0000FF", DBLUE = "0000CC", INK = "000000";
const PINK = "FBD5D5", GREEN = "C6EFCE", PINK2 = "FFCCCC", BADGE = "FFF9C4", NUM = "333333";
const FONT = "Arial";

// frame px -> inches (960x540 frame, 1px = 1pt = 1/72 in)
const X = (px) => px / 72, Y = (px) => px / 72, W = (px) => px / 72, H = (px) => px / 72;

let s = pptx.addSlide();
s.background = { color: BG };

// --- HOUSE CHROME (root AGENTS.md, overrides everything) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 }
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 }
});
s.addText("30", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.5, align: "center", valign: "middle",
  fontSize: 26, bold: true, color: RED, fontFace: FONT, margin: 0
});

// --- BLUE STRUCTURAL GRID (measured from frame) ---
// left block outer rect x[61,634] y[51,507]
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(61), y: Y(51), w: W(634 - 61), h: H(507 - 51),
  fill: { color: "FFFFFF" }, line: { color: DBLUE, width: 1.25 }
});
// vertical divider x=342 full height of left block
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(342) - 0.008, y: Y(51), w: 0.016, h: H(507 - 51),
  fill: { color: DBLUE }, line: { color: DBLUE, width: 0.25 }
});
// right divider x=641 (plot panel edge overlays y81..387)
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(641) - 0.008, y: Y(51), w: 0.016, h: H(507 - 51),
  fill: { color: DBLUE }, line: { color: DBLUE, width: 0.25 }
});
// horizontal dividers y=288 and y=401 across left block
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(61), y: Y(288) - 0.008, w: W(634 - 61), h: 0.016,
  fill: { color: DBLUE }, line: { color: DBLUE, width: 0.25 }
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(61), y: Y(401) - 0.008, w: W(895 - 61), h: 0.016,
  fill: { color: DBLUE }, line: { color: DBLUE, width: 0.25 }
});

// --- CONFUSION MATRIX PANEL helper ---
function matrixPanel(px, py, header, cells, metrics) {
  // red-bordered pink panel x[60,341]
  s.addShape(pptx.shapes.RECTANGLE, {
    x: X(60), y: Y(py), w: W(341 - 60), h: H(py === 48 ? 159 - 48 : 283 - 167),
    fill: { color: PINK }, line: { color: RED, width: 1.5 }
  });
  s.addText(header, {
    x: X(68), y: Y(py + 5), w: W(172 - 68) + 0.6, h: H(24),
    fontSize: 15, bold: true, color: RED, fontFace: FONT, margin: 0
  });
  const tx = px, ty = py === 48 ? 92 : 206;
  s.addTable(
    [
      [{ text: "", options: { fill: { color: PINK } } },
       { text: "Predicted as", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center", colspan: 2 } }],
      [{ text: "Actual", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } },
       { text: "P", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } },
       { text: "N", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } }],
      [{ text: "P", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } },
       { text: cells[0], options: { fill: { color: PINK }, fontSize: 13, color: cells[4], fontFace: FONT, align: "center", bold: true } },
       { text: cells[1], options: { fill: { color: PINK }, fontSize: 13, color: INK, fontFace: FONT, align: "center" } }],
      [{ text: "N", options: { bold: true, fill: { color: PINK }, fontSize: 11, color: INK, fontFace: FONT, align: "center" } },
       { text: cells[2], options: { fill: { color: PINK }, fontSize: 13, color: cells[5], fontFace: FONT, align: "center", bold: true } },
       { text: cells[3], options: { fill: { color: PINK }, fontSize: 13, color: cells[6], fontFace: FONT, align: "center", bold: true } }],
    ],
    {
      x: X(tx), y: Y(ty), w: W(225 - tx), h: H((py === 48 ? 157 : 273) - ty),
      border: { type: "solid", pt: 1, color: RED },
      colW: [W(40), W(40), W(40)],
      rowH: [H(18), H(16), H(24), H(24)],
      margin: 0.02, valign: "middle",
    }
  );
  s.addText(metrics, {
    x: X(264), y: Y(py === 48 ? 108 : 220), w: W(339 - 264), h: H(36),
    fontSize: 10.5, color: INK, fontFace: FONT, margin: 0, lineSpacing: 13
  });
}

matrixPanel(113, 48, "Threshold=0.0", ["5", "0", "6", "0", BLUE, RED, INK],
  [{ text: "TPR=5/(5+0)=1", options: { fontSize: 10.5, color: INK, fontFace: FONT, breakLine: true } },
   { text: "FPR=6/(6+0)=1", options: { fontSize: 10.5, color: INK, fontFace: FONT, breakLine: true } }]);
matrixPanel(113, 167, "Threshold=0.1", ["5", "0", "4", "2", BLUE, RED, BLUE],
  [{ text: "TPR=5/(5+0)=1", options: { fontSize: 10.5, color: INK, fontFace: FONT, breakLine: true } },
   { text: "FPR=4/(4+2)=0.66", options: { fontSize: 10.5, color: INK, fontFace: FONT, breakLine: true } }]);

// --- ROC PLOT (generated matplotlib image, whole panel baked) ---
s.addImage({
  path: ASSETS + "/roc_030.png",
  x: X(641), y: Y(81), w: W(254), h: H(306)
});

// --- TITLE BOX (lower-left, blue outline, pink fill) ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(353), y: Y(426), w: W(622 - 353), h: H(474 - 426),
  fill: { color: PINK }, line: { color: DBLUE, width: 1.25 }
});
s.addText("ROC Curve for Same Model -different thresholds", {
  x: X(358), y: Y(428), w: W(612 - 358), h: H(470 - 428),
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: RED, fontFace: FONT, margin: 0, lineSpacing: 15
});

// --- BOTTOM-RIGHT CELL: pink fill + formula box + legend ---
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(641), y: Y(403), w: W(895 - 641), h: H(507 - 403),
  fill: { color: PINK }, line: { color: DBLUE, width: 1.25 }
});
// formula box (blue outline) around the two definition equations
s.addShape(pptx.shapes.RECTANGLE, {
  x: X(649), y: Y(415), w: W(752 - 649), h: H(500 - 415),
  fill: { color: PINK }, line: { color: DBLUE, width: 1.25 }
});
// drift items: TPR = TP/(TP+FN), FPR = FP/(FP+TN) as professional 2D fractions (600dpi PNG, exact size)
s.addImage({ path: ASSETS + "/eq_030_tpr.png", x: X(656), y: Y(424), w: 728 / 600, h: 230 / 600 });
s.addImage({ path: ASSETS + "/eq_030_fpr.png", x: X(656), y: Y(462), w: 725 / 600, h: 230 / 600 });

// legend 2x2 confusion-matrix key at x[784,869] y[440,500]
s.addTable(
  [
    [{ text: "", options: { fill: { color: PINK } } },
     { text: "Predicted as", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK }, colspan: 2 } }],
    [{ text: "Actual", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } },
     { text: "P", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } },
     { text: "N", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } }],
    [{ text: "P", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } },
     { text: "TP", options: { fontSize: 10, bold: true, color: INK, fontFace: FONT, align: "center", fill: { color: GREEN } } },
     { text: "FN", options: { fontSize: 10, bold: true, color: INK, fontFace: FONT, align: "center", fill: { color: PINK2 } } }],
    [{ text: "N", options: { bold: true, fontSize: 9, color: INK, fontFace: FONT, align: "center", fill: { color: PINK } } },
     { text: "FP", options: { fontSize: 10, bold: true, color: INK, fontFace: FONT, align: "center", fill: { color: PINK2 } } },
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

const outPath = NS + "/recreated_pptx/slide_030_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
