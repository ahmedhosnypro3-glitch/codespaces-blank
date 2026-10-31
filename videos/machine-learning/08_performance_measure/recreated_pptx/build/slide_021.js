const pptxgen = require("pptxgenjs");

// Slide 21 — Effect of Selecting Threshold Value on Model Performance
// Geometry measured from unique_slides/slide_021.jpg (960x540, 1px = 1pt -> inches = px/72).
// Frame-vs-spec decisions (frame wins, measured with PIL):
//  - data matrix cells TP=5 (red-circled), FN=0, FP=4, TN=2 (11 samples; series-consistent,
//    see sources/slide_021_research.md); legend cells row P = TP, FN; row N = FP, TN
//    (banked docparse crop pool_run/docparse/slide021/crops/slide_021.crop01__chart.parse.md).
//  - model annotation corrected to "[Any value] -> (0, +1)" per slide_021_research.md.
//  - original content frame x58..902 y43..517 (house frame overrides in recreation);
//    plot x-axis red line at y436, tick labels below at y452-462, lower red line y500.
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";
const RED = "C00000";
const YELLOW = "FFF9C4";
const DARK = "333333";
const FONT = "Arial";

const DARKRED = "9C0006";
const DARKRED_LINE = "600000";
const BLUE = "0000FF";
const BLUE_TXT = "1F3864";
const PANEL_FILL = "FFF2CC";
const PANEL_LINE = "BFA05A";
const CALLOUT_FILL = "FFFF00";
const GREEN_FILL = "D1F2DD";
const GREEN_LINE = "2E7D32";
const PLUM_FILL = "FBD5FE";
const PLUM_LINE = "8E24AA";
const GRAY = "404040";
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

const I = (px) => px / 72;

// ---- confusion-matrix table builder (frame: x57..230, dividers x129 + x178) ----
function confusionTable(topPx, bottomPx, headerText, colHeads, rowLabels, cells, circleCell) {
  const x0 = I(57), y0 = I(topPx), w = I(230 - 57), h = I(bottomPx - topPx);
  s.addShape(pptx.shapes.RECTANGLE, {
    x: x0, y: y0, w: w, h: h,
    fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 },
  });
  const xDiv1 = I(129), xDiv2 = I(178), xR = I(228);
  const yHeadEnd = I(topPx + 27);
  s.addShape(pptx.shapes.RECTANGLE, { x: xDiv1, y: yHeadEnd, w: xR - xDiv1, h: I(1.5), fill: { color: RED }, line: { color: RED, width: 0.5 } });
  s.addText(headerText, {
    x: xDiv1, y: y0 + I(1), w: xR - xDiv1, h: I(25),
    align: "center", valign: "middle",
    fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
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
  s.addShape(pptx.shapes.RECTANGLE, { x: xDiv1, y: y0, w: I(1.5), h: h, fill: { color: RED }, line: { color: RED, width: 0.5 } });
  s.addShape(pptx.shapes.RECTANGLE, { x: xDiv2, y: yHeadEnd, w: I(1.5), h: y0 + h - yHeadEnd, fill: { color: RED }, line: { color: RED, width: 0.5 } });
  const yMid = I((topPx + 66 + bottomPx) / 2);
  s.addShape(pptx.shapes.RECTANGLE, { x: x0, y: yMid, w: w, h: I(1.5), fill: { color: RED }, line: { color: RED, width: 0.5 } });
  s.addText(rowLabels[0], {
    x: x0, y: yColEnd + I(1), w: xDiv1 - x0, h: yMid - yColEnd - I(1),
    align: "center", valign: "middle", fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
  });
  s.addText(rowLabels[1], {
    x: x0, y: yMid + I(1), w: xDiv1 - x0, h: y0 + h - yMid - I(1),
    align: "center", valign: "middle", fontSize: 12, bold: true, color: DARK, fontFace: FONT, margin: 0,
  });
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
  // vertical "Actual" label along the far-left edge, rotated -90 (box centered at x=25px)
  const cy = y0 + h / 2;
  s.addText("Actual", {
    x: I(25) - I(30), y: cy - I(8), w: I(60), h: I(16),
    align: "center", valign: "middle", rotate: -90,
    fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0,
  });
}

// Table 1 (legend): y 81..198, cells TP/FN ; FP/TN (row P then row N)
confusionTable(81, 198, "Predicted as", ["P", "N"], ["P", "N"], ["TP", "FN", "FP", "TN"], -1);
// Table 2 (data): y 198..263, cells 5 (circled) / 0 ; 4 / 2
confusionTable(198, 263, "Predicted as", ["P", "N"], ["P", "N"], ["5", "0", "4", "2"], 0);

// ---- Threshold=0.1 callout (yellow rounded box, red bold text) x240..345 y100..130 ----
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: I(240), y: I(100), w: I(105), h: I(30),
  fill: { color: CALLOUT_FILL }, line: { color: RED, width: 1.5 }, adjustValue: 0.35,
});
s.addText("Threshold=0.1", {
  x: I(240), y: I(100), w: I(105), h: I(30),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- beige pipeline panel x270..900 y70..200 ----
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: I(270), y: I(70), w: I(630), h: I(130),
  fill: { color: PANEL_FILL }, line: { color: PANEL_LINE, width: 1 }, adjustValue: 0.08,
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
function drawPlane(slide, cx, cy, w, dotColor, skull) {
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
  if (dotColor) {
    slide.addShape(pptx.shapes.OVAL, {
      x: cx - I(3), y: cy - h * 0.55 - I(3), w: I(6), h: I(6),
      fill: { color: dotColor }, line: { color: dotColor, width: 0.5 },
    });
  }
  if (skull) {
    slide.addShape(pptx.shapes.OVAL, {
      x: cx - I(5), y: cy - I(5), w: I(10), h: I(10),
      fill: { color: "000000" }, line: { color: "000000", width: 0.5 },
    });
    slide.addShape(pptx.shapes.LINE, { x: cx - I(6), y: cy - I(6), w: I(12), h: 0, line: { color: "FFFFFF", width: 1 } });
    slide.addShape(pptx.shapes.LINE, { x: cx - I(6), y: cy - I(6), w: 0, h: I(12), line: { color: "FFFFFF", width: 1 } });
  }
}
drawPlane(s, I(386), I(166), I(46));

// arrow Test Sample -> Model
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(452), y: FMID - I(8), w: I(20), h: I(16),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});

