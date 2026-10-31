const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";
const RED = "C00000";      // house frame
const RED2 = "FF0000";     // original slide's bright-red accents
const DRED = "8B2E3A";     // measured dark maroon (outer rect, title text)
const BLUE = "6666CC";     // measured blue grid/borders
const CELLBLUE = "2020C0"; // measured matrix TP/TN glyph blue
const GREEN = "A9D08E";
const YELLOW = "FFF9C4";
const DARK = "333333";
const BLACK = "000000";
const FONT = "Arial";

const P = (px) => px / 72; // 960x540 frame, 1px = 1pt = 1/72 in
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets/";

let s = pptx.addSlide();
s.background = { color: BG };

// ============================================================
// HOUSE CHROME (root AGENTS.md 2026-10-09 — overrides everything)
// ============================================================
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("32", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// (house title text is added LAST so content panels never cover it)

// ============================================================
// ORIGINAL CONTENT (measured from unique_slides/slide_032.jpg)
// ============================================================

// white content canvas (original slide interior is white)
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(43), y: P(43), w: P(902 - 43), h: P(516 - 43),
  fill: { color: "FFFFFF" }, line: { type: "none" },
});

// outer dark-maroon border of the left+middle region: x[58,635] y[48,517]
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(58), y: P(48), w: P(635 - 58), h: P(517 - 48),
  fill: { type: "none" }, line: { color: DRED, width: 2 },
});

// blue graph-paper grid lines (measured extents)
const gridV = [[342, 43, 507]];
const gridH = [
  [80, 342, 894],
  [162, 70, 895],
  [288, 63, 895],
  [386, 342, 895],
  [400, 61, 634],
];
for (const [x, y0, y1] of gridV) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(x), y: P(y0), w: P(2), h: P(y1 - y0),
    fill: { color: BLUE }, line: { type: "none" },
  });
}
for (const [y, x0, x1] of gridH) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(x0), y: P(y), w: P(x1 - x0), h: P(2),
    fill: { color: BLUE }, line: { type: "none" },
  });
}

// ---------- four threshold panels in the left column ----------
const bands = [48, 162, 288, 403];
const panels = [
  { th: "Threshold=0.0", tp: "5", fn: "0", fp: "6", tn: "0", tpr: "TPR=5/(5+0)=1", fpr: "FPR=6/(6+0)=1" },
  { th: "Threshold=0.1", tp: "5", fn: "0", fp: "4", tn: "2", tpr: "TPR=5/(5+0)=1", fpr: "FPR=4/(4+2)=.66" },
  { th: "Threshold=0.3", tp: "5", fn: "0", fp: "2", tn: "4", tpr: "TPR=5/(5+0)=1", fpr: "FPR=2/(2+4)=.33" },
  { th: "Threshold=0.4", tp: "4", fn: "1", fp: "1", tn: "5", tpr: "TPR=4/(4+1)=4/5", fpr: "FPR=1/(1+5)=.16" },
];

panels.forEach((p, i) => {
  const T = bands[i];

  // threshold label in a thin red-bordered pale-yellow box x[61,160] (single line)
  const labY = T + 2;
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(61), y: P(labY), w: P(160 - 61), h: P(28),
    fill: { color: "FFF9C4" }, line: { color: RED2, width: 1 },
  });
  s.addText(p.th, {
    x: P(61), y: P(labY), w: P(160 - 61), h: P(28),
    align: "center", valign: "middle",
    fontSize: 9, bold: true, color: RED2, fontFace: FONT, margin: 0,
  });

  // rotated vertical "Actual" label on the far left
  s.addText("Actual", {
    x: P(61), y: P(T + 65), w: P(13), h: P(T + 109 - (T + 65)),
    align: "center", valign: "middle",
    fontSize: 9, color: RED2, fontFace: FONT, margin: 0,
    vert: "vert270",
  });

  // "Predicted as" header centered above the P/N columns
  s.addText("Predicted as", {
    x: P(113), y: P(T + 33), w: P(102), h: P(12),
    align: "center", valign: "middle",
    fontSize: 9, bold: true, color: BLACK, fontFace: FONT, margin: 0,
  });

  // full 3x3 red-bordered matrix: corner col x[80,113], P col x[113,166],
  // N col x[166,215]; header row y[T+50,T+63], row P y[T+63,T+86], row N y[T+86,T+109]
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(80), y: P(T + 50), w: P(215 - 80), h: P(109 - 50),
    fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 },
  });
  for (const cx of [113, 166]) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: P(cx), y: P(T + 50), w: P(1.5), h: P(109 - 50),
      fill: { color: RED2 }, line: { type: "none" },
    });
  }
  for (const ry of [T + 63, T + 86]) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: P(80), y: P(ry), w: P(215 - 80), h: P(1.5),
      fill: { color: RED2 }, line: { type: "none" },
    });
  }

  // bordered header cells P / N (header row), bordered row-label cells P / N
  const hcell = (x, y, w, h, txt, color, bold) => s.addText(txt, {
    x: P(x), y: P(y), w: P(w), h: P(h),
    align: "center", valign: "middle",
    fontSize: 9, bold: bold, color: color, fontFace: FONT, margin: 0,
  });
  hcell(113, T + 50, 53, 13, "P", BLACK, false);
  hcell(166, T + 50, 49, 13, "N", BLACK, false);
  hcell(80, T + 63, 33, 23, "P", BLACK, false);
  hcell(80, T + 86, 33, 23, "N", BLACK, false);

  // cell digits: TP/TN blue (correct), FN/FP red (errors) — measured glyph colors
  const cell = (x, y, txt, color) => s.addText(txt, {
    x: P(x), y: P(y), w: P(40), h: P(13),
    align: "center", valign: "middle",
    fontSize: 10, bold: true, color: color, fontFace: FONT, margin: 0,
  });
  cell(120, T + 70, p.tp, CELLBLUE);  // (P,P)
  cell(168, T + 70, p.fn, RED2);      // (P,N)
  cell(120, T + 93, p.fp, RED2);      // (N,P)
  cell(168, T + 93, p.tn, CELLBLUE);  // (N,N)

  // TPR/FPR calc pair in a thin red-bordered pale-yellow box x[224,333]
  const boxY = i === 0 ? T + 50 : (i === 1 ? 218 : i === 2 ? 332 : 449);
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(224), y: P(boxY), w: P(333 - 224), h: P(49),
    fill: { color: "FFF9C4" }, line: { color: RED2, width: 1 },
  });
  s.addText([
    { text: p.tpr, options: { fontSize: 9, color: DRED, fontFace: FONT, breakLine: true } },
    { text: p.fpr, options: { fontSize: 9, color: BLUE, fontFace: FONT, breakLine: true } },
  ], {
    x: P(226), y: P(boxY), w: P(333 - 226), h: P(49),
    align: "left", valign: "middle", margin: 0, lineSpacing: 20,
  });
});

