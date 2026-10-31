// Slide 35 — "ROC Curve for Same Model -different thresholds" (7 threshold panels)
// Frame-measured geometry (960x540 original, 1px = 1pt = 1/72 in).
// Content laid out at the ORIGINAL's measured pixel positions; house chrome
// (root AGENTS.md) replaces the original's own outer frame/badge/title band.
// Copy base: certified build/slide_034.js (same deck, 6 panels + caption).
const pptxgenpkg = require("pptxgenjs");
const fs = require("fs");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure";
const MAN = JSON.parse(fs.readFileSync(NS + "/recreated_pptx/build/assets/slide035_manifest.json", "utf8"));

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", DRED = "8B0000", INK = "000000", BADGE = "FFF9C4", NUM = "333333";
const HDR_FILL = "FBD6C7", PANEL_FILL = "FCF8E7", CAP_FILL = "ECECEC", EQBOX_FILL = "F9ECEC";
const GREEN_TP = "A7FF5F", GREEN_TN = "8AFF11", BLUE = "00008B";
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
s.addText("35", {
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

// Panel geometry (px, absolute frame coords) — measured from slide_035.jpg
const COLS = [58, 346];
const ROWS = [[43, 118], [166, 118], [290, 108], [405, 112]];

// panel-internal layout (px, relative to the panel's top-left) — as certified on slide 34
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
  "1":   { vals: [["0", "5"], ["0", "6"]], k: "M3" },
};

function panel(cx, ry, thr) {
  const [bx, by] = [COLS[cx], ROWS[ry][0]];
  const bw = cx === 0 ? 284 : 289;
  const bh = ROWS[ry][1];
  const m = MATRICES[thr];

  // panel body (pale cream per frame measurement)
  s.addShape(pptx.shapes.RECTANGLE, {
    x: rel(bx), y: rel(by), w: rel(bw), h: rel(bh),
    fill: { color: PANEL_FILL }, line: { color: DRED, width: 1 },
  });
  // header: small peach box at the panel's upper-left (frame-measured x[bx+10..bx+114] y[by+10..by+33])
  s.addShape(pptx.shapes.RECTANGLE, {
    x: rel(bx + 10), y: rel(by + 10), w: rel(104), h: rel(23),
    fill: { color: HDR_FILL }, line: { color: DRED, width: 1 },
  });
  txt(rel(bx + 10), rel(by + 10), rel(104), rel(23),
    "Threshold=" + thr, 13, DRED, { bold: true });

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
  cell(1, 1, m.vals[0][0], 14, DRED); cell(2, 1, m.vals[0][1], 14, DRED);
  cell(1, 2, m.vals[1][0], 14, DRED); cell(2, 2, m.vals[1][1], 14, DRED);

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
    fill: { color: "FFF2CC" }, line: { color: DRED, width: 1 },
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
panel(1, 2, "1");

// ---------------- bottom-middle caption box (x345..639, y403..490) ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(345), y: rel(403), w: rel(294), h: rel(87),
  fill: { color: CAP_FILL }, line: { color: DRED, width: 1 },
});
s.addText([
  { text: "ROC Curve for", options: { breakLine: true } },
  { text: "Same Model -different thresholds", options: {} },
], {
  x: rel(348), y: rel(406), w: rel(288), h: rel(81), align: "center", valign: "middle",
  fontSize: 14, bold: true, color: DRED, fontFace: FONT, margin: 0, lineSpacing: 22,
});

// ---------------- ROC panel (generated image, x637 y42 w267 h357 px) ----------------
const roc = MAN.roc_panel;
s.addImage({ path: roc.path, x: rel(roc.x_px), y: rel(roc.y_px), w: roc.w_in, h: roc.h_in });

// ---------------- bottom-right box: formulas + legend (x634..903, y399..527) ----------------
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(634), y: rel(399), w: rel(269), h: rel(128),
  fill: { color: "FFFFFF" }, line: { color: DRED, width: 1 },
});
// two pale-rose formula boxes stacked at the left (frame-measured x648..750)
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(648), y: rel(412), w: rel(102), h: rel(44),
  fill: { color: EQBOX_FILL }, line: { color: DRED, width: 1 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(648), y: rel(464), w: rel(102), h: rel(41),
  fill: { color: EQBOX_FILL }, line: { color: DRED, width: 1 },
});
const dtpr = MAN.eq_def_tpr, dfpr = MAN.eq_def_fpr;
s.addImage({ path: dtpr.path, x: rel(652), y: rel(421), w: dtpr.w_in, h: dtpr.h_in });
s.addImage({ path: dfpr.path, x: rel(652), y: rel(470), w: dfpr.w_in, h: dfpr.h_in });

// legend matrix: x750..903, y422..500; cols [53,42,58], rows [25,28,25]
txt(rel(750), rel(404), rel(153), rel(14), "Predicted as", 9, BLUE);
const lgx = 750, lgy = 422, lgw = 153, lgh = 78;
const lcols = [53, 42, 58], lrows = [25, 28, 25];
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(lgx), y: rel(lgy), w: rel(lgw), h: rel(lgh),
  fill: { color: "FFFFFF" }, line: { color: DRED, width: 1 },
});
const lc1 = lgx + lcols[0], lc2 = lgx + lcols[0] + lcols[1];
const lr1 = lgy + lrows[0], lr2 = lgy + lrows[0] + lrows[1];
vline(rel(lc1), rel(lgy), rel(lgh));
vline(rel(lc2), rel(lgy), rel(lgh));
hline(rel(lgx), rel(lr1), rel(lgw));
hline(rel(lgx), rel(lr2), rel(lgw));
// green highlight cells: TP (col1,row1) and TN (col2,row2)
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(lc1), y: rel(lr1), w: rel(lcols[1]), h: rel(lrows[1]),
  fill: { color: GREEN_TP }, line: { color: DRED, width: 1 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: rel(lc2), y: rel(lr2), w: rel(lcols[2]), h: rel(lrows[2]),
  fill: { color: GREEN_TN }, line: { color: DRED, width: 1 },
});
const lccx = [lgx + lcols[0] / 2, lgx + lcols[0] + lcols[1] / 2, lgx + lcols[0] + lcols[1] + lcols[2] / 2];
const lccy = [lgy + lrows[0] / 2, lgy + lrows[0] + lrows[1] / 2, lgy + lrows[0] + lrows[1] + lrows[2] / 2];
const lcell = (col, row, str, size, color) => {
  txt(rel(lccx[col] - lcols[col] / 2), rel(lccy[row] - 8), rel(lcols[col]), rel(16), str, size || 9, color || INK);
};
lcell(1, 0, "P", 9, BLUE); lcell(2, 0, "N", 9, BLUE);
lcell(0, 1, "P", 9, BLUE); lcell(1, 1, "TP", 9, INK); lcell(2, 1, "FN", 9, DRED);
lcell(0, 2, "N", 9, BLUE); lcell(1, 2, "FP", 9, DRED); lcell(2, 2, "TN", 9, INK);

const outPath = NS + "/recreated_pptx/slide_035_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));
