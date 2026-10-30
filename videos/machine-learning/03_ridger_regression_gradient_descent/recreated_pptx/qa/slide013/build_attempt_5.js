// Build slide 013 — "Effect of Overfitting on model parameter "W""
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
//
// CHILD of slide 012 (dependency edge 13 > 12). The composition lives in the
// shared component components/slide_013.js, which imports the certified parent
// component (table PATTERN) and redraws it at 013's own measured geometry.
// This script is only the writer.
//
// Run: cd <project root> && NODE_PATH=$(npm root -g) node <this file>
const path = require("path");
const pptxgen = require("pptxgenjs");
const C = require(path.resolve(__dirname, "./components/slide_013.js"));

const OUT = path.resolve(__dirname, "../slide_013_recreated.pptx");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

C.renderBase(pres, slide, { numeral: 13 });

pres.writeFile({ fileName: OUT })
  .then((f) => console.log("wrote " + f))
  .catch((e) => { console.error(e); process.exit(1); });
