const pptxgen = require("pptxgenjs");

// Slide 21 — Effect of Selecting Threshold Value on Model Performance
// Geometry measured from unique_slides/slide_021.jpg (960x540, 1px = 1pt -> inches = px/72).
// House chrome per root AGENTS.md 2026-10-09 (overrides everything).
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const FONT = "Arial";

const DARKRED = "9C0006";   // model box fill (measured ~#9E0000)
const DARKRED_LINE = "600000";
const BLUE = "0000FF";      // (0 --- 1) box
const BLUE_TXT = "1F3864";
const CALLOUT_FILL = "F5E6C8"; // measured ~#F0F0DC pale peach
const CALLOUT_LINE = "C00000";
const GREEN_FILL = "D1F2DD";   // Class I oval (measured ~#D1F2DD)
const PLUM_FILL = "FBD5FE";    // Class II oval (measured ~#FBD5FE)
const GRAY = "404040";         // airplane sketch ink
const SIGPURPLE = "800080";
const SIGLAV = "E6C8F0";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- house chrome ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  line: { color: RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText("21", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
s.addText("Effect of Selecting Threshold Value on Model Performance", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.62,
  align: "center", valign: "middle",
  fontSize: 24, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
});

// px -> in helper
const I = (px) => px / 72;

// ---- confusion-matrix table builder ----
// frame: x 57..230 px, top y; 3 columns: label col 57-129, cell1 129-228 (divider 129-137), cell2 228-230...
// measured verticals: outer 57-59 & 64-67 (double border), dividers 129-137 and 228-230.
// We draw: outer rect x=I(57) w=I(230-57); vertical lines at x=I(129) and x=I(228).
function confusionTable(topPx, rows) {
  // rows: array of {label, c1, c2, circleC1}
  const x0 = I(57), y0 = I(topPx), w = I(230 - 57);
  const headerH = I(108 - topPx);       // header band to first inner horiz (108-110)
  const colHeadH = I(147 - 108);         // P/N header band (108..147)
  const rowH = I(198 - 147);             // data rows (147..198)
  const totalH = headerH + colHeadH + 2 * rowH;
  // outer border (red)
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x0, y: y0, w: w, h: totalH,
    fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 },
  });
  // header text "Predicted as" spanning the two data columns
  s.addText("Predicted as", {
    x: I(108), y: y0 + I(2), w: I(228 - 108), h: I(24),
    align: "center", valign: "middle",
    fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
  // vertical divider between label col and cells (x=129), from below header to bottom
  s.addShape(pptx.shapes.RECTANGLE, {
    x: I(129), y: y0, w: I(230 - 129) - I(230 - 228) > 0 ? I(1) : I(1), h: totalH,
    fill: { color: RED }, line: { color: RED, width: 0.75 },
  });
  // divider between the two cells (x=228)
  s.addShape(pptx.shapes.RECTANGLE, {
    x: I(228), y: y0, w: I(1), h: totalH,
    fill: { color: RED }, line: { color: RED, width: 0.75 },
  });
  // horizontal line under header band (y=108)
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x0, y: I(108), w: w, h: I(1.5), fill: { color: RED }, line: { color: RED, width: 0.5 },
  });
  // horizontal line under col headers (y=147)
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x0 + I(72), y: I(147), w: I(230 - 129), h: I(1.5), fill: { color: RED }, line: { color: RED, width: 0.5 },
  });
  // horizontal line between rows (y=175)
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x0 + I(72), y: I(175), w: I(230 - 129), h: I(1.5), fill: { color: RED }, line: { color: RED, width: 0.5 },
  });
  // column headers P, N
  s.addText("P", {
    x: I(129), y: I(111), w: I(99), h: I(34), align: "center", valign: "middle",
    fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
  });
  s.addText("N", {
    x: I(228), y: I(111), w: I(2) + I(0), h: I(34), align: "center", valign: "middle",
    fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
  });
  // fix N width: give it the remaining 2px? use cell2 width 230-228=2px too small; actual cell2 is 228..230? No:
  // measured verticals at 228-230 are the RIGHT border; cell2 spans 137..228. Recompute below instead.
  return { x0, y0, w, headerH, colHeadH, rowH };
}

