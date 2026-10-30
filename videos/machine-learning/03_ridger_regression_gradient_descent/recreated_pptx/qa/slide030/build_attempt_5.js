/**
 * Slide 030 build — Convex Function, Learning Rate =0.2, Start at X=3
 * Measured from unique_slides/slide_030.jpg (960x540, 1px = 1pt).
 *
 * 2026-10-24 rebuild (worker w030, attempt 2) — fixes the previous build's
 * catastrophic z-order bug (drawHouseChrome LAST painted the opaque E9E9E7
 * panel over ALL content) and re-derives the whole composition from the frame:
 *   - fine 1-unit grid plot (x572..810, y65..311), axes x=0 at 630.5 / y=0 at
 *     266.5, parabola f(x)=(x-5)^2+1, red dashed x=5, black secant y=10 with
 *     three dots + gray "3" span labels, red/green point markers + labels
 *   - iteration table: navy outer frame + 5 colour-banded groups with their own
 *     border colours (olive / purple / tan / green / red), label col 61px +
 *     11 value cols x 44px, white gutters between groups
 *   - param table: navy border, row fills green/pink/yellow (frame truth; the
 *     spec's "white value cells" does not match the frame)
 *   - equation f(x)=(x-5)^2+1 as 2D mathtext PNG at measured 119px ink width;
 *     "X = 5" re-rendered in RED (previous asset was black)
 *   - callout is a filled lavender box (not an underline rule), text italic
 *   - title widened to the measured 58..556 ink span (old box 370px forced wrap)
 *
 * Measured geometry (frame px, 1px = 1pt):
 *   title ink x58..556 y65..84 (red C00000 / green 008000 / red)
 *   param table x103..237 y199..281 (col split 180; rows 226/253)
 *   upper red eq box x399..530 y185..212 ; eq ink x404..523 y190..208
 *   green box x348..554 y234..281 ; "X = 5" ink 354..417 y240..251 ;
 *     line2 ink 353..547 y260..277
 *   callout box x335..569 y292..320, fill F7C8FA, border purple, text ink
 *     344..554 y300..315
 *   plot x572..810 y65..311 ; x-axis y265..266 ; y-axis x630..631 ;
 *     grid 11.45px/unit x, 12.0px/unit y ; dashed x=5 at 687..689 ;
 *     secant y145..147 from x654 to x722, dots at 654/688/722 ;
 *     gray "3" labels at 671/705 y133..141 ; (2,10) x631..660 y150..166 ;
 *     (7,7) x725..748 y143..150 ; red dot (662,183) d8 ; green dot (688,255) d9
 *   red arrow (white fill, red outline, tilted) x172..194 y304..340
 *   iteration table navy frame x78..654 y325..530 ; cell block x89..634,
 *     y334..523 ; label col 89..150 ; 11 value cols 44px from 150 to 634
 */
const path = require("path");
const pptxgen = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const slide = pres.addSlide();

const FONT = "Arial";
const PT = 1 / 72; // 1pt in inches
const ST = pres.ShapeType;
const px = (v) => v * PT;

const COL = {
  titleRed: "C00000",
  titleGreen: "008000",
  bodyBlack: "000000",
  formulaBlue: "0000FF",
  calloutPurple: "7030A0",
  calloutFill: "F7C8FA",
  calloutBorder: "B761BE",
  greenBoxFill: "EAF6E3",
  upBoxBorder: "C00000",
  formulaBorder: "00B050",
  paramBorder: "000080",
  paramRow1: "E2EFDA",
  paramRow2: "FFC7CE",
  paramRow3: "FFFF00",
  iterFrame: "000080",
  iterG1Fill: "D6E17D",
  iterG1Border: "A6AD55",
  iterG2Fill: "D4B1F1",
  iterG2Border: "A98FC7",
  iterG3Fill: "F3DBBE",
  iterG3Border: "C8A47B",
  iterSlopeFill: "D5F5C5",
  iterSlopeBorder: "00B050",
  iterStopFill: "F7BFC6",
  iterStopBorder: "C00000",
  plotFrame: "C00000",
  gridGray: "D9D9D9",
  axisBlack: "000000",
  parabolaBlue: "4F81BD",
  tickGray: "404040",
  labelGray: "7F7F7F",
  threeGray: "A0A0B0",
};

