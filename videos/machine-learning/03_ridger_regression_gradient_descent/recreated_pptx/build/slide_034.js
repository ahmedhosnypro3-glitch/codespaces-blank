// Build slide 034 — "Non-Convex Function" (attempt 27)
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (house chrome = shared_patterns/house_chrome.js)
//
// ATTEMPT 27 — rebuilt per qa/slide034/HANDOFF.md 8-item fix list (att26 FAIL
// adjudicated; all geometry PIL-pinned in qa/slide034/att27_frame_measure*.txt
// + prephase/orig_judges/desc_{table,plot,leftblock}.txt). Structure follows the
// certified build/slide_033.js pattern (same slide family) with THIS frame's
// measured values.
//
// MEASURED GEOMETRY (frame px; 1px = 1pt = 1/72 in):
//   Title "Non-Convex Function" 8B0000 bold serif, ink x195..434 y67..84 (cx 315)
//   Sub L1 "May reach different minimum value based on:" 8B0000, ink x113..533 y94..113 (cx 323)
//   Sub L2 runs: "initial point" 0000CC / " and " C00000 / "learning rate" 0000CC,
//         ink x192..461 y122..140 (cx 326); frame runs blue 192..297, red 304..336, blue 343..460
//   Param box x75..174 y246..308 white, navy border; cell rows y255..270 E9FFD4 /
//         y270..285 F9BBC1 / y285..300 FDFD00; label col x80 w50, value col x130 w40;
//         values 0.2 / 7 (RED bold — '7' ink mean (120,76,75) reddish) / 0.1
//   Red hollow block arrow, bbox x163..184 y304..339, tilted ~15-20deg (tip swings left)
//   Equation box x465..601 y169..218 (borders y168-170 / y217-219 / x465-466 / x600-601)
//   Callout box x270..596 y252..300 EFFFE2 green border;
//         L1 ink x270..593 y255..275 (X red 271..285, "is in between" 318..404,
//         "9.6" red 413..432, " and color red bold " 442..567, "9.8" red 568..588)
//         L2 ink x270..593 y276..299 (f(x) BLUE 276..307, "-10.03" blue 414..462,
//         "-9.92" blue 503..543)
//   Plot box x607..845 y60..312 (border x607 / x845 / y60 / y312, dark red);
//         asset slide_034_plot_v27.png 1975x2116 @600dpi = 237x253.92pt covers x608..845 y59..313
//   Table: navy box x68..881 y320..517; bands x83..868 (border x81-82/x869-870):
//         band1 y331..368 D9E275 | band2 y373..410 D6B2F5 | band3 y416..453 F7DDC2
//   Column separators pinned from the next-x strong-red verticals (measure4 §3):
//         SEP = 139,179,220,260,301,341.5,382,423,463,504,545,585,626,666.5,707,748,788,829,869
//         (pitch ≈40.6 from x139 — matches the desc_table 40.6px audit)
//   Row centers: 341,359,383,401,427,445 (bands) / 469 (slope) / 493 (next-x)
//   Slope row: pale-green E9FFD4 full-width strip y459..478 (dark-green edges y459-461/y477-478),
//         green label divider x136-139, 18 red-bordered salmon DEAC95 inset boxes
//         (~36x15, inset ~3px) with pale-yellow FDFDBE cells at cols [14] and [16]
//   next-x row: pink F7BEC4 strip y483..503, red border w1.5 (edges y483/484/y502),
//         full red grid (strong-red verticals at every SEP, y483..503)
//   Cyan insert x666..792 y325..369 (top maroon dash y325, sides x666-667/x792,
//         bottom ~y368) fill 8BF8AB, maroon dashed border, text 006400; covers c14-c16
//
// Laws: hex without '#'; fontFace explicit; margin 0; eq image at certified
// display size 112x24pt centered (533,193.5); OMML wrap is orchestrator-only.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_034_recreated.pptx";

const px = (v) => v / 72;
const A = "Arial";
const T = "Times New Roman";

const C_RED = "C00000";
const C_BLUE = "0000CC";
const C_NAVY = "1E1856";
const C_TITLE = "8B0000";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

drawHouseChrome(pptx, slide, { numeral: 34 });

