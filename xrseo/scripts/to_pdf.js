// Turn an XRSEO report (HTML) into a PDF.
// Usage: node to_pdf.js report.html report.pdf
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [src, out] = process.argv.slice(2);
  if (!src || !out) {
    console.error('Usage: node to_pdf.js report.html report.pdf');
    process.exit(1);
  }
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({
    path: out, format: 'Letter', printBackground: true,
    margin: { top: '0.5in', bottom: '0.6in', left: '0.5in', right: '0.5in' },
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#888;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  });
  await browser.close();
  console.log(out);
})();
