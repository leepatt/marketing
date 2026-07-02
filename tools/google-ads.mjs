#!/usr/bin/env node
/**
 * google-ads.mjs — Craftons Marketing Engine ↔ Google Ads API.
 *
 * READ-ONLY by default. Two commands today:
 *   node google-ads.mjs accounts          list accounts under the MCC + identify Craftons
 *   node google-ads.mjs report [--days N]  performance report (default 7 days)
 *
 * Writes (create campaign, add negatives, pause/adjust) will be added behind a
 * CONFIRM=1 gate once we've connected and confirmed the target account — we do
 * not ship untested money-spending code.
 *
 * Auth via environment variables (never committed — set in the environment's
 * secret store):
 *   GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET,
 *   GOOGLE_ADS_REFRESH_TOKEN, GOOGLE_ADS_LOGIN_CUSTOMER_ID (the MCC, 275-347-3695),
 *   GOOGLE_ADS_CUSTOMER_ID (the Craftons advertiser — confirm via `accounts` first).
 */
import process from 'node:process';

const BASE_ENV = [
  'GOOGLE_ADS_DEVELOPER_TOKEN',
  'GOOGLE_ADS_CLIENT_ID',
  'GOOGLE_ADS_CLIENT_SECRET',
  'GOOGLE_ADS_REFRESH_TOKEN',
  'GOOGLE_ADS_LOGIN_CUSTOMER_ID',
];

const clean = (id) => (id || '').replace(/-/g, '');
const dollars = (m) => (Number(m || 0) / 1e6);

function need(keys) {
  const missing = keys.filter((k) => !process.env[k]);
  if (missing.length) {
    console.error('Missing required env vars:\n  ' + missing.join('\n  ') +
      "\n\nSet these in the environment's secret store (not in the repo or chat).");
    process.exit(1);
  }
}

async function loadApi() {
  try {
    const mod = await import('google-ads-api');
    return mod.GoogleAdsApi;
  } catch {
    console.error('Dependency missing. Run:  cd tools && npm install');
    process.exit(1);
  }
}

function customerFor(api, customerId, loginId) {
  return api.Customer({
    customer_id: clean(customerId),
    login_customer_id: clean(loginId),
    refresh_token: process.env.GOOGLE_ADS_REFRESH_TOKEN,
  });
}

// Query with a login-customer-id fallback. The Craftons advertiser (3104912421)
// is reached DIRECTLY, not through the MCC (2753473695) — they aren't linked in
// the API. So try the configured login first, and if the account isn't reachable
// that way, retry with the account as its own login-customer-id.
async function gaql(api, customerId, query) {
  const configured = process.env.GOOGLE_ADS_LOGIN_CUSTOMER_ID || customerId;
  try {
    return await customerFor(api, customerId, configured).query(query);
  } catch (e) {
    const msg = String(e?.message || '') + ' ' +
      (Array.isArray(e?.errors) ? e.errors.map((x) => x?.message || '').join(' ') : '');
    if (/permission/i.test(msg) && clean(configured) !== clean(customerId)) {
      return await customerFor(api, customerId, customerId).query(query);
    }
    throw e;
  }
}

// --- accounts: list accessible customers + name/currency/conversions ----------
async function cmdAccounts() {
  need(BASE_ENV);
  const GoogleAdsApi = await loadApi();
  const api = new GoogleAdsApi({
    client_id: process.env.GOOGLE_ADS_CLIENT_ID,
    client_secret: process.env.GOOGLE_ADS_CLIENT_SECRET,
    developer_token: process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
  });

  const { resource_names } = await api.listAccessibleCustomers(process.env.GOOGLE_ADS_REFRESH_TOKEN);
  console.log(`Accounts accessible under MCC ${process.env.GOOGLE_ADS_LOGIN_CUSTOMER_ID}:\n`);

  for (const rn of resource_names) {
    const id = rn.split('/')[1];
    try {
      const rows = await gaql(api, id,
        'SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.manager FROM customer LIMIT 1');
      const c = rows[0]?.customer || {};
      let conv = '';
      try {
        const m = await gaql(api, id,
          'SELECT metrics.conversions FROM customer WHERE segments.date DURING LAST_30_DAYS');
        const total = m.reduce((s, r) => s + Number(r.metrics?.conversions || 0), 0);
        conv = `  conv(30d)=${total.toFixed(0)}`;
      } catch { /* manager accounts have no metrics */ }
      console.log(`  ${c.id}  ${c.descriptive_name || '(no name)'}  [${c.currency_code || '?'}]` +
        `${c.manager ? '  (manager)' : ''}${conv}`);
    } catch (e) {
      console.log(`  ${id}  (couldn't read: ${(e.message || '').slice(0, 70)})`);
    }
  }
  console.log('\n→ Find the Craftons advertiser by name + conversions (≈23 purchases + 443 lead forms),');
  console.log('  then set GOOGLE_ADS_CUSTOMER_ID to that id and run `report`.');
}

