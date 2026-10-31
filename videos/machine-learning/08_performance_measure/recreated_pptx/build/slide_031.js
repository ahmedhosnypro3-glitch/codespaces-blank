// Slide 031 — ROC Curve for Same Model - Different Thresholds (v3, re-measured 2026-10-31)
// Frame-vs-spec notes (PIL-measured from unique_slides/slide_031.jpg, 960x540, 1px=1pt):
// - Original has NO top title; its only title text is the bottom-center caption box.
// - FPR inline values render without leading zero (".66", ".33") per the fresh image-analysis
//   read (pool_run/image_analysis/slide_031_analysis.txt = designated source of truth).
// - Matrix value colors measured from pixels: diagonal (TP, TN) blue, off-diagonal (FN, FP) red.
// - Left panel x58..635 y48..503; blue dividers x344, y163/286/401/475.
// - Caption cell x354..622 y401..476 (blue border), red bold two-line text.
// - ROC plot is a generated matplotlib image (build/assets/slide031_roc.png) at the measured
//   region x642..894 y81..387; circles at (725,148),(809,148),(873,148) with cream-boxed
//   labels 0.3/0.1/0.0, plus the mandated "1.0" label inside the frame at the upper-right
//   corner (spec_gaps slide_031: label '1.0', chart value 1.0).
// - TPR/FPR definition equations rendered as professional 2D stacked fractions (mathtext PNGs)
//   inside the original's red-bordered boxes — spec_gaps drift items.
// - Side TPR line blue, FPR line red (reanalysis typography); rotated "Actual" labels get
//   h>=16 boxes so LibreOffice does not clip them.
const pptxgenpkg = require("pptxgenjs");
const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", NAVY = "1414A0", BLUE = "0000FF",
      INK = "000000", BADGE = "FFF9C4", NUM = "333333", WHITE = "FFFFFF",
      HDRFILL = "FADCC7", GREEN = "8BFF17", PINK = "FFC0CB", TITLEFILL = "EAECEB";
const FONT = "Arial";
const P = (px) => px / 72;           // 1px = 1pt = 1/72 in
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx";

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
s.addText("31", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0
});
// The original frame carries NO top title (its only title text is the bottom-centre box),
// and the left content panel starts at y=48px, so no top-title ink is drawn: the house
// title-box geometry stays free of added ink that would collide with the panel.

// --- helpers ---
function rect(x, y, w, h, fill, lineColor, lineW) {
  const o = { x: P(x), y: P(y), w: P(w), h: P(h), fill: { color: fill } };
  if (lineColor) o.line = { color: lineColor, width: lineW || 1.5 };
  s.addShape(pptx.shapes.RECTANGLE, o);
}
function lineH(x, y, w, color, px) { rect(x, y, w, px || 2, color, null); }
function lineV(x, y, h, color, px) { rect(x, y, px || 2, h, color, null); }
function text(str, cx, cy, wpx, hpx, size, color, opts) {
  opts = opts || {};
  s.addText(str, {
    x: P(cx - wpx / 2), y: P(cy - hpx / 2), w: P(wpx), h: P(hpx),
    align: "center", valign: "middle", fontSize: size, color: color,
    fontFace: FONT, margin: 0, bold: !!opts.bold, italic: !!opts.italic,
    ...(opts.rotate ? { rotate: opts.rotate } : {})
  });
}
function textBox(str, x, y, w, h, size, color, opts) {
  opts = opts || {};
  s.addText(str, {
    x: P(x), y: P(y), w: P(w), h: P(h),
    align: opts.align || "center", valign: opts.valign || "middle",
    fontSize: size, color: color, fontFace: FONT, margin: 0,
    bold: !!opts.bold, italic: !!opts.italic,
    ...(opts.lineSpacing ? { lineSpacing: opts.lineSpacing } : {}),
    ...(opts.rotate ? { rotate: opts.rotate } : {})
  });
}

