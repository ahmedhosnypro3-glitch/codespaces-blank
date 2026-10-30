const pptxgen = require("pptxgenjs");

// Slide 022: Derivatives of some Activation Functions
// Equations embedded as 600dpi mathtext PNGs (Professional Format 2D) per MISSION_PROTOCOL.
const NUM = 22;
const TITLE = "Derivatives of some Activation Functions";
const FONT = "Arial";
const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const EQ_DIR = BUILD + "/equations_slide022";

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "0000CC";
const GREEN = "008000";
const BORDER_RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const LIGHT_YELLOW = "FFFFE0";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: BORDER_RED, width: 1.5 },
});

// 2. Slide-number badge - HOUSE CHROME LAW
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "4B0082", fontFace: FONT, margin: 0,
});

// 3. Title - HOUSE CHROME LAW
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 4. Content container: white rectangle with blue border
const container_x = 0.6;
const container_y = 1.15;
const container_w = 12.13;
const container_h = 5.8;
s.addShape(pres.shapes.RECTANGLE, {
  x: container_x, y: container_y, w: container_w, h: container_h,
  fill: { color: WHITE }, line: { color: BLUE, width: 2 },
});

// 5. Four rows - each has left box, center "Derivative" + arrow, right box
const row_h = container_h / 4;
const left_box_w = container_w * 0.38;
const center_w = container_w * 0.18;
const right_box_w = container_w * 0.38;
const gap = (container_w - left_box_w - center_w - right_box_w) / 2;

const left_x = container_x + gap;
const center_x = left_x + left_box_w + gap;
const right_x = center_x + center_w + gap;

const left_border = RED;
const right_border = BLUE;
const box_fill = LIGHT_YELLOW;
const box_border_width = 1.5;

const text_font_size = 14;
const label_font_size = 16;

function addEquationBox(slide, x, y, w, h, borderColor, imagePath, imageW, imageH, label) {
  // Rounded rectangle
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: x, y: y, w: w, h: h,
    fill: { color: box_fill }, line: { color: borderColor, width: box_border_width },
  });
  // Equation image centered in box
  const ix = x + (w - imageW) / 2;
  const iy = y + (h - imageH) / 2;
  slide.addImage({
    path: imagePath,
    x: ix, y: iy, w: imageW, h: imageH,
  });
}

// Row 1: ReLU
let y = container_y + 0.15;
const box_h = row_h - 0.3;

addEquationBox(s, left_x, y, left_box_w, box_h, left_border, EQ_DIR + "/eq_relu_f.png", 3.16167, 0.17833, "ReLU f(x)");
s.addText([
  { text: "Derivative", options: { color: RED, bold: true, fontSize: label_font_size, fontFace: FONT } },
  { text: "\n\u21d2", options: { color: RED, bold: true, fontSize: label_font_size, fontFace: FONT } },
], {
  x: center_x, y: y, w: center_w, h: box_h,
  align: "center", valign: "middle", margin: 0,
});
addEquationBox(s, right_x, y, right_box_w, box_h, right_border, EQ_DIR + "/eq_relu_df.png", 2.595, 0.18667, "ReLU f'(x)");

// Row 2: Parametric ReLU
y += row_h;
addEquationBox(s, left_x, y, left_box_w, box_h, left_border, EQ_DIR + "/eq_prelu_f.png", 4.39833, 0.17833, "PReLU f(x)");
s.addText([
  { text: "Derivative", options: { color: RED, bold: true, fontSize: label_font_size, fontFace: FONT } },
  { text: "\n\u21d2", options: { color: RED, bold: true, fontSize: label_font_size, fontFace: FONT } },
], {
  x: center_x, y: y, w: center_w, h: box_h,
  align: "center", valign: "middle", margin: 0,
});
addEquationBox(s, right_x, y, right_box_w, box_h, right_border, EQ_DIR + "/eq_prelu_df.png", 2.6, 0.18667, "PReLU f'(x)");

// Row 3: Exponential LU (ELU)
y += row_h;
addEquationBox(s, left_x, y, left_box_w, box_h, left_border, EQ_DIR + "/eq_elu_f.png", 4.61833, 0.19333, "ELU f(x)");
s.addText([
  { text: "Derivative", options: { color: RED, bold: true, fontSize: label_font_size, fontFace: FONT } },
  { text: "\n\u21d2", options: { color: RED, bold: true, fontSize: label_font_size, fontFace: FONT } },
], {
  x: center_x, y: y, w: center_w, h: box_h,
  align: "center", valign: "middle", margin: 0,
});
addEquationBox(s, right_x, y, right_box_w, box_h, right_border, EQ_DIR + "/eq_elu_df.png", 3.09167, 0.18667, "ELU f'(x)");

// Row 4: SoftPlus
y += row_h;
addEquationBox(s, left_x, y, left_box_w, box_h, left_border, EQ_DIR + "/eq_softplus_f.png", 2.34833, 0.19333, "SoftPlus f(x)");
s.addText([
  { text: "Derivative", options: { color: RED, bold: true, fontSize: label_font_size, fontFace: FONT } },
  { text: "\n\u21d2", options: { color: RED, bold: true, fontSize: label_font_size, fontFace: FONT } },
], {
  x: center_x, y: y, w: center_w, h: box_h,
  align: "center", valign: "middle", margin: 0,
});
addEquationBox(s, right_x, y, right_box_w, box_h, right_border, EQ_DIR + "/eq_softplus_df.png", 0.44, 0.23667, "SoftPlus f'(x)");

// 6. Bottom black footer bar
s.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: H - 0.35, w: W, h: 0.35,
  fill: { color: BLACK }, line: { color: "none" },
});

pres.writeFile({ 
  fileName: BUILD + "/slide_022_recreated.pptx" 
}).then(() => console.log("wrote slide_022_recreated.pptx"));