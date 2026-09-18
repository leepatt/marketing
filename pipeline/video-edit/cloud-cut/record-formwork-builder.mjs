import { chromium } from 'playwright';
import { readFileSync, renameSync } from 'node:fs';
const spki = readFileSync('spki.txt','utf8').trim();
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: [`--ignore-certificate-errors-spki-list=${spki}`] });
const ctx = await b.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1,
  recordVideo: { dir: 'rec', size: { width: 1080, height: 1920 } } });
const p = await ctx.newPage();
const t0 = Date.now(); const mark = (l) => console.log(`${((Date.now()-t0)/1000).toFixed(2)}s  ${l}`);
await p.goto('https://craftons-curves-calculator.vercel.app/apps/formwork', { waitUntil: 'domcontentloaded', timeout: 60000 });
await p.addStyleTag({ content: 'html{zoom:2}' }); await p.waitForSelector('canvas'); await p.waitForTimeout(6000);            // let the 3D model settle
mark('START (model visible)');
const wheel = async (px, steps=12) => { for (let i=0;i<steps;i++){ await p.mouse.wheel(0, px/steps); await p.waitForTimeout(40);} };
await p.mouse.move(540, 400); await p.waitForTimeout(1500);
// --- design your concrete structure ---
const radius = p.locator('#radius, input[name="radius"], input[id*="radius" i]'); await radius.scrollIntoViewIfNeeded(); await p.waitForTimeout(600);
await radius.click({ clickCount: 3 }); mark('radius focus');
await radius.pressSequentially('1300', { delay: 140 }); await radius.press('Tab'); mark('radius=1300'); await p.waitForTimeout(1400);
const height = p.locator('#wall-height, input[name="wall-height"], input[id*="wall-height" i]'); await height.click({ clickCount: 3 });
await height.pressSequentially('600', { delay: 140 }); await height.press('Tab'); mark('height=600'); await p.waitForTimeout(1400);
// --- select your formwork ---
await wheel(520); await p.waitForTimeout(500); mark('scrolled to formwork');
for (const name of ['Plates','Shutters','End Caps']) {
  await p.getByText(name, { exact: true }).first().click(); mark(`tick ${name}`); await p.waitForTimeout(800);
}
// --- get an instant price ---
await wheel(700, 16); await p.waitForTimeout(600); mark('scrolled to order summary');
await p.waitForTimeout(3000); mark('END');
const txt = await p.locator('text=Order Summary').locator('..').innerText().catch(()=>'(n/a)');
console.log('ORDER SUMMARY TEXT:', txt.replace(/\s+/g,' ').slice(0,300));
await p.screenshot({ path: 'rec/final.png' });
await ctx.close(); await b.close();