const ASSETS = path.resolve(__dirname, "assets");

// ------------------------------------------------ 0. HOUSE CHROME (BOTTOM layer)
// The panel is opaque: it must be painted FIRST, content on top of it.
drawHouseChrome(pres, slide, { numeral: "30" });

// ---------------------------------------------------------------- 1. TITLE
slide.addText([
  { text: "Convex Function,  ", options: { fontSize: 20, bold: true, color: COL.titleRed, fontFace: FONT } },
  { text: "Learning Rate =0.2,  ", options: { fontSize: 20, bold: true, color: COL.titleGreen, fontFace: FONT } },
  { text: "Start at X=3", options: { fontSize: 20, bold: true, color: COL.titleRed, fontFace: FONT } },
], {
  x: px(57), y: px(62), w: px(543), h: px(30),
  margin: 0, align: "left", valign: "middle",
});

// ------------------------------------------------- 2. PARAMETER TABLE
// Frame truth: navy border, all cells of a row share its fill
// (row1 light green, row2 pink, row3 yellow) — spec's "white value cells" is wrong.
slide.addTable(
  [
    ["step", "0.2"],
    ["initial X", "3"],
    ["delta", "0.1"],
  ].map((row, ri) => row.map((cell) => ({
    text: cell,
    options: {
      fontSize: 12, bold: true, color: COL.bodyBlack, fontFace: FONT,
      fill: { color: [COL.paramRow1, COL.paramRow2, COL.paramRow3][ri] },
      margin: [0.014, 0.04, 0.014, 0.04], align: "center", valign: "middle",
      border: { pt: 0.75, color: "808080" },
    },
  }))),
  {
    x: px(104), y: px(200), w: px(132), h: px(80),
    colW: [px(76), px(56)],
    rowH: [px(26), px(26), px(28)],
  }
);
// navy outer frame (measured x103..237 y199..281)
slide.addShape(ST.rect, {
  x: px(103), y: px(199), w: px(134), h: px(82),
  fill: { type: "none" },
  line: { color: COL.paramBorder, width: 1.5 },
});

// --------------------------------------------- 3. UPPER EQUATION BOX (red)
// Box x399..530 y185..212; eq ink 119x18px. 2D mathtext PNG placed at the
// measured ink width (119px), baseline on the measured ink bottom (y=208).
{
  const fs = require(path.join(ASSETS, "eq_030_fx.json"));
  const wIn = 119 / 72;                       // measured ink width
  const hIn = (fs.h_px / fs.w_px) * wIn;      // 16.35px tall
  slide.addShape(ST.rect, {
    x: px(399), y: px(185), w: px(131), h: px(27),
    fill: { color: "FFFFFF" },
    line: { color: COL.upBoxBorder, width: 1.5 },
  });
  slide.addImage({
    path: path.join(ASSETS, "eq_030_fx.png"),
    x: px(405), y: px(208 - fs.baseline_frac * (hIn * 72)),
    w: wIn, h: hIn,
  });
}

// ------------------------------------------ 4. GREEN FORMULA BOX
// Box x348..554 y234..281 (pale green fill). "X = 5" red mathtext,
// then "f(x) Minimum value is 1.0" (black + blue 1.0).
slide.addShape(ST.rect, {
  x: px(348), y: px(234), w: px(206), h: px(47),
  fill: { color: COL.greenBoxFill },
  line: { color: COL.formulaBorder, width: 2 },
});
{
  const x5 = require(path.join(ASSETS, "eq_030_x5_red.json"));
  const wIn = x5.w_in;                        // natural 18pt size (58.7pt wide)
  const hIn = x5.h_in;                        // 15.24pt
  slide.addImage({
    path: path.join(ASSETS, "eq_030_x5_red.png"),
    x: px(354), y: px(251 - x5.baseline_frac * (hIn * 72)),
    w: wIn, h: hIn,
  });
}
slide.addText([
  { text: "f(x)", options: { fontSize: 16, italic: true, color: COL.formulaBlue, fontFace: FONT } },
  { text: " Minimum value is ", options: { fontSize: 16, color: COL.bodyBlack, fontFace: FONT } },
  { text: "1.0", options: { fontSize: 17, bold: true, color: COL.formulaBlue, fontFace: FONT } },
], {
  x: px(352), y: px(258), w: px(200), h: px(20),
  align: "center", valign: "middle", margin: 0,
});

