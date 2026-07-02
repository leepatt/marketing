#!/usr/bin/env node
/** Render the Google Ads API tool design doc to a PDF for the Basic-access application. */
import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";

const out = resolve("exports/craftons-google-ads-api-tool-design.pdf");

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; }
  body { font-family: Arial, Helvetica, sans-serif; color: #16201b; line-height: 1.5; font-size: 11.5pt; }
  h1 { font-size: 20pt; color: #194431; margin: 0 0 2px; }
  .sub { color: #555; font-size: 10pt; margin: 0 0 18px; }
  h2 { font-size: 13pt; color: #194431; border-bottom: 1px solid #cdd8d2; padding-bottom: 3px; margin: 18px 0 8px; }
  p, li { font-size: 11.5pt; }
  ul { margin: 4px 0 8px 18px; padding: 0; }
  code, pre { font-family: "Courier New", monospace; font-size: 10pt; }
  pre { background: #f3f6f4; border: 1px solid #d7e0db; border-radius: 4px; padding: 10px; white-space: pre-wrap; }
  strong { color: #123022; }
</style></head><body>
  <h1>Google Ads API — Tool Design Document</h1>
  <p class="sub">Craftons (Peninsula Studio T/A Craftons) · craftons.com.au · 2026 · Internal in-house tool</p>

  <h2>1. Tool name</h2>
  <p>Craftons Marketing Engine — Google Ads integration (<code>google-ads.mjs</code>).</p>

  <h2>2. Company type / who it serves</h2>
  <p><strong>In-house.</strong> It manages <strong>only Craftons' own</strong> Google Ads account
  (advertiser 310-491-2421) under our manager account (275-347-3695). It is not offered to third
  parties, not resold, and not a commercial product. Single company, single account.</p>

  <h2>3. Purpose</h2>
  <p>Automate reporting and assist with campaign management for our own account:</p>
  <ul>
    <li>Reduce manual weekly review time.</li>
    <li>Catch wasted spend (irrelevant search terms, non-converting keywords) faster.</li>
    <li>Keep ad copy, keywords and negatives in sync with our content/keyword plan.</li>
  </ul>

  <h2>4. Functionality (what it does with the API)</h2>
  <p><strong>Reporting (read):</strong> pull campaign / ad group / keyword / search-term performance
  via GAQL (clicks, cost, conversions, CTR, cost-per-conversion, impression share) for the last
  7/30 days, and generate a weekly performance report with recommendations.</p>
  <p><strong>Campaign management (write — human-approved):</strong> create / edit campaigns, ad groups
  and responsive search ads; add / edit keywords and negative keywords; adjust budgets and bids;
  pause / enable keywords, ads and campaigns.</p>
  <p><strong>Operational:</strong> handle API errors and partial failures and surface them to the user;
  respect rate limits; use the manager account login-customer-id.</p>

  <h2>5. Architecture &amp; data flow</h2>
  <ul>
    <li><strong>Runtime:</strong> Node.js script (<code>google-ads.mjs</code>) using the official
      Google Ads API client library.</li>
    <li><strong>Auth:</strong> OAuth2 — developer token + client ID/secret + refresh token + customer
      IDs read from environment variables, never committed to source control.</li>
    <li><strong>Flow:</strong> script &rarr; Google Ads API &rarr; results rendered as a report. Write
      operations run only when a human passes an explicit CONFIRM flag after reviewing the change.</li>
    <li><strong>No third-party data.</strong> Only our own account's data is read or modified.</li>
  </ul>

  <h2>6. Controls / safety</h2>
  <ul>
    <li><strong>Read-only by default.</strong> All change operations are gated behind explicit human
      approval (CONFIRM=1).</li>
    <li>Daily budget cap on the account; no autonomous spend increases without approval.</li>
    <li>Every change is logged for audit.</li>
  </ul>

  <h2>7. Compliance</h2>
  <ul>
    <li>Adheres to the Google Ads API Terms &amp; Conditions and Required Minimum Functionality.</li>
    <li>No prohibited use: no scraping, no unauthorised data, no managing accounts we don't own.</li>
  </ul>

  <h2>8. Mockup — weekly report output (sample)</h2>
  <pre>CRAFTONS ADWORDS — WEEKLY REPORT (last 7 days)
Spend $312  |  Clicks 84  |  Conv 6  |  Cost/lead $52  |  CTR 5.1%
Top wasted search terms -> add as negatives: "free curved wall plans", "skateboard ply"
Keywords to pause (>=20 clicks, 0 conv): [curved plywood panels]
Best ad group by cost/lead: Curved Architraves ($31)  ->  shift budget here
Proposed changes (need approval): +5 negatives, pause 1 keyword, +$10/day to architraves</pre>
</body></html>`;

await mkdir(dirname(out), { recursive: true });
const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: "networkidle" });
  await page.pdf({
    path: out,
    format: "A4",
    printBackground: true,
    margin: { top: "16mm", bottom: "16mm", left: "15mm", right: "15mm" },
  });
  console.log("✓ PDF →", out);
} finally {
  await browser.close();
}