// --- report: last-N-day performance ------------------------------------------
async function cmdReport(days) {
  need([...BASE_ENV, 'GOOGLE_ADS_CUSTOMER_ID']);
  const GoogleAdsApi = await loadApi();
  const api = new GoogleAdsApi({
    client_id: process.env.GOOGLE_ADS_CLIENT_ID,
    client_secret: process.env.GOOGLE_ADS_CLIENT_SECRET,
    developer_token: process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
  });
  const custId = process.env.GOOGLE_ADS_CUSTOMER_ID;
  const range = days === 30 ? 'LAST_30_DAYS' : 'LAST_7_DAYS';

  const campaigns = await gaql(api, custId,
    `SELECT campaign.name, metrics.cost_micros, metrics.clicks, metrics.conversions, ` +
    `metrics.ctr, metrics.average_cpc, metrics.cost_per_conversion ` +
    `FROM campaign WHERE segments.date DURING ${range} ORDER BY metrics.cost_micros DESC`);

  console.log(`CRAFTONS ADWORDS — REPORT (${range.replace('_', ' ').toLowerCase()})\n`);
  if (!campaigns.length) {
    console.log('No spend in this window.');
  } else {
    let cost = 0, clicks = 0, conv = 0;
    for (const r of campaigns) {
      cost += dollars(r.metrics.cost_micros); clicks += Number(r.metrics.clicks || 0);
      conv += Number(r.metrics.conversions || 0);
    }
    console.log(`Totals: spend $${cost.toFixed(2)} | clicks ${clicks} | conv ${conv.toFixed(1)} | ` +
      `cost/conv ${conv ? '$' + (cost / conv).toFixed(2) : 'n/a'}\n`);
    console.log('By campaign:');
    for (const r of campaigns) {
      console.log(`  ${r.campaign.name}: $${dollars(r.metrics.cost_micros).toFixed(2)}, ` +
        `${r.metrics.clicks} clicks, ${Number(r.metrics.conversions).toFixed(1)} conv, ` +
        `CTR ${(Number(r.metrics.ctr) * 100).toFixed(1)}%`);
    }
  }

  const terms = await gaql(api, custId,
    `SELECT search_term_view.search_term, metrics.clicks, metrics.cost_micros, metrics.conversions ` +
    `FROM search_term_view WHERE segments.date DURING ${range} AND metrics.clicks > 0 ` +
    `ORDER BY metrics.cost_micros DESC LIMIT 25`);
  const wasted = terms.filter((r) => Number(r.metrics.conversions || 0) === 0);
  if (wasted.length) {
    console.log('\nTop spend, 0 conversions (negative-keyword candidates):');
    for (const r of wasted.slice(0, 15)) {
      console.log(`  "${r.search_term_view.search_term}" — $${dollars(r.metrics.cost_micros).toFixed(2)}, ` +
        `${r.metrics.clicks} clicks`);
    }
  }
}

// --- main --------------------------------------------------------------------
const argv = process.argv.slice(2);
const cmd = argv[0];
const daysFlag = argv.includes('--days') ? parseInt(argv[argv.indexOf('--days') + 1], 10) : 7;

try {
  if (cmd === 'accounts') await cmdAccounts();
  else if (cmd === 'report') await cmdReport(daysFlag);
  else {
    console.log('Usage:\n  node google-ads.mjs accounts\n  node google-ads.mjs report [--days 7|30]');
    process.exit(cmd ? 1 : 0);
  }
} catch (e) {
  console.error('✗ Google Ads API error:', e.message || e);
  if (e.errors) console.error(JSON.stringify(e.errors, null, 2));
  process.exit(1);
}
