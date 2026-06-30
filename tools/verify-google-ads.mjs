// Verify Google Ads creds in this env: token validity + Test vs Basic access.
// Uses the REST API directly (no library install). Prints NO secret values.

const {
  GOOGLE_ADS_DEVELOPER_TOKEN: DEV_TOKEN,
  GOOGLE_ADS_CLIENT_ID: CLIENT_ID,
  GOOGLE_ADS_CLIENT_SECRET: CLIENT_SECRET,
  GOOGLE_ADS_REFRESH_TOKEN: REFRESH_TOKEN,
  GOOGLE_ADS_CUSTOMER_ID: CUSTOMER_ID,
  GOOGLE_ADS_LOGIN_CUSTOMER_ID: LOGIN_CID,
} = process.env;

const cid = (CUSTOMER_ID || '').replace(/[^0-9]/g, '');
const login = (LOGIN_CID || '').replace(/[^0-9]/g, '');

function log(...a) { console.log(...a); }

// 1) Mint an access token from the refresh token
async function getAccessToken() {
  const body = new URLSearchParams({
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    refresh_token: REFRESH_TOKEN,
    grant_type: 'refresh_token',
  });
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  const j = await r.json();
  if (!r.ok) throw new Error(`OAuth token exchange failed (${r.status}): ${JSON.stringify(j)}`);
  return j.access_token;
}

async function tryVersion(accessToken, version) {
  // GAQL query against the live advertiser account — the real Test-vs-Basic gate.
  const url = `https://googleads.googleapis.com/${version}/customers/${cid}/googleAds:searchStream`;
  const r = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'developer-token': DEV_TOKEN,
      'login-customer-id': login,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: 'SELECT customer.id, customer.descriptive_name, customer.currency_code, customer.test_account FROM customer LIMIT 1',
    }),
  });
  const text = await r.text();
  return { status: r.status, text, version };
}

(async () => {
  log('Creds present:',
    ['DEV_TOKEN', 'CLIENT_ID', 'CLIENT_SECRET', 'REFRESH_TOKEN'].every(Boolean) ? 'yes' : 'no',
    '| customer:', cid, '| login(MCC):', login);

  let accessToken;
  try {
    accessToken = await getAccessToken();
    log('OAuth refresh token: VALID (access token minted ok)');
  } catch (e) {
    log('OAuth refresh token: FAILED —', e.message);
    process.exit(1);
  }

  // Probe API versions newest-first until one isn't a 404 "version not found".
  const versions = ['v21', 'v20', 'v19', 'v18', 'v17'];
  for (const v of versions) {
    let res;
    try {
      res = await tryVersion(accessToken, v);
    } catch (e) {
      log(`${v}: request error — ${e.message}`);
      continue;
    }
    // A 404 with NOT_FOUND on the path usually means the API version is retired.
    const looksRetired = res.status === 404 && /not found|Requested entity was not found|is not found/i.test(res.text) && !/customers\/\d+/.test(res.text);
    if (looksRetired) { log(`${v}: version not available, trying older`); continue; }

    log(`\n=== Live query via ${v} → HTTP ${res.status} ===`);
    log(res.text.slice(0, 1500));

    if (res.status === 200) {
      log('\nRESULT: Creds work AND the developer token can query the LIVE account → BASIC access (or better).');
    } else if (/DEVELOPER_TOKEN_NOT_APPROVED|not been approved|test account/i.test(res.text)) {
      log('\nRESULT: Creds/OAuth valid, but developer token is still TEST access — cannot touch the live account yet. Basic access not granted.');
    } else if (/USER_PERMISSION_DENIED|permission/i.test(res.text)) {
      log('\nRESULT: OAuth valid but the authenticated user lacks permission on this customer/login-customer-id. Check account linkage.');
    } else {
      log('\nRESULT: See error above — unexpected response.');
    }
    process.exit(0);
  }
  log('Could not find a working API version among:', versions.join(', '));
})();