// ================= TITLE / SUBTITLE (033 certified pattern, 034 colors) =================
slide.addText("Non-Convex Function", {
  x: px(100), y: px(60), w: px(430), h: px(26),
  align: "center", valign: "top", margin: 0,
  fontFace: T, fontSize: 25, bold: true, color: C_TITLE,
});
slide.addText("May reach different minimum value based on:", {
  x: px(103), y: px(91), w: px(440), h: px(20),
  align: "center", valign: "top", margin: 0,
  fontFace: T, fontSize: 17, bold: true, color: C_TITLE, charSpacing: 1.8,
});
slide.addText([
  { text: "initial point", options: { fontFace: T, fontSize: 21, bold: true, color: C_BLUE } },
  { text: " and ", options: { fontFace: T, fontSize: 21, bold: true, color: C_RED } },
  { text: "learning rate", options: { fontFace: T, fontSize: 21, bold: true, color: C_BLUE } },
], {
  x: px(176), y: px(114), w: px(300), h: px(27),
  align: "center", valign: "top", margin: 0,
});

// ================= PARAMETER BOX (033 cell-row pattern, 034 values) =================
slide.addShape(pptx.ShapeType.rect, {
  x: px(75), y: px(246), w: px(99), h: px(61),
  fill: { color: "FFFFFF" }, line: { color: C_NAVY, width: 1.25 },
});
const PCELLS = [
  { y0: 255, y1: 270, fill: "E9FFD4", label: "step", value: "0.2", vcolor: "000000" },
  { y0: 270, y1: 285, fill: "F9BBC1", label: "initial X", value: "7", vcolor: C_RED },
  { y0: 285, y1: 300, fill: "FDFD00", label: "delta", value: "0.1", vcolor: "000000" },
];
for (const c of PCELLS) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(80), y: px(c.y0), w: px(50), h: px(c.y1 - c.y0),
    fill: { color: c.fill }, line: { color: C_NAVY, width: 0.5 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(130), y: px(c.y0), w: px(40), h: px(c.y1 - c.y0),
    fill: { color: c.fill }, line: { color: C_NAVY, width: 0.5 },
  });
  slide.addText(c.label, {
    x: px(81), y: px(c.y0), w: px(48), h: px(c.y1 - c.y0),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 8, bold: true, color: "000000",
  });
  slide.addText(c.value, {
    x: px(131), y: px(c.y0), w: px(38), h: px(c.y1 - c.y0),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 8, bold: true, color: c.vcolor,
  });
}

// ================= EQUATION BOX =================
slide.addShape(pptx.ShapeType.rect, {
  x: px(465), y: px(169), w: px(136), h: px(49),
  fill: { color: "FFFFFF" }, line: { color: C_RED, width: 1.25 },
});
// eq_034_main.png — certified display size 112x24pt, centered at (533,193.5)
slide.addImage({
  path: ASSET_DIR + "/eq_034_main.png",
  x: px(533 - 112 / 2), y: px(193.5 - 24 / 2),
  w: px(112), h: px(24),
});

// ================= CALLOUT (green box; literal words "color red bold" kept) =================
slide.addShape(pptx.ShapeType.rect, {
  x: px(270), y: px(252), w: px(326), h: px(48),
  fill: { color: "EFFFE2" }, line: { color: "00B000", width: 1.25 },
});
slide.addText("X", {
  x: px(271), y: px(257), w: px(40), h: px(16),
  align: "left", valign: "middle", margin: 0,
  fontFace: T, fontSize: 17, bold: true, italic: true, color: C_RED,
});
slide.addText([
  { text: "is in between ", options: { fontFace: T, fontSize: 17, bold: true, color: "000000" } },
  { text: "9.6", options: { fontFace: T, fontSize: 17, bold: true, color: C_RED } },
  { text: " and color red bold ", options: { fontFace: T, fontSize: 17, bold: true, color: "000000" } },
  { text: "9.8", options: { fontFace: T, fontSize: 17, bold: true, color: C_RED } },
], {
  x: px(316), y: px(257), w: px(284), h: px(16),
  align: "left", valign: "middle", margin: 0,
});
slide.addText("f(x)", {
  x: px(272), y: px(276), w: px(44), h: px(20),
  align: "left", valign: "middle", margin: 0,
  fontFace: T, fontSize: 17, bold: true, italic: true, color: C_BLUE,
});
slide.addText([
  { text: "is in between ", options: { fontFace: T, fontSize: 17, bold: true, color: "000000" } },
  { text: "-10.03", options: { fontFace: T, fontSize: 17, bold: true, color: C_BLUE } },
  { text: " and ", options: { fontFace: T, fontSize: 17, bold: true, color: "000000" } },
  { text: "-9.92", options: { fontFace: T, fontSize: 17, bold: true, color: C_BLUE } },
], {
  x: px(316), y: px(276), w: px(284), h: px(20),
  align: "left", valign: "middle", margin: 0,
});

