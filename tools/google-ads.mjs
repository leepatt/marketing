#!/usr/bin/env node
// Craftons Marketing Engine — Google Ads reporter (read-only)
//
// Zero-dependency. Uses Node's native fetch (Node 18+) and the Google Ads REST API.
// Reads creds from environment variables only — nothing is committed.
//
// Usage:
//   node tools/google-ads.mjs whoami            # account identity + access sanity check
//   node tools/google-ads.mjs accounts          # list accounts this OAuth user can reach
//   node tools/google-ads.mjs report [days]     # campaign performance report (default 7 days)
//   node tools/google-ads.mjs terms  [days]     # search-terms report — wasted-spend hunt (default 30)
//
// This tool is READ-ONLY by design. Campaign changes (negatives, pauses, bids, budgets) are
// intentionally NOT implemented here yet — they belong behind an explicit CONFIRM=1 gate, mirroring
// tools/meta-ads.mjs. Build that as a separate, deliberate step. See campaigns/adwords/api-tool-design.md.
//
// Linkage note (verified 2026-06-30): advertiser 310-491-2421 ("Craftons Google Ads account") is
// reached via DIRECT user access, NOT through the manager MCC (275-347-3695). Forcing the manager as
// login-customer-id returns USER_PERMISSION_DENIED because the advertiser isn't linked under it.
// So we default to NO login-customer-id. Set GOOGLE_ADS_USE_LOGIN_CUSTOMER_ID=1 to send it anyway
// (needed only if/when the account is moved under the manager).

const API_VERSION = 'v21';

const ENV = {
  developerToken: process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
  clientId: process.env.GOOGLE_ADS_CLIENT_ID,
  clientSecret: process.env.GOOGLE_ADS_CLIENT_SECRET,
  refreshToken: process.env.GOOGLE_ADS_REFRESH_TOKEN,
  customerId: process.env.GOOGLE_ADS_CUSTOMER_ID,
  loginCustomerId: process.env.GOOGLE_ADS_LOGIN_CUSTOMER_ID,
  useLoginCustomerId: process.env.GOOGLE_ADS_USE_LOGIN_CUSTOMER_ID === '1',
};

function requireEnv(keys) {
  const missing = keys.filter((k) => !ENV[k]);
  if (missing.length) {
    const names = missing.map((k) => k.replace(/[A-Z]/g, (c) => '_' + c).toUpperCase()).join(', ');
    console.error(`Missing required env vars: ${names}`);
    console.error('Set them in the session environment (never commit). See campaigns/adwords/api-access.md.');
    process.exit(1);
  }
}

async function getAccessToken() {
  requireEnv(['clientId', 'clientSecret', 'refreshToken']);
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: ENV.clientId,
      client_secret: ENV.clientSecret,
      refresh_token: ENV.refreshToken,
      grant_type: 'refresh_token',
    }),
  });
  const data = await res.json();
  if (!res.ok || !data.access_token) {
    throw new Error(`OAuth refresh failed (${res.status}): ${data.error_description || data.error || 'unknown'}`);
  }
  return data.access_token;
}

// Run a GAQL query against a customer. Returns a flat array of result rows.
async function gaql(query, { customerId = ENV.customerId } = {}) {
  requireEnv(['developerToken', 'customerId']);
  const accessToken = await getAccessToken();
  const headers = {
    Authorization: `Bearer ${accessToken}`,
    'developer-token': ENV.developerToken,
    'Content-Type': 'application/json',
  };
  if (ENV.useLoginCustomerId && ENV.loginCustomerId) {
    headers['login-customer-id'] = ENV.loginCustomerId;
  }
  const url = `https://googleads.googleapis.com/${API_VERSION}/customers/${customerId}/googleAds:searchStream`;
  const res = await fetch(url, { method: 'POST', headers, body: JSON.stringify({ query }) });
  const text = await res.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    throw new Error(`Non-JSON response (${res.status}): ${text.slice(0, 300)}`);
  }
  if (!res.ok) {
    const err = Array.isArray(body) ? body[0]?.error : body?.error;
    const detail = err?.details?.[0]?.errors?.[0]?.message || err?.message || JSON.stringify(body).slice(0, 300);
    throw new Error(`Google Ads API error (${res.status}): ${detail}`);
  }
  const batches = Array.isArray(body) ? body : [body];
  return batches.flatMap((b) => b.results || []);
}