// --- LEFT PANEL (red border x58..635, y48..503; measured) ---
rect(58, 48, 577, 455, WHITE, RED, 1.5);
lineV(344, 49, 454, NAVY, 2);                       // blue vertical divider
lineH(61, 163, 573, NAVY, 2);                       // band dividers (measured y163/286/401/475)
lineH(62, 286, 572, NAVY, 2);
lineH(61, 401, 573, NAVY, 2);
lineH(61, 475, 573, NAVY, 2);

// --- threshold bands ---
// band = {hy: header box y, my: matrix top, tpr: tpr/fpr box y, thr: label, fpr: fpr line}
const bands = [
  { hy: 53, my: 92, tprY: 98,  thr: "Threshold=0.0", fpr: "FPR=6/(6+0)=1",
    mx: 80, mw: 136, v1: 117, v2: 166, r1: 113, r2: 136, mb: 157,
    cols: ["P", "N"], rows: ["P", "N"],
    vals: [["5", BLUE], ["0", RED], ["6", RED], ["0", BLUE]],
    vc: [139, 185], vr: [127, 148.5], tlines: [116, 135] },
  { hy: 175, my: 213, tprY: 218, thr: "Threshold=0.1", fpr: "FPR=4/(4+2)=.66",
    mx: 78, mw: 136, v1: 115, v2: 164, r1: 234, r2: 256, mb: 278,
    cols: ["P", "N"], rows: ["P", "N"],
    vals: [["5", BLUE], ["0", RED], ["4", RED], ["2", BLUE]],
    vc: [139, 185], vr: [248, 269], tlines: [237, 256] },
  { hy: 292, my: 328, tprY: 333, thr: "Threshold=0.3", fpr: "FPR=2/(2+4)=.33",
    mx: 77, mw: 137, v1: 115, v2: 164, r1: 349, r2: 372, mb: 394,
    cols: ["P", "N"], rows: ["P", "N"],
    vals: [["5", BLUE], ["0", RED], ["2", RED], ["4", BLUE]],
    vc: [139, 184], vr: [363, 385], tlines: [350, 370] }
];

for (const b of bands) {
  // header box + label
  rect(68, b.hy, 104, 23, HDRFILL, RED, 1.5);
  text(b.thr, 120, b.hy + 11.5, 96, 16, 12.5, RED, { bold: true });
  // "Predicted as" above the matrix, over the value columns
  textBox("Predicted as", b.v1 - 4, b.my - 11, (b.mx + b.mw) - b.v1 + 8, 11,
          12, RED, { italic: true });
  // matrix grid
  lineH(b.mx, b.my, b.mw, RED, 2);                   // top
  lineH(b.mx, b.r1, b.mw, RED, 2);
  lineH(b.mx, b.r2, b.mw, RED, 2);
  lineH(b.mx, b.mb, b.mw, RED, 2);                   // bottom
  lineV(b.mx, b.my, b.mb - b.my, RED, 2);            // left
  lineV(b.v1, b.my, b.mb - b.my, RED, 2);
  lineV(b.v2, b.my, b.mb - b.my, RED, 2);
  lineV(b.mx + b.mw, b.my, b.mb - b.my, RED, 2);     // right
  // column headers P N (header row), row labels P N
  text(b.cols[0], (b.v1 + b.v2) / 2, b.my + 13.5, 14, 14, 12, INK, { bold: true });
  text(b.cols[1], (b.v2 + b.mx + b.mw) / 2, b.my + 13.5, 14, 14, 12, INK, { bold: true });
  text(b.rows[0], (b.mx + b.v1) / 2, (b.r1 + b.r2) / 2, 14, 14, 12, INK, { bold: true });
  text(b.rows[1], (b.mx + b.v1) / 2, (b.r2 + b.mb) / 2, 14, 14, 12, INK, { bold: true });
  // "Actual" vertical label left of the label column; textBox takes top-left, rotation is
  // about the box center, so center the box at (mx-14, matrix mid) with w=56,h=18 (visual
  // footprint after 270deg rotation: 18 wide x 56 tall, clear of the matrix edge)
  textBox("Actual", b.mx - 14 - 28, (b.my + b.mb) / 2 - 9, 56, 18, 10, RED, { rotate: 270 });
  // values: [[P,P],[P,N],[N,P],[N,N]]
  const vpos = [[b.vc[0], b.vr[0]], [b.vc[1], b.vr[0]], [b.vc[0], b.vr[1]], [b.vc[1], b.vr[1]]];
  b.vals.forEach((v, i) => text(v[0], vpos[i][0], vpos[i][1], 14, 15, 14, v[1], { bold: true }));
  // TPR/FPR box + lines
  const boxH = (b === bands[0]) ? 48 : 54;
  rect(225, b.tprY, 114, boxH, WHITE, RED, 1.5);
  s.addText([
    { text: "TPR=5/(5+0)=1", options: { fontSize: 11.5, color: "0000FF", fontFace: FONT, breakLine: true } },
    { text: b.fpr, options: { fontSize: 11.5, color: "FF0000", fontFace: FONT, breakLine: false } }
  ], {
    x: P(233), y: P(b.tprY + 5), w: P(104), h: P(boxH - 8),
    align: "left", valign: "middle", margin: 0, lineSpacing: 19
  });
}

