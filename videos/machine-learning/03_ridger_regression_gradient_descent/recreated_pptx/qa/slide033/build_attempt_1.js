// Build: slide 033 — "Non-Convex Function"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_033.jpg (960x540, 1px=1pt=1/72in)
// Spec: analysis/slide_033_final.json — verbatim_text, layout, visual_elements, recreation_brief
//
// MEASURED GEOMETRY (frame px from PIL measurement):
//   Canvas: white FFFFFF (house chrome draws panel, strokes, badge)
//   Panel: gray E9E9E7 rect x54..903 y45..540 (no top stroke)
//   Badge: numeral "33" at (876, 73) d~35, fill FDFD96, ring 6A5ACD 2pt, numeral 333333 bold Arial 18pt
//   Title: "Non-Convex Function" red #FF0000 ~28pt bold, cap-top row 75, left x~342
//   Subtitle: 2 lines blue #0000FF bold ~18pt:
//     L1: "May reach different minimum value based on:" at row 86
//     L2: "initial point and learning rate" at row 108, "initial point" red #FF0000, "learning rate" blue #0000FF
//   Parameter box: x 70-170, y 240-280, bordered
//     Rows: "step | 0.1", "initial x | -11", "delta x | 0.1"
//     Yellow #FFFF00 accent on row 2 (initial x) cols 103-160
//   Red block arrow: from box (x~180) down-right toward table
//   Formula & annotation: center x 350-650, y 165-290
//     Equation: f(x) = (x^2 cos(x) - x) / 10 as stacked fraction — eq_033_main.png (2.405x0.515in)
//     Annotation 1: "X is in between -9.7 and -9.6" with "-9.6" red bold at y~255
//     Annotation 2: "f(x) is in between -8.08 and -8.011" verbatim at y~278
//   Function plot: right, x 615-930, y 120-330
//     X-axis at row 172 (y=0), Y-axis at col 615 (x=-12)
//     Gridlines: horizontal at y=2,0,-2,-4,-6,-8 (rows 134,172,209,246,283,316)
//                vertical at x=-10,-8,-6,-4,-2 (cols ~685,740,775,810,885)
//     Green #00B050 curve: f(x) = (x^2 cos(x) - x)/10 over x∈[-12,-2]
//     Red #FF0000 dot at initial point (-11, 1.15) → frame (646, 220)
//     Orange #ED7D31 thick arrow following curve down to local minimum
//     Green #00B050 square at local minimum near (-9.6, -8.11) — drawn at computed pos
//     Purple #7030A0 rounded callout "Reach Local Minima" with pointer, at bottom of plot (rows 320-329)
//   Numeric table: bottom, x 20-940, y 330-520
//     8 row labels + 16 data columns. Row labels: x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x
//     Exact values from recreation_brief
//     Alternating row fills: #E2EFDA, #DDEBF7, #E4DFEC, #FCE4D6 over white #FFFFFF
//     Highlight columns x=-9.7 and x=-9.6 in yellow #FFFF00
//     Cells x=-9.6 and f(x)=-8.11 in red #FF0000 bold
//
// Laws: hex without '#'; fontFace explicit; margin 0; measured geometry; closed-loop check.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome, CHROME } = require("../../shared_patterns/house_chrome.js");
const fs = require("fs");

const ASSET_DIR = __dirname + "/assets";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_033_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches
const A = "Arial";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// ---- HOUSE CHROME ----
drawHouseChrome(pptx, slide, { numeral: "33" });

// ---- TITLE BLOCK (top-left) ----
slide.addText("Non-Convex Function", {
  x: px(342), y: px(69), w: px(500), h: px(40),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 28, bold: true, color: "FF0000",
});

slide.addText("May reach different minimum value based on:", {
  x: px(342), y: px(86), w: px(500), h: px(26),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 18, bold: true, color: "0000FF",
});

