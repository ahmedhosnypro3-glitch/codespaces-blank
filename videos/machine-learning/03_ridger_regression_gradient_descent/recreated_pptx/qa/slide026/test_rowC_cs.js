// rowC red-tail charSpacing calibration: which value lands the red tail at x520..682?
const pptxgenpkg = require("pptxgenjs");
const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
const PX = 1/72, RED = "C00000", BLUE = "0000FF", FONT = "Arial", BODY = 17.5;
const r = (t, o) => ({ text: t, options: o });
const SPACINGS = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50];
SPACINGS.forEach((s, i) => {
  const y = 80 + i * 60;
  slide.addText([
    r("(w.r.t. W) (", { color: BLUE, fontSize: BODY, charSpacing: 0.11 }),
    r("moving step is a hyper parameter,", { color: BLUE, fontSize: BODY, bold: true, charSpacing: 0.11 }),
    r(" ", { color: BLUE, fontSize: BODY, charSpacing: 0.11 }),
    r("AKA Learning Rate", { color: RED, fontSize: BODY, bold: true, charSpacing: s }),
    r(")", { color: RED, fontSize: BODY, charSpacing: s }),
  ], { x: 146 * PX, y: y * PX, w: 560 * PX, h: 30 * PX, valign: "top", align: "left",
       margin: 0, fontFace: FONT, fontSize: BODY });
});
pptx.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/scratch/tmp/lo_boldtest/rowc_cs.pptx" })
  .then(() => console.log("wrote rowc_cs.pptx"));