// NOTE: the layout is: label col 57..129, cell1 129..228? No — measured verticals 129-137 AND 228-230.
// Interpretation: outer left 57-67, divider1 129-137, right border 228-230. So label col = 67..129,
// cell1 = 137..228? That leaves only ONE data column between dividers... but two headers P and N exist.
// Actual: verticals at 129-137 is divider between label col and cell1; 228-230 is right border; the P/N
// split is at x~178 (mid). Simpler faithful approach: draw grid with dividers at 129 and 178 and right 228.
function confusionTable2(topPx, bottomPx, headerText, colHeads, rowLabels, cells, circleCell) {
  const x0 = I(57), y0 = I(topPx), w = I(230 - 57), h = I(bottomPx - topPx);
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x0, y: y0, w: w, h: h,
    fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 },
  });
  const xDiv1 = I(129);        // label col | cells
  const xDiv2 = I(178);        // cell1 | cell2
  const xR = I(228);
  // header band: "Predicted as" spans both cell columns
  const yHeadEnd = I(topPx + 27); // ~108 when top=81
  s.addShape(pptx.shapes.RECTANGLE, { x: xDiv1, y: yHeadEnd, w: xR - xDiv1, h: I(1.5), fill: { color: RED }, line: { color: RED, width: 0.5 } });
  s.addText(headerText, {
    x: xDiv1, y: y0 + I(1), w: xR - xDiv1, h: I(25),
    align: "center", valign: "middle",
    fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
  // column header band y 108..147 with P and N
  const yColEnd = I(topPx + 66);
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: yColEnd, w: w, h: I(1.5), fill: { color: RED }, line: { color: RED, width: 0.5 } });
  s.addText(colHeads[0], {
    x: xDiv1, y: yHeadEnd + I(1), w: xDiv2 - xDiv1, h: yColEnd - yHeadEnd - I(1),
    align: "center", valign: "middle", fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
  });
  s.addText(colHeads[1], {
    x: xDiv2, y: yHeadEnd + I(1), w: xR - xDiv2, h: yColEnd - yHeadEnd - I(1),
    align: "center", valign: "middle", fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
  });
  // vertical dividers full height
  s.addShape(pptx.shapes.RECTANGLE, { x: xDiv1, y: y0, w: I(1.5), h: h, fill: { color: RED }, line: { color: RED, width: 0.5 } });
  s.addShape(pptx.shapes.RECTANGLE, { x: xDiv2, y: yHeadEnd, w: I(1.5), h: y0 + h - yHeadEnd, fill: { color: RED }, line: { color: RED, width: 0.5 } });
  // row divider (middle of the two data rows)
  const yMid = I((topPx + 66 + bottomPx) / 2);
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: yMid, w: w, h: I(1.5), fill: { color: RED }, line: { color: RED, width: 0.5 } });
  // row labels P, N (vertical "Actual" handled separately)
  s.addText(rowLabels[0], {
    x: x0, y: yColEnd + I(1), w: xDiv1 - x0, h: yMid - yColEnd - I(1),
    align: "center", valign: "middle", fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
  });
  s.addText(rowLabels[1], {
    x: x0, y: yMid + I(1), w: xDiv1 - x0, h: y0 + h - yMid - I(1),
    align: "center", valign: "middle", fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
  });
  // cells
  const cellBoxes = [
    { x: xDiv1, y: yColEnd + I(1), w: xDiv2 - xDiv1, h: yMid - yColEnd - I(1) },
    { x: xDiv2, y: yColEnd + I(1), w: xR - xDiv2, h: yMid - yColEnd - I(1) },
    { x: xDiv1, y: yMid + I(1), w: xDiv2 - xDiv1, h: y0 + h - yMid - I(1) },
    { x: xDiv2, y: yMid + I(1), w: xR - xDiv2, h: y0 + h - yMid - I(1) },
  ];
  cells.forEach((c, i) => {
    s.addText(c, {
      x: cellBoxes[i].x, y: cellBoxes[i].y, w: cellBoxes[i].w, h: cellBoxes[i].h,
      align: "center", valign: "middle",
      fontSize: 13, bold: i === circleCell, color: DARK, fontFace: FONT, margin: 0,
    });
  });
  if (circleCell >= 0) {
    const b = cellBoxes[circleCell];
    s.addShape(pptx.shapes.OVAL, {
      x: b.x + b.w / 2 - I(22), y: b.y + b.h / 2 - I(22), w: I(44), h: I(44),
      line: { color: "FF0000", width: 2 },
    });
  }
  // vertical "Actual" label along the far-left edge, rotated -90
  s.addText("Actual", {
    x: x0 - I(2) - I(60), y: y0 + h / 2 - I(8), w: I(60), h: I(16),
    align: "center", valign: "middle", rotate: -90,
    fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
}

// Table 1 (legend): y 81..198, cells TP/FP, FN/TN
confusionTable2(81, 198, "Predicted as", ["P", "N"], ["P", "N"], ["TP", "FP", "FN", "TN"], -1);
// Table 2 (data): y 198..263, cells 5 (circled), 0, 4, 2
confusionTable2(198, 263, "Predicted as", ["P", "N"], ["P", "N"], ["5", "0", "4", "2"], 0);

// ---- Threshold=0.1 callout (pale peach box with red border, x~250-345, y~108-136) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(250), y: I(108), w: I(95), h: I(28),
  fill: { color: CALLOUT_FILL }, line: { color: CALLOUT_LINE, width: 1.5 },
});
s.addText("Threshold=0.1", {
  x: I(250), y: I(108), w: I(95), h: I(28),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- flowchart row (y 99..197) ----
const FY0 = I(99), FY1 = I(197), FMID = I(148);
// Test Sample box x 324..448
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(324), y: FY0, w: I(448 - 324), h: FY1 - FY0,
  fill: { color: "FFFFFF" }, line: { color: DARKRED_LINE, width: 1.5 },
});
s.addText("Test Sample", {
  x: I(324), y: I(120), w: I(124), h: I(18),
  align: "center", valign: "middle",
  fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// airplane sketch inside Test Sample box (centered ~x386, y165)
function drawPlane(slide, cx, cy, w) {
  const h = w * 0.40;
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: cx - w / 2, y: cy - h * 0.10, w: w, h: h * 0.20,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, adjustValue: 0.5,
  });
  slide.addShape(pptx.shapes.OVAL, {
    x: cx + w / 2 - h * 0.24, y: cy - h * 0.11, w: h * 0.24, h: h * 0.22,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 },
  });
  slide.addShape(pptx.shapes.LINE, { x: cx + w / 2 + 0.02, y: cy - h * 0.32, w: 0, h: h * 0.64, line: { color: GRAY, width: 1.5 } });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx + w * 0.14, y: cy + h * 0.05, w: w * 0.22, h: h * 0.45,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, rotate: 205,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx + w * 0.14, y: cy - h * 0.50, w: w * 0.22, h: h * 0.45,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, rotate: 155,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w * 0.44, y: cy + h * 0.04, w: w * 0.18, h: h * 0.36,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, rotate: 195,
  });
  slide.addShape(pptx.shapes.ISOSCELES_TRIANGLE, {
    x: cx - w * 0.44, y: cy - h * 0.40, w: w * 0.18, h: h * 0.36,
    fill: { color: "FFFFFF" }, line: { color: GRAY, width: 1.25 }, rotate: 165,
  });
  for (let i = 0; i < 3; i++) {
    slide.addShape(pptx.shapes.OVAL, {
      x: cx + w * 0.06 + i * w * 0.11, y: cy - h * 0.05, w: h * 0.10, h: h * 0.10,
      fill: { color: "FFFFFF" }, line: { color: GRAY, width: 0.75 },
    });
  }
}
drawPlane(s, I(386), I(166), I(46));