slide.addText([
  { text: "initial point", options: { fontFace: A, fontSize: 18, bold: true, color: "FF0000" } },
  { text: " and ", options: { fontFace: A, fontSize: 18, bold: true, color: "0000FF" } },
  { text: "learning rate", options: { fontFace: A, fontSize: 18, bold: true, color: "0000FF" } },
], {
  x: px(342), y: px(108), w: px(500), h: px(26),
  align: "left", valign: "top", margin: 0,
});

// ---- PARAMETER BOX (left-middle) ----
const pb_x = 70, pb_y = 240, pb_w = 100, pb_h = 45;

slide.addShape(pptx.ShapeType.rect, {
  x: px(pb_x), y: px(pb_y), w: px(pb_w), h: px(pb_h),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});

// Yellow accent on "initial x" row (row index 1)
slide.addShape(pptx.ShapeType.rect, {
  x: px(103), y: px(260), w: px(57), h: px(9),
  fill: { color: "FFFF00" }, line: { color: "FFFF00", width: 0 },
});

const param_rows = [
  { label: "step", value: "0.1" },
  { label: "initial x", value: "-11" },
  { label: "delta x", value: "0.1" },
];
for (let i = 0; i < param_rows.length; i++) {
  const ry = pb_y + 3 + i * 14;
  slide.addText(param_rows[i].label, {
    x: px(pb_x + 5), y: px(ry), w: px(55), h: px(14),
    align: "left", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: "000000",
  });
  slide.addText(param_rows[i].value, {
    x: px(pb_x + 60), y: px(ry), w: px(35), h: px(14),
    align: "right", valign: "middle", margin: 0,
    fontFace: A, fontSize: 11, color: "000000",
  });
}

// ---- RED BLOCK ARROW (from parameter box toward table) ----
slide.addShape(pptx.ShapeType.rightArrow, {
  x: px(180), y: px(275), w: px(60), h: px(12),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
});
slide.addShape(pptx.ShapeType.downArrow, {
  x: px(230), y: px(280), w: px(12), h: px(40),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
});

// ---- FORMULA & ANNOTATION (center) ----
const eq_w = 2.405, eq_h = 0.515;
const eq_cx = 499; // center of formula area
const eq_cy = 190;
slide.addImage({
  path: ASSET_DIR + "/eq_033_main.png",
  x: px(eq_cx) - eq_w/2, y: px(eq_cy),
  w: eq_w, h: eq_h,
});

slide.addText([
  { text: "X is in between -9.7 and ", options: { fontFace: A, fontSize: 14, color: "000000" } },
  { text: "-9.6", options: { fontFace: A, fontSize: 14, bold: true, color: "FF0000" } },
], {
  x: px(350), y: px(255), w: px(300), h: px(22),
  align: "left", valign: "top", margin: 0,
});

slide.addText("f(x) is in between -8.08 and -8.011", {
  x: px(350), y: px(278), w: px(300), h: px(22),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 14, color: "000000",
});

// ---- FUNCTION PLOT (right) ----
// Plot frame: x 615-930 (315px), y 120-330 (210px)
// x: -12 to -2 (10 units) => 31.5 px/unit
// y: 2 to -8 (10 units) => 18.3 px/unit, x-axis at row 172 (y=0)
const PLOT_X0 = 615, PLOT_Y0 = 120, PLOT_W = 315, PLOT_H = 210;
const X_AXIS_Y = 172; // row where y=0
const Y_AXIS_X = 615; // col where x=-12
const PX_PER_X_UNIT = 31.5;
const PX_PER_Y_UNIT = 18.3; // (317-134)/10 = 18.3

function f(x) { return (x*x * Math.cos(x) - x) / 10; }

