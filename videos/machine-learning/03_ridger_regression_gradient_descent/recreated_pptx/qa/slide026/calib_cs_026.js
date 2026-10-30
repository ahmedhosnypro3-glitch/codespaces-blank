// Calibration test: how many frame-px of ink extension does charSpacing add per
// character in LO's render? NOT a deliverable — scratch calibration only.
const pptxgenpkg = require("pptxgenjs");
const PX = 1 / 72;
const BLUE = "0000FF";
const FONT = "Arial";
const BODY = 17.5;

const TXT = [
  { text: "[3] Stop when the ", options: { color: BLUE, fontSize: BODY } },
  { text: "gradient is ", options: { color: BLUE, fontSize: BODY, underline: true } },
  { text: "almost zero", options: { color: BLUE, fontSize: BODY, bold: true, underline: true } },
  { text: " (this is at the minimum value of the function)", options: { color: BLUE, fontSize: BODY } },
];

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// white bg so ink masks work
slide.background = { color: "FFFFFF" };

const SPCS = [0, 0.08, 0.16, 0.24];
SPCS.forEach((spc, i) => {
  const y = 60 + i * 100;
  slide.addText(
    TXT.map(r => ({ text: r.text, options: Object.assign({}, r.options, { charSpacing: spc }) })),
    { x: 100 * PX, y: y * PX, w: 800 * PX, h: 30 * PX, valign: "top", align: "left", margin: 0, fontFace: FONT }
  );
});
pptx.writeFile({ fileName: "calib_cs_026.pptx" }).then(() => console.log("wrote calib_cs_026.pptx"));
