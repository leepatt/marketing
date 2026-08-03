#!/usr/bin/env node
/**
 * google-ads.mjs — Craftons Marketing Engine · Google Ads integration (READ-ONLY)
 *
 * Pulls performance data from our own Google Ads account via the REST API + GAQL.
 * Design doc: campaigns/adwords/api-tool-design.md
 *
 * Control model: this file is read-only by design. Any write operation (negatives,
 * pausing keywords, bid/budget changes) must land in a separate code path gated behind
 * an explicit CONFIRM=1 human approval — see the design doc. Claude reports, Lee approves.
 *
 * Env vars required:
 *   GOOGLE_ADS_DEVELOPER_TOKEN  GOOGLE_ADS_CLIENT_ID  GOOGLE_ADS_CLIENT_SECRET
 *   GOOGLE_ADS_REFRESH_TOKEN    GOOGLE_ADS_CUSTOMER_ID
 *   GOOGLE_ADS_LOGIN_CUSTOMER_ID (optional — only needed when the target account is a
 *                                 child of that manager account)
 *
 * Usage:
 *   node tools/google-ads.mjs accounts
 *   node tools/google-ads.mjs report [--days 30] [--customer 3104912421]
 *   node tools/google-ads.mjs raw "SELECT campaign.name FROM campaign"
 */

const API_VERSION = 'v22';
const BASE = `https://googleads.googleapis.com/${API_VERSION}`;

const env = (k) => {
  const v = process.env[k];
  if (!v) throw new Error(`Missing env var ${k}`);
  return v;
};

// ── auth ──────────────────────────────────────────────────────────────────────
let _token = null;
async function accessToken() {
  if (_token) return _token;
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: env('GOOGLE_ADS_CLIENT_ID'),
      client_secret: env('GOOGLE_ADS_CLIENT_SECRET'),
      refresh_token: env('GOOGLE_ADS_REFRESH_TOKEN'),
      grant_type: 'refresh_token',
    }),
  });
  const json = await res.json();
  if (!json.access_token) throw new Error(`OAuth refresh failed: ${JSON.stringify(json)}`);
  _token = json.access_token;
  return _token;
}

