// Scripted capture of the Formwork Builder (blank route) through the local reverse proxy.
// Output: cap/frames/*.png with cap/steps.json = [{name, frames:[{file,t}]}] (t = seconds within the step).
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
const OUT = process.env.CAP_OUT || 'cap'; fs.rmSync(OUT, { recursive: true, force: true }); fs.mkdirSync(OUT + '/frames', { recursive: true });
const browser = await puppeteer.launch({ executablePath: process.env.HYPERFRAMES_BROWSER_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', headless: true,
  args: ['--no-sandbox','--no-proxy-server','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--disable-dev-shm-usage','--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: 540, height: 960, deviceScaleFactor: 2 });
await page.goto(process.env.CAP_URL || 'http://127.0.0.1:8787/apps/formwork', { waitUntil: 'networkidle2', timeout: 90000 });
await page.addStyleTag({ content: `*{transition:none!important;animation:none!important;scroll-behavior:auto!important} ::-webkit-scrollbar{display:none}` });
await new Promise(r => setTimeout(r, 3000));
// pin the 3D preview to the top of the viewport
await page.evaluate(() => { const c = document.querySelector('canvas'); let el = c; for (let i = 0; i < 6 && el && el.parentElement; i++) { el = el.parentElement; const h = el.getBoundingClientRect().height; if (h > 300 && h < 480) break; }
  el.style.position = 'sticky'; el.style.top = '0px'; el.style.zIndex = '50'; el.style.background = '#fff'; el.style.boxShadow = '0 8px 24px -12px rgba(20,20,18,.25)'; });
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const cdp = await page.createCDPSession();
let cur = null; const steps = []; let n = 0;
cdp.on('Page.screencastFrame', async ({ data, metadata, sessionId }) => {
  if (cur) { const f = `f${String(n++).padStart(5, '0')}.png`; fs.writeFileSync(`${OUT}/frames/${f}`, Buffer.from(data, 'base64')); cur.frames.push({ file: f, t: +(metadata.timestamp - cur.t0).toFixed(3) }); }
  await cdp.send('Page.screencastFrameAck', { sessionId }).catch(() => {});
});
await cdp.send('Page.startScreencast', { format: 'png', maxWidth: 1080, maxHeight: 1920, everyNthFrame: 1 });
const step = async (name, fn, settle = 900) => {
  cur = { name, t0: Date.now() / 1000, frames: [] }; const t0 = Date.now();
  await fn(); await sleep(settle);
  const f = `f${String(n++).padStart(5, '0')}.png`; await page.screenshot({ path: `${OUT}/frames/${f}` });
  cur.frames.push({ file: f, t: +((Date.now() - t0) / 1000).toFixed(3), final: true });
  steps.push(cur); console.log(`${name}: ${cur.frames.length} frames over ${cur.frames.at(-1).t}s`); cur = null;
};
const btn = (txt, exact = true) => page.evaluate((txt, exact) => { const b = [...document.querySelectorAll('button')].find(b => exact ? b.textContent.trim().replace(/^✓\s*/, '') === txt : b.textContent.trim().includes(txt)); if (!b) return false; b.scrollIntoView({ block: 'center', behavior: 'instant' }); b.click(); return b.textContent.trim().slice(0, 30); }, txt, exact);
const isOn = (txt) => page.evaluate((txt) => { const b = [...document.querySelectorAll('button')].find(b => b.textContent.trim().replace(/^✓\s*/, '').startsWith(txt)); return !!b && b.textContent.trim().startsWith('✓'); }, txt);
const typeIn = async (id, value, delay = 130) => {
  await page.evaluate((id) => { const el = document.getElementById(id); el.scrollIntoView({ block: 'center', behavior: 'instant' }); el.focus(); }, id);
  await sleep(250);
  const s = String(value);
  for (let i = 1; i <= s.length; i++) {
    await page.evaluate((id, v) => { const el = document.getElementById(id); const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set; set.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); }, id, s.slice(0, i));
    await sleep(delay);
  }
  await page.evaluate((id) => document.getElementById(id).blur(), id);
};
const scrollToText = async (txt) => page.evaluate((txt) => { const el = document.evaluate(`//*[normalize-space(text())='${txt}']`, document, null, 9, null).singleNodeValue; if (el) el.scrollIntoView({ block: 'start', behavior: 'instant' }); window.scrollBy(0, -380); return !!el; }, txt);

const checkRow = async (label) => page.evaluate((label) => {
  const el = document.evaluate(`//p[normalize-space(text())='${label}']`, document, null, 9, null).singleNodeValue; if (!el) return 'no-label';
  el.scrollIntoView({ block: 'center', behavior: 'instant' }); el.click(); return 'clicked'; }, label);
const clickBothNear = async (label) => page.evaluate((label) => {
  const el = document.evaluate(`//*[normalize-space(text())='${label}']`, document, null, 9, null).singleNodeValue; if (!el) return 'no-label';
  let row = el; for (let i = 0; i < 6 && row; i++) { const b = [...row.querySelectorAll('button')].find(b => b.textContent.trim() === 'Both'); if (b) { b.click(); return 'both'; } row = row.parentElement; }
  return 'no-both'; }, label);
await step('s00-load', async () => { await page.evaluate(() => window.scrollTo(0, 0)); }, 1200);
await step('s01-ushape', () => btn('U-Shape'), 1400);
await step('s02-lshape', () => btn('L-Shape'), 1400);
await step('s03-circle', () => btn('Circle'), 1200);
await step('s04-thickness', () => typeIn('wall-width', 1030), 600);
await step('s05-radius', () => typeIn('radius', 2750), 600);
await step('s06-height', () => typeIn('wall-height', 550), 900);
await step('s07-straights', async () => { await btn('U-Shape'); await sleep(900); await typeIn('start-straight-length', 1500); await typeIn('end-straight-length', 1500); }, 1200);
await step('s08-circle-angle', async () => { await btn('Circle'); await sleep(900); await typeIn('angle', 220); }, 1800);
await step('s09-features', () => scrollToText('FEATURES'), 1200);
await step('s10-rounded-on', () => btn('Rounded Ends'), 1400);
await step('s11-rounded-off', () => btn('Rounded Ends'), 900);
await step('s12-backrest-on', async () => { if (!(await isOn('Backrest'))) await btn('Backrest'); }, 1400);
await step('s13-br-height', () => typeIn('backrest-height', 450), 600);
await step('s14-br-width', () => typeIn('backrest-top-width', 300), 600);
await step('s15-br-taper', () => typeIn('backrest-taper', 15), 1000);
await step('s16-cantilever-on', async () => { if (!(await isOn('Cantilever'))) await btn('Cantilever'); }, 1600);
await step('s17-scroll-formwork', () => scrollToText('FORMWORK'), 1200);
await step('s18-plates', async () => { console.log('  plates:', await checkRow('Plates')); await sleep(700); console.log('  plates both:', await clickBothNear('Plates')); }, 1200);
await step('s19-shutters', async () => { console.log('  shutters:', await checkRow('Shutters')); await sleep(700); console.log('  shutters both:', await clickBothNear('Shutters')); }, 1200);
await step('s20-endcaps', async () => { console.log('  endcaps:', await checkRow('End Caps')); }, 1400);
await step('s21-summary', () => scrollToText('Order Summary'), 1800);
await step('s22-summary-bottom', async () => { await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight)); }, 1800);
await step('s23-model', async () => { await page.evaluate(() => window.scrollTo(0, 0)); }, 1800);
await cdp.send('Page.stopScreencast');
const state = await page.evaluate(() => ({ fields: [...document.querySelectorAll('input')].map(i => (i.id || i.type) + '=' + i.value).join(' '), summary: (document.body.innerText.match(/Order Summary[\s\S]{0,400}/) || [''])[0].replace(/\s+/g, ' ') }));
console.log(JSON.stringify(state, null, 1));
fs.writeFileSync(`${OUT}/steps.json`, JSON.stringify(steps, null, 1));
await browser.close();
console.log('total frames', n);
