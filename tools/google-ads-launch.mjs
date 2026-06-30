#!/usr/bin/env node
// Craftons Marketing Engine — one-time campaign launcher (WRITE, gated)
//
// Creates the "Craftons – Customised Building Products" Search campaign on the live account
// (310-491-2421) from the assets in campaigns/adwords/. Built PAUSED — nothing spends until a human
// enables it in the Google Ads UI.
//
// SAFETY MODEL
//   • Dry-run by default: validates the whole thing via the API's validateOnly flag, creates nothing.
//   • CONFIRM=1 actually writes.
//   • Structure is one ATOMIC mutate (all-or-nothing) → a failure creates nothing (no partial build,
//     no duplicates). Extensions are a second atomic mutate after the campaign exists.
//   • Campaign status = PAUSED. Ad groups/ads/keywords ENABLED, so flipping the campaign on serves all.
//
// USAGE
//   node tools/google-ads-launch.mjs            # dry-run (validate only, no writes)
//   CONFIRM=1 node tools/google-ads-launch.mjs  # create the campaign (PAUSED) for real

const API = 'v21';
const ENV = {
  developerToken: process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
  clientId: process.env.GOOGLE_ADS_CLIENT_ID,
  clientSecret: process.env.GOOGLE_ADS_CLIENT_SECRET,
  refreshToken: process.env.GOOGLE_ADS_REFRESH_TOKEN,
  customerId: process.env.GOOGLE_ADS_CUSTOMER_ID,
};
const CONFIRM = process.env.CONFIRM === '1';
const CID = ENV.customerId;

// ─────────────────────────────────────────────────────────────────────────────
// CAMPAIGN SPEC — sourced verbatim from campaigns/adwords/*
// ─────────────────────────────────────────────────────────────────────────────
const BUDGET_MICROS = '50000000';   // $50.00/day
const MAX_CPC_MICROS = '3500000';   // ~$3.50 max CPC (Manual CPC cap)
const CAMPAIGN_NAME = 'Craftons – Customised Building Products';

// Geo (verified via geo_target_constant lookup 2026-06-30)
const GEO = {
  melbourneProximity: { lat: -37813600, lng: 144963100, radiusKm: 50 }, // Melbourne CBD, 50km
  locations: ['1000537' /* Geelong */, '9056922' /* Surf Coast */, '9056918' /* Mornington Peninsula */],
  language: 'languageConstants/1000', // English
};