// arrow Test Sample -> Model (x 448..470? measured gap 448-571 is model box start... arrow between)
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(440), y: FMID - I(8), w: I(20), h: I(16),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});

// Model box x 448..571, y 119..181, dark red fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(448), y: I(119), w: I(571 - 448), h: I(181 - 119),
  fill: { color: DARKRED }, line: { color: DARKRED_LINE, width: 1.5 },
});
s.addText("Model", {
  x: I(448), y: I(122), w: I(123), h: I(18),
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("[Any value] \u2192 (0, +1)", {
  x: I(448), y: I(142), w: I(123), h: I(14),
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: "FFFF00", fontFace: FONT, margin: 0,
});
// sigmoid icon circle inside model box, right side (x~530-560, y~125-155)
s.addShape(pptx.shapes.OVAL, {
  x: I(528), y: I(124), w: I(34), h: I(34),
  fill: { color: SIGLAV }, line: { color: SIGPURPLE, width: 1 },
});
s.addShape(pptx.shapes.LINE, { x: I(531), y: I(141), w: I(28), h: 0, line: { color: SIGPURPLE, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: I(545), y: I(127), w: 0, h: I(28), line: { color: SIGPURPLE, width: 0.75 } });
(function () {
  const steps = 16;
  let px = null, py = null;
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps - 0.5) * 8;
    const sig = 1 / (1 + Math.exp(-t));
    const x = I(533) + (i / steps) * I(24);
    const y = I(154) - sig * I(24);
    if (px !== null) s.addShape(pptx.shapes.LINE, { x: px, y: py, w: x - px, h: y - py, line: { color: SIGPURPLE, width: 1 } });
    px = x; py = y;
  }
})();

// arrow Model -> blue box
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(572), y: FMID - I(8), w: I(18), h: I(16),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});

