const pptxgen = require("pptxgenjs");
const PptxGenJS = require("pptxgenjs");
const JSZip = require("jszip");
const fs = require("fs");
const path = require("path");

// Helper to copy a slide from one PPTX to another at OPC package level
async function replaceSlideInDeck(finalDeckPath, slideNum, sourcePptxPath) {
  const finalZip = await JSZip.loadAsync(fs.readFileSync(finalDeckPath));
  const sourceZip = await JSZip.loadAsync(fs.readFileSync(sourcePptxPath));

  // Find slide XML in source
  const sourceSlidePath = `ppt/slides/slide1.xml`;
  const sourceSlideXml = await sourceZip.file(sourceSlidePath).async("string");

  // Find slide XML in final deck
  const finalSlidePath = `ppt/slides/slide${slideNum}.xml`;
  
  // Get the rels for the source slide
  const sourceRelsPath = `ppt/slides/_rels/slide1.xml.rels`;
  const sourceRels = await sourceZip.file(sourceRelsPath).async("string");

  // Get the rels for the target slide
  const finalRelsPath = `ppt/slides/_rels/slide${slideNum}.xml.rels`;
  
  // Replace slide XML
  finalZip.file(finalSlidePath, sourceSlideXml);

  // Replace rels
  finalZip.file(finalRelsPath, sourceRels);

  // Copy media files from source to final
  for (const [fileName, file] of Object.entries(sourceZip.files)) {
    if (fileName.startsWith("ppt/media/") && !file.dir) {
      const content = await file.async("nodebuffer");
      finalZip.file(fileName, content);
    }
  }

  // Copy any embedded fonts if present
  for (const [fileName, file] of Object.entries(sourceZip.files)) {
    if (fileName.startsWith("ppt/fonts/") && !file.dir) {
      const content = await file.async("nodebuffer");
      finalZip.file(fileName, content);
    }
  }

  // Copy theme if different
  const sourceThemePath = `ppt/theme/theme1.xml`;
  if (sourceZip.file(sourceThemePath)) {
    const sourceTheme = await sourceZip.file(sourceThemePath).async("string");
    finalZip.file(sourceThemePath, sourceTheme);
  }

  // Write updated final deck
  const updatedContent = await finalZip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" });
  fs.writeFileSync(finalDeckPath, updatedContent);
  console.log(`Replaced slide ${slideNum} in final deck`);
}

async function main() {
  const finalDeck = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/06_svm_with_kernels_quadratic_programming_libraries_final.pptx";
  
  // Replace slides 40-44
  for (let i = 40; i <= 44; i++) {
    const sourcePptx = `/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/slide_${i.toString().padStart(3, '0')}_recreated.pptx`;
    await replaceSlideInDeck(finalDeck, i, sourcePptx);
  }
  console.log("All slides replaced");
}

main().catch(e => console.error(e));