const AD_GROUPS = [
  {
    name: 'Radius Pro',
    finalUrl: 'https://craftons.com.au/products/radius-online',
    path1: 'radius-pro', path2: 'curved-ply',
    phrase: ['curved plywood', 'radius plywood', 'custom curved plywood', 'curved plywood cut to size',
             'curved plywood panels', 'curved ply', 'bendy ply', 'bendy ply melbourne', 'flexible plywood'],
    exact: ['curved plywood', 'radius plywood', 'bendy ply', 'custom curved plywood', 'curved plywood melbourne'],
    pinnedHeadline: 'Radius Pro Curved Plywood',
    headlines: ['Curved Plywood, Cut To Size', 'Radius Pro Curved Plywood', 'Designed Online, CNC-Cut',
      'Dispatched In 3 Days', 'Curved Ply, Ready To Fix', 'No On-Site Curve Cutting', 'Custom Curved Plywood',
      'Cut To Your Set-Out', 'Curves, Made To Spec', 'Radius Parts, Cut To Size', 'Design Your Curve Online',
      'Flawless Fit, Less Rework', 'Australian Made Curved Ply', 'Install-Ready Curved Ply', 'Get A Curved Ply Quote'],
    descriptions: [
      'Design your curve online, we CNC-cut it and dispatch in 3 days. Ready to install.',
      'Curved plywood cut to your radius and set-out. No on-site cutting, no rework.',
      'Big curves auto-split with Part IDs engraved. Flawless fit, less waste on site.',
      'Radius Pro: design curved plywood online, made to spec, delivered. Australian made.'],
  },
  {
    name: 'Curved Bench Seat / Formwork',
    finalUrl: 'https://craftons.com.au/products/craftons-formwork-builder-custom-online-formwork',
    path1: 'formwork', path2: 'bench-seat',
    phrase: ['curved formwork', 'formwork for curved walls', 'curved concrete wall formwork', 'circular formwork',
             'curved bench seat', 'curved concrete bench seat', 'curved bench seat formwork',
             'curved retaining wall formwork', 'firepit formwork'],
    exact: ['curved formwork', 'curved bench seat', 'curved bench seat formwork', 'circular formwork',
            'curved concrete bench seat'],
    pinnedHeadline: 'Curved Bench Seat Formwork',
    headlines: ['Curved Bench Seat Formwork', 'Curved Formwork, Done', 'Design Curved Formwork', 'No On-Site Cutting',
      'Curved Formwork, Online', 'Just Brace And Pour', 'Circular, U & L Walls', 'CNC-Cut Formwork Kit',
      'Curved Concrete, Sorted', 'Ready-To-Assemble Kit', 'Pour A Perfect Curve', 'Formwork To Your Shape',
      'Stop Building Site Forms', 'Bench Seat Curves, Cut', 'Design It Online, Pour It'],
    descriptions: [
      'Design curved formwork online. CNC-cut, labelled kit delivered ready to assemble.',
      'Circular, U-shape and L-shape walls. No on-site cutting. Just brace and pour.',
      'Curved bench seat? Get the formwork cut to your shape and delivered to site.',
      'Skip the hand-built forms. Design your curve online and order the kit. Australian made.'],
  },
  {
    name: 'Curved Architraves',
    finalUrl: 'https://craftons.com.au/products/curved-architraves',
    path1: 'curved', path2: 'architraves',
    phrase: ['curved architrave', 'curved architraves', 'arched door architrave', 'curved window architrave',
             'mdf curved architrave', 'arched doorway trim', 'curved head door'],
    exact: ['curved architrave', 'curved architraves', 'curved window architrave', 'arched architrave'],
    pinnedHeadline: 'Curved Architraves, Online',
    headlines: ['Curved Architraves, Online', 'Custom Curved Architraves', 'Arched Door Architraves',
      'Design Curved Architraves', 'Curved Heads, Instant Price', 'Architraves To Any Curve',
      'No Hand-Shaping Architraves', 'Arched Doorway Trim', '3D Builder, Instant Price', 'Curved Window Architraves',
      'MDF Curved Architraves', 'Order Curved Architraves', 'Arches, Circles, Niches', 'Curved Architraves, Cut',
      'Build It In 3D, Get A Price'],
    descriptions: [
      'Design custom curved architraves in 3D. Enter your sizes, get instant pricing.',
      'Arched doors, curved windows, circles and niches. MR MDF, made to your opening.',
      'No hand-shaping. Design your curved architrave online and order with instant pricing.',
      'Curved-head doors sorted. Preview in 3D, get a price, order. Australian made.'],
  },
];

// Campaign-level negatives (phrase match) — from negative-keywords.md
const NEGATIVES = ['free', 'cheap', 'cheapest', 'discount', 'bargain', 'second hand', 'secondhand', 'used',
  'recycled', 'salvage', 'diy', 'plans', 'blueprint', 'how to draw', 'drawing', 'sketchup', 'autocad', 'revit',
  'template', 'tutorial', 'youtube', 'job', 'jobs', 'career', 'careers', 'salary', 'wage', 'apprenticeship',
  'recruitment', 'hire', 'rent', 'rental', 'lease', 'repair', 'repairs', 'restoration', 'course', 'courses',
  'class', 'training', 'tafe', 'diploma', 'certificate', 'skateboard', 'longboard', 'skate', 'surfboard', 'guitar',
  'ukulele', 'drum', 'speaker box', 'chair', 'stool', 'furniture', 'table', 'boat', 'kayak', 'model making',
  'prototype', 'lego', 'minecraft', 'cardboard', 'foam', 'wikipedia', 'meaning', 'definition', 'history',
  'bunnings', 'ikea', 'kmart'];