// ── API ───────────────────────────────────────────────────────────────────────
async function call(path, { body, useLoginHeader = true } = {}) {
  const headers = {
    Authorization: `Bearer ${await accessToken()}`,
    'developer-token': env('GOOGLE_ADS_DEVELOPER_TOKEN'),
    'Content-Type': 'application/json',
  };
  // The manager header is only valid when the target account really sits under that MCC.
  // Sending it for a directly-granted account returns USER_PERMISSION_DENIED, so we retry without.
  const login = process.env.GOOGLE_ADS_LOGIN_CUSTOMER_ID;
  if (useLoginHeader && login) headers['login-customer-id'] = login;

  const res = await fetch(`${BASE}/${path}`, {
    method: body ? 'POST' : 'GET',
    headers,
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  const json = await res.json();
  if (!res.ok) {
    const err = json?.error?.details?.[0]?.errors?.[0];
    if (useLoginHeader && err?.errorCode?.authorizationError === 'USER_PERMISSION_DENIED') {
      return call(path, { body, useLoginHeader: false });
    }
    throw new Error(`${res.status} ${err?.message || json?.error?.message || JSON.stringify(json)}`);
  }
  return json;
}

/** Run a GAQL query, following pagination. Returns a flat array of result rows. */
async function gaql(customerId, query) {
  const rows = [];
  let pageToken;
  do {
    const json = await call(`customers/${customerId}/googleAds:search`, {
      body: { query, ...(pageToken ? { pageToken } : {}) },
    });
    rows.push(...(json.results || []));
    pageToken = json.nextPageToken;
  } while (pageToken);
  return rows;
}

async function listAccessibleCustomers() {
  const json = await call('customers:listAccessibleCustomers');
  return (json.resourceNames || []).map((r) => r.split('/')[1]);
}

// ── formatting ────────────────────────────────────────────────────────────────
const money = (micros) => (Number(micros || 0) / 1e6);
const aud = (micros) => `$${money(micros).toFixed(2)}`;
const pct = (n) => `${(Number(n || 0) * 100).toFixed(2)}%`;
const num = (n) => Number(n || 0);

function table(headers, rows) {
  if (!rows.length) return '_(none)_\n';
  const widths = headers.map((h, i) => Math.max(h.length, ...rows.map((r) => String(r[i] ?? '').length)));
  const line = (cells) => '| ' + cells.map((c, i) => String(c ?? '').padEnd(widths[i])).join(' | ') + ' |';
  return [line(headers), '|' + widths.map((w) => '-'.repeat(w + 2)).join('|') + '|', ...rows.map(line)].join('\n') + '\n';
}

// ── queries ───────────────────────────────────────────────────────────────────
const METRICS = `metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions,
  metrics.conversions_value, metrics.ctr, metrics.average_cpc`;

const QUERIES = {
  account: `SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.time_zone,
    customer.manager, customer.status, customer.auto_tagging_enabled FROM customer`,

  campaigns: (d) => `SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
    campaign.bidding_strategy_type, campaign.start_date, campaign_budget.amount_micros,
    metrics.search_impression_share, metrics.search_budget_lost_impression_share,
    metrics.search_rank_lost_impression_share, ${METRICS}
    FROM campaign WHERE segments.date DURING ${d} AND campaign.status != 'REMOVED'`,

  adGroups: (d) => `SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status, ${METRICS}
    FROM ad_group WHERE segments.date DURING ${d} AND ad_group.status != 'REMOVED'`,

  keywords: (d) => `SELECT campaign.name, ad_group.name, ad_group_criterion.criterion_id,
    ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
    ad_group_criterion.status, ad_group_criterion.quality_info.quality_score, ${METRICS}
    FROM keyword_view WHERE segments.date DURING ${d} AND ad_group_criterion.status != 'REMOVED'`,

  searchTerms: (d) => `SELECT search_term_view.search_term, search_term_view.status, campaign.name,
    ad_group.name, ${METRICS}
    FROM search_term_view WHERE segments.date DURING ${d}`,

  ads: (d) => `SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status,
    ad_group_ad.ad_strength, ad_group_ad.ad.responsive_search_ad.headlines,
    ad_group_ad.ad.final_urls, ${METRICS}
    FROM ad_group_ad WHERE segments.date DURING ${d} AND ad_group_ad.status != 'REMOVED'`,

  conversionActions: (d) => `SELECT conversion_action.name, conversion_action.category,
    conversion_action.status, conversion_action.primary_for_goal, conversion_action.type,
    metrics.all_conversions, metrics.all_conversions_value
    FROM conversion_action WHERE segments.date DURING ${d}`,

  daily: (d) => `SELECT segments.date, ${METRICS} FROM campaign
    WHERE segments.date DURING ${d} AND campaign.status != 'REMOVED'`,

  devices: (d) => `SELECT segments.device, ${METRICS} FROM campaign WHERE segments.date DURING ${d}`,

  geo: (d) => `SELECT campaign.name, geographic_view.country_criterion_id, ${METRICS}
    FROM geographic_view WHERE segments.date DURING ${d}`,
};

// ── report ────────────────────────────────────────────────────────────────────
function sumMetrics(rows) {
  return rows.reduce(
    (a, r) => {
      const m = r.metrics || {};
      a.impressions += num(m.impressions);
      a.clicks += num(m.clicks);
      a.cost += money(m.costMicros);
      a.conversions += num(m.conversions);
      a.value += num(m.conversionsValue);
      return a;
    },
    { impressions: 0, clicks: 0, cost: 0, conversions: 0, value: 0 }
  );
}

async function report(customerId, range) {
  const out = [];
  const [acct] = await gaql(customerId, QUERIES.account);
  const c = acct.customer;
  out.push(`# Google Ads report — ${c.descriptiveName} (${customerId})`);
  out.push(`Range: **${range}** · Currency ${c.currencyCode} · TZ ${c.timeZone}\n`);

  const campaigns = await gaql(customerId, QUERIES.campaigns(range));
  const t = sumMetrics(campaigns);
  out.push('## Account totals');
  out.push(
    table(
      ['Impr', 'Clicks', 'CTR', 'Cost', 'Avg CPC', 'Conv', 'Cost/conv', 'Conv value'],
      [[
        t.impressions, t.clicks,
        t.impressions ? pct(t.clicks / t.impressions) : '—',
        `$${t.cost.toFixed(2)}`,
        t.clicks ? `$${(t.cost / t.clicks).toFixed(2)}` : '—',
        t.conversions.toFixed(1),
        t.conversions ? `$${(t.cost / t.conversions).toFixed(2)}` : '—',
        `$${t.value.toFixed(2)}`,
      ]]
    )
  );

  out.push('## Campaigns');
  out.push(
    table(
      ['Campaign', 'Status', 'Type', 'Budget/day', 'Impr', 'Clicks', 'CTR', 'Cost', 'CPC', 'Conv', 'Cost/conv', 'IS', 'Lost(budget)', 'Lost(rank)'],
      campaigns
        .sort((a, b) => money(b.metrics?.costMicros) - money(a.metrics?.costMicros))
        .map((r) => {
          const m = r.metrics || {};
          const cost = money(m.costMicros);
          return [
            r.campaign.name, r.campaign.status, r.campaign.advertisingChannelType,
            aud(r.campaignBudget?.amountMicros), num(m.impressions), num(m.clicks),
            pct(m.ctr), `$${cost.toFixed(2)}`, aud(m.averageCpc), num(m.conversions).toFixed(1),
            num(m.conversions) ? `$${(cost / num(m.conversions)).toFixed(2)}` : '—',
            m.searchImpressionShare != null ? pct(m.searchImpressionShare) : '—',
            m.searchBudgetLostImpressionShare != null ? pct(m.searchBudgetLostImpressionShare) : '—',
            m.searchRankLostImpressionShare != null ? pct(m.searchRankLostImpressionShare) : '—',
          ];
        })
    )
  );

  out.push('## Ad groups');
  const adGroups = await gaql(customerId, QUERIES.adGroups(range));
  out.push(
    table(
      ['Campaign', 'Ad group', 'Status', 'Impr', 'Clicks', 'CTR', 'Cost', 'CPC', 'Conv', 'Cost/conv'],
      adGroups
        .sort((a, b) => money(b.metrics?.costMicros) - money(a.metrics?.costMicros))
        .map((r) => {
          const m = r.metrics || {};
          const cost = money(m.costMicros);
          return [
            r.campaign.name, r.adGroup.name, r.adGroup.status, num(m.impressions), num(m.clicks),
            pct(m.ctr), `$${cost.toFixed(2)}`, aud(m.averageCpc), num(m.conversions).toFixed(1),
            num(m.conversions) ? `$${(cost / num(m.conversions)).toFixed(2)}` : '—',
          ];
        })
    )
  );

  out.push('## Keywords');
  const keywords = await gaql(customerId, QUERIES.keywords(range));
  out.push(
    table(
      ['Keyword', 'Match', 'Ad group', 'QS', 'Impr', 'Clicks', 'CTR', 'Cost', 'CPC', 'Conv'],
      keywords
        .sort((a, b) => money(b.metrics?.costMicros) - money(a.metrics?.costMicros))
        .map((r) => {
          const m = r.metrics || {};
          const k = r.adGroupCriterion || {};
          return [
            k.keyword?.text, k.keyword?.matchType, r.adGroup.name,
            k.qualityInfo?.qualityScore ?? '—', num(m.impressions), num(m.clicks), pct(m.ctr),
            aud(m.costMicros), aud(m.averageCpc), num(m.conversions).toFixed(1),
          ];
        })
    )
  );

  out.push('## Search terms (what people actually typed)');
  const terms = await gaql(customerId, QUERIES.searchTerms(range));
  out.push(
    table(
      ['Search term', 'Ad group', 'Impr', 'Clicks', 'Cost', 'Conv', 'Added/Excluded'],
      terms
        .sort((a, b) => money(b.metrics?.costMicros) - money(a.metrics?.costMicros))
        .map((r) => {
          const m = r.metrics || {};
          return [
            r.searchTermView.searchTerm, r.adGroup?.name, num(m.impressions), num(m.clicks),
            aud(m.costMicros), num(m.conversions).toFixed(1), r.searchTermView.status || 'NONE',
          ];
        })
    )
  );

  out.push('## Ads');
  const ads = await gaql(customerId, QUERIES.ads(range));
  out.push(
    table(
      ['Ad group', 'Ad ID', 'Status', 'Strength', 'Impr', 'Clicks', 'CTR', 'Cost', 'Conv'],
      ads.map((r) => {
        const m = r.metrics || {};
        return [
          r.adGroup.name, r.adGroupAd.ad.id, r.adGroupAd.status, r.adGroupAd.adStrength || '—',
          num(m.impressions), num(m.clicks), pct(m.ctr), aud(m.costMicros), num(m.conversions).toFixed(1),
        ];
      })
    )
  );

  out.push('## Conversion actions');
  const convs = await gaql(customerId, QUERIES.conversionActions(range));
  out.push(
    table(
      ['Action', 'Category', 'Status', 'Primary', 'All conv', 'Value'],
      convs
        .filter((r) => num(r.metrics?.allConversions) > 0)
        .sort((a, b) => num(b.metrics?.allConversions) - num(a.metrics?.allConversions))
        .map((r) => [
          r.conversionAction.name, r.conversionAction.category, r.conversionAction.status,
          r.conversionAction.primaryForGoal === false ? 'secondary' : 'PRIMARY',
          num(r.metrics.allConversions).toFixed(1), `$${num(r.metrics.allConversionsValue).toFixed(2)}`,
        ])
    )
  );

  out.push('## Daily spend');
  const daily = await gaql(customerId, QUERIES.daily(range));
  const byDate = new Map();
  for (const r of daily) {
    const d = r.segments.date;
    const acc = byDate.get(d) || { cost: 0, clicks: 0, impressions: 0, conversions: 0 };
    acc.cost += money(r.metrics.costMicros);
    acc.clicks += num(r.metrics.clicks);
    acc.impressions += num(r.metrics.impressions);
    acc.conversions += num(r.metrics.conversions);
    byDate.set(d, acc);
  }
  out.push(
    table(
      ['Date', 'Impr', 'Clicks', 'Cost', 'Conv'],
      [...byDate.entries()].sort().map(([d, v]) => [
        d, v.impressions, v.clicks, `$${v.cost.toFixed(2)}`, v.conversions.toFixed(1),
      ])
    )
  );

  out.push('## Devices');
  const devices = await gaql(customerId, QUERIES.devices(range));
  const byDevice = new Map();
  for (const r of devices) {
    const d = r.segments.device;
    const acc = byDevice.get(d) || { cost: 0, clicks: 0, impressions: 0, conversions: 0 };
    acc.cost += money(r.metrics.costMicros);
    acc.clicks += num(r.metrics.clicks);
    acc.impressions += num(r.metrics.impressions);
    acc.conversions += num(r.metrics.conversions);
    byDevice.set(d, acc);
  }
  out.push(
    table(
      ['Device', 'Impr', 'Clicks', 'CTR', 'Cost', 'Conv'],
      [...byDevice.entries()].map(([d, v]) => [
        d, v.impressions, v.clicks, v.impressions ? pct(v.clicks / v.impressions) : '—',
        `$${v.cost.toFixed(2)}`, v.conversions.toFixed(1),
      ])
    )
  );

  return out.join('\n');
}

// ── CLI ───────────────────────────────────────────────────────────────────────
const [cmd, ...rest] = process.argv.slice(2);
const flag = (name, def) => {
  const i = rest.indexOf(`--${name}`);
  return i >= 0 ? rest[i + 1] : def;
};

try {
  if (cmd === 'accounts') {
    const ids = await listAccessibleCustomers();
    console.log('Accessible customer IDs:');
    for (const id of ids) {
      try {
        const [r] = await gaql(id, QUERIES.account);
        const c = r.customer;
        console.log(`  ${id}  ${c.descriptiveName}  ${c.manager ? '(manager)' : '(advertiser)'}  ${c.currencyCode}  ${c.status}`);
      } catch (e) {
        console.log(`  ${id}  <no access: ${e.message.slice(0, 80)}>`);
      }
    }
  } else if (cmd === 'report') {
    const days = flag('days', '30');
    const range = /^\d+$/.test(days) ? `LAST_${days}_DAYS` : days;
    console.log(await report(flag('customer', env('GOOGLE_ADS_CUSTOMER_ID')), range));
  } else if (cmd === 'raw') {
    const rows = await gaql(flag('customer', env('GOOGLE_ADS_CUSTOMER_ID')), rest[0]);
    console.log(JSON.stringify(rows, null, 2));
  } else {
    console.log('Usage: node tools/google-ads.mjs <accounts|report|raw> [--days N] [--customer ID]');
    process.exit(1);
  }
} catch (e) {
  console.error(`ERROR: ${e.message}`);
  process.exit(1);
}