const micros = (v) => (Number(v || 0) / 1e6);
const money = (v) => `$${micros(v).toLocaleString('en-AU', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

async function cmdWhoami() {
  const rows = await gaql(
    'SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.time_zone, ' +
    'customer.manager, customer.test_account FROM customer LIMIT 1'
  );
  const c = rows[0]?.customer;
  if (!c) return console.log('No customer returned.');
  console.log('Account:', c.descriptiveName, `(${c.id})`);
  console.log('Currency:', c.currencyCode, '| Timezone:', c.timeZone);
  console.log('Manager account:', c.manager ? 'yes' : 'no', '| Test account:', c.testAccount ? 'yes' : 'no');
  console.log(c.testAccount ? '\n⚠ Test account — dev token is operating in Test access.'
                            : '\n✓ Live (non-test) account reachable — dev token has Basic access.');
}

async function cmdAccounts() {
  const accessToken = await getAccessToken();
  requireEnv(['developerToken']);
  const res = await fetch(
    `https://googleads.googleapis.com/${API_VERSION}/customers:listAccessibleCustomers`,
    { headers: { Authorization: `Bearer ${accessToken}`, 'developer-token': ENV.developerToken } }
  );
  const data = await res.json();
  if (!res.ok) throw new Error(`listAccessibleCustomers failed (${res.status}): ${JSON.stringify(data).slice(0, 300)}`);
  console.log('Accessible customers:');
  for (const r of data.resourceNames || []) console.log(' -', r.replace('customers/', ''));
}

async function cmdReport(days = 7) {
  const rows = await gaql(
    'SELECT campaign.name, campaign.status, campaign.advertising_channel_type, ' +
    'metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, ' +
    'metrics.conversions_value, metrics.ctr ' +
    `FROM campaign WHERE segments.date DURING LAST_${days}_DAYS ORDER BY metrics.cost_micros DESC`
  );
  console.log(`CRAFTONS ADWORDS — CAMPAIGN REPORT (last ${days} days)\n`);
  if (!rows.length) return console.log('No campaign activity in the window.');
  let cost = 0, clicks = 0, conv = 0, value = 0;
  for (const r of rows) {
    const c = r.campaign, m = r.metrics || {};
    cost += micros(m.costMicros); clicks += Number(m.clicks || 0);
    conv += Number(m.conversions || 0); value += micros(m.conversionsValue);
    const cpl = Number(m.conversions) ? micros(m.costMicros) / Number(m.conversions) : null;
    console.log(`• ${c.name}  [${c.status} · ${c.advertisingChannelType}]`);
    console.log(`    ${money(m.costMicros)}  |  ${m.clicks || 0} clicks  |  ${m.impressions || 0} impr  |  ` +
                `${Number(m.conversions || 0).toFixed(0)} conv` + (cpl ? `  |  ${'$' + cpl.toFixed(2)}/conv` : ''));
  }
  const cpl = conv ? cost / conv : null;
  console.log('\n— TOTALS —');
  console.log(`Spend $${cost.toFixed(2)}  |  ${clicks} clicks  |  ${conv.toFixed(0)} conv` +
              (cpl ? `  |  $${cpl.toFixed(2)}/conv` : '') + `  |  conv value $${value.toFixed(2)}`);
}

async function cmdTerms(days = 30) {
  const rows = await gaql(
    'SELECT search_term_view.search_term, campaign.name, metrics.cost_micros, metrics.clicks, ' +
    'metrics.conversions FROM search_term_view ' +
    `WHERE segments.date DURING LAST_${days}_DAYS ORDER BY metrics.cost_micros DESC LIMIT 50`
  );
  console.log(`CRAFTONS ADWORDS — SEARCH TERMS (last ${days} days, top 50 by spend)\n`);
  if (!rows.length) return console.log('No search-term data (Performance Max / Shopping report search terms differently).');
  const wasted = [];
  for (const r of rows) {
    const t = r.searchTermView?.searchTerm, m = r.metrics || {};
    const conv = Number(m.conversions || 0);
    console.log(`• "${t}"  —  ${money(m.costMicros)} · ${m.clicks || 0} clicks · ${conv.toFixed(0)} conv` +
                `  [${r.campaign?.name || ''}]`);
    if (Number(m.clicks || 0) >= 5 && conv === 0) wasted.push(t);
  }
  if (wasted.length) {
    console.log('\nWasted-spend candidates (≥5 clicks, 0 conv) — review as negatives:');
    for (const t of wasted) console.log('  -', t);
  }
}

async function main() {
  const [cmd, arg] = process.argv.slice(2);
  try {
    switch (cmd) {
      case 'whoami': await cmdWhoami(); break;
      case 'accounts': await cmdAccounts(); break;
      case 'report': await cmdReport(arg ? parseInt(arg, 10) : 7); break;
      case 'terms': await cmdTerms(arg ? parseInt(arg, 10) : 30); break;
      default:
        console.log('Usage: node tools/google-ads.mjs <whoami|accounts|report [days]|terms [days]>');
        process.exit(cmd ? 1 : 0);
    }
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