// ---------- ROC plot (right-top): blue border + generated PNG ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(641), y: P(80), w: P(895 - 641), h: P(386 - 80),
  fill: { type: "none" }, line: { color: BLUE, width: 2 },
});
// roc_032_v5.png 2233x2891 px at 600dpi; box x[634,902] y[43,390]
s.addImage({
  path: NS + "roc_032_v5.png",
  x: P(634), y: P(43), w: 2233 / 600, h: 2891 / 600,
});

// ---------- center-bottom title box: blue border, maroon 2-line text ----------
// x[354,621] y[426,474]
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(354), y: P(426), w: P(621 - 354), h: P(474 - 426),
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 2 },
});
s.addText([
  { text: "ROC Curve for", options: { fontSize: 13, bold: true, color: DRED, fontFace: FONT, breakLine: true } },
  { text: "Same Model -different thresholds", options: { fontSize: 13, bold: true, color: DRED, fontFace: FONT, breakLine: true } },
], {
  x: P(354), y: P(426), w: P(621 - 354), h: P(474 - 426),
  align: "center", valign: "middle", margin: 0, lineSpacing: 16,
});

// ---------- bottom-right: TPR/FPR definition equations in red boxes ----------
// eq PNGs 634x296 / 622x296 px at 600dpi; boxes x[651,748] y[417,455] / y[466,503]
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(651), y: P(417), w: P(748 - 651), h: P(455 - 417),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 },
});
s.addImage({
  path: NS + "eq_032_tpr_v4.png",
  x: P(655), y: P(420), w: 634 / 600, h: 296 / 600,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(651), y: P(466), w: P(748 - 651), h: P(503 - 466),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 },
});
s.addImage({
  path: NS + "eq_032_fpr_v4.png",
  x: P(655), y: P(469), w: 622 / 600, h: 296 / 600,
});

// ---------- bottom-right legend matrix x[771,886] y[438,499] ----------
const LX = 771, LY = 438, LW = 886 - 771, LH = 499 - 438;
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(LX), y: P(LY), w: P(LW), h: P(LH),
  fill: { color: "FFFFFF" }, line: { color: RED2, width: 1 },
});
// grid: corner col x[771,800], P col x[800,844], N col x[844,886];
// header rows y[438,460], row P y[460,479], row N y[479,499]
for (const cx of [800, 844]) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(cx), y: P(LY), w: P(1.5), h: P(LH),
    fill: { color: RED2 }, line: { type: "none" },
  });
}
for (const ry of [460, 479]) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: P(LX), y: P(ry), w: P(LW), h: P(1.5),
    fill: { color: RED2 }, line: { type: "none" },
  });
}
s.addText("Predicted as", {
  x: P(800), y: P(LY), w: P(886 - 800), h: P(460 - LY),
  align: "center", valign: "middle", fontSize: 7, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});
s.addText("Actual", {
  x: P(757), y: P(460), w: P(12), h: P(LH - 22),
  align: "center", valign: "middle", fontSize: 7, color: RED2, fontFace: FONT, margin: 0,
  vert: "vert270",
});
const lcell = (x, y, w, h, txt, color, bold) => s.addText(txt, {
  x: P(x), y: P(y), w: P(w), h: P(h),
  align: "center", valign: "middle",
  fontSize: 8, bold: bold, color: color, fontFace: FONT, margin: 0,
});
lcell(786, 460, 14, 19, "P", BLACK, false);
lcell(786, 479, 14, 20, "N", BLACK, false);
// green fills TP (row P, col P) and TN (row N, col N)
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(801.5), y: P(461.5), w: P(844 - 801.5), h: P(479 - 461.5),
  fill: { color: GREEN }, line: { type: "none" },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: P(845.5), y: P(480.5), w: P(886 - 845.5), h: P(499 - 480.5),
  fill: { color: GREEN }, line: { type: "none" },
});
lcell(800, 460, 44, 19, "TP", "006400", true);
lcell(844, 460, 42, 19, "FN", BLACK, true);
lcell(800, 479, 44, 20, "FP", BLACK, true);
lcell(844, 479, 42, 20, "TN", "006400", true);

// house title on top of all content panels (17pt top-anchored: glyphs stay above
// the content border at y=48px so no ink crosses inner frame lines)
s.addText("ROC Curve for Same Model -different thresholds", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  align: "center", valign: "top",
  fontSize: 17, bold: true, color: RED, fontFace: FONT, margin: 0,
});

pptx.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_032_recreated.pptx",
});
console.log("written slide_032_recreated.pptx");
