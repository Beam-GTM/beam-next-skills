const fs = require('fs');
const path = require('path');
const { Remarkable } = require('remarkable');
const puppeteer = require('puppeteer');

const PRESETS = {
  legal: {
    font: '"Times New Roman", Times, Georgia, serif',
    fontSize: '11pt',
    lineHeight: '1.65',
    textAlign: 'justify',
    h2Align: 'center',
    h2Size: '14pt',
    h3Size: '11pt',
    margin: { top: '30mm', bottom: '25mm', left: '30mm', right: '30mm' },
  },
  business: {
    font: 'Helvetica, Arial, "Helvetica Neue", sans-serif',
    fontSize: '11pt',
    lineHeight: '1.55',
    textAlign: 'left',
    h2Align: 'left',
    h2Size: '16pt',
    h3Size: '12pt',
    margin: { top: '25mm', bottom: '20mm', left: '25mm', right: '25mm' },
  },
  minimal: {
    font: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontSize: '10.5pt',
    lineHeight: '1.5',
    textAlign: 'left',
    h2Align: 'left',
    h2Size: '15pt',
    h3Size: '11.5pt',
    margin: { top: '20mm', bottom: '18mm', left: '20mm', right: '20mm' },
  },
};

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { preset: 'legal' };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input' && args[i + 1]) opts.input = args[++i];
    else if (args[i] === '--output' && args[i + 1]) opts.output = args[++i];
    else if (args[i] === '--preset' && args[i + 1]) opts.preset = args[++i];
    else if (args[i] === '--header' && args[i + 1]) opts.header = args[++i];
    else if (args[i] === '--no-page-numbers') opts.noPageNumbers = true;
    else if (args[i] === '--html') opts.htmlOnly = true;
  }
  if (!opts.input) {
    console.error('Usage: node render.js --input <file.md> --output <file.pdf> [--preset legal|business|minimal] [--header "text"] [--no-page-numbers] [--html]');
    process.exit(1);
  }
  if (!opts.output) {
    opts.output = opts.input.replace(/\.md$/, opts.htmlOnly ? '.html' : '.pdf');
  }
  return opts;
}

function buildHtml(markdownContent, preset, opts = {}) {
  const md = new Remarkable({ html: true, breaks: true });
  const body = md.render(markdownContent);
  const s = PRESETS[preset] || PRESETS.legal;

  const headerHtml = opts.header
    ? `<div style="font-size:8.5pt;color:#666;text-align:right;width:100%;padding:0 10mm;">${opts.header}</div>`
    : '<span></span>';

  const footerHtml = '<div style="font-size:8pt;color:#888;text-align:center;width:100%;padding:0 10mm;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>';

  return {
    html: `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: ${s.font};
    font-size: ${s.fontSize};
    line-height: ${s.lineHeight};
    color: #1a1a1a;
  }

  h2 {
    font-size: ${s.h2Size};
    text-align: ${s.h2Align};
    margin-bottom: 1em;
    font-weight: bold;
    letter-spacing: 0.03em;
  }

  h3 {
    font-size: ${s.h3Size};
    margin-top: 1.2em;
    margin-bottom: 0.3em;
    font-weight: bold;
    page-break-after: avoid;
  }

  p {
    text-align: ${s.textAlign};
    margin-bottom: 0.5em;
    orphans: 3;
    widows: 3;
  }

  /* Keep heading + first paragraph/list together */
  h3 + p, h3 + ul {
    page-break-before: avoid;
  }

  ul {
    margin-top: 0.2em;
    margin-bottom: 0.5em;
    padding-left: 1.8em;
  }
  li { margin-bottom: 0.1em; }

  hr {
    border: none;
    border-top: 1px solid #444;
    margin: 1.5em 0;
  }

  strong { font-weight: bold; }
  em { font-style: italic; }

  table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.8em 0;
    font-size: inherit;
    page-break-inside: avoid;
  }
  th, td {
    border: 1px solid #999;
    padding: 0.4em 0.6em;
    text-align: left;
  }
  th { background: #f5f5f5; font-weight: bold; }

  blockquote {
    border-left: 3px solid #999;
    margin: 0.8em 0;
    padding: 0.3em 1em;
    color: #444;
  }

  code {
    font-family: "SF Mono", Menlo, Consolas, monospace;
    font-size: 0.9em;
    background: #f4f4f4;
    padding: 0.15em 0.3em;
    border-radius: 3px;
  }
  pre code { display: block; padding: 0.8em; overflow-x: auto; }
</style>
</head>
<body>${body}</body>
</html>`,
    headerHtml,
    footerHtml,
    margin: s.margin,
  };
}

(async () => {
  const opts = parseArgs();
  const markdownContent = fs.readFileSync(path.resolve(opts.input), 'utf8');
  const { html, headerHtml, footerHtml, margin } = buildHtml(markdownContent, opts.preset, {
    header: opts.header,
  });

  const outputPath = path.resolve(opts.output);

  if (opts.htmlOnly) {
    fs.writeFileSync(outputPath, html, 'utf8');
    const sizeKB = Math.round(fs.statSync(outputPath).size / 1024);
    console.log(`HTML generated: ${outputPath} (${sizeKB} KB)`);
    return;
  }

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle0' });

  const pdfOpts = {
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin,
  };

  if (!opts.noPageNumbers) {
    pdfOpts.displayHeaderFooter = true;
    pdfOpts.headerTemplate = headerHtml;
    pdfOpts.footerTemplate = footerHtml;
  }

  await page.pdf(pdfOpts);
  await browser.close();

  const stats = fs.statSync(outputPath);
  const sizeKB = Math.round(stats.size / 1024);
  console.log(`PDF generated: ${outputPath} (${sizeKB} KB)`);
})();
