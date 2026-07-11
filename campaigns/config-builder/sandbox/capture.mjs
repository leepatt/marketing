import { chromium } from 'playwright-core';
import { execFileSync } from 'node:child_process';
import { mkdirSync, rmSync, existsSync } from 'node:fs';
import path from 'node:path';

const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const HERE = path.resolve('.');
const v = parseInt(process.argv[2] ?? '0', 10);
const fps = parseInt(process.argv[3] ?? '30', 10);
const W = parseInt(process.argv[4] ?? '1080', 10);
const H = parseInt(process.argv[5] ?? '1920', 10);
const scale = W / 1080;

const framesDir = path.join(HERE, 'frames', `v${v}`);
rmSync(framesDir, { recursive: true, force: true });
mkdirSync(framesDir, { recursive: true });
mkdirSync(path.join(HERE, 'out'), { recursive: true });

const browser = await chromium.launch({ executablePath: EXE, args: ['--no-sandbox', '--force-color-profile=srgb'] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
// scale the 1080x1920 stage to requested W/H
await page.goto('file://' + path.join(HERE, 'scene.html') + '?v=' + v, { waitUntil: 'load' });
await page.addStyleTag({ content: `#viewport{transform:scale(${scale});transform-origin:0 0}` });
await page.waitForFunction('window.__ready === true', { timeout: 15000 });
const dur = await page.evaluate('window.__duration');
const total = Math.round(dur * fps);
console.log(`variant ${v}: ${dur.toFixed(2)}s, ${total} frames @ ${fps}fps, ${W}x${H}`);

for (let i = 0; i <= total; i++) {
  const t = i / fps;
  await page.evaluate((tt) => window.__seek(tt), t);
  await page.screenshot({ path: path.join(framesDir, `f_${String(i).padStart(4, '0')}.png`), clip: { x: 0, y: 0, width: W, height: H } });
}
await browser.close();

const outFile = path.join(HERE, 'out', `demo_v${v}.mp4`);
execFileSync('ffmpeg', ['-y', '-framerate', String(fps), '-i', path.join(framesDir, 'f_%04d.png'),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', outFile], { stdio: 'inherit' });
console.log('wrote ' + outFile);
rmSync(framesDir, { recursive: true, force: true });