// blue box "(0 --- 1)" x 590..688, y 119..181; label "Predicted Value" above
s.addText("Predicted Value", {
  x: I(590), y: I(103), w: I(98), h: I(14),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(590), y: I(119), w: I(98), h: I(62),
  fill: { color: "DCE6F5" }, line: { color: BLUE, width: 1.5 },
});
s.addText("(0 --- 1)", {
  x: I(590), y: I(119), w: I(98), h: I(62),
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// arrow blue box -> threshold box
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(689), y: FMID - I(8), w: I(10), h: I(16),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});

// threshold vertical box x 700..731, y 109..188 (red border, white fill, vertical text)
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(700), y: I(109), w: I(31), h: I(79),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 },
});
s.addText("Threshold (e.g. 0.5)", {
  x: I(700) - I(30), y: I(148) - I(8), w: I(91), h: I(16),
  align: "center", valign: "middle", rotate: -90,
  fontSize: 9, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// branching arrows threshold -> ovals
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(733), y: I(138), w: I(30), h: I(12),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(733), y: I(168), w: I(30), h: I(12),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});

// Class I oval (green) x 765..825, y 133..163
s.addShape(pptx.shapes.OVAL, {
  x: I(765), y: I(133), w: I(60), h: I(30),
  fill: { color: GREEN_FILL }, line: { color: "2E7D32", width: 1 },
});
s.addText("Class I", {
  x: I(765), y: I(133), w: I(60), h: I(30),
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// Class II oval (plum) x 765..825, y 163..193
s.addShape(pptx.shapes.OVAL, {
  x: I(765), y: I(163), w: I(60), h: I(30),
  fill: { color: PLUM_FILL }, line: { color: "8E24AA", width: 1 },
});
s.addText("Class II", {
  x: I(765), y: I(163), w: I(60), h: I(30),
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// ---- bottom scatter plot (y 330..503) ----
// plot frame area x 68..895, y 330..503 (inside the slide's own border which we do NOT redraw;
// the house red frame serves as outer border). Red x-axis at y 500..503.
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(68), y: I(500), w: I(895 - 68), h: I(3),
  fill: { color: RED }, line: { color: RED, width: 0.5 },
});
// tick marks + labels 0.0, 0.5, 1.0 at x 84-103, 467-486, 857-875 (y 451-461 labels above axis)
function tick(xc, label) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: I(xc), y: I(500), w: I(1.5), h: I(8),
    fill: { color: DARK }, line: { color: DARK, width: 0.5 },
  });
  s.addText(label, {
    x: I(xc - 10), y: I(505), w: I(24), h: I(12),
    align: "center", valign: "top",
    fontSize: 10, color: DARK, fontFace: FONT, margin: 0,
  });
}
tick(84, "0.0");
tick(467, "0.5");
tick(857, "1.0");
// dashed vertical threshold line at x 162-166, y 330..500 (blue dashes)
(function () {
  const x = I(164);
  for (let y = 330; y < 500; y += 12) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: x, y: I(y), w: I(2), h: I(7),
      fill: { color: BLUE }, line: { color: BLUE, width: 0.25 },
    });
  }
})();
// airplane scatter icons (measured cluster centers, px): 
const planes = [
  [153, 356], [249, 383], [362, 347], [547, 355], [553, 387], [719, 371], [822, 371],
];
planes.forEach(([cx, cy]) => drawPlane(s, I(cx), I(cy), I(40)));

pptx.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_021_recreated.pptx"
}).then(() => console.log("done"));
