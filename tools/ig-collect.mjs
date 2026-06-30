#!/usr/bin/env node
/**
 * ig-collect.mjs — collect a public IG profile's images + videos into a local
 * folder, for the Craftons inspiration / image-gen reference library.
 *
 * RUN THIS ON YOUR DESKTOP (logged into Instagram), NOT in the cloud session —
 * the cloud environment blocks instagram.com and IG blocks datacenter/headless
 * traffic. On your own machine + IP + login it behaves like a normal browser.
 *
 *   cd tools && npm install          # one-time: installs playwright
 *   npx playwright install chromium  # one-time: gets the browser
 *
 *   # 1) one-time: log in, save your session (cookies) to tools/.ig-session.json
 *   node ig-collect.mjs login
 *
 *   # 2) collect a profile (reuses the saved session)
 *   node ig-collect.mjs modernconcreteco --max 60
 *   #   --out DIR     output root (default ./collected)
 *   #   --max N       stop after N posts (default: all found)
 *   #   --headful     show the browser (default headless; use if IG challenges)
 *
 * Output:
 *   collected/<handle>/raw/<shortcode>_<n>.{jpg,mp4}   downloaded media
 *   collected/<handle>/manifest.json                   index of posts + files
 *
 * Then hand the videos to the frame extractor:
 *   python3 video-frames.py collected/<handle>/raw -o collected/<handle>/frames
 * and upload collected/<handle>/ into Drive 01 Inspiration/<handle>/.
 *
 * NOTES / hygiene:
 *  - Session cookies live in tools/.ig-session.json — git-ignored, never committed.
 *  - Reference/mood use only (third-party content); rate-limited to be polite.
 *  - IG's DOM/CDN changes often. If post discovery returns 0, IG likely tweaked
 *    markup — the POST_LINK selector below is the thing to update.
 */
import { chromium } from 'playwright';
import { mkdir, writeFile, access } from 'node:fs/promises';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SESSION = path.join(__dirname, '.ig-session.json');
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
           '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const jitter = (min, max) => sleep(min + Math.floor(Math.random() * (max - min)));

function waitForEnter(msg) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((res) => rl.question(msg, () => { rl.close(); res(); }));
}

async function exists(p) { try { await access(p); return true; } catch { return false; } }

// --- login: open a real browser, let the human sign in, save the session -----
async function login() {
  const browser = await chromium.launch({ headless: false });
  const ctx = await browser.newContext({ userAgent: UA });
  const page = await ctx.newPage();
  await page.goto('https://www.instagram.com/accounts/login/', { waitUntil: 'domcontentloaded' });
  console.log('\nA browser window opened. Log into Instagram there (and clear any');
  console.log('"save info"/2FA prompts until you can see your normal feed).');
  await waitForEnter('\nWhen you are fully logged in, press Enter here to save the session… ');
  await ctx.storageState({ path: SESSION });
  await browser.close();
  console.log(`✓ Saved session to ${SESSION} (git-ignored). You won't need to log in again unless it expires.`);
}

// --- collect ------------------------------------------------------------------
function parseArgs(argv) {
  const handle = argv[0]?.replace(/^@/, '');
  const opt = { out: 'collected', max: Infinity, headful: false };
  for (let i = 1; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') opt.out = argv[++i];
    else if (a === '--max') opt.max = parseInt(argv[++i], 10);
    else if (a === '--headful') opt.headful = true;
  }
  return { handle, opt };
}

// Collapse IG CDN resolution variants of the same media to one key, so we keep
// only the largest copy of each photo/video rather than every size.
function mediaKey(url) {
  const file = url.split('?')[0].split('/').pop() || url;
  const m = file.match(/([0-9]{6,}_[0-9]+_[0-9]+)/); // stable IG media id
  return m ? m[1] : file;
}

