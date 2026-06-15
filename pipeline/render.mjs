#!/usr/bin/env node
/**
 * Craftons render pipeline — HTML/CSS template → on-brand PNG.
 *
 * Usage:
 *   node render.mjs --template templates/post-hero-1080x1350.html \
 *                   --content content/example-radius-pro.json \
 *                   --out exports/radius-pro.png \
 *                   [--width 1080] [--height 1350] [--scale 2]
 *
 * Templates use {{PLACEHOLDER}} tokens; the content JSON supplies their values.
 * Renders at `scale`× for crispness via Playwright, then downscales to the exact
 * target dimensions with sharp.
 */
import { chromium } from "playwright";
import sharp from "sharp";
import { readFile, writeFile, mkdir, rm } from "node:fs/promises";
import { dirname, resolve, join } from "node:path";

function arg(flag, def) {
  const i = process.argv.indexOf(flag);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : def;
}

const templatePath = resolve(arg("--template", "templates/post-hero-1080x1350.html"));
const contentPath = resolve(arg("--content", "content/example-radius-pro.json"));
const outPath = resolve(arg("--out", "exports/out.png"));
const width = parseInt(arg("--width", "1080"), 10);
const height = parseInt(arg("--height", "1350"), 10);
const scale = parseInt(arg("--scale", "2"), 10);

const html = await readFile(templatePath, "utf8");
const content = JSON.parse(await readFile(contentPath, "utf8"));

// Fill {{PLACEHOLDER}} tokens (missing keys render empty, never literal braces).
const filled = html.replace(/\{\{(\w+)\}\}/g, (_, k) => content[k] ?? "");

// Write a temp file next to the template so relative ../tokens.css + fonts resolve.
const tmp = join(dirname(templatePath), `.__render_${Date.now()}.html`);
await writeFile(tmp, filled, "utf8");

await mkdir(dirname(outPath), { recursive: true });

const browser = await chromium.launch();
try {
  const page = await browser.newPage({
    viewport: { width, height },
    deviceScaleFactor: scale,
  });
  await page.goto("file://" + tmp, { waitUntil: "networkidle" });
  await page.evaluate(() => document.fonts.ready);
  const shot = await page.screenshot({ clip: { x: 0, y: 0, width, height } });
  // Normalise to the exact target dimensions and optimise.
  await sharp(shot).resize(width, height).png({ quality: 90 }).toFile(outPath);
  console.log(`✓ Rendered ${width}×${height} → ${outPath}`);
} finally {
  await browser.close();
  await rm(tmp, { force: true });
}