// Gridlines (light gray #D9D9D9)
// Horizontal: y=2,0,-2,-4,-6,-8
const y_ticks = [2, 0, -2, -4, -6, -8];
for (let yt of y_ticks) {
  const gy = X_AXIS_Y - yt * PX_PER_Y_UNIT;
  slide.addShape(pptx.ShapeType.line, {
    x: px(PLOT_X0), y: px(gy), w: px(PLOT_W), h: 0,
    line: { color: "D9D9D9", width: 0.5 },
  });
}
// Vertical: x=-10,-8,-6,-4,-2
const x_ticks = [-10, -8, -6, -4, -2];
for (let xt of x_ticks) {
  const gx = Y_AXIS_X + (xt + 12) * PX_PER_X_UNIT;
  slide.addShape(pptx.ShapeType.line, {
    x: px(gx), y: px(PLOT_Y0), w: 0, h: px(PLOT_H),
    line: { color: "D9D9D9", width: 0.5 },
  });
}

// Axes (black #000000, 1pt)
slide.addShape(pptx.ShapeType.line, { // x-axis
  x: px(Y_AXIS_X), y: px(X_AXIS_Y), w: px(PLOT_W), h: 0,
  line: { color: "000000", width: 1 },
});
slide.addShape(pptx.ShapeType.line, { // y-axis
  x: px(Y_AXIS_X), y: px(PLOT_Y0), w: 0, h: px(PLOT_H),
  line: { color: "000000", width: 1 },
});

// Axis labels
slide.addText("x", { // x-axis label at right end
  x: px(Y_AXIS_X + PLOT_W - 20), y: px(X_AXIS_Y + 5), w: px(20), h: px(16),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 12, bold: true, color: "000000",
});
slide.addText("y", { // y-axis label at top
  x: px(Y_AXIS_X - 25), y: px(PLOT_Y0 - 5), w: px(25), h: px(16),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 12, bold: true, color: "000000",
});

// X tick labels and marks
for (let xt of [-12, -10, -8, -6, -4, -2]) {
  const tx = Y_AXIS_X + (xt + 12) * PX_PER_X_UNIT;
  slide.addText(String(xt), {
    x: px(tx - 15), y: px(X_AXIS_Y + 5), w: px(30), h: px(16),
    align: "center", valign: "top", margin: 0,
    fontFace: A, fontSize: 10, color: "000000",
  });
  // Tick mark
  slide.addShape(pptx.ShapeType.line, {
    x: px(tx), y: px(X_AXIS_Y - 2), w: 0, h: px(4),
    line: { color: "000000", width: 1 },
  });
}
// Y tick labels and marks
for (let yt of [2, 0, -2, -4, -6, -8]) {
  const ty = X_AXIS_Y - yt * PX_PER_Y_UNIT;
  slide.addText(String(yt), {
    x: px(Y_AXIS_X - 40), y: px(ty - 8), w: px(35), h: px(16),
    align: "right", valign: "middle", margin: 0,
    fontFace: A, fontSize: 10, color: "000000",
  });
  // Tick mark
  slide.addShape(pptx.ShapeType.line, {
    x: px(Y_AXIS_X - 2), y: px(ty), w: px(4), h: 0,
    line: { color: "000000", width: 1 },
  });
}

// Green curve as polyline (smooth: many short segments)
const curve_pts = [];
for (let x = -12; x <= -2; x += 0.02) {
  const y = f(x);
  const px_x = Y_AXIS_X + (x + 12) * PX_PER_X_UNIT;
  const px_y = X_AXIS_Y - y * PX_PER_Y_UNIT;
  if (px_y >= PLOT_Y0 && px_y <= PLOT_Y0 + PLOT_H) {
    curve_pts.push({ x: px_x, y: px_y });
  }
}
for (let i = 0; i < curve_pts.length - 1; i++) {
  const p1 = curve_pts[i], p2 = curve_pts[i + 1];
  slide.addShape(pptx.ShapeType.line, {
    x: px(p1.x), y: px(p1.y), w: px(p2.x - p1.x), h: px(p2.y - p1.y),
    line: { color: "00B050", width: 1.5 },
  });
}

