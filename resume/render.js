// node resume/render.js  -> renders every *.html here to an A4 PDF
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const f of fs.readdirSync(__dirname).filter(f => f.endsWith('.html'))) {
    await p.goto('file://' + path.join(__dirname, f));
    await p.pdf({ path: path.join(__dirname, f.replace('.html', '.pdf')), format: 'A4', preferCSSPageSize: true });
    console.log('wrote', f.replace('.html', '.pdf'));
  }
  await b.close();
})();
