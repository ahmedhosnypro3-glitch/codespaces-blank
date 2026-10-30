// Controlled regular-vs-bold render of the disputed words, same pipeline as slide_026.js.
const pptxgenpkg = require("pptxgenjs");
const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
const PX = 1/72, FONT = "Arial", BLUE = "0000FF", BODY = 17.5;
const WORDS = ["moving", "gradient", "negative gradient", "almost zero", "minimum", "Loss function"];
// two rows per word: regular on the left, bold on the right, at identical baselines
let y = 60;
for (const w of WORDS) {
  slide.addText([{ text: w, options: { fontFace: FONT, fontSize: BODY, color: BLUE } }],
    { x: 100*PX, y: y*PX, w: 700*PX, h: 30*PX, valign: "top", align: "left", margin: 0, fontSize: BODY });
  slide.addText([{ text: w, options: { fontFace: FONT, fontSize: BODY, color: BLUE, bold: true } }],
    { x: 500*PX, y: y*PX, w: 700*PX, h: 30*PX, valign: "top", align: "left", margin: 0, fontSize: BODY });
  y += 46;
}
pptx.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/scratch/tmp/lo_boldtest/boldtest.pptx" })
  .then(() => console.log("wrote boldtest.pptx"));