// Red initial point at (-11, f(-11)=1.15)
const init_x = Y_AXIS_X + 1 * PX_PER_X_UNIT;      // -11 is 1 unit from -12
const init_y = X_AXIS_Y - 1.15 * PX_PER_Y_UNIT;   // 1.15 above x-axis
slide.addShape(pptx.ShapeType.ellipse, {
  x: px(init_x - 4), y: px(init_y - 4), w: px(8), h: px(8),
  fill: { color: "FF0000" }, line: { color: "FF0000", width: 0 },
});

// Local minimum at x≈-9.6 (from table/spec)
const min_x_val = -9.6;
const min_y_val = f(min_x_val); // ≈ -8.11
const min_x = Y_AXIS_X + (min_x_val + 12) * PX_PER_X_UNIT;
const min_y = X_AXIS_Y - min_y_val * PX_PER_Y_UNIT;

// Green square marker at local minimum (if in plot bounds)
if (min_y >= PLOT_Y0 && min_y <= PLOT_Y0 + PLOT_H) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(min_x - 5), y: px(min_y - 5), w: px(10), h: px(10),
    fill: { color: "00B050" }, line: { color: "00B050", width: 0 },
  });
}

// Orange arrow from initial point following curve to local minimum
// Draw as a curved polyline along the function between x=-11 and x=-9.6
const arrow_pts = [];
for (let x = -11; x >= -9.6; x -= 0.05) {
  const y = f(x);
  const px_x = Y_AXIS_X + (x + 12) * PX_PER_X_UNIT;
  const px_y = X_AXIS_Y - y * PX_PER_Y_UNIT;
  if (px_y >= PLOT_Y0 && px_y <= PLOT_Y0 + PLOT_H) {
    arrow_pts.push({ x: px_x, y: px_y });
  }
}
for (let i = 0; i < arrow_pts.length - 1; i++) {
  const p1 = arrow_pts[i], p2 = arrow_pts[i + 1];
  slide.addShape(pptx.ShapeType.line, {
    x: px(p1.x), y: px(p1.y), w: px(p2.x - p1.x), h: px(p2.y - p1.y),
    line: { color: "ED7D31", width: 2.5 },
  });
}
// Arrowhead at end (triangle at min_x, min_y)
if (arrow_pts.length > 0) {
  const end = arrow_pts[arrow_pts.length - 1];
  const prev = arrow_pts[Math.max(0, arrow_pts.length - 2)];
  const dx = end.x - prev.x, dy = end.y - prev.y;
  const len = Math.sqrt(dx*dx + dy*dy);
  if (len > 0) {
    const ux = dx/len, uy = dy/len;
    const head = 8; // px
    const hx = end.x, hy = end.y;
    const b1x = hx - ux*head - uy*head*0.5;
    const b1y = hy - uy*head + ux*head*0.5;
    const b2x = hx - ux*head + uy*head*0.5;
    const b2y = hy - uy*head - ux*head*0.5;
    slide.addShape(pptx.ShapeType.freeform, {
      fill: { color: "ED7D31" }, line: { color: "ED7D31", width: 0 },
      points: [
        { x: px(hx), y: px(hy) },
        { x: px(b1x), y: px(b1y) },
        { x: px(b2x), y: px(b2y) },
      ],
    });
  }
}

// Purple callout "Reach Local Minima" at bottom of plot (measured rows 320-329)
// Callout box: rounded rect at ~x 615-880, y 315-329
const callout_x = 620, callout_y = 315, callout_w = 260, callout_h = 22;
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(callout_x), y: px(callout_y), w: px(callout_w), h: px(callout_h),
  fill: { color: "7030A0" }, line: { color: "7030A0", width: 0 },
});
slide.addText("Reach Local Minima", {
  x: px(callout_x), y: px(callout_y), w: px(callout_w), h: px(callout_h),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 11, bold: true, color: "FFFFFF",
});
// Pointer from callout to green square (downward triangle)
if (min_y <= callout_y) {
  const px_x = min_x;
  const py_y = callout_y;
  slide.addShape(pptx.ShapeType.freeform, {
    fill: { color: "7030A0" }, line: { color: "7030A0", width: 0 },
    points: [
      { x: px(px_x), y: px(py_y) },
      { x: px(px_x - 6), y: px(py_y + 10) },
      { x: px(px_x + 6), y: px(py_y + 10) },
    ],
  });
}

