# Google Ads API — tool design document (for the Basic-access application)

_Use this to answer the API Token Application's tool-design questions. Craftons manages its **own
single** Google Ads account — this is an internal tool, not a third-party product._

## 1. Tool name
Craftons Marketing Engine — Google Ads integration (`google-ads.mjs`).

## 2. Company type / who it serves
**In-house.** It manages **only Craftons' own** Google Ads account (advertiser 310-491-2421) under
our manager account (275-347-3695). It is **not** offered to third parties, not resold, not a
commercial product. Single company, single account.

## 3. Purpose
Automate **reporting** and **assist with campaign management** for our own account:
- Reduce manual weekly review time.
- Catch wasted spend (irrelevant search terms, non-converting keywords) faster.
- Keep ad copy, keywords and negatives in sync with our content/keyword plan.

## 4. Functionality (what it does with the API)
**Reporting (read):**
- Pull campaign / ad group / keyword / search-term performance via GAQL (clicks, cost, conversions,
  CTR, cost-per-conversion, impression share) for the last 7/30 days.
- Generate a weekly performance report with recommendations.

**Campaign management (write — human-approved):**
- Create / edit campaigns, ad groups, responsive search ads.
- Add / edit keywords and **negative keywords**.
- Adjust budgets and bids; pause / enable keywords, ads, campaigns.

**Operational:**
- Handle API errors and partial failures; surface them to the user.
- Respect rate limits and use the manager account `login-customer-id`.

## 5. Architecture & data flow
- **Runtime:** Node.js script (`google-ads.mjs`) using the official Google Ads API (google-ads-api
  client library).
- **Auth:** OAuth2 — developer token + client ID/secret + refresh token + customer IDs read from
  environment variables (never committed to source control). Rotated 2026-06-23.
- **Flow:** script → Google Ads API → results rendered as a Markdown report. Writes only run when a
  human passes an explicit `CONFIRM=1` flag after reviewing the proposed change.
- **No third-party data.** Only our own account's data is read or modified.

## 6. Controls / safety
- **Read-only by default.** All change operations are gated behind explicit human approval
  (`CONFIRM=1`), mirroring our existing `meta-ads.mjs` guardrail.
- Daily budget cap on the account; no autonomous spend increases without approval.
- Audit: every change is logged.

## 7. Compliance
- Adheres to the Google Ads API Terms & Conditions and Required Minimum Functionality.
- No prohibited use (no scraping, no unauthorised data, no managing accounts we don't own).

## 8. Mockup — weekly report output (sample)
```
CRAFTONS ADWORDS — WEEKLY REPORT (last 7 days)
Spend $312  |  Clicks 84  |  Conv 6  |  Cost/lead $52  |  CTR 5.1%
Top wasted search terms → add as negatives: "free curved wall plans", "skateboard ply"
Keywords to pause (≥20 clicks, 0 conv): [curved plywood panels]
Best ad group by cost/lead: Curved Architraves ($31)  →  shift budget here
Proposed changes (need approval): +5 negatives, pause 1 keyword, +$10/day to architraves
```