// Extensions — from ad-extensions.md
const SITELINKS = [
  { text: 'Radius Pro', url: 'https://craftons.com.au/products/radius-online',
    d1: 'Curved plywood, cut to size', d2: 'Designed online, CNC-cut' },
  { text: 'Formwork Builder', url: 'https://craftons.com.au/products/craftons-formwork-builder-custom-online-formwork',
    d1: 'Curved formwork, ready to fit', d2: 'Circular, U-shape & L-shape' },
  { text: 'Curved Architraves', url: 'https://craftons.com.au/products/curved-architraves',
    d1: 'Arched doors, curved windows', d2: 'Design in 3D, instant pricing' },
  { text: 'Get a Quote', url: 'https://craftons.com.au/pages/contact',
    d1: 'Custom curves, fast quote', d2: 'Dispatched in 3 business days' },
];
const CALLOUTS = ['CNC-Cut To Spec', 'Dispatched In 3 Days', 'Australian Made', 'No On-Site Cutting',
  'Ready To Install', 'Cut To Your Set-Out', 'Minimal Rework', 'Trade Accounts Available'];
const SNIPPETS = [
  { header: 'Types', values: ['Curved Plywood', 'Formply', 'Radius MDF', 'Curved Formwork', 'Curved Architraves'] },
  { header: 'Services', values: ['Design Online', 'CNC Cutting', 'Cut To Size', 'Delivery'] },
];
const CALL = { countryCode: 'AU', phoneNumber: '0485500227' };

// ─────────────────────────────────────────────────────────────────────────────
// Client-side validation (catch length issues before hitting the API)
// ─────────────────────────────────────────────────────────────────────────────
function validateCopy() {
  const errs = [];
  for (const g of AD_GROUPS) {
    if (g.headlines.length < 3 || g.headlines.length > 15) errs.push(`${g.name}: ${g.headlines.length} headlines (need 3-15)`);
    if (g.descriptions.length < 2 || g.descriptions.length > 4) errs.push(`${g.name}: ${g.descriptions.length} descriptions (need 2-4)`);
    g.headlines.forEach((h) => h.length > 30 && errs.push(`${g.name} headline >30: "${h}" (${h.length})`));
    g.descriptions.forEach((d) => d.length > 90 && errs.push(`${g.name} description >90: "${d}" (${d.length})`));
    [g.path1, g.path2].forEach((p) => p && p.length > 15 && errs.push(`${g.name} path >15: "${p}"`));
    if (!g.headlines.includes(g.pinnedHeadline)) errs.push(`${g.name}: pinned headline not in headline list`);
  }
  SITELINKS.forEach((s) => {
    if (s.text.length > 25) errs.push(`sitelink text >25: "${s.text}"`);
    if (s.d1.length > 35 || s.d2.length > 35) errs.push(`sitelink desc >35 on "${s.text}"`);
  });
  CALLOUTS.forEach((c) => c.length > 25 && errs.push(`callout >25: "${c}"`));
  SNIPPETS.forEach((s) => s.values.forEach((v) => v.length > 25 && errs.push(`snippet value >25: "${v}"`)));
  return errs;
}