async function collectPostUrls(page, handle, max) {
  await page.goto(`https://www.instagram.com/${handle}/`, { waitUntil: 'domcontentloaded' });
  if (/accounts\/login/.test(page.url())) {
    throw new Error('Redirected to login — session missing/expired. Run: node ig-collect.mjs login');
  }
  const found = new Set();
  let stable = 0;
  while (found.size < max && stable < 4) {
    const hrefs = await page.$$eval('a[href*="/p/"], a[href*="/reel/"]',
      (as) => as.map((a) => a.href));
    const before = found.size;
    for (const h of hrefs) {
      const m = h.match(/\/(p|reel)\/[^/]+\//);
      if (m) found.add('https://www.instagram.com' + m[0]);
    }
    if (found.size === before) stable++; else stable = 0;
    await page.mouse.wheel(0, 4000);
    await jitter(1200, 2600);
  }
  return [...found].slice(0, max === Infinity ? undefined : max);
}

async function downloadPost(ctx, url) {
  const page = await ctx.newPage();
  const grabbed = new Map(); // mediaKey -> { url, ext, buf }
  page.on('response', async (resp) => {
    try {
      const ct = resp.headers()['content-type'] || '';
      let ext;
      if (/^image\/jpeg/.test(ct)) ext = 'jpg';
      else if (/^image\/png/.test(ct)) ext = 'png';
      else if (/^image\/webp/.test(ct)) ext = 'webp';
      else if (/^video\/mp4/.test(ct)) ext = 'mp4';
      else return;
      const buf = await resp.body();
      if (buf.length < 20 * 1024) return; // skip icons/thumbnails
      const key = mediaKey(resp.url());
      const prev = grabbed.get(key);
      if (!prev || buf.length > prev.buf.length) grabbed.set(key, { url: resp.url(), ext, buf });
    } catch { /* redirects / opaque responses */ }
  });

  await page.goto(url, { waitUntil: 'domcontentloaded' }).catch(() => {});
  await jitter(1500, 2500);
  // Click through carousel slides (if any) to trigger the rest of the media.
  for (let i = 0; i < 12; i++) {
    const next = await page.$('button[aria-label="Next"], button[aria-label="Next photo"]');
    if (!next) break;
    await next.click().catch(() => {});
    await jitter(700, 1400);
  }
  await page.close();
  return [...grabbed.values()];
}

async function collect(handle, opt) {
  if (!handle) throw new Error('Usage: node ig-collect.mjs <handle> [--max N] [--out DIR] [--headful]');
  if (!(await exists(SESSION))) throw new Error('No session. Run first: node ig-collect.mjs login');

  const browser = await chromium.launch({ headless: !opt.headful });
  const ctx = await browser.newContext({ storageState: SESSION, userAgent: UA, viewport: { width: 1280, height: 1600 } });
  const page = await ctx.newPage();

  const outRaw = path.join(opt.out, handle, 'raw');
  await mkdir(outRaw, { recursive: true });

  console.log(`Discovering posts for @${handle}…`);
  const posts = await collectPostUrls(page, handle, opt.max);
  console.log(`Found ${posts.length} posts. Downloading media…`);

  const manifest = [];
  for (const [i, url] of posts.entries()) {
    const shortcode = (url.match(/\/(?:p|reel)\/([^/]+)/) || [])[1] || `post${i}`;
    const media = await downloadPost(ctx, url);
    const files = [];
    for (const [n, m] of media.entries()) {
      const name = `${shortcode}_${n}.${m.ext}`;
      await writeFile(path.join(outRaw, name), m.buf);
      files.push(name);
    }
    manifest.push({ shortcode, url, type: url.includes('/reel/') ? 'reel' : 'post', files });
    console.log(`  [${i + 1}/${posts.length}] ${shortcode}: ${files.length} file(s)`);
    await jitter(1500, 4000); // be polite between posts
  }

  await writeFile(path.join(opt.out, handle, 'manifest.json'),
    JSON.stringify({ handle, collectedCount: posts.length, posts: manifest }, null, 2));
  await browser.close();

  const vids = manifest.flatMap((p) => p.files).filter((f) => f.endsWith('.mp4')).length;
  console.log(`\n✓ Done. ${manifest.length} posts -> ${outRaw}/  (${vids} videos)`);
  console.log(`Next: python3 video-frames.py "${outRaw}" -o "${path.join(opt.out, handle, 'frames')}"`);
}

// --- main ---------------------------------------------------------------------
const [cmd, ...rest] = process.argv.slice(2);
try {
  if (cmd === 'login') {
    await login();
  } else {
    const { handle, opt } = parseArgs([cmd, ...rest]);
    await collect(handle, opt);
  }
} catch (e) {
  console.error('✗', e.message);
  process.exit(1);
}