// ------------------------------------------------------- 5. CALLOUT
// A filled lavender box with purple border — NOT an underline rule.
slide.addShape(ST.rect, {
  x: px(335), y: px(292), w: px(234), h: px(28),
  fill: { color: COL.calloutFill },
  line: { color: COL.calloutBorder, width: 1.5 },
});
slide.addText("Reach Minimum after 11 Steps", {
  x: px(335), y: px(292), w: px(234), h: px(28),
  fontSize: 14, bold: true, italic: true, color: COL.calloutPurple, fontFace: FONT,
  align: "center", valign: "middle", margin: 0,
});

// ------------------------------------------------------- 6. PLOT
const BX0 = 572, BX1 = 810, BY0 = 65, BY1 = 311;
const X0 = 630.5;      // frame px of x = 0
const Y0 = 266.5;      // frame px of y = 0
const UX = 11.45;      // px per x unit
const UY = 12.0;       // px per y unit
const XS = (v) => X0 + v * UX;
const YS = (v) => Y0 - v * UY;

// white plot background + red frame
slide.addShape(ST.rect, {
  x: px(BX0), y: px(BY0), w: px(BX1 - BX0), h: px(BY1 - BY0),
  fill: { color: "FFFFFF" },
  line: { color: COL.plotFrame, width: 1.5 },
});

// fine 1-unit grid (solid light gray) across the whole plot area
for (let k = -5; k <= 15; k++) {
  const x = XS(k);
  if (x <= BX0 + 1 || x >= BX1 - 1) continue;
  slide.addShape(ST.line, {
    x: px(x), y: px(BY0 + 1), w: 0, h: px(BY1 - BY0 - 2),
    line: { color: COL.gridGray, width: 0.5 },
  });
}
for (let k = -3; k <= 16; k++) {
  const y = YS(k);
  if (y <= BY0 + 1 || y >= BY1 - 1) continue;
  slide.addShape(ST.line, {
    x: px(BX0 + 1), y: px(y), w: px(BX1 - BX0 - 2), h: 0,
    line: { color: COL.gridGray, width: 0.5 },
  });
}

// black axes (full span, measured y-axis x630..631, x-axis y265..266)
slide.addShape(ST.line, {
  x: px(X0), y: px(BY0 + 0.5), w: 0, h: px(BY1 - BY0 - 1),
  line: { color: COL.axisBlack, width: 1.2 },
});
slide.addShape(ST.line, {
  x: px(BX0 + 0.5), y: px(265.8), w: px(BX1 - BX0 - 1), h: 0,
  line: { color: COL.axisBlack, width: 1.2 },
});