// ─────────────────────────────────────────────────────────────────────────────
// API plumbing
// ─────────────────────────────────────────────────────────────────────────────
function requireEnv() {
  const missing = Object.entries(ENV).filter(([, v]) => !v).map(([k]) => k);
  if (missing.length) { console.error('Missing env:', missing.join(', ')); process.exit(1); }
}
async function getAccessToken() {
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id: ENV.clientId, client_secret: ENV.clientSecret,
      refresh_token: ENV.refreshToken, grant_type: 'refresh_token' }),
  });
  const d = await res.json();
  if (!d.access_token) throw new Error('OAuth refresh failed: ' + JSON.stringify(d).slice(0, 200));
  return d.access_token;
}
async function atomicMutate(accessToken, operations, validateOnly) {
  const res = await fetch(`https://googleads.googleapis.com/${API}/customers/${CID}/googleAds:mutate`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${accessToken}`, 'developer-token': ENV.developerToken, 'Content-Type': 'application/json' },
    body: JSON.stringify({ mutateOperations: operations, validateOnly, partialFailure: false }),
  });
  const text = await res.text();
  let body; try { body = JSON.parse(text); } catch { throw new Error(`Non-JSON (${res.status}): ${text.slice(0, 400)}`); }
  if (!res.ok) {
    const err = body.error || (Array.isArray(body) && body[0]?.error);
    const gfail = err?.details?.find((d) => d['@type']?.includes('GoogleAdsFailure'));
    const msgs = gfail?.errors?.map((e) => `  • ${e.message}` + (e.trigger ? ` [${JSON.stringify(e.trigger)}]` : '')).join('\n');
    throw new Error(`API error (${res.status}): ${err?.message}\n${msgs || JSON.stringify(body).slice(0, 500)}`);
  }
  return body;
}

// ─────────────────────────────────────────────────────────────────────────────
// Operation builders
// ─────────────────────────────────────────────────────────────────────────────
const rn = (svc, id) => `customers/${CID}/${svc}/${id}`;
const matchKw = (text, matchType) => ({ keyword: { text, matchType } });

function buildStructureOps() {
  const ops = [];
  const budgetRN = rn('campaignBudgets', -1);
  const campRN = rn('campaigns', -2);
  ops.push({ campaignBudgetOperation: { create: {
    resourceName: budgetRN, name: `${CAMPAIGN_NAME} — daily`, amountMicros: BUDGET_MICROS,
    deliveryMethod: 'STANDARD', explicitlyShared: false } } });
  ops.push({ campaignOperation: { create: {
    resourceName: campRN, name: CAMPAIGN_NAME, status: 'PAUSED', advertisingChannelType: 'SEARCH',
    campaignBudget: budgetRN, manualCpc: {},
    containsEuPoliticalAdvertising: 'DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING',
    networkSettings: { targetGoogleSearch: true, targetSearchNetwork: false, targetContentNetwork: false, targetPartnerSearchNetwork: false },
    geoTargetTypeSetting: { positiveGeoTargetType: 'PRESENCE' } } } });
  // campaign criteria: language, proximity, locations
  ops.push({ campaignCriterionOperation: { create: { campaign: campRN, language: { languageConstant: GEO.language } } } });
  ops.push({ campaignCriterionOperation: { create: { campaign: campRN, proximity: {
    geoPoint: { latitudeInMicroDegrees: GEO.melbourneProximity.lat, longitudeInMicroDegrees: GEO.melbourneProximity.lng },
    radius: GEO.melbourneProximity.radiusKm, radiusUnits: 'KILOMETERS' } } } });
  for (const id of GEO.locations)
    ops.push({ campaignCriterionOperation: { create: { campaign: campRN, location: { geoTargetConstant: `geoTargetConstants/${id}` } } } });
  // negatives (phrase)
  for (const text of NEGATIVES)
    ops.push({ campaignCriterionOperation: { create: { campaign: campRN, negative: true, ...matchKw(text, 'PHRASE') } } });
  // ad groups + keywords + ads
  AD_GROUPS.forEach((g, i) => {
    const agRN = rn('adGroups', -(10 + i));
    ops.push({ adGroupOperation: { create: {
      resourceName: agRN, name: g.name, campaign: campRN, type: 'SEARCH_STANDARD',
      cpcBidMicros: MAX_CPC_MICROS, status: 'ENABLED' } } });
    for (const text of g.phrase) ops.push({ adGroupCriterionOperation: { create: { adGroup: agRN, status: 'ENABLED', ...matchKw(text, 'PHRASE') } } });
    for (const text of g.exact) ops.push({ adGroupCriterionOperation: { create: { adGroup: agRN, status: 'ENABLED', ...matchKw(text, 'EXACT') } } });
    const headlines = g.headlines.map((h) => h === g.pinnedHeadline ? { text: h, pinnedField: 'HEADLINE_1' } : { text: h });
    ops.push({ adGroupAdOperation: { create: { adGroup: agRN, status: 'ENABLED', ad: {
      finalUrls: [g.finalUrl],
      responsiveSearchAd: { headlines, descriptions: g.descriptions.map((d) => ({ text: d })), path1: g.path1, path2: g.path2 } } } } });
  });
  return ops;
}

function buildExtensionOps(campaignResourceName) {
  const ops = [];
  let tmp = 0;
  const link = (assetRN, fieldType) => ops.push({ campaignAssetOperation: { create: { campaign: campaignResourceName, asset: assetRN, fieldType } } });
  for (const s of SITELINKS) {
    const a = rn('assets', -(++tmp));
    ops.push({ assetOperation: { create: { resourceName: a, finalUrls: [s.url], sitelinkAsset: { linkText: s.text, description1: s.d1, description2: s.d2 } } } });
    link(a, 'SITELINK');
  }
  for (const c of CALLOUTS) {
    const a = rn('assets', -(++tmp));
    ops.push({ assetOperation: { create: { resourceName: a, calloutAsset: { calloutText: c } } } });
    link(a, 'CALLOUT');
  }
  for (const s of SNIPPETS) {
    const a = rn('assets', -(++tmp));
    ops.push({ assetOperation: { create: { resourceName: a, structuredSnippetAsset: { header: s.header, values: s.values } } } });
    link(a, 'STRUCTURED_SNIPPET');
  }
  const ca = rn('assets', -(++tmp));
  ops.push({ assetOperation: { create: { resourceName: ca, callAsset: {
    countryCode: CALL.countryCode, phoneNumber: CALL.phoneNumber,
    callConversionReportingState: 'USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION' } } } });
  link(ca, 'CALL');
  return ops;
}

// ─────────────────────────────────────────────────────────────────────────────
function printPlan() {
  const kw = AD_GROUPS.reduce((n, g) => n + g.phrase.length + g.exact.length, 0);
  console.log('LAUNCH PLAN — Craftons – Customised Building Products');
  console.log(`  Account: ${CID}  |  Status on create: PAUSED  |  Budget: $${(+BUDGET_MICROS / 1e6).toFixed(2)}/day  |  Max CPC: $${(+MAX_CPC_MICROS / 1e6).toFixed(2)}`);
  console.log('  Networks: Google Search only (Search Partners OFF, Display OFF)');
  console.log('  Geo: Melbourne 50km radius + Geelong + Surf Coast + Mornington Peninsula | Presence only | English');
  console.log(`  Ad groups: ${AD_GROUPS.length}  |  Keywords: ${kw}  |  RSAs: ${AD_GROUPS.length}  |  Campaign negatives: ${NEGATIVES.length}`);
  console.log(`  Extensions: ${SITELINKS.length} sitelinks, ${CALLOUTS.length} callouts, ${SNIPPETS.length} snippet sets, 1 call (${CALL.phoneNumber})`);
  AD_GROUPS.forEach((g) => console.log(`    - ${g.name}: ${g.phrase.length} phrase + ${g.exact.length} exact kw, 1 RSA -> ${g.finalUrl}`));
}

async function main() {
  requireEnv();
  const copyErrs = validateCopy();
  if (copyErrs.length) { console.error('Copy validation failed:\n' + copyErrs.map((e) => '  • ' + e).join('\n')); process.exit(1); }
  printPlan();
  console.log('');

  const accessToken = await getAccessToken();
  const structureOps = buildStructureOps();

  if (!CONFIRM) {
    console.log(`Dry-run (validateOnly) — ${structureOps.length} structure operations. No changes will be made.`);
    await atomicMutate(accessToken, structureOps, true);
    console.log('✓ Structure validated by Google Ads API — no errors.');
    console.log('(Extensions are validated at execution, after the campaign exists.)');
    console.log('\nTo create it for real (PAUSED), re-run with:  CONFIRM=1 node tools/google-ads-launch.mjs');
    return;
  }

  console.log(`CONFIRM=1 — creating campaign (PAUSED). ${structureOps.length} structure operations (atomic)...`);
  const res = await atomicMutate(accessToken, structureOps, false);
  const results = res.mutateOperationResponses || [];
  const campResult = results.find((r) => r.campaignResult)?.campaignResult;
  const campaignRN = campResult?.resourceName;
  if (!campaignRN) throw new Error('No campaign resource name returned: ' + JSON.stringify(res).slice(0, 400));
  const campaignId = campaignRN.split('/').pop();
  console.log(`✓ Campaign created: ${campaignRN} (id ${campaignId}) — PAUSED.`);

  console.log('Adding extensions (sitelinks, callouts, snippets, call)...');
  try {
    const extOps = buildExtensionOps(campaignRN);
    await atomicMutate(accessToken, extOps, false);
    console.log(`✓ Extensions added (${extOps.length} operations).`);
  } catch (e) {
    console.error('Extensions step failed (campaign + ads are fine; add extensions in UI or re-run extensions):\n' + e.message);
  }

  console.log('\n✅ DONE — campaign is built and PAUSED on account ' + CID + '.');
  console.log('Next: review it in the Google Ads UI, then flip the campaign to ENABLED to go live.');
  console.log(`Verify here:  node tools/google-ads.mjs report 1   (or whoami)`);
}

main().catch((e) => { console.error('\nError:', e.message); process.exit(1); });