// --- bottom band: blue caption box (measured x354..622, y401..476) ---
rect(354, 401, 268, 75, TITLEFILL, NAVY, 2);
s.addText([
  { text: "ROC Curve for", options: { fontSize: 14, bold: true, color: RED, fontFace: FONT, breakLine: true } },
  { text: "Same Model -different thresholds", options: { fontSize: 14, bold: true, color: RED, fontFace: FONT, breakLine: false } }
], {
  x: P(355), y: P(403), w: P(266), h: P(71), align: "center", valign: "middle",
  margin: 0, lineSpacing: 20
});

// --- RIGHT COLUMN ---
// ROC plot (generated image at measured region)
s.addImage({
  path: NS + "/build/assets/slide031_roc.png",
  x: P(642), y: P(81), w: P(252), h: P(306)
});
// right column has no outer red frame in the original (measured); no stray bottom line

// formula boxes with stacked 2D fractions (red border, white fill)
rect(650, 416, 98, 39, WHITE, RED, 1.5);
s.addImage({
  path: NS + "/build/assets/slide031_eq_tpr.png",
  x: P(699) - P(88.32) / 2, y: P(435.5) - P(29.88) / 2, w: P(88.32), h: P(29.88)
});
rect(651, 465, 98, 38, WHITE, RED, 1.5);
s.addImage({
  path: NS + "/build/assets/slide031_eq_fpr.png",
  x: P(700) - P(88.08) / 2, y: P(484) - P(29.88) / 2, w: P(88.08), h: P(29.88)
});

// legend matrix (measured x771..886, y437..499; header row y437..455, cells y455..499)
rect(771, 437, 115, 62, WHITE, RED, 1.5);
lineV(802, 437, 62, RED, 2);
lineV(844, 437, 62, RED, 2);
lineH(771, 455, 115, RED, 2);
lineH(771, 478, 115, RED, 2);
// cell fills: TP/TN green, FN/FP pink
rect(803, 456, 40, 21, GREEN, null);
rect(845, 456, 40, 21, PINK, null);
rect(803, 479, 40, 19, PINK, null);
rect(845, 479, 40, 19, GREEN, null);
// "Predicted as" above, column headers, row labels, Actual
textBox("Predicted as", 806, 428, 90, 12, 11, RED, { italic: true });
text("P", 823, 446, 14, 13, 11, INK, { bold: true });
text("N", 865, 446, 14, 13, 11, INK, { bold: true });
text("P", 787.5, 466, 14, 13, 11, INK, { bold: true });
text("N", 788, 489, 14, 13, 11, INK, { bold: true });
textBox("Actual", 757 - 25, 468 - 8, 50, 16, 10, RED, { rotate: 270 });
text("TP", 823, 467, 16, 13, 12, INK, { bold: true });
text("FN", 865, 467, 16, 13, 12, INK, { bold: true });
text("FP", 824, 489, 16, 13, 12, INK, { bold: true });
text("TN", 865, 489, 16, 13, 12, INK, { bold: true });

const outPath = NS + "/slide_031_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