// tick labels (measured centres)
[[-5, 580.5], [0, 625.5], [5, 688], [10, 745], [15, 804]].forEach(([v, cx]) => {
  slide.addText(String(v), {
    x: px(cx - 13), y: px(269), w: px(26), h: px(12),
    fontSize: 9, color: COL.tickGray, fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});
[[15, 85], [10, 146], [5, 205]].forEach(([v, cy]) => {
  slide.addText(String(v), {
    x: px(596), y: px(cy - 6), w: px(26), h: px(12),
    fontSize: 9, color: COL.tickGray, fontFace: FONT, align: "right", valign: "middle", margin: 0,
  });
});

// red dashed vertical at x = 5
slide.addShape(ST.line, {
  x: px(XS(5)), y: px(BY0 + 1), w: 0, h: px(BY1 - BY0 - 2),
  line: { color: COL.plotFrame, width: 1, dashType: "dash" },
});

// THE CURVE: f(x) = (x-5)^2 + 1, clipped to the plot top (y <= 17)
{
  const halfW = Math.sqrt((Y0 - BY0) / UY - 1); // |x-5| where curve exits the top
  const pts = [];
  for (let xd = 5 - halfW; xd <= 5 + halfW + 1e-9; xd += 0.05) {
    pts.push({ x: XS(xd), y: YS(Math.pow(xd - 5, 2) + 1) });
  }
  pts.push({ x: XS(5 + halfW), y: YS(Math.pow(halfW, 2) + 1) });
  for (let i = 0; i < pts.length - 1; i++) {
    slide.addShape(ST.line, {
      x: px(pts[i].x), y: px(pts[i].y),
      w: px(pts[i + 1].x - pts[i].x), h: px(pts[i + 1].y - pts[i].y),
      line: { color: COL.parabolaBlue, width: 2 },
    });
  }
}

// black secant segment y = 10 from x = 2 to x = 8, with three dots
slide.addShape(ST.line, {
  x: px(XS(2)), y: px(146.3), w: px(XS(8) - XS(2)), h: 0,
  line: { color: COL.axisBlack, width: 2.5 },
});
[2, 5, 8].forEach((v) => {
  slide.addShape(ST.ellipse, {
    x: px(XS(v) - 3.5), y: px(146.3 - 3.5), w: px(7), h: px(7),
    fill: { color: COL.axisBlack }, line: { color: COL.axisBlack, width: 0 },
  });
});
// gray "3" span labels above the secant halves
[[671.5, "3"], [705.5, "3"]].forEach(([cx]) => {
  slide.addText("3", {
    x: px(cx - 8), y: px(131), w: px(16), h: px(12),
    fontSize: 9, italic: true, color: COL.threeGray, fontFace: FONT,
    align: "center", valign: "middle", margin: 0,
  });
});

// point markers + labels (measured)
slide.addShape(ST.ellipse, {
  x: px(658), y: px(179), w: px(8), h: px(8),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
});
slide.addShape(ST.ellipse, {
  x: px(683.9), y: px(250.5), w: px(9), h: px(9),
  fill: { color: "00B050" }, line: { color: "00B050", width: 0 },
});

slide.addText("(2, 10)", {
  x: px(634), y: px(152), w: px(46), h: px(13),
  fontSize: 9, italic: true, color: COL.labelGray, fontFace: FONT, margin: 0, align: "left",
});
slide.addText("(7, 7)", {
  x: px(724), y: px(144), w: px(40), h: px(13),
  fontSize: 9, italic: true, color: COL.labelGray, fontFace: FONT, margin: 0, align: "left",
});
slide.addText("(5, 1)", {
  x: px(696), y: px(244), w: px(36), h: px(13),
  fontSize: 9, italic: true, color: COL.labelGray, fontFace: FONT, margin: 0, align: "left",
});

// --------------------------------------------------- 7. RED DOWN ARROW
// White-filled block arrow with red outline, tilted ~15° (measured bbox
// x172..194 y304..340; tip points down-left).
slide.addShape(ST.downArrow, {
  x: px(173), y: px(306), w: px(19), h: px(30),
  fill: { color: "FFFFFF" },
  line: { color: COL.titleRed, width: 1.5 },
  rotate: 15,
});

// --------------------------------------------- 8. ITERATION TABLE
// Navy outer frame x78..654 y325..530; cell block x89..634 y334..523.
// 12 columns: label 61px + 11 value columns of 44px.
const COLW = [px(61)].concat(Array(11).fill(px(44)));

const iterGroups = [
  {
    rows: [
      ["x", "3", "3.2", "3.4", "3.6", "3.8", "4", "4.2", "4.4", "4.6", "4.8", "5"],
      ["f(x)", "5", "4.24", "3.56", "2.96", "2.44", "2", "1.64", "1.36", "1.16", "1.04", "1"],
    ],
    x: 89, y: 334, h: 43, rowH: [px(21.5), px(21.5)],
    fill: COL.iterG1Fill, border: COL.iterG1Border,
    redCells: [[0, 1], [0, 11]],
  },
  {
    rows: [
      ["x-delta", "2.9", "3.1", "3.3", "3.5", "3.7", "3.9", "4.1", "4.3", "4.5", "4.7", "4.9"],
      ["f(x-delta)", "5.41", "4.61", "3.89", "3.25", "2.69", "2.21", "1.81", "1.49", "1.25", "1.09", "1.01"],
    ],
    x: 89, y: 380, h: 43, rowH: [px(21.5), px(21.5)],
    fill: COL.iterG2Fill, border: COL.iterG2Border,
    redCells: [],
  },
  {
    rows: [
      ["x+delta", "3.1", "3.3", "3.5", "3.7", "3.9", "4.1", "4.3", "4.5", "4.7", "4.9", "5.1"],
      ["f(x+delta)", "4.61", "3.89", "3.25", "2.69", "2.21", "1.81", "1.49", "1.25", "1.09", "1.01", "1.01"],
    ],
    x: 89, y: 427, h: 43, rowH: [px(21.5), px(21.5)],
    fill: COL.iterG3Fill, border: COL.iterG3Border,
    redCells: [],
  },
  {
    rows: [
      ["slope", "-8", "-7.2", "-6.4", "-5.6", "-4.8", "-4", "-3.2", "-2.4", "-1.6", "-0.8", "0"],
    ],
    x: 89, y: 473, h: 24, rowH: [px(24)],
    fill: COL.iterSlopeFill, border: COL.iterSlopeBorder,
    redCells: [],
  },
  {
    rows: [
      ["next x", "3.2", "3.4", "3.6", "3.8", "4", "4.2", "4.4", "4.6", "4.8", "5", "stop"],
    ],
    x: 89, y: 499, h: 24, rowH: [px(24)],
    fill: COL.iterStopFill, border: COL.iterStopBorder,
    redCells: [],
  },
];

iterGroups.forEach((grp) => {
  slide.addTable(
    grp.rows.map((row, ri) => row.map((cell, ci) => {
      const isRed = grp.redCells.some(([r2, c2]) => r2 === ri && c2 === ci);
      return {
        text: cell,
        options: {
          fontSize: 9, bold: true,
          color: isRed ? COL.titleRed : COL.bodyBlack,
          fontFace: FONT,
          fill: { color: grp.fill },
          margin: [0.006, 0.028, 0.006, 0.028],
          align: "center", valign: "middle",
          border: { pt: 1, color: grp.border },
        },
      };
    })),
    {
      x: px(grp.x), y: px(grp.y), w: px(545), h: px(grp.h),
      colW: COLW, rowH: grp.rowH,
    }
  );
});
// navy outer frame
slide.addShape(ST.rect, {
  x: px(78), y: px(325), w: px(576), h: px(205),
  fill: { type: "none" },
  line: { color: COL.iterFrame, width: 2 },
});

// ---------------------------------------------- 9. BADGE (top-most, redrawn)
{
  const b = CHROME.badge;
  const bx = b.cx - b.d / 2, by = b.cy - b.d / 2;
  slide.addShape(ST.ellipse, {
    x: bx, y: by, w: b.d, h: b.d,
    fill: { color: b.fill },
    line: { color: b.ring, width: b.ringWidth },
  });
  slide.addText("30", {
    x: bx, y: by, w: b.d, h: b.d,
    align: "center", valign: "middle", bold: true,
    fontSize: b.numeralSize, color: b.numeralColor, fontFace: b.fontFace, margin: 0,
  });
}

// ---------------------------------------------------------------- output
const outPath = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_030_recreated.pptx";
pres.writeFile(outPath).then(() => {
  console.log("Written:", outPath);
}).catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