// Model box x 476..599, y 119..181, dark red fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(476), y: I(119), w: I(123), h: I(62),
  fill: { color: DARKRED }, line: { color: DARKRED_LINE, width: 1.5 },
});
s.addText("Model", {
  x: I(476), y: I(122), w: I(123), h: I(18),
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
// sigmoid icon circle inside model box, right side
s.addShape(pptx.shapes.OVAL, {
  x: I(556), y: I(124), w: I(34), h: I(34),
  fill: { color: SIGLAV }, line: { color: SIGPURPLE, width: 1 },
});
s.addShape(pptx.shapes.LINE, { x: I(559), y: I(141), w: I(28), h: 0, line: { color: SIGPURPLE, width: 0.75 } });
s.addShape(pptx.shapes.LINE, { x: I(573), y: I(127), w: 0, h: I(28), line: { color: SIGPURPLE, width: 0.75 } });
(function () {
  const steps = 16;
  let px = null, py = null;
  for (let i = 0; i <= steps; i++) {
    const t = (i / steps - 0.5) * 8;
    const sig = 1 / (1 + Math.exp(-t));
    const x = I(561) + (i / steps) * I(24);
    const y = I(154) - sig * I(24);
    if (px !== null) s.addShape(pptx.shapes.LINE, { x: px, y: py, w: x - px, h: y - py, line: { color: SIGPURPLE, width: 1 } });
    px = x; py = y;
  }
})();
// corrected annotation below the Model box
s.addText("[Any value] \u2192 (0, +1)", {
  x: I(476), y: I(183), w: I(123), h: I(14),
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// arrow Model -> blue box
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(600), y: FMID - I(8), w: I(18), h: I(16),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});

// blue box "(0 — 1)" x 620..718, y 119..181; label "Predicted Value" above
s.addText("Predicted Value", {
  x: I(620), y: I(103), w: I(98), h: I(14),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: BLUE_TXT, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(620), y: I(119), w: I(98), h: I(62),
  fill: { color: "DCE6F5" }, line: { color: BLUE, width: 1.5 },
});
s.addText("(0 \u2014 1)", {
  x: I(620), y: I(119), w: I(98), h: I(62),
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// arrow blue box -> threshold box
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(719), y: FMID - I(8), w: I(14), h: I(16),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});

// threshold box x 735..835, y 110..165 (white fill, red border, two-line text)
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(735), y: I(110), w: I(100), h: I(55),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1.5 },
});
s.addText("Threshold", {
  x: I(735), y: I(114), w: I(100), h: I(20),
  align: "center", valign: "middle",
  fontSize: 11, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("(e.g. 0.5)", {
  x: I(735), y: I(136), w: I(100), h: I(16),
  align: "center", valign: "middle",
  fontSize: 9, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// branching arrows threshold -> ovals
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(838), y: I(118), w: I(26), h: I(11),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});
s.addShape(pptx.shapes.RIGHT_ARROW, {
  x: I(838), y: I(148), w: I(26), h: I(11),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 1 },
});

// Class I oval (green) x 866..920 clipped by frame is fine in original; keep inside: x 862..916
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: I(862), y: I(108), w: I(54), h: I(24),
  fill: { color: GREEN_FILL }, line: { color: GREEN_LINE, width: 1 }, adjustValue: 0.5,
});
s.addText("Class I", {
  x: I(862), y: I(108), w: I(54), h: I(24),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: DARK, fontFace: FONT, margin: 0,
});
// Class II oval (plum)
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: I(862), y: I(140), w: I(54), h: I(24),
  fill: { color: PLUM_FILL }, line: { color: PLUM_LINE, width: 1 }, adjustValue: 0.5,
});
s.addText("Class II", {
  x: I(862), y: I(140), w: I(54), h: I(24),
  align: "center", valign: "middle",
  fontSize: 10, bold: true, color: DARK, fontFace: FONT, margin: 0,
});

