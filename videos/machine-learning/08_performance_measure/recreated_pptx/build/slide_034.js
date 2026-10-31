// Slide 34 — "ROC Curve for Same Model -different thresholds"
// Frame-measured geometry (960x540 original, 1px = 1pt = 1/72 in).
// Content is laid out at the ORIGINAL's measured pixel positions; house chrome
// (root AGENTS.md) replaces the original's own outer frame/badge/title band.
const pptxgenpkg = require("pptxgenjs");
const fs = require("fs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";
const MAN = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/slide034_manifest.json", "utf8"));

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", DRED = "8B0000", INK = "000000", BADGE = "FFF9C4", NUM = "333333";
const HDR_FILL = "FDE1CB", GREEN = "ACFC7D", TP_FILL = "D3FA94", EQ_FILL = "F9FBDF";
const CAP_TXT = "963C48", CAP_BRD = "5D5795";
const FONT = "Arial";
const PX = 1 / 72;                       // px -> inches

const s = pptx.addSlide();
s.background = { color: BG };

// ---------------- HOUSE CHROME ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("34", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: NUM, fontFace: FONT, margin: 0,
});
// no top title exists on the original (its title text is the bottom-middle caption box)

// ---------------- helpers ----------------
const rel = (n) => n * PX;

function hline(x, y, w) {               // 1px horizontal rule
  s.addShape(pptx.shapes.RECTANGLE, { x, y, w, h: rel(1.2), fill: { color: DRED } });
}
function vline(x, y, h) {
  s.addShape(pptx.shapes.RECTANGLE, { x, y, w: rel(1.2), h, fill: { color: DRED } });
}
function txt(x, y, w, h, str, size, color, extra) {
  s.addText(str, Object.assign({
    x, y, w, h, align: "center", valign: "middle", fontSize: size, color, fontFace: FONT, margin: 0,
  }, extra || {}));
}

// Panel geometry (px, absolute frame coords)
const COLS = [58, 346];
const ROWS = [[43, 118], [166, 118], [289, 110], [405, 112]];

// panel-internal layout (px, relative to the panel's top-left)
const HDR = [4, 5, 28];                 // x, y, h
const GRID = [22, 49, 136, 64];         // x, y, w, h
const GCOLS = [35, 48, 53];             // label, P, N
const GROWS = [20, 24, 20];             // header, P, N
const EQBOX = [167, 55, 114, 48];

const MATRICES = {
  "0.0": { vals: [["5", "0"], ["6", "0"]], k: "L1" },
  "0.1": { vals: [["5", "0"], ["4", "2"]], k: "L2" },
  "0.3": { vals: [["5", "0"], ["2", "4"]], k: "L3" },
  "0.4": { vals: [["4", "1"], ["1", "5"]], k: "L4" },
  "0.6": { vals: [["3", "1"], ["1", "5"]], k: "M1" },
  "0.7": { vals: [["3", "2"], ["0", "6"]], k: "M2" },
};

function panel(cx, ry, thr) {
  const [bx, by] = [COLS[cx], ROWS[ry][0]];
  const bw = cx === 0 ? 284 : 289;
  const bh = ROWS[ry][1];
  const m = MATRICES[thr];

  // panel body
  s.addShape(pptx.shapes.RECTANGLE, {
    x: rel(bx), y: rel(by), w: rel(bw), h: rel(bh),
    fill: { color: "FFFFFF" }, line: { color: DRED, width: 1 },
  });
  // header strip
  s.addShape(pptx.shapes.RECTANGLE, {
    x: rel(bx + HDR[0]), y: rel(by + HDR[1]), w: rel(bw - 2 * HDR[0]), h: rel(HDR[2]),
    fill: { color: HDR_FILL }, line: { color: HDR_FILL, width: 0 },
  });
  txt(rel(bx + HDR[0]), rel(by + HDR[1]), rel(bw - 2 * HDR[0]), rel(HDR[2]),
    "Threshold=" + thr, 16, DRED, { bold: true });

  // "Predicted as" caption over the P/N columns
  txt(rel(bx + GRID[0]), rel(by + 36), rel(GRID[2]), rel(12), "Predicted as", 9, INK);

  // matrix grid
  const gx = bx + GRID[0], gy = by + GRID[1];
  const gw = GRID[2], gh = GRID[3];
  s.addShape(pptx.shapes.RECTANGLE, {
    x: rel(gx), y: rel(gy), w: rel(gw), h: rel(gh),
    fill: { color: "FFFFFF" }, line: { color: DRED, width: 1 },
  });
  const c1 = gx + GCOLS[0], c2 = gx + GCOLS[0] + GCOLS[1];
  const r1 = gy + GROWS[0], r2 = gy + GROWS[0] + GROWS[1];
  vline(rel(c1), rel(gy), rel(gh));
  vline(rel(c2), rel(gy), rel(gh));
  hline(rel(gx), rel(r1), rel(gw));
  hline(rel(gx), rel(r2), rel(gw));

  const ccx = [gx + GCOLS[0] / 2, gx + GCOLS[0] + GCOLS[1] / 2, gx + GCOLS[0] + GCOLS[1] + GCOLS[2] / 2];
  const ccy = [gy + GROWS[0] / 2, gy + GROWS[0] + GROWS[1] / 2, gy + GROWS[0] + GROWS[1] + GROWS[2] / 2];
  const cell = (col, row, str, size, color) => {
    txt(rel(ccx[col] - 22), rel(ccy[row] - 9), rel(44), rel(18), str, size || 13, color || INK);
  };
  cell(1, 0, "P"); cell(2, 0, "N");
  cell(0, 1, "P"); cell(0, 2, "N");
  cell(1, 1, m.vals[0][0], 14); cell(2, 1, m.vals[0][1], 14);
  cell(1, 2, m.vals[1][0], 14); cell(2, 2, m.vals[1][1], 14);

  // rotated "Actual" label in the panel's left gutter
  const acx = bx + 12, acy = by + 91;
  s.addText("Actual", {
    x: rel(acx) - rel(44) / 2, y: rel(acy) - rel(16) / 2, w: rel(44), h: rel(16),
    rotate: 270, align: "center", valign: "middle", fontSize: 9, color: INK,
    fontFace: FONT, margin: 0,
  });

  // equation box with the panel's TPR / FPR computation lines (2D format)
  const ex = bx + EQBOX[0], ey = by + EQBOX[1], ew = EQBOX[2], eh = EQBOX[3];
  s.addShape(pptx.shapes.RECTANGLE, {
    x: rel(ex), y: rel(ey), w: rel(ew), h: rel(eh),
    fill: { color: EQ_FILL }, line: { color: DRED, width: 1 },
  });
  const a1 = MAN["eq_" + m.k + "_tpr"], a2 = MAN["eq_" + m.k + "_fpr"];
  s.addImage({ path: a1.path, x: rel(ex + 5), y: rel(ey + 4), w: a1.w_in, h: a1.h_in });
  s.addImage({ path: a2.path, x: rel(ex + 5), y: rel(ey + 25), w: a2.w_in, h: a2.h_in });
}