// ================= FUNCTION PLOT =================
// white backing, then the generated analytic plot, then the red border on top
// (the asset is opaque and butts the border, so the border must redraw over it)
slide.addShape(pptx.ShapeType.rect, {
  x: px(607), y: px(60), w: px(238), h: px(253),
  fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 },
});
// slide_034_plot.png: 1975 x 2116 px at 600 dpi -> 237.00 x 253.92 pt
slide.addImage({
  path: ASSET_DIR + "/slide_034_plot.png",
  x: px(608), y: px(59),
  w: 1975 / 600, h: 2116 / 600,
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(607), y: px(60), w: px(238), h: px(253),
  fill: { color: "FFFFFF", transparency: 100 }, line: { color: C_RED, width: 1.25 },
});
// red dashed drop guide from the marked local max down to the x-axis (x783, y148->172)
slide.addShape(pptx.ShapeType.line, {
  x: px(783), y: px(148), w: 0, h: px(24),
  line: { color: "C41E1E", width: 1, dashType: "dash" },
});
// red initial-point dot (frame x779..787 y144..152)
slide.addShape(pptx.ShapeType.ellipse, {
  x: px(779), y: px(144), w: px(8), h: px(8),
  fill: { color: "C41E1E" }, line: { color: "C41E1E", width: 0 },
});
// orange arrow pointing down-right at the marked max (frame (763,113)->(782,138))
slide.addShape(pptx.ShapeType.line, {
  x: px(763), y: px(113), w: px(19), h: px(25),
  line: { color: "F5841F", width: 3, endArrowType: "triangle" },
});
// green marker on the reached global minimum (frame pair 799..816 y255..266)
slide.addShape(pptx.ShapeType.ellipse, {
  x: px(799), y: px(255), w: px(17), h: px(11),
  fill: { color: "7CFC00" }, line: { color: "7CFC00", width: 0 },
});
// pink "Reach / global Minima" callout
slide.addShape(pptx.ShapeType.rect, {
  x: px(741), y: px(268), w: px(94), h: px(35),
  fill: { color: "F9C7EF" }, line: { color: "C040B0", width: 1.25 },
});
slide.addText([
  { text: "Reach", options: { fontFace: T, fontSize: 10, bold: true, italic: true, color: "B0188C", breakLine: true } },
  { text: "global Minima", options: { fontFace: T, fontSize: 10, bold: true, italic: true, color: "B0188C" } },
], {
  x: px(741), y: px(268), w: px(94), h: px(35),
  align: "center", valign: "middle", margin: 0, lineSpacing: 12,
});

// ================= TABLE =================
// outer white table box with navy border
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(320), w: px(813), h: px(197),
  fill: { color: "FFFFFF" }, line: { color: C_NAVY, width: 1.25 },
});
// 034's own column grid (next-x strong-red verticals, measure4 §3)
const SEP = [139, 179, 220, 260, 301, 341.5, 382, 423, 463, 504, 545, 585, 626, 666.5, 707, 748, 788, 829, 869];

// bands: [y0, y1, fill, border]
const BANDS = [
  { y0: 331, y1: 369, fill: "D9E275", border: C_NAVY, bw: 1.25 },
  { y0: 374, y1: 411, fill: "D6B2F5", border: "5B2C6F", bw: 1.25 },
  { y0: 417, y1: 455, fill: "F7DDC2", border: "6B4226", bw: 1.25 },
];
for (const bd of BANDS) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(82), y: px(bd.y0), w: px(787), h: px(bd.y1 - bd.y0),
    fill: { color: bd.fill }, line: { color: bd.border, width: bd.bw },
  });
}
// slope strip: pale-green label cell + pale-green data area (dark-green border);
// 18 red-bordered inset boxes (salmon; pale-yellow at cols 14 and 16)
slide.addShape(pptx.ShapeType.rect, {
  x: px(81), y: px(459), w: px(58), h: px(19),
  fill: { color: "E9FFD4" }, line: { color: "2E7D32", width: 1.5 },
});
slide.addShape(pptx.ShapeType.rect, {
  x: px(139), y: px(459), w: px(731), h: px(19),
  fill: { color: "E9FFD4" }, line: { color: "2E7D32", width: 1.5 },
});
for (let ci = 0; ci < 18; ci++) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(SEP[ci] + 3), y: px(461), w: px(SEP[ci + 1] - SEP[ci] - 6), h: px(15),
    fill: { color: (ci === 14 || ci === 16) ? "FDFDBE" : "DEAC95" },
    line: { color: "C00000", width: 1 },
  });
}
// next-x strip: pink with a full red grid (border + strong-red verticals)
slide.addShape(pptx.ShapeType.rect, {
  x: px(81), y: px(483), w: px(789), h: px(20),
  fill: { color: "F7BEC4" }, line: { color: "C00000", width: 1.5 },
});
for (let ci = 0; ci <= 17; ci++) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(SEP[ci]), y: px(483), w: 0, h: px(20),
    line: { color: "C00000", width: 1 },
  });
}
// cyan insert over band1 cols 13-15 with the maroon dashed border
slide.addShape(pptx.ShapeType.rect, {
  x: px(666), y: px(325), w: px(126), h: px(44),
  fill: { color: "8BF8AB" }, line: { color: "8B0000", width: 1.25, dashType: "dash" },
});