// ---- bottom scatter plot ----
// red x-axis at y436 x60..895; lower red line y500 (plot box bottom); labels below axis y448..464
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(60), y: I(435), w: I(895 - 60), h: I(2.5),
  fill: { color: RED }, line: { color: RED, width: 0.5 },
});
s.addShape(pptx.shapes.RECTANGLE, {
  x: I(60), y: I(499), w: I(895 - 60), h: I(2),
  fill: { color: RED }, line: { color: RED, width: 0.5 },
});
function tick(xc, label, major) {
  s.addShape(pptx.shapes.RECTANGLE, {
    x: I(xc), y: I(436), w: I(1.5), h: major ? I(9) : I(5),
    fill: { color: DARK }, line: { color: DARK, width: 0.5 },
  });
  if (label) {
    s.addText(label, {
      x: I(xc - 16), y: I(449), w: I(32), h: I(14),
      align: "center", valign: "top",
      fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
    });
  }
}
const X0 = 95, X1 = 868;
for (let k = 0; k <= 20; k++) {
  const xc = X0 + (X1 - X0) * k / 20;
  tick(xc, k === 0 ? "0.0" : k === 10 ? "0.5" : k === 20 ? "1.0" : null, k % 10 === 0);
}
// dashed blue vertical threshold line at x~170 (threshold 0.1), y 230..435
(function () {
  const x = I(170);
  for (let y = 230; y < 435; y += 12) {
    s.addShape(pptx.shapes.RECTANGLE, {
      x: x, y: I(y), w: I(2), h: I(7),
      fill: { color: BLUE }, line: { color: BLUE, width: 0.25 },
    });
  }
})();
// rotated red "Predicted" label on the left of the plot
s.addText("Predicted", {
  x: I(78) - I(30), y: I(360) - I(8), w: I(60), h: I(16),
  align: "center", valign: "middle", rotate: -90,
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// airplane scatter: 11 samples in two rows above the axis; dots encode class, skulls on two right-side
const planes = [
  [170, 300, "FF0000", false], [265, 300, "0000FF", false], [360, 300, "FF0000", false],
  [470, 300, "0000FF", false], [580, 300, "FF0000", false], [820, 300, "0000FF", true],
  [220, 385, "0000FF", false], [315, 385, "FF0000", false], [440, 385, "0000FF", false],
  [570, 385, "FF0000", false], [830, 385, "000000", true],
];
planes.forEach(([cx, cy, dot, skull]) => drawPlane(s, I(cx), I(cy), I(40), dot, skull));

pptx.writeFile({
  fileName: "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/slide_021_recreated.pptx"
}).then(() => console.log("done"));