// ---- NUMERIC TABLE (bottom) ----
// Table frame: x 20-940 (920px = 12.78in), y 330-520 (190px = 2.64in)
// 8 rows + header, 1 label col + 16 data cols = 9x17 grid
// Row labels: x, f(x), x-delta, f(x-delta), x+delta, f(x+delta), slope, next x
// Column data: 16 values each (from recreation_brief)

const tbl_x0 = 20, tbl_y0 = 330, tbl_w = 920, tbl_h = 190;
const n_rows = 9; // 1 header + 8 data
const n_cols = 17; // 1 label + 16 data
const row_h = tbl_h / n_rows; // ~21.1 px
const label_col_w = 80; // px for label column
const data_col_w = (tbl_w - label_col_w) / 16; // ~52.5 px

// Row data from recreation_brief
const row_labels = ["x", "f(x)", "x-delta", "f(x-delta)", "x+delta", "f(x+delta)", "slope", "next x"];
const row_data = {
  "x":           [-11, -10.9, -10.8, -10.7, -10.6, -10.5, -10.4, -10.3, -10.2, -10.1, -10, -9.9, -9.8, -9.7, -9.6, -9.5],
  "f(x)":        [1.15, -0.04, -1.19, -2.26, -3.27, -4.19, -5.03, -5.77, -6.41, -6.95, -7.39, -7.72, -7.96, -8.08, -8.11, -8.05],
  "x-delta":     [-11.1, -11, -10.9, -10.8, -10.7, -10.6, -10.5, -10.4, -10.3, -10.2, -10.1, -10, -9.9, -9.8, -9.7, -9.6],
  "f(x-delta)":  [2.39, 1.15, -0.04, -1.19, -2.26, -3.27, -4.19, -5.03, -5.77, -6.41, -6.95, -7.39, -7.72, -7.96, -8.08, -8.11],
  "x+delta":     [-10.9, -10.8, -10.7, -10.6, -10.5, -10.4, -10.3, -10.2, -10.1, -10, -9.9, -9.8, -9.7, -9.6, -9.5, -9.4],
  "f(x+delta)":  [-0.04, -1.19, -2.26, -3.27, -4.19, -5.03, -5.77, -6.41, -6.95, -7.39, -7.72, -7.96, -8.08, -8.11, -8.05, -7.89],
  "slope":       [-24.3, -23.4, -22.2, -20.8, -19.3, -17.6, -15.8, -13.8, -11.8, -9.8, -7.7, -5.7, -3.6, -1.5, 0.3, 2.2],
  "next x":      [-10.9, -10.8, -10.7, -10.6, -10.5, -10.4, -10.3, -10.2, -10.1, -10, -9.9, -9.8, -9.7, -9.6, -9.7, -9.6],
};

// Row fill colors (alternating bands)
const row_fills = ["E2EFDA", "DDEBF7", "E4DFEC", "FCE4D6", "FFFFFF", "E2EFDA", "DDEBF7", "E4DFEC"]; // 8 data rows

// Highlight columns: x=-9.7 (index 13) and x=-9.6 (index 14) in yellow #FFFF00
const highlight_cols = [13, 14]; // 0-indexed data columns
// Red bold cells: x=-9.6 (row 0, col 14) and f(x)=-8.11 (row 1, col 14)
const red_bold = { "x": 14, "f(x)": 14 }; // row_label -> col_index

// Draw table background
slide.addShape(pptx.ShapeType.rect, {
  x: px(tbl_x0), y: px(tbl_y0), w: px(tbl_w), h: px(tbl_h),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 0.5 },
});

