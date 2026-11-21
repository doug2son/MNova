// XRSEO first-screen screenshots, laptop and phone size.
// Usage: node screenshots.js OUT_DIR URL [URL ...]
// Saves OUT_DIR/<slug>-desktop.jpg and OUT_DIR/<slug>-mobile.jpg for each URL.
const { chromium, devices } = require('playwright');
const fs = require('fs');
const path = require('path');

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36';

(async () => {
  const [out, ...urls] = process.argv.slice(2);
  if (!out || !urls.length) {
    console.error('Usage: node screenshots.js OUT_DIR URL [URL ...]');
    process.exit(1);
  }
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const desktop = await browser.newContext({ viewport: { width: 1366, height: 768 }, userAgent: UA });
  const mobile = await browser.newContext({ ...devices['iPhone 13'] });
  for (const url of urls) {
    const slug = (new URL(url).pathname.replace(/^\/|\/$/g, '').replace(/[^a-z0-9]+/gi, '-') || 'home').slice(0, 80);
    for (const [label, ctx] of [['desktop', desktop], ['mobile', mobile]]) {
      const page = await ctx.newPage();
      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
      } catch (e) { /* slow trackers: take what has loaded */ }
      await page.waitForTimeout(1500);
      const file = path.join(out, `${slug}-${label}.jpg`);
      await page.screenshot({ path: file, type: 'jpeg', quality: 70 });
      console.log(file);
      await page.close();
    }
  }
  await browser.close();
})();