panel(0, 0, "0.0");
panel(0, 1, "0.1");
panel(0, 2, "0.3");
panel(0, 3, "0.4");
panel(1, 0, "0.6");
panel(1, 1, "0.7");

// "Best (FPR)" annotation at the right of the Threshold=0.7 panel
s.addText([
  { text: "Best", options: { breakLine: true } },
  { text: "(FPR)", options: {} },
], {
  x: rel(560), y: rel(163), w: rel(85), h: rel(36), align: "center", valign: "middle",
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0, lineSpacing: 14,
});

// ---------------- bottom-middle caption box ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(342), y: rel(426), w: rel(293), h: rel(50),
  fill: { color: "FFFFFF" }, line: { color: CAP_BRD, width: 1 },
});
s.addText([
  { text: "ROC Curve for", options: { breakLine: true } },
  { text: "Same Model -different thresholds", options: {} },
], {
  x: rel(345), y: rel(429), w: rel(287), h: rel(44), align: "center", valign: "middle",
  fontSize: 15, color: CAP_TXT, fontFace: FONT, margin: 0, lineSpacing: 20,
});

// ---------------- ROC panel (generated image) ----------------
const roc = MAN.roc_panel;
s.addImage({ path: roc.path, x: rel(645), y: rel(55), w: roc.w_in, h: roc.h_in });

// ---------------- bottom-right formulas + legend ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(643), y: rel(413), w: rel(247), h: rel(94),
  fill: { color: "FFFFFF" }, line: { color: DRED, width: 1 },
});
const dtpr = MAN.eq_def_tpr, dfpr = MAN.eq_def_fpr;
s.addImage({ path: dtpr.path, x: rel(648), y: rel(416), w: dtpr.w_in, h: dtpr.h_in });
s.addImage({ path: dfpr.path, x: rel(795), y: rel(427), w: dfpr.w_in, h: dfpr.h_in });

// legend: left label block (x 650..749) + 2x2 cell grid (x 771..886, y 455..503)
const lgx = 650, lgy = 455;
// left block: "Predicted as" header + P/N row labels
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(lgx), y: rel(lgy), w: rel(99), h: rel(48),
  fill: { color: "FFFFFF" }, line: { color: DRED, width: 1 },
});
hline(rel(lgx), rel(lgy + 10), rel(99));
txt(rel(lgx + 4), rel(lgy + 1), rel(91), rel(9), "Predicted as", 7, INK, { align: "left" });
txt(rel(lgx + 20), rel(lgy + 22), rel(40), rel(14), "P", 9, INK);
txt(rel(lgx + 20), rel(lgy + 34), rel(40), rel(14), "N", 9, INK);
// 2x2 grid: cols [771..844, 844..886], rows [455..477, 477..503]
const gx2 = 771, gy2 = 455, gw2 = 115, gh2 = 48;
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(gx2), y: rel(gy2), w: rel(gw2), h: rel(gh2),
  fill: { color: "FFFFFF" }, line: { color: DRED, width: 1 },
});
vline(rel(gx2 + 73), rel(gy2), rel(gh2));
hline(rel(gx2), rel(gy2 + 22), rel(gw2));
// TP (top-left) and TN (bottom-right) green
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(gx2), y: rel(gy2), w: rel(73), h: rel(22),
  fill: { color: TP_FILL }, line: { color: DRED, width: 1 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(gx2 + 73), y: rel(gy2 + 22), w: rel(42), h: rel(26),
  fill: { color: GREEN }, line: { color: DRED, width: 1 },
});
const gcell = (cx, cy, str) => {
  txt(rel(cx - 16), rel(cy - 8), rel(32), rel(16), str, 10, INK);
};
gcell(gx2 + 36, gy2 + 11, "TP");   // green
gcell(gx2 + 73 + 21, gy2 + 11, "FN");
gcell(gx2 + 36, gy2 + 22 + 13, "FP");
gcell(gx2 + 73 + 21, gy2 + 22 + 13, "TN");  // green

const outPath = NS + "/recreated_pptx/slide_034_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