// thin white separators between cells (033 pattern; the three 2-row bands)
for (const bd of [[331, 369], [374, 411], [417, 455]]) {
  for (const sx of SEP) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(sx), y: px(bd[0] + 1), w: 0, h: px(bd[1] - bd[0] - 2),
      line: { color: "FFFFFF", width: 0.5 },
    });
  }
}
// thin white separators between the two text rows of each band
for (const hy of [350, 392.5, 436]) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(88), y: px(hy), w: px(780), h: 0,
    line: { color: "FFFFFF", width: 0.5 },
  });
}

// ---- table content: 8 rows x 18 columns (frame-verified values, att26 confirmed) ----
const rows = [
  { label: "x", vals: ["7", "7.2", "7.4", "7.6", "7.8", "8", "8.2", "8.4", "8.6", "8.8", "9", "9.2", "9.4", "9.6", "9.8", "9.6", "9.8", "9.6"] },
  { label: "f(x)", vals: ["2.99", "2.43", "1.66", "0.69", "-0.45", "-1.73", "-3.1", "-4.5", "-5.88", "-7.16", "-8.28", "-9.17", "-9.77", "-10.03", "-9.92", "-10.03", "-9.92", "-10.03"] },
  { label: "x-delta", vals: ["6.9", "7.1", "7.3", "7.5", "7.7", "7.9", "8.1", "8.3", "8.5", "8.7", "8.9", "9.1", "9.3", "9.5", "9.7", "9.5", "9.7", "9.5"] },
  { label: "f(x-delta)", vals: ["3.19", "2.74", "2.07", "1.2", "0.14", "-1.08", "-2.41", "-3.8", "-5.2", "-6.54", "-7.75", "-8.76", "-9.51", "-9.95", "-10.02", "-9.95", "-10.02", "-9.95"] },
  { label: "x+delta", vals: ["7.1", "7.3", "7.5", "7.7", "7.9", "8.1", "8.3", "8.5", "8.7", "8.9", "9.1", "9.3", "9.5", "9.7", "9.9", "9.7", "9.9", "9.7"] },
  { label: "f(x+delta)", vals: ["2.74", "2.07", "1.2", "0.14", "-1.08", "-2.41", "-3.8", "-5.2", "-6.54", "-7.75", "-8.76", "-9.51", "-9.95", "-10.02", "-9.7", "-10.02", "-9.7", "-10.02"] },
  { label: "slope", vals: ["-4.5", "-6.7", "-8.7", "-10.6", "-12.2", "-13.3", "-13.9", "-14", "-13.4", "-12.1", "-10.1", "-7.5", "-4.4", "-0.7", "3.2", "-0.7", "3.2", "-0.7"] },
  { label: "next x", vals: ["7.2", "7.4", "7.6", "7.8", "8", "8.2", "8.4", "8.6", "8.8", "9", "9.2", "9.4", "9.6", "9.8", "9.6", "9.8", "9.6", "9.8"] },
];
const row_ys = [341, 359, 383, 401, 427, 445, 469, 493];
for (let ri = 0; ri < rows.length; ri++) {
  const ymid = row_ys[ri];
  slide.addText(rows[ri].label, {
    x: px(88), y: px(ymid - 7), w: px(53), h: px(14),
    align: "right", valign: "middle", margin: 0,
    fontFace: A, fontSize: 8, bold: true, color: "000000",
  });
  for (let ci = 0; ci < 18; ci++) {
    const inCyan = (ri < 2 && ci >= 13 && ci <= 15);
    slide.addText(rows[ri].vals[ci], {
      x: px(SEP[ci]), y: px(ymid - 7), w: px(SEP[ci + 1] - SEP[ci]), h: px(14),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 8, bold: true,
      color: inCyan ? "006400" : "000000",
    });
  }
}

// ================= RED HOLLOW BLOCK ARROW (after the table — it overlaps its top rule) =================
slide.addShape(pptx.ShapeType.downArrow, {
  x: px(162), y: px(304), w: px(22), h: px(35), rotate: 17,
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1.5 },
});

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});