// Draw row bands and cells
for (let ri = 0; ri < n_rows; ri++) {
  const ry = tbl_y0 + ri * row_h;
  const is_header = (ri === 0);
  const data_ri = ri - 1; // 0-7 for data rows

  // Row fill
  let fill_color = "FFFFFF";
  if (!is_header) {
    fill_color = row_fills[data_ri % row_fills.length];
  }
  slide.addShape(pptx.ShapeType.rect, {
    x: px(tbl_x0), y: px(ry), w: px(tbl_w), h: px(row_h),
    fill: { color: fill_color }, line: { color: "000000", width: 0.25 },
  });

  // Label column
  if (is_header) {
    slide.addText("", { // empty header corner
      x: px(tbl_x0), y: px(ry), w: px(label_col_w), h: px(row_h),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 8, bold: true, color: "000000",
    });
  } else {
    slide.addText(row_labels[data_ri], {
      x: px(tbl_x0), y: px(ry), w: px(label_col_w), h: px(row_h),
      align: "center", valign: "middle", margin: 0,
      fontFace: A, fontSize: 8, bold: true, color: "000000",
    });
  }

  // Data columns
  if (is_header) {
    // Header: column indices 1-16
    for (let ci = 0; ci < 16; ci++) {
      const cx = tbl_x0 + label_col_w + ci * data_col_w;
      slide.addText(String(ci + 1), { // or just numbers
        x: px(cx), y: px(ry), w: px(data_col_w), h: px(row_h),
        align: "center", valign: "middle", margin: 0,
        fontFace: A, fontSize: 7, bold: true, color: "000000",
      });
    }
  } else {
    const label = row_labels[data_ri];
    const vals = row_data[label];
    for (let ci = 0; ci < 16; ci++) {
      const cx = tbl_x0 + label_col_w + ci * data_col_w;
      const val = vals[ci];
      const is_highlight = highlight_cols.includes(ci);
      const is_red_bold = (red_bold[label] === ci);
      const cell_fill = is_highlight ? "FFFF00" : fill_color;
      const font_color = is_red_bold ? "FF0000" : "000000";
      const font_bold = is_red_bold;

      // Cell background (for highlight)
      if (is_highlight) {
        slide.addShape(pptx.ShapeType.rect, {
          x: px(cx), y: px(ry), w: px(data_col_w), h: px(row_h),
          fill: { color: "FFFF00" }, line: { color: "000000", width: 0.25 },
        });
      }

      // Format value
      let txt = String(val);
      if (val % 1 === 0) txt = String(val); // integer
      else txt = val.toFixed(2).replace(/\.00$/, "");

      slide.addText(txt, {
        x: px(cx), y: px(ry), w: px(data_col_w), h: px(row_h),
        align: "center", valign: "middle", margin: 0,
        fontFace: A, fontSize: 7, bold: font_bold, color: font_color,
      });
    }
  }
}

// Vertical grid lines
for (let ci = 1; ci < n_cols; ci++) {
  const cx = tbl_x0 + label_col_w + (ci - 1) * data_col_w;
  slide.addShape(pptx.ShapeType.line, {
    x: px(cx), y: px(tbl_y0), w: 0, h: px(tbl_h),
    line: { color: "000000", width: 0.25 },
  });
}
// Horizontal grid lines (row separators)
for (let ri = 1; ri < n_rows; ri++) {
  const ry = tbl_y0 + ri * row_h;
  slide.addShape(pptx.ShapeType.line, {
    x: px(tbl_x0), y: px(ry), w: px(tbl_w), h: 0,
    line: { color: "000000", width: 0.25 },
  });
}

// Label column separator
slide.addShape(pptx.ShapeType.line, {
  x: px(tbl_x0 + label_col_w), y: px(tbl_y0), w: 0, h: px(tbl_h),
  line: { color: "000000", width: 0.5 },
});

// Write output
pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